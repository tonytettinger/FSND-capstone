import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor

""" Permission list
get:movies
get:actors
post:movies
post:actors
delete:movies
delete:actors
patch:movies
patch:actors
"""

def insert_test_movie():
    data = {
        'title': 'Inception 2',
        'release_date': '2024-04-04'
    }
    movie = Movie(**data)
    movie.insert()
    
    return data


def query_test_movie():
    query = Movie.query.filter_by(title="Inception 2").first()
    return query


def delete_test_movie():
    query = Movie.query.filter_by(title="Inception 2").first()
    if query is not None:
        query.deletes()


class MoviesTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "movies_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.test_movie = {
        'title': 'Inception 2',
        'release_date': '2024-04-04'
         }
        # Casting Assistant (can view movies and actors)
        CA_TOKEN = os.getenv("CA_TOKEN")
        # Casting Director (CA role + can add, delete, patch actors and movies)
        CD_TOKEN = os.getenv("CD_TOKEN")
        database_path = os.getenv("DATABASE_URL")
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    TEST: Endpoint POST /movie
    '''
    def test_post_movie(self):
        response = self.client().post(f"/movie", data=json.dumps(self.test_movie), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response  = json.loads(response.data)
        self.assertEqual( json_response, self.test_movie)
        delete_test_movie()
    '''
    TEST: Endpoint POST /movie, 422
    Missing submission field
    def test_post_movie_422(self):
        wrong_post = self.test_post
        # Simulate missing answer 
        wrong_post.pop('answer')

        response = self.client().post(f"/questionsPost", data=json.dumps(wrong_post), content_type='application/json')
        json_response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response_data["error"], 422)
        delete_test_post()
        
    '''
    
   
# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
