from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    nick: Mapped[str] = mapped_column(String(30), unique=True)

    movies: Mapped[List["Movie"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, nick={self.nick!r})"


class Movie(db.Model):
    __tablename__ = "movie"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str]
    year: Mapped[int]
    genre: Mapped[str]
    imdb_id: Mapped[str] = mapped_column(unique=True)
    stars: Mapped[str]
    director: Mapped[str]
    writer: Mapped[str]
    plot: Mapped[str]
    poster_link: Mapped[str] = mapped_column(unique=True)
    imdb_rating: Mapped[int]

    user: Mapped["User"] = relationship(back_populates="movies")

    def __repr__(self) -> str:
        return f"Movie(id={self.id!r}, title={self.title!r})"
