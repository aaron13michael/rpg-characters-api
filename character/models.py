from app import db

class Character(db.Model):

    __tablename__ = "Characters"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    hp = db.Column(db.Integer)
    mana = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    luck = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    
    def __init__(self, name, hp, mana, attack, defense, intelligence, luck):
        self.name = name
        self.hp = hp
        self.mana = mana
        self.attack = attack
        self.defense = defense
        self.intelligence = intelligence
        self.luck = luck

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

