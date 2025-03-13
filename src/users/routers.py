from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.events.schemas import EventResponse
from src.users.models import User
from sqlalchemy import select
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from src.users.schemas import UserResponse, UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[UserResponse])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    query_result = await session.scalars(query)
    result = query_result.unique.all()
    return result


@router.post("/create", response_model=UserResponse)
async def create_user(payload: UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = User(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        is_admin=payload.is_admin
    )
    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already used")
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, payload: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in payload.model_dump().items():
        if value is not None:
            setattr(result, field, value)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already used")
    return result


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(result)
    await session.commit()
    return None


@router.get("/{user_id}/events", response_model=Optional[List[EventResponse]])
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result.events
