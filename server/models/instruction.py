from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


from config import db, bcrypt

class Instruction(db.Model, SerializerMixin):
    __tablename__ = 'instructions'

    serialize_rules = ('-user', '-routine.instructions', '-medication.instructions')

    id=db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False)
    amount = db.Column(db.String, nullable=False)

    # One to many relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='instructions')

    # One to many relationship with Routine
    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id'))
    routine = db.relationship('Routine', back_populates='instructions')

     # One to many relationship with Medication
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'))
    medication = db.relationship('Medication', back_populates='instructions')

   
