from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship
    signup = db.relationship('Signup', backref='activities')
    
    # Add serialization rules

    serialize_rules = ('-signups.activities',)
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Add relationship
    signup = db.relationship('Signup', backref='campers')
    
    # Add serialization rules

    serialize_rules = ('-signups.campers',)
    
    # Add validation
    @validates('name')
    def validates_name(self, key, name):
        if not isinstance(name, str):
            raise ValueError('Wrong name')
        return name
    
    @validates('age')
    def validates_age(self, key, age):
        if not isinstance(age, int) and 8 <= age <= 18:
            raise ValueError('Your too young bruh or old')
        return age

    
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    # Add relationships
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id')) 

    camper = db.relationship('Camper', backref='signups')
    activity = db.relationship('Activity', backref='signups')
    
    # Add serialization rules

    serialize_rules = ('-campers.signups', '-activities.signups',)

    
    # Add validation
    @validates('time')
    def validates_time(self, key, time):
        if not isinstance(time, int) and 0 <= time <= 23:
            raise ValueError('Nah son')
        return time
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
