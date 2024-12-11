from db_manager.data_models import db, Movie, User
from db_manager.db_func import (
    create_new_movie,
    write_to_db,
    get_users,
    add_movie_to_user,
    create_new_user,
    remove_movie_from_user,
)
from db_manager.dummy_data import populate_database
from flask import Flask, request, render_template, redirect
from omdb_api import search_movies_from_omdb
import os


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = "./data"
DB_NAME = "library.sqlite"
FULL_DB_PATH = os.path.join(ROOT_PATH, DB_FOLDER, DB_NAME)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{FULL_DB_PATH}"
db.init_app(app)

# create Tables and populate with Dummy Date when no db file exists
if not os.path.exists(FULL_DB_PATH):
    with app.app_context():
        db.create_all()
        populate_database()
        print("Database populated with dummy data.")


@app.route("/", methods=["GET", "POST"])
def landing_page():
    if request.method == "POST":
        user_id = request.form.get("user_id", None)
        return redirect(f"/users/{user_id}")
    users = get_users()
    return render_template("index.html", users=users)


@app.route("/users/<int:user_id>", methods=["GET"])
def user_page(user_id):
    user = db.session.get(User, user_id)
    movie_count = len(user.movies)
    return render_template("user.html", user=user, movie_count=movie_count)


@app.route("/add_movie", methods=["GET", "POST"])
def add_user_movie():
    user_id = request.args.get("user_id")
    user = db.session.get(User, user_id)

    if request.method == "POST":
        new_movie, user = create_new_movie(Movie, request)
        existing_movie = Movie.get_movie_from_imdb_id(new_movie.imdb_id)
        if not existing_movie:
            write_to_db(new_movie)
            add_movie_to_user(new_movie, user)
        add_movie_to_user(existing_movie, user)

        return redirect(f"/users/{user.id}")

    return render_template("user_add_movie.html", user=user)


@app.route("/search_movie", methods=["GET", "POST"])
def search_movies():
    user_id = request.args.get("user_id")
    user = db.session.get(User, user_id)

    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        search_results = search_movies_from_omdb(title, year)
        search = search_results.get("Search")
        print(search)
        return render_template(
            "movies_found.html", user=user, search_results=search
        )

    return render_template("search_movie.html", user=user)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        new_user = create_new_user(User, request)
        write_to_db(new_user)
        return redirect(f"/users/{new_user.id}")

    return render_template("add_user.html")


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>", methods=["GET"])
def delete_user_movie(user_id, movie_id):
    remove_movie_from_user(user_id, movie_id)
    return redirect(f"/users/{user_id}")


# @app.route("/users", methods=["GET", "POST"])
# def handle_users():
#     if request.method == "POST":
#         new_user = process_new_user(User, request)
#         return f"New User {new_user.name} added!"

#     users = model.query.order_by(model.name).all()
#     return render_template("users.html", users=users)


# @app.route("/movies", methods=["GET", "PUT", "POST"])
# def handle_movies():
#     if request.method == "POST":
#         new_movie = create_new_object(Movie, request)
#         write_to_db(new_movie)
#         return f"New Movie {new_movie.title} added!"

#     if request.method == "PUT":
#         return "not implemented"

#     movies = Movie.query.order_by(Movie.title).all()
#     return render_template("movies.html", movies=movies)


# @app.route("/user/<int:user_id>", methods=["GET", "PUT", "DELETE"])
# def handle_user(user_id: int):
#     user = db.session.get(User, user_id)
#     if not user:
#         return "User not found", 404  # type: ignore

#     if request.method == "PUT":
#         pass

#     return render_template("user.html", user=user)


# @app.route("/movie/<int:movie_id>", methods=["GET", "PUT", "DELETE"])
# def handle_movie(movie_id: int):
#     movie = db.session.get(Movie, movie_id)
#     if not movie:
#         return "Movie not found!", 404  # type: ignore

#     if request.method == "PUT":
#         updated_movie = update_object(movie, request)

#         return f"Movie {updated_movie.title} updated!"

#     if request.method == "DELETE":
#         movie_title = movie.title
#         db.session.delete(movie)
#         return f"Movie {movie_title} removed!"

#     return f"Movie: {movie.title}"


# @app.route("/user/<int:user_id>/movies", methods=["GET", "POST"])
# def add_movie(user_id: int) -> str:
#     user = db.session.get(User, user_id)
#     if not user:
#         return f"User {user_id} does not exist!"

#     if request.method == "POST":
#         data = request.get_json()
#         new_movie = create_new_object(Movie, data)
#         user.movies.append(new_movie)
#         db.session.commit()
#         return "Added new Movie"

#     return render_template("user.html", user=user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)


# Movie Dummy: {"user_id": 1, "title": "New Title", "year": 2004, "genre": "Action", "imdb_id": "imdb ID", "stars": "John Hoppkins", "director": "PHILIPP", "writer": "Christopher Nolan", "plot": "Hello this is the plot.", "poster_link": "https://google.com", "imdb_rating": 8.9}

# User Dummy: {"name": "Philipp", "nick": "Philzn"}
