from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


from config import db, bcrypt


# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ('-_password_hash',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    # ratings = db.Column(MutableList.as_mutable(ARRAY(db.Integer)), nullable=True)
    birthday = db.Column(db.Date, nullable=False)
    _password_hash = db.Column(db.String)

    # One to many relationship with Condition
    conditions = db.relationship('Condition', back_populates='user', cascade='all, delete-orphan')

    # One to many relationship with Provider
    providers = db.relationship('Provider', back_populates='user', cascade='all, delete-orphan')

    # One to many relationship with Instruction
    instructions = db.relationship('Instruction', back_populates='user', cascade='all, delete-orphan')

    # One to many relationship with Medication
    medications = db.relationship('Medication', back_populates='user', cascade='all, delete-orphan')

    # One to many relationship with Routine
    routines = db.relationship('Routine', back_populates='user', cascade='all, delete-orphan')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")
        print('password set')

    def authenticate(self, password):
        print('authenticate')
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    @validates("username")
    def validate_username(self, key, username):
        if username == "":
            raise ValueError("username must not be empty")
        if db.session.query(User.id).filter_by(username=username.lower()).first():
            raise ValueError("username must be unique")
        return username.lower()

    def __repr__(self):
        return f"User {self.username}, ID {self.id}"