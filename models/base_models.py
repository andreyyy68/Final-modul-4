from pydantic import BaseModel, Field, field_validator
from typing import Optional

import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator
from enums.roles import Roles
from typing import Union
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base


class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен вполностью совпадать с полем password")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None


    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        # Проверяем, совпадение паролей
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    # Добавляем кастомный JSON-сериализатор для Enum
    class Config:
        json_encoders = {
            Roles: lambda v: v.value  # Преобразуем Enum в строку
        }
        extra = "allow"


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value


class TestMovie(BaseModel):
    name: str
    imageUrl: str
    price: Union[int, float]
    description: str
    location: str
    published: bool
    genreId: int


class CreateMovieResponse(BaseModel):
    id: int
    name: str
    price: Union[int, float]
    description: str
    imageUrl: str
    location: str
    published: bool
    genreId: int
    genre: dict
    createdAt: datetime.datetime
    rating: Union[int, float]


class Movie(BaseModel):
    id: int
    name: str
    price: float
    description: str
    imageUrl: str
    location: str
    published: bool
    genreId: int
    genre: dict
    createdAt: str
    rating: float


class MovieResponse(BaseModel):
    movies: list[Movie]
    count: int
    page: int
    pageSize: int
    pageCount: int


class UserCreateResponse(BaseModel):
    id: str
    email: str
    fullName: str
    roles: list[str]
    verified: Optional[bool] = None
    createdAt: datetime.datetime
    banned: Optional[bool] = None


Base = declarative_base()

class MovieDBModel(Base):
    """
    Модель для таблицы movies.
    """
    __tablename__ = 'movies'  #

    # Поля таблицы
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    genre_id = Column(String, ForeignKey('genres.id'), nullable=False)
    image_url = Column(String)
    location = Column(String)
    rating = Column(Integer)
    published = Column(Boolean)
    created_at = Column(DateTime)

class UserDBModel(Base):

    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    email = Column(String)
    full_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    verified = Column(Boolean)
    banned = Column(Boolean)
    roles = Column(String)


class AccountTransactionTemplate(Base):
    __tablename__ = 'accounts_transaction_template'
    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)



