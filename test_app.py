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

def insert_test_actor():
    data = {
        'name': 'Roberta',
        'age': '24',
        'gender': 'female'
    }
    actor = Actor(**data)
    actor.insert()
    
    return data


def query_test_actor():
    query = Actor.query.filter_by(name="Roberta").first()
    return query


def delete_test_actor():
    query = Actor.query.filter_by(name="Roberta").first()
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
        self.director_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + CD_TOKEN,
        }
        self.assistant_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + CA_TOKEN,
        }
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
    Task Criteria: Demonstrate validity of API behavior
    -Includes at least one test for expected success and error behavior for each endpoint using the unittest library
    -Includes tests demonstrating role-based access control, at least two per role.
    
    Description: For the success behavior it is necessary to have the right role,
    therefore the first test is both a test for RBAC and success behavior.
    For the failure there is one failure and one RBAC based failure included for a given endpoint
    '''
    
    #Endpoint: POST /movie tests: RBAC success, 422 failure, RBAC failure
    
    '''
    TEST ROLE BASED SUCCESS: Endpoint POST /movie
    A Casting Director can post a movie:
    '''
    def test_post_movie_director(self):
        response = self.client().post(f"/movie", data=json.dumps(self.test_movie), content_type='application/json', headers=self.director_headers)
        self.assertEqual(response.status_code, 200)
        json_response  = json.loads(response.data)
        self.assertEqual( json_response, self.test_movie)
        delete_test_movie()
    
    '''
    TEST FAIL: Endpoint POST /movie
    Not well formatted movie post return 422 unprocessable exception:
    '''
    def test_post_movie_422(self):
        wrong_movie = {
        'titles': 'Inception 2',
        'release_date': '2024-04-04'
         }
        response = self.client().post(f"/movie", data=json.dumps(wrong_movie), content_type='application/json', headers=self.director_headers)
        self.assertEqual(response.status_code, 422)
 
    '''
    TEST ROLE BASED FAIL: Endpoint POST /movie
    A Casting Assistant can't post a movie return 403 unathorized exception:
    '''
    def test_post_movie_assistant(self):
        response = self.client().post(f"/movie", data=json.dumps(self.test_movie), content_type='application/json', headers=self.assistant_headers)
        self.assertEqual(response.status_code, 403)
        
    #Endpoint: DELETE /movie tests: RBAC success, 422 failure, RBAC failure
    
    '''
    TEST ROLE BASED SUCCESS:  Endpoint DELETE /movie/<int:post_id>
    When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    def test_delete_movie(self):
        insert_test_movie()
        movie = query_test_movie()
        movie_id = movie.id

        # Check the post exists before deleting
        
        self.assertIsNotNone(movie)
        
        print(movie_id)
        response = self.client().delete(f"/movie/{movie_id}", content_type='application/json', headers=self.director_headers)
        # Removal persist in the database
        deleted = Movie.query.get(movie_id)
        
        #self.assertEqual(response.status_code, 200)
        self.assertIsNone(deleted)
        
    """
    TEST FAILURE: Endpoint DELETE /movie/<int:post_id>, 404
    Method Not Allowed when requesting delete using wrong method.
    """
    
    def test_delete_movie_doesnt_exist(self):
        insert_test_movie()
        response = self.client().delete(f"/movie/9999", content_type='application/json', headers=self.director_headers)
        self.assertEqual(response.status_code, 404)
        delete_test_movie()
   
# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
