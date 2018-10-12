from app import db

class Character(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Character.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Character: {}>".format(self.name)

class EarthboundCharacter(Character):

    __tablename__='Earthbound_Characters'

    psi = db.Column(db.Integer)

    def __init__(self, name, hp, attack, defense, psi):
        super(self, name, hp, attack, defense)
        self.psi = psi


