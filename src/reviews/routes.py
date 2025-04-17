from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import get_current_user
from src.db.main import get_session
from src.db.models import User
from .schemas import ReviewCreateModel
from .service import ReviewService
from src.auth.dependencies import RoleChecker
from fastapi.exceptions import HTTPException
from uuid import UUID

import uuid

review_router = APIRouter()
review_service = ReviewService()
admin_role_checker = Depends(RoleChecker(['admin']))
user_role_checker = Depends(RoleChecker(['admin','user']))

# Read/Get all reviews
@review_router.get('/', dependencies=[admin_role_checker])
async def get_all_reviews(session:AsyncSession=Depends(get_session)):
    reviews = await review_service.get_all_reviews(session)
    return reviews

# get Single review by uid
@review_router.get('/{review_uid}', dependencies=[user_role_checker])
async def get_a_review(review_uid:UUID, session:AsyncSession=Depends(get_session)):
    review = await review_service.get_review(review_uid,session)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


# Create Review
@review_router.post('/book/{book_uid}', dependencies=[user_role_checker])
async def add_review_to_books(book_uid:UUID, review_data:ReviewCreateModel, current_user:User=Depends(get_current_user), session:AsyncSession=Depends(get_session)):
    new_review = await review_service.add_review_to_book(user_email=current_user.email ,review_data=review_data ,book_uid=book_uid ,session=session)
    return new_review

# Delete a review
@review_router.delete('/{review_uid}', dependencies=[user_role_checker], status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(review_uid: UUID, current_details=Depends(get_current_user), session:AsyncSession=Depends(get_session)):
    await review_service.delete_review_to_from_book(review_uid,current_details.email,session)
    return None


