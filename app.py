from db_manager.data_models import db, User, Movie
from db_manager.db_func import (
    create_new_object,
    update_object,
    write_to_db,
    attribute_exists,
)
from flask import Flask, request, render_template
import os


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = "./data"
DB_NAME = "library.sqlite"
FULL_DB_PATH = os.path.join(ROOT_PATH, DB_FOLDER, DB_NAME)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{FULL_DB_PATH}"
db.init_app(app)

# create Tables
with app.app_context():
    db.create_all()


@app.route("/users", methods=["GET", "PUT", "POST"])
def handle_users():
    if request.method == "POST":
        if attribute_exists(User, "nick", request):
            return "Nickname already exists!"
        new_user = create_new_object(User, request)
        write_to_db(new_user)
        return f"New User {new_user.name} added!"

    if request.method == "PUT":
        return "not implemented"

    users = User.query.order_by(User.name).all()
    return render_template("users.html", users=users)


@app.route("/movies", methods=["GET", "PUT", "POST"])
def handle_movies():
    if request.method == "POST":
        new_movie = create_new_object(Movie, request)
        write_to_db(new_movie)
        return f"New Movie {new_movie.title} added!"

    if request.method == "PUT":
        return "not implemented"

    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movies.html", movies=movies)


@app.route("/user/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def handle_user(user_id: int):
    user = db.session.get(User, user_id)
    if not user:
        return "User not found", 404  # type: ignore

    if request.method == "PUT":
        pass

    return render_template("user.html", user=user)


@app.route("/movie/<int:movie_id>", methods=["GET", "PUT", "DELETE"])
def handle_movie(movie_id: int):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        return "Movie not found!", 404  # type: ignore

    if request.method == "PUT":
        updated_movie = update_object(movie, request)

        return f"Movie {updated_movie.title} updated!"

    if request.method == "DELETE":
        movie_title = movie.title
        db.session.delete(movie)
        return f"Movie {movie_title} removed!"

    return f"Movie: {movie.title}"


@app.route("/user/<int:user_id>/movies", methods=["GET", "POST"])
def add_movie(user_id: int) -> str:
    user = db.session.get(User, user_id)
    if not user:
        return f"User {user_id} does not exist!"

    if request.method == "POST":
        data = request.get_json()
        new_movie = create_new_object(Movie, data)
        user.movies.append(new_movie)
        db.session.commit()
        return "Added new Movie"

    return render_template("user.html", user=user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)


# Movie Dummy: {"user_id": 1, "title": "New Title", "year": 2004, "genre": "Action", "imdb_id": "imdb ID", "stars": "John Hoppkins", "director": "PHILIPP", "writer": "Christopher Nolan", "plot": "Hello this is the plot.", "poster_link": "https://google.com", "imdb_rating": 8.9}

# User Dummy: {"name": "Philipp", "nick": "Philzn"}
