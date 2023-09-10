import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db,Actor,Movie
import pdb


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'new movie title',
            'release_date': '2024-05-08 14:30:45'
        }

        self.new_actor = {
            'name': 'new name',
            'age': 35,
            'gender': 'male'
        }
        self.movie_update = {
            "title": "test update",
        }

        self.actor_update = {
            'name':'My new name',
            'age':36
        }
        self.executive_producer = os.environ.get("EXECUTIVE_PRODUCER")
        self.casting_director = os.environ.get("CASTING_DIRECTOR")
        self.casting_assistant = os.environ.get("CASTING_ASSISTANT")
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

#Movies
    
    # Success behaviour for POST/movies enpoint for executive_producer role
    def test_create_movie(self):
        
        total_movies_before = len(Movie.query.all())
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)
        total_movies_after = len(Movie.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_movies_after, total_movies_before + 1)
    
    def test_401_create_movie_no_auth_hedder(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        

    def test_403_create_movie_no_permission(self):
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization':self.casting_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_422_if_adding_Movie_fails(self):
        new_movie = {
            'title': 'title with no release date',
        }
        res = self.client().post('/movies', json=new_movie,headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    
    # Success behaviour for GET/movies enpoint for all 3 roles
    def test_list_movies_executive_producer(self):
        res = self.client().get('/movies',headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_list_movies_casting_director(self):
        res = self.client().get('/movies',headers={'Authorization':self.casting_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_list_movies_casting_assistant(self):
        res = self.client().get('/movies',headers={'Authorization':self.casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    #Error behaviour for GET/movies enpoint for all 3 roles
    def test_404_sent_requesting_non_existing_movie(self):
        res = self.client().get('/movies/9999',headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_sent_requesting_non_existing_movie_casting_director(self):
        res = self.client().get('/movies/9999',headers={'Authorization':self.casting_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
   

    def test_delete_movie(self):
        movie = Movie(title='new movie to be deleted', release_date='2024-05-08 14:30:45')
        movie.insert()
        movie_id = movie.id

        res = self.client().delete(f'/movies/{movie_id}',headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)

        movie = Movie.query.filter(
            Movie.id == movie.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie_id)

    
    def test_404_delete_non_existing_movie(self):
        res = self.client().delete('/movies/9999',headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_movie_title(self):
        res = self.client().patch('/movies/1',
                                  json=self.movie_update,
                                  headers={'Authorization': self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
#Actors

    def test_create_actor(self):
        
        total_actors_before = len(Actor.query.all())
        res = self.client().post('/actors', json=self.new_actor,headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)
        total_actors_after = len(Actor.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_actors_after, total_actors_before + 1)

    def test_401_create_actor_no_auth_hedder(self):
        res = self.client().post('/actors', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        

    def test_403_create_actor_no_permission(self):
        res = self.client().post('/actors', json=self.new_movie, headers={'Authorization':self.casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_422_if_adding_Actor_no_name_fails_(self):
        new_actor = {
            'age': 32
        }
        res = self.client().post('/actors', json=new_actor,headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        

    #Success behaviour for GET/actors enpoint for all 3 roles
    def test_list_actors_executive_producer(self):
        res = self.client().get('/actors',headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_list_actors_executive_producer(self):
        res = self.client().get('/actors',headers={'Authorization':self.casting_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_list_actors_executive_producer(self):
        res = self.client().get('/actors',headers={'Authorization':self.casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))


    def test_remove_actor(self):
        actor = Actor(name='new name', age=45,gender='Male')
        actor.insert()
        actor_id = actor.id

        res = self.client().delete(f'/actors/{actor_id}',headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)

        actor = Actor.query.filter(
            Actor.id == actor.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)

    def test_404_sent_deleting_non_existing_actor(self):
        res = self.client().delete('/actors/9999',headers={'Authorization':self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_update_actor(self):
        res = self.client().patch('/actors/1',
                                  json=self.actor_update,
                                  headers={'Authorization': self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()