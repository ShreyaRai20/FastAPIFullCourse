from src.db.models import Tag
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import get_current_user
from .schemas import TagCreateModel, TagAddModel
from sqlmodel import select, desc
from fastapi import status
from fastapi.exceptions import HTTPException
from src.errors import BookNotFound, TagNotFound, TagAlreadyExists

book_service = BookService()

class TagService:
    # Get all tags
    async def get_tags(self, session: AsyncSession):
        statement = select(Tag).order_by(desc(Tag.created_at))
        result = await session.exec(statement)
        return result.all()
    
    # Add tags to book
    async def add_tags_to_book(self, tag_data:TagAddModel, book_uid:str, session:AsyncSession):
        book = await book_service.get_book(book_uid, session)

        if not book:
            raise BookNotFound
        
        for tag_item in tag_data.tags:
            result =  await session.exec(select(Tag).where(Tag.name==tag_item.name))
            tag = result.one_or_none
            book.tags.append(tag)
        session.add(book)
        await session.commit()
        return book
    
    # Get tag by uid
    async def get_tag_by_uid(self, tag_uid:str, session:AsyncSession):
        statement = select(Tag).where(Tag.uid==tag_uid)
        result = await session.exec(statement)
        tag = result.first()
        return tag
    
    # Add Tags
    async def add_tag(self, tag_data:TagCreateModel, session:AsyncSession):
        statement = select(Tag).where(Tag.uid==tag_uid)
        result = await session.exec(statement)
        tag = result.first()
        if tag:
            raise TagAlreadyExists
        new_tag = Tag(tag_data.name)
        session.add(new_tag)
        await session.commit()
        return new_tag

    async def update_tag(self,tag_uid:str,  tag_update_data:TagCreateModel, session:AsyncSession):
        tag = await self.get_book(tag_uid, session)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        update_data_dict = tag_update_data.model_dump()
        for k, v in update_data_dict.items():
            setattr(tag,k,v)            
            await session.commit()
        return tag
    
    # Delete a tag
    async def delete_tag(self, tag_uid:str, session:AsyncSession):
        tag = await self.get_tag_by_uid(tag_uid, session)
        if not tag:
            raise TagNotFound
        
        await session.delete(tag)
        await session.commit()
        
