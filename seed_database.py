"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (movie["title"], movie["overview"], movie["poster_path"])
    date_str = movie["release_date"]
    date_format = "%Y-%M-%d"
    release_date = datetime.strptime(date_str, date_format)

    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()


for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    # TODO: create a user here
    db_user = crud.create_user(email, password)
    model.db.session.add(db_user)

    # TODO: create 10 ratings for the user
    for x in range(10):
      
      db_rating = crud.create_rating(db_user, choice(movies_in_db), randint(1,6))
      model.db.session.add(db_rating)

model.db.session.commit()