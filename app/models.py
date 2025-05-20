from . import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """Represents a registered user in the system."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    photo = db.Column(db.String(2083), nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # One-to-many relationship
    profiles = db.relationship('Profile', back_populates='user')
    # List of users this user has marked as favourite
    favourites = db.relationship('Favourite', foreign_keys='Favourite.user_id_fk', back_populates='user', cascade="all, delete-orphan")
    # List of users who have marked this user as their favourite
    fans = db.relationship('Favourite', foreign_keys='Favourite.fav_user_id_fk', back_populates='fav_user', cascade="all, delete-orphan")

    def __init__(self, username, password, name, email, photo):
        self.username = username
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        self.name = name
        self.email = email
        self.photo = photo
    
    def can_add_profile(self):
        return len(self.profiles) < 3 # Enforce max profile rule

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'photo': self.photo,
            'date_joined': self.date_joined.isoformat() if self.date_joined else None
        }


class Profile(db.Model):
    """Represents a user's profile with personal and preference data."""
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    parish = db.Column(db.String(100), nullable=False)
    biography = db.Column(db.String(180), nullable=False) #db.text
    sex = db.Column(db.String(10), nullable=False)  # M/F/O
    race = db.Column(db.String(64), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    fav_cuisine = db.Column(db.String(100), nullable=False)
    fav_colour = db.Column(db.String(50), nullable=False)
    fav_school_subject = db.Column(db.String(100), nullable=False)
    political = db.Column(db.Boolean, nullable=False)
    religious = db.Column(db.Boolean, nullable=False)
    family_oriented = db.Column(db.Boolean, nullable=False)

    # Relationship back to user
    user = db.relationship('User', back_populates='profiles')

    def __init__(self, user_id_fk, description, parish, biography, sex,
                 race, birth_year, height, fav_cuisine,
                 fav_colour, fav_school_subject, political,
                 religious, family_oriented):
        self.user_id_fk = user_id_fk
        self.description = description
        self.parish = parish
        self.biography = biography
        self.sex = sex
        self.race = race
        self.birth_year = birth_year
        self.height = height
        self.fav_cuisine = fav_cuisine
        self.fav_colour = fav_colour
        self.fav_school_subject = fav_school_subject
        self.political = political
        self.religious = religious
        self.family_oriented = family_oriented

    def __repr__(self):
        return f"<Profile for User ID {self.user_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'parish': self.parish,
            'biography': self.biography,
            'sex': self.sex,
            'race': self.race,
            'birth_year': self.birth_year,
            'height': self.height,
            'fav_cuisine': self.fav_cuisine,
            'fav_colour': self.fav_colour,
            'fav_school_subject': self.fav_school_subject,
            'political': self.political,
            'religious': self.religious,
            'family_oriented': self.family_oriented
        }


class Favourite(db.Model):
    """Represents a user's favourite relationship with another user."""
    __tablename__ = 'favourites'

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships (you can access favourite users and users who favourited them)
    user = db.relationship('User', foreign_keys=[user_id_fk], back_populates='favourites')
    fav_user = db.relationship('User', foreign_keys=[fav_user_id_fk], back_populates='fans')

    # Add unique constraint on the combination of user_id_fk and fav_user_id_fk
    __table_args__ = (
        db.UniqueConstraint('user_id_fk', 'fav_user_id_fk', name='uix_user_fav'),
    )

    def __init__(self, user_id_fk, fav_user_id_fk):
        self.user_id_fk = user_id_fk
        self.fav_user_id_fk = fav_user_id_fk