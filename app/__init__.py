from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from flask import request, jsonify, abort

db = SQLAlchemy()

def create_app(config_name):
    from app.models import Character
    from app.views import CharacterListCreate, CharacterRetrieveUpdateDelete, CharacterLevelUp
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/characters/', methods=['POST', 'GET'])
    def characters():
        if request.method == "POST":
            return CharacterListCreate.post()
        elif request.method == "GET":
            return CharacterListCreate.get()

    @app.route('/characters/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
    def character_detail(id, **kwargs):
        # get a character from it's ID
        character = Character.query.filter_by(id=id).first()
        if not character:
            # Raise an HTTPException with a 404
            abort(404)
        if request.method == "GET":
            return CharacterRetrieveUpdateDelete.get(character)
        elif request.method == "DELETE":
            return CharacterRetrieveUpdateDelete.delete(character)
        elif request.method == "PATCH":
            return CharacterRetrieveUpdateDelete.patch(request, character)

    @app.route('/characters/addexp/', methods=['POST'])
    def character_level_up():
        return CharacterLevelUp.post()

    return app