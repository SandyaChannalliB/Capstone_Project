import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db,Actor,Movie
from datetime import datetime
from auth import AuthError,requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app,resources={r"/api/*": {"origins": "*"}})

  '''
  Set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Origin","*")
    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods","GET,PUT,POST,DELETE,OPTIONS")
    return response
  
  @app.route('/')
  def get_greeting():
    excited = os.environ['EXCITED']
    greeting = "Hello" 
    if excited == 'true': greeting = greeting + "!!!!!"
    return greeting


  #Movies
  '''
  Endpoint to handle GET requests for all available movies.
  '''
  @app.route("/movies", methods=['GET'])
  @requires_auth('get:movies')
  def list_movies(payload):
    try:
      movies = Movie.query.order_by(Movie.id).all()
      if len(movies) == 0:
        abort(404)
      formatted_Movies = [movie.format() for movie in movies]
      return jsonify({
        "success":True,
        "movies": formatted_Movies
      })
    except:
      abort(422)

  '''
  Endpoint to handle POST requests to add new movie.
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movie')
  def create_movie(payload):
    body = request.get_json()
    movie_title = body.get("title", None)
    movie_release_date = body.get("release_date", None)
    try:
      if None in (movie_title, movie_release_date):
        abort(400)
      movie = Movie(movie_title,movie_release_date)
      movie.insert()
      return jsonify({
        'success': True, 
        'movies': [movie.format()]
        })
    except:
      abort(422)

  '''
  Endpoint to handle GET request for a particular movie.
  '''
  @app.route("/movies/<int:movie_id>",methods=['GET'])
  @requires_auth('get:movies')
  def get_movie(payload,movie_id):
    movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
    if movie is None:
      abort(404)
    return jsonify({
      "success":True,
      "movies": [movie.format()]
    })
  
  '''
  Endpoint to handle PATCH request to update particular movie.
  '''
  @app.route("/movies/<int:movie_id>",methods=['PATCH'])
  @requires_auth('update:movie')
  def edit_movie(payload,movie_id):
    try:
      movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
      if movie is None:
        abort(404)
      body = request.get_json()
      if 'title' in body:
        movie.title = body.get('title')
      if 'release_date' in body:
        movie.release_date = body.get('release_date')
      movie.update()
      return jsonify({
        "success":True,
        "movies": [movie.format()]
      })
    except:
      abort(422)

  '''
  Endpoint to handle DELETE request for a particular movie.
  '''
  @app.route("/movies/<int:movie_id>",methods=['DELETE'])
  @requires_auth('delete:movie')
  def remove_movie(payload,movie_id):
    movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
    if movie is None:
      abort(404)
    try:
      movie.delete()
      return jsonify({
        "success":True,
        "deleted":movie_id
      })
    except:
      abort(422)

  
  #Actors 

  '''
  Endpoint to handle GET requests for all available actors.
  '''
  @app.route("/actors",methods=['GET'])
  @requires_auth('get:actors')
  def list_actors(payload):
    try:
      actors = Actor.query.order_by(Actor.id).all()
      print(len(actors))
      if len(actors) == 0:
        abort(404)
      formatted_actors = [actor.format() for actor in actors]
      return jsonify({
        "success":True,
        "actors":formatted_actors
      })
    except:
      abort(422)

  '''
  Endpoint to handle GET requests for a particular actor.
  '''
  @app.route("/actors/<int:actor_id>",methods=['GET'])
  @requires_auth('get:actors')
  def get_single_actor(payload,actor_id):
    try:
      actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
      if actor is None:
        abort(404)
      return jsonify({
        "success":True,
        "actors":[actor.format()]
      })
    except:
      abort(422)

  '''
  Endpoint to handle POST requests to add new actor.
  '''
  @app.route("/actors",methods=['POST'])
  @requires_auth('post:actor')
  def add_new_actor(payload):
    try:
      body = request.get_json()
      actor_name = body.get('name',None)
      actor_age = body.get('age',None)
      actor_gender = body.get('gender',None)
      actor = Actor(actor_name,actor_age,actor_gender)
      actor.insert()
      return jsonify({
        "success":True,
        "actor":[actor.format()]
      })
    except:
      abort(422)

  '''
  Endpoint to handle PATCH request to update particular actor.
  '''
  @app.route("/actors/<int:actor_id>",methods=['PATCH'])
  @requires_auth('update:actor')
  def edit_actor(payload,actor_id):
    try:
      actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
      if actor is None:
        abort(404)
      body = request.get_json()
      if 'name' in body:
        actor.name = body.get('name')
      if 'age' in body:
        actor.age = body.get('age')
      if 'gender' in body:
        actor.gender = body.get('gender')
      return jsonify({
        "success":True,
        "actor":[actor.format()]
      })
    except:
      abort(422)
    
  '''
  Endpoint to handle DELETE request for a particular actor.
  '''
  @app.route("/actors/<int:actor_id>",methods=['DELETE'])
  @requires_auth('delete:actor')
  def remove_actor(payload,actor_id):
    actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
    if actor is None:
      abort(404)
    try:
      actor.delete()
      return jsonify({
        "success":True,
        "deleted":actor_id
      })
    except:
      abort(422)

  
  '''
  Error handlers for all expected errors 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "resource not found"}),404,
    
  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({"success": False, "error": 405, "message": "Method Not allowed"}),405,

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}),422,
    
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({"success":False,"error":500,"message":"Internal server error"}),500
  
  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
    return jsonify({"success": False,"error": ex.status_code,'message': ex.error}),ex.status_code
  
  return app  

app = create_app()
if __name__ == '__main__':
    app.run()
    
'''if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)'''