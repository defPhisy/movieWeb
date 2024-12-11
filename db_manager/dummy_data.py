from datetime import datetime
from random import randint, choice
from db_manager.data_models import (
    db,
    User,
    Movie,
    UserMovie,
)


def populate_database():
    # Clear existing data
    UserMovie.query.delete()
    Movie.query.delete()
    User.query.delete()
    db.session.commit()

    # Dummy users
    users = [
        User(name="Alice", nick="alice123"),
        User(name="Bob", nick="bobby"),
        User(name="Charlie", nick="charlie_c"),
    ]
    db.session.add_all(users)
    db.session.commit()

    # Dummy movies
    movies = [
        Movie(
            title="The Shawshank Redemption",
            year=1994,
            genre="Drama",
            imdb_id="tt0111161",
            stars="Tim Robbins, Morgan Freeman",
            director="Frank Darabont",
            writer="Stephen King (short story), Frank Darabont (screenplay)",
            plot="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            poster_link="https://example.com/shawshank.jpg",
            imdb_rating=9,
        ),
        Movie(
            title="The Godfather",
            year=1972,
            genre="Crime, Drama",
            imdb_id="tt0068646",
            stars="Marlon Brando, Al Pacino",
            director="Francis Ford Coppola",
            writer="Mario Puzo (novel), Francis Ford Coppola (screenplay)",
            plot="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
            poster_link="https://example.com/godfather.jpg",
            imdb_rating=9,
        ),
        Movie(
            title="The Dark Knight",
            year=2008,
            genre="Action, Crime, Drama",
            imdb_id="tt0468569",
            stars="Christian Bale, Heath Ledger",
            director="Christopher Nolan",
            writer="Jonathan Nolan (screenplay), Christopher Nolan (screenplay)",
            plot="When the menace known as The Joker emerges, he starts wreaking havoc on Gotham, and Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
            poster_link="https://example.com/dark_knight.jpg",
            imdb_rating=9,
        ),
    ]
    db.session.add_all(movies)
    db.session.commit()

    # Associate users with movies (randomized)
    for user in users:
        for _ in range(randint(1, len(movies))):
            movie = choice(movies)
            # Avoid duplicate associations
            if not UserMovie.query.filter_by(
                user_id=user.id, movie_id=movie.id
            ).first():
                association = UserMovie(
                    user_id=user.id,
                    movie_id=movie.id,
                    date_added=datetime.now().strftime("%Y-%m-%d"),
                    user_rating=randint(1, 5),
                )
                db.session.add(association)

    db.session.commit()


if __name__ == "__main__":
    with db.app.app_context():
        populate_database()
        print("Database populated with dummy data.")
