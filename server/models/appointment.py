from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


from config import db, bcrypt


class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointments"

    serialize_rules = ('-user.appointments', '-provider.appointments')

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    # One to many relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='appointments')

     # One to many relationship with Provider
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'))
    provider = db.relationship('Provider', back_populates='appointments')

    @validates("category")
    def validate_username(self, key, category):
        if category == "":
            raise ValueError("category must not be empty")
        if category not in ['Vision', 'Dental', 'Medical', 'Mental Health', 'Fitness/Wellness']:
            raise ValueError("category must be one of 'Vision', 'Dental', 'Medical', 'Mental Health', 'Fitness/Wellness'")
        return category.lower()

    def __repr__(self):
        return f"Appointment {self.location}, ID {self.id}"