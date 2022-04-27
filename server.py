"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db, db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def index():
    """go to homepage"""
    return render_template("homepage.html")

@app.route('/movies')
def get_movies():
    """go to movies"""
    movies = crud.all_movies()
    return render_template("all_movies.html", movies = movies)

@app.route('/movies/<movie_id>')
def get_movie_details(movie_id):
    """ show movie details for each movie """
    movie_details = crud.get_movie_by_id(movie_id)
    ratings = crud.get_rating_by_movieid(movie_id)
    return render_template("movie_details.html", movie = movie_details, ratings = ratings)

@app.route('/users')
def show_users():
    """ show user email and profile link"""
    users = crud.all_users()
    return render_template("users.html", users = users)

@app.route('/users/<user_id>')
def get_user_details(user_id):
    """ show user details for each user """
    user_details = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user = user_details)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    user_email = request.form.get("email")
    password = request.form.get("password")

    email_check = crud.get_user_by_email(user_email)

    if email_check is None:
        new_user = crud.create_user(user_email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Congrats! You are now a member of the Movie Ratings app. Go log in.")
    else:
        flash("An account already exists with that email address. Try signing up again with a different email.")
    
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    """log in existing user"""
    input_email = request.form.get("email")
    input_password = request.form.get("password")

    user_info = crud.get_user_by_email(input_email)

    if input_password == user_info.password:
        session["user_id"] = user_info.user_id
        flash("Logged in!")
    return redirect("/")


@app.route("/movies/<movie_id>/rating", methods=["POST"])
def submit_rating(movie_id):
    """add rating to movie"""
    loggedin_user = session.get("user_id")
    score = int(request.form.get("give-score"))
    user = crud.get_user_by_id(loggedin_user)
    movie = crud.get_movie_by_id(movie_id)


    new_rating = crud.create_rating(user, movie, score)
    db.session.add(new_rating)
    db.session.commit()
    flash("Thanks for submitting a rating!")

    return redirect(f'/movies/{ movie_id }')

# Go to movie's page
# Add dropdown to rate a movie 0-5
# Append rating to existing rating, average ratings and show on page




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
