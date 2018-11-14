from character.models import Character
from flask import request, jsonify, abort

class CharacterListCreate():
    @staticmethod
    def get():
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
    
    @staticmethod
    def post():
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

class CharacterRetrieveUpdateDelete():
    @staticmethod
    def get(character):
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
    
    @staticmethod
    def delete(character):
        character.delete()
        return {
            'message' : "character {0} ({1}) deleted successfully".format(character.name, character.id)
        }, 200
    
    @staticmethod
    def patch(request, character):
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
