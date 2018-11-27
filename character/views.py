from character.models import Character
from flask import request, jsonify, abort

class CharacterListCreate():
    @staticmethod
    def get():
        characters = Character.get_all()
        results =[]
        for c in characters:
            obj = makeCharacterObject(c)
            results.append(obj)
            response = jsonify(results)
            response.status_code = 200
        return response
    
    @staticmethod
    def post():
        name = request.data.get('name', None)
        try:
            hp = int(request.data.get('hp', ''))
            mana = int(request.data.get('mana', ''))
            attack = int(request.data.get('attack', ''))
            defense = int(request.data.get('defense', ''))
            intelligence = int(request.data.get('intelligence', ''))
            luck = int(request.data.get('luck', ''))
        except ValueError:
            return {
            'message' : "Invalid stat data. All stats must be integers"
        }, 400
        if name is not None:
            character = Character(name=name, hp=hp, mana=mana, attack=attack, defense=defense, intelligence=intelligence, luck=luck)
            character.save()
            response = jsonify(makeCharacterObject(character))
            response.status_code = 201
            return response

class CharacterRetrieveUpdateDelete():
    @staticmethod
    def get(character):
        obj = makeCharacterObject(character)
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
        character.save()
        obj = makeCharacterObject(character)
        response = jsonify(obj)
        response.status_code = 200
        return response
    
class CharacterLevelUp():
    @staticmethod
    def post():
        try:
            id = int(request.data.get('id', ''))
            exp = int(request.data.get('exp', ''))
        except ValueError as e:
            return {
                'message' : 'invalid values passed id: {0}, exp: {1}. Values must be integers'.format(request.data.get('id', '<empty>'), request.data.get('exp', '<empty>'))
            }, 400
        character = Character.query.filter_by(id=id).first()
        character.levelUp(exp)
        character.save()
        obj = makeCharacterObject(character)
        response = jsonify(obj)
        response.status_code = 200
        return response

def makeCharacterObject(character):
    obj = {
            'id' : character.id,
            'name' : character.name,
            'hp' : character.hp,
            'mana' : character.mana,
            'attack' : character.attack,
            'defense' : character.defense,
            'intelligence' : character.intelligence,
            'luck' : character.luck,
            'level' : character.level,
            'Exp to next level' : character.expToNext,
            'date_created' : character.date_created,
            'date_modified' : character.date_modified
        }
    return obj

