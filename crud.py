"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


# Functions start here!

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def all_users():
    """returns all users."""
    
    return User.query.all()

def get_user_by_id(user_id):
    """returns user's id"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """return user with the email"""
    return User.query.filter(User.email == email).first()
    # what happens if we remove .first() above?
    # Must use .first() to use the data within the object



def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    return movie

def all_movies():
    """returns all movies."""
    
    return Movie.query.all()

def get_movie_by_id(movie_id):
    """returns movie's id"""
    return Movie.query.get(movie_id)


def create_rating(user, movie, score):
    """Create and return a new rating."""
    rating = Rating(user=user, movie=movie, score=score)
    return rating


def get_rating_by_movieid(movie_id):
    """returns ratings for movie"""
    return Rating.query.filter(Rating.movie_id == movie_id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)