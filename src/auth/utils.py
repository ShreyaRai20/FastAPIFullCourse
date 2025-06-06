from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from src.config import Config
from itsdangerous import URLSafeTimedSerializer
import uuid
import logging
import pytz

password_context = CryptContext(
    schemes=['bcrypt']
)
ACCESS_TOKEN_EXPIRY = 1

def generate_password_hash(password: str) -> str:
    hash = password_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool=False):
    payload = {}
    payload['user'] = user_data
    payload['exp'] = datetime.now(pytz.utc) + (expiry if expiry is not None else timedelta(hours=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

token_serializer = URLSafeTimedSerializer(secret_key=Config.JWT_SECRET, salt='email-configuration')

def create_url_safe_token(data: dict):
    token = token_serializer.dumps(data,salt='email-configuration')
    return token


def decode_url_safe_token(token:str):
    try:
        token_data = token_serializer.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))

    