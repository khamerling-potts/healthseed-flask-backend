from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

import phonenumbers


from config import db, bcrypt


# Models go here!
class Provider(db.Model, SerializerMixin):
    __tablename__ = "providers"

    serialize_rules = ('-user',)

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    address = db.Column(db.String)

    # One to many relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='providers')

    @validates("name")
    def validate_username(self, key, name):
        if name == "":
            raise ValueError("name must not be empty")
        return name
    
    @validates('phone')
    def validate_phone(self, key, phone):
        if not phone=='':
            try:
                number = phonenumbers.parse(phone, None)
                if not phonenumbers.is_possible_number(number) or not phonenumbers.is_valid_number(number):
                    raise ValueError('Not a valid phone number')
                return number.national_number
            except Exception as exc:
                raise Exception(exc)
        return phone

    def __repr__(self):
        return f"Provider {self.id}, {self.name}"