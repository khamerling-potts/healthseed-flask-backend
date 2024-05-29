from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from config import db, bcrypt

from models.instruction import Instruction

class Routine(db.Model, SerializerMixin):
    __tablename__ = 'routines'

    serialize_rules = ('-user', "-instructions.routine", "-medications.routines")

    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    notes = db.Column(db.String)
    times = db.Column(MutableList.as_mutable(ARRAY(db.String)), nullable=False)

    # One to many relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='routines')

    # One to many relationship with Instruction
    # Removing 'delete' and 'delete-orphan' cascade bc I want an instruction to exist without a routine
    instructions = db.relationship('Instruction', back_populates='routine', cascade='save-update, merge')

    # Many to many relationship with Medication
    medications = association_proxy('instructions', 'medication', creator=lambda medication_obj: Instruction(medication=medication_obj))

    @validates('times')
    def validate_time(self, key, times):
        for time in times:
            if time not in ['morning', 'afternoon', 'evening', 'any time']:
                raise ValueError('each time must be morning, afternoon, evening, or any time')
        return times
    

    




