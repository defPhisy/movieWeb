from db_manager.data_models import User, Movie, UserMovie, db
from typing import Type
from flask import Request
from datetime import datetime


def get_users():
    return User.query.order_by(User.name).all()


def process_new_user(model: Type[User], request: Request) -> User | str:
    if attribute_exists(model, "nick", request):
        return "Nickname already exists!"
    new_user = create_new_movie(model, request)
    write_to_db(new_user)
    return new_user


def update_object(obj: Movie | User, request: Request) -> None:
    if not request:
        return "No Data"

    data = request.get_json()
    for key, value in data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)

    write_to_db(obj)


def create_new_movie(model: Type[Movie], request: Request):
    if not request:
        return "No data!"

    data = request.form.to_dict()
    user_id = data.get("user_id")
    user = db.session.get(User, user_id)
    del data["user_id"]
    new_obj = model(**data)

    return new_obj, user


def create_new_user(model: Type[User], request: Request) -> User:
    if not request:
        return "No data!"

    data = request.form.to_dict()
    new_obj = model(**data)

    return new_obj


def add_movie_to_user(movie, user):
    new_association = UserMovie(
        user_id=user.id,
        movie_id=movie.id,
        date_added="24/03/24",  # datetime.now()
        user_rating=4,
    )
    db.session.add(new_association)
    db.session.commit()


def remove_movie_from_user(user_id, movie_id):
    # Find the UserMovie entry that links the user and movie
    user_movie = (
        db.session.query(UserMovie)
        .filter_by(user_id=user_id, movie_id=movie_id)
        .first()
    )

    if user_movie:
        # Delete the association
        db.session.delete(user_movie)
        db.session.commit()
        print(f"Movie {movie_id} removed from user {user_id}'s list.")
    else:
        print(
            f"No such association found between user {user_id} and movie {movie_id}."
        )


def attribute_exists(model, attribute_name, request):
    """Check if an attribute exists in a model."""
    data = request.get_json()
    value = data.get(attribute_name, None)

    if not value:
        return f"{attribute_name} does not exist!"

    attribute_filter = {attribute_name: value}

    # Use the attribute_filter to filter the query
    item = model.query.filter_by(**attribute_filter).first()

    return True if item else False


def write_to_db(obj: User | Movie) -> None:
    db.session.add(obj)
    db.session.commit()
