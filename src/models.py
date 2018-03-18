from src import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(db.Model):
    """Create users table
    One-to-Many relationship with review and business
    User has many businessess
    User has many reviews
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    businesses = db.relationship(
        'Business',
        backref='owner',
        cascade='all, delete-orphan'
    )
    reviews = db.relationship(
        'Review',
        backref='reviewer',
        cascade='all, delete-orphan'
    )

    def __init__(self, username, password):
        """Initialize a user instance
        usernames are stripped off any spaces and case set to lower
        Passwords are encrypted before saving to db
        Admin privellege is set to false by default
        """
        self.username = username.lower().strip()
        self.password = generate_password_hash(password, method='sha256')
        self.public_id = str(uuid.uuid4())
        self.admin = False

    def add(self):
        """Add user to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a user from the database"""
        db.session.add(self)
        db.session.commit()


class Business(db.Model):
    """Create table businesses
    a business belongs to user
    a business has many reviews
    """
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    logo = db.Column(db.String())
    description = db.Column(db.String())
    category = db.Column(db.String(50), index=True)
    location = db.Column(db.String(50), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    reviews = db.relationship(
        'Review',
        backref='business',
        cascade='all, delete-orphan'
    )

    def add(self):
        """Add a business to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a business"""
        db.session.delete(self)
        db.session.commit()


class Review(db.Model):
    """Create table reviews
    a review belongs to a business
    a review belongs to a user
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    message = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    business_id = db.Column(
        db.Integer,
        db.ForeignKey('businesses.id'),
    )

    def add(self):
        """Add a review to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a review."""
        db.session.delete(self)
        db.session.commit()
