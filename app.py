#!/usr/bin/env python3
import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Movie, Actor
from flask_cors import CORS
from auth import AuthError, requires_auth
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response
    
    @app.route('/')
    def home_run():
        AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
        AUTH0_CALLBACK_URL = os.getenv("CALLBACK_URL")
        API_AUDIENCE = os.getenv("API_AUDIENCE")
        CLIENT_ID = os.getenv("CLIENT_ID")
        url = (
            f"https://{AUTH0_DOMAIN}/authorize"
            f"?audience={API_AUDIENCE}"
            f"&response_type=token&client_id="
            f"{CLIENT_ID}&redirect_uri="
            f"{AUTH0_CALLBACK_URL}"
        )
        
        return jsonify({
            'message': 'Please login to this URL',
            'url': url
        })
    
    @app.route('/movie', methods=['POST'])
    def add_movie():
        
        if not request.method == 'POST':
            abort(405)

        try:
            body = request.get_json()
            data = {
            'title': body['title'],
            'release_date': body['release_date']
            }

        except:
            abort(422)

        try:
            movie = Movie(**data)
            movie.insert()
            return jsonify(data)

        except:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
    