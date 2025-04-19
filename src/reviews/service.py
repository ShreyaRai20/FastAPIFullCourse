from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import get_current_user
from .schemas import ReviewCreateModel
from sqlmodel import select, desc
from fastapi import status
from fastapi.exceptions import HTTPException
from src.errors import BookNotFound
import logging

book_service = BookService()
user_service = UserService()

class ReviewService:
    # Create
    async def add_review_to_book(
            self,
            user_email: str, 
            book_uid: str,
            review_data: ReviewCreateModel, 
            session: AsyncSession):
        try:
            book = await book_service.get_book(book_uid,session)
            user = await user_service.get_user_by_email(user_email,session)
            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)
            if not book:
                BookNotFound()
            if not user:
                BookNotFound()
            new_review.user = user
            new_review.book = book
            session.add(new_review)
            await session.commit()
            return new_review

        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Oop... Something went wrong'
            )
        
    # Read Single review
    async def get_review(self, review_uid:str, session:AsyncSession):
        statement = select(Review).where(Review.uid==review_uid)
        result = await session.exec(statement)
        return result.first()

    # Read all review
    async def get_all_reviews(self, session:AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))
        result = await session.exec(statement)
        return result.all()
    
    # Delete a review
    async def delete_review_to_from_book(self, review_uid:str, user_email:str, session:AsyncSession):
        user = await user_service.get_user_by_email(user_email,session)
        review = await self.get_review(review_uid, session)
        if not review or (review.user != user):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Cannot delete the review')
        session.delete(review)
        await session.commit()