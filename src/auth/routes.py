from fastapi import APIRouter, Depends, status, BackgroundTasks
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserBooksModel, EmailModel, PasswordResetRequestModel, PasswordResetConfirmModel
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi.exceptions import HTTPException
from .utils import create_access_token, decode_token, verify_password, create_url_safe_token, decode_url_safe_token, generate_password_hash
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist
from src.errors import UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken
from src.mail import mail, create_message
import asyncio
from src.config import Config
from src.celery_tasks import send_email

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])

REFRESH_TOKEN_EXPIRY = 3

# Bearer_Token

@auth_router.post('/send_email')
async def send_email(emails:EmailModel):
    emails = emails.addresses
    # email = ['shreya200199@gmail.com', 'anurai483@gmail.com']
    subject = 'welcome to the app'
    html = '<h1>Hello Didi</h1>'
    send_email.delay(emails, subject, html)
    # message = create_message(recipent=emails, subject='Welcome', body=html)
    # await mail.send_message(message)
    return {'message':'Email send  sucessfully'}

@auth_router.post('/signup', response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, bg_tasks:BackgroundTasks, session:AsyncSession=Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exist(email, session)
    if user_exists:
        raise UserAlreadyExists()
    new_user = await user_service.create_user(user_data,session)
    token = create_url_safe_token({"email":email})
    link = f'http://{Config.DOMAIN}/api/v1/auth/verify/{token}'
    html_message = f'<h1>Verify your email</h1> <p>Please click this <a href="{link}">link</a> below<p> '
    emails = [email]
    subject = 'verify your email'
    send_email.delay(emails,subject,html_message)

    # message = create_message(recipent=[email], subject='verify your email', body=html_message)
    # bg_tasks.add_task(mail.send_message,message)
    # await mail.send_message(message)
    # try:
    #     email_data = EmailModel(addresses=[new_user.email])  # create EmailModel instance
    #     await send_email(email_data)
    # except Exception as e:
    #     return {'error': f'Failed to send welcome email: {str(e)}'}
    return {'message':'account created! check your email to verify your account', 'user' : new_user}

@auth_router.get('/verify/{token}')
async def verify_user_account(token:str, session:AsyncSession=Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get('email')
    if user_email:
        user = await user_service.get_user_by_email(user_email,session)
        if not user:
            raise UserNotFound()
        
        await user_service.update_user(user, {'is_verified':True}, session)
        return JSONResponse(content={'message':'Account verified successfully'}, status_code=status.HTTP_200_OK)
        
    return JSONResponse(content={'message':'Some error occurred'}, status_code=status.HTTP_404_NOT_FOUND)


@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    user =  await user_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid),
                    'role': user.role
                }
            )
            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                refresh=True,
                expiry= timedelta(days=REFRESH_TOKEN_EXPIRY),
            )
            return JSONResponse(
                content={
                    "message":"Login Successful",
                    "access_token": access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
        
        raise InvalidCredentials()


@auth_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    print(expiry_timestamp)
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )

        return JSONResponse(
            content={
                'access_token': new_access_token
            })
    
    raise InvalidToken()

@auth_router.get('/me', response_model=UserBooksModel)
async def get_current_user(user = Depends(get_current_user), _:bool=Depends(role_checker)):
    return user


@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']

    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            'message': 'logged out sucessfully',
        },
        status_code=status.HTTP_200_OK
    )



"""
1. PROVIDE THE EMAIL -> PASSWORD RESET REQUEST
2. SEND PASSWORD RESET LINK
3. RESET PASSWORD -> PASSWORD RESET CONFIRMATION
"""

@auth_router.post('/password-reset-request')
async def password_reset_request(email_data:PasswordResetRequestModel):
    email = email_data.email
    token = create_url_safe_token({"email":email})
    link = f'http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}'
    html_message = f'<h1>Reset Password</h1> <p>Please click this <a href="{link}">link</a> below<p> '
    message = create_message(recipent=[email], subject='verify your email', body=html_message)
    await mail.send_message(message)
    return JSONResponse(content={'message':'Reset password'}, status_code=status.HTTP_200_OK)


@auth_router.post('/password-reset-confirm/{token}')
async def reset_account_password(token:str,passwords:PasswordResetConfirmModel, session:AsyncSession=Depends(get_session)):
    new_password = passwords.new_password
    confirm_password = passwords.confirm_password
    if new_password != confirm_password:
        raise HTTPException(detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST)
    token_data = decode_url_safe_token(token)
    user_email = token_data.get('email')
    if user_email:
        user = await user_service.get_user_by_email(user_email,session)
        if not user:
            raise UserNotFound()
        password_hash = generate_password_hash(new_password)
        await user_service.update_user(user, {'password_hash':password_hash}, session)
        return JSONResponse(content={'message':'Password  reset successfull'}, status_code=status.HTTP_200_OK)
        
    return JSONResponse(content={'message':'Error in password reset'}, status_code=status.HTTP_404_NOT_FOUND)


