from db_manager.data_models import User, Movie, db
from typing import Type
from flask import Request


def update_object(obj: Movie | User, request: Request) -> None:
    if not request:
        return "No Data"

    data = request.get_json()
    for key, value in data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)

    write_to_db(obj)


def create_new_object(
    model: Type[Movie] | Type[User], request: Request
) -> User | Movie:
    if not request:
        return "No data!"

    data = request.get_json()
    new_obj = model(**data)

    return new_obj


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
