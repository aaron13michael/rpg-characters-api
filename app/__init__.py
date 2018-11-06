from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from flask import request, jsonify, abort

db = SQLAlchemy()

def create_app(config_name):
    from app.models import Character
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/characters/', methods=['POST', 'GET'])
    def characters():
        if request.method == "POST":
            name = request.data.get('name', None)
            hp = int(request.data.get('hp', ''))
            attack = int(request.data.get('attack', ''))
            defense = int(request.data.get('defense', ''))
            if name is not None:
                character = Character(name=name, hp=hp, attack=attack, defense=defense)
                character.save()
                response = jsonify({
                    'id' : character.id,
                    'name' : character.name,
                    'hp' : character.hp,
                    'attack' : character.attack,
                    'defense' : character.defense,
                    'date_created' : character.date_created,
                    'date_modified' : character.date_modified
                })
                response.status_code = 201
                return response
        elif request.method == "GET":
            characters = Character.get_all()
            results =[]

            for c in characters:
                obj = {
                    'id' : c.id,
                    'name' : c.name,
                    'hp' : c.hp,
                    'attack' : c.attack,
                    'defense' : c.defense,
                    'date_created' : c.date_created,
                    'date_modified' : c.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'message' : "Method {} not allowed".format(request.method)
            })
            response.status_code = 400
            return response
    
    @app.route('/characters/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
    def character_detail(id, **kwargs):
        # get a character from it's ID
        character = Character.query.filter_by(id=id).first()
        if not character:
            # Raise an HTTPException with a 404
            abort(404)
        if request.method == "GET":
            obj = {
                'id' : character.id,
                'name' : character.name,
                'hp' : character.hp,
                'attack' : character.attack,
                'defense' : character.defense,
                'date_created' : character.date_created,
                'date_modified' : character.date_modified
            }
            response = jsonify(obj)
            response.status_code = 200
            return response
        elif request.method == "DELETE":
            character.delete()
            return {
                'message' : "character {0} ({1}) deleted successfully".format(character.name, character.id)
            }, 200
        elif request.method == "PATCH":
            # PATCH values are optional
            n_name = repr(request.data.get('name', ''))
            character.name = n_name
            try:
                
                character.hp = int(request.data.get('hp', character.hp))
                character.attack = int(request.data.get('attack', character.attack))
                character.defense = int(request.data.get('defense', character.defense))
            except ValueError as e:
                bad_value = str(e).split(":")[-1]
                return {
                    'message' : "stat value {} is invalid".format(bad_value)
                }, 400
            character.save()
            obj = {
                'id' : character.id,
                'name' : character.name,
                'hp' : character.hp,
                'attack' : character.attack,
                'defense' : character.defense,
                'date_created' : character.date_created,
                'date_modified' : character.date_modified
            }
            response = jsonify(obj)
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'message' : "Method {} not allowed".format(request.method)
            })
            response.status_code = 400
            return response

    return app
