from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class UserMovie(db.Model):
    __tablename__ = "user_movie"
    id: Mapped[int] = mapped_column(
        primary_key=True
    )  # Primary key for the association table
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    date_added: Mapped[
        str
    ]  # Additional data (e.g., timestamp of the association)
    user_rating: Mapped[float]  # Rating a user gives to the movie

    # Optional relationships to allow reverse mapping
    user: Mapped["User"] = relationship("User", back_populates="user_movies")
    movie: Mapped["Movie"] = relationship(
        "Movie", back_populates="movie_users"
    )

    def __repr__(self) -> str:
        return (
            f"UserMovie(user_id={self.user_id!r}, movie_id={self.movie_id!r})"
        )


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    nick: Mapped[str] = mapped_column(String(30), unique=True)

    # Relationship with the association table
    user_movies: Mapped[List["UserMovie"]] = relationship(
        "UserMovie", back_populates="user"
    )
    movies: Mapped[List["Movie"]] = relationship(
        "Movie", secondary="user_movie", back_populates="users", viewonly=True
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, nick={self.nick!r})"


class Movie(db.Model):
    __tablename__ = "movie"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int]
    genre: Mapped[str]
    imdb_id: Mapped[str] = mapped_column(unique=True)
    stars: Mapped[str]
    director: Mapped[str]
    writer: Mapped[str]
    plot: Mapped[str]
    poster_link: Mapped[str]
    imdb_rating: Mapped[int]

    # Relationship with the association table
    movie_users: Mapped[List["UserMovie"]] = relationship(
        "UserMovie", back_populates="movie"
    )
    users: Mapped[List["User"]] = relationship(
        "User", secondary="user_movie", back_populates="movies", viewonly=True
    )

    def __repr__(self) -> str:
        return f"Movie(id={self.id!r}, title={self.title!r})"

    @classmethod
    def get_movie_from_imdb_id(cls, imdb_id):
        movie = Movie.query.filter_by(imdb_id=imdb_id).first()

        if movie:
            return movie
        return None

    @classmethod
    def __len__(cls):
        """Return the total number of movies in the database."""
        return db.session.query(cls).count()
