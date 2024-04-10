from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates


from config import db, bcrypt

class Condition(db.Model, SerializerMixin):
    __tablename__ = 'conditions'

    serialize_rules = ('-user.conditions',)

    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String, nullable=False)

    # One to many relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='conditions')

    def __repr__(self):
        return f"Condition {self.id}, {self.description}"