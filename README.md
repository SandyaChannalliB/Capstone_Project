# Capstone_Project
Render URL : https://capstone-sandya.onrender.com

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

Run the shell scrip file to assign environment variables
```bash
source setup.sh;
```
or

add the environment variables
```bash
export API_AUDIENCE="Capstone"
export AUTH0_DOMAIN="auth0domain.us.auth0.com"
export CLIENT_ID="4FjyUPdra01Bf2WFm8udcnRNav0XEAnZ"
export DATABASE_PATH="postgresql://capstone_26y9_user:ePlMGtMa5ox3yy3NdCdXFCTxClBeRV26@localhost/capstone_26y9"

```

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - get:movies
    - get:actors
    - post:movie
    - post:actor
    - update:movie
    - update:actor
    - delete:movie
    - delete:actor
6. Create new roles for:
   - Casting Assistant
     - can view the movies and actors list `get:movies` and `get:actors`
   - Casting Director
     - Casting Director can view movies/actors list, add or delete actors, modify actors/movies i.e `get:movies`,`get:actors`,`post:actor`,`update:movie`,`update:actor` and `delete:actor`
   - Executive Producer
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 3 users - assign the a different role to each user.
   - Sign into each account and make note of the JWT.
    ```bash
    GET https://YOUR_DOMAIN/authorize?
        audience=YOUR_AUDIENCE&
        response_type=token&
        client_id=YOUR_CLIENT_ID&
        redirect_uri=https://callbackurl
    ```
   - Create the postman collection Capdtone and add collection folder for each role. 
   - Right-clicking the collection folder for CastingAssistant,CastingDirector and ExecutiveProducer, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!


