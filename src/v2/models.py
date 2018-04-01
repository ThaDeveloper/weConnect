from src import db
from werkzeug.security import generate_password_hash
import uuid
from src.utils import ValidationError


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
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
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

    def __init__(self, username, password, first_name, last_name, admin=False):
        """Initialize a user instance
        usernames are stripped off any spaces and case set to lower
        Passwords are encrypted before saving to db
        Admin privellege is set to false by default
        """
        self.username = username.strip()
        self.password = generate_password_hash(password, method='sha256')
        self.first_name = first_name.strip().replace(" ", "").title()
        self.last_name = last_name.strip().replace(" ", "").title()
        self.public_id = str(uuid.uuid4())
        self.admin = admin

    def add(self):
        """Add user to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a user from the database"""
        db.session.delete(self)
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

    def import_data(self, data):
        """Validates request data from user"""
        try:
            if len(data['name'].strip()) == 0:
                return "Invalid"
            else:
                self.name = data['name']
                self.description = data['description']
                self.location = data['location']
                self.category = data['category']
        except KeyError as e:
            raise ValidationError("Invalid: Field required: " + e.args[0])
        return self

    def search(self, params):
        """Search by name and filter by category and location"""
        page = params['page']
        limit = params['limit']
        location = params['location']
        category = params['category']
        query = params['query']

        if query or location or category:
            if query and not location and not category:
                return self.query.filter(
                    Business.name.ilike(
                        '%' +
                        query +
                        '%')).paginate(
                    page,
                    limit,
                    error_out=False).items
            if category and not location:
                return self.query.filter(
                    Business.category == category
                ).paginate(page, limit, error_out=False).items
            if location and not category:
                return self.query.filter(
                    Business.location == location
                ).paginate(page, limit, error_out=False).items
            if category and location:
                return self.query.filter(
                    Business.category == category,
                    Business.location == location).paginate(
                    page,
                    limit,
                    error_out=False).items
            if query and location and not category:
                return self.query.filter(
                    Business.location == location,
                    Business.name.ilike('%' + query + '%')
                ).paginate(page, limit, error_out=False).items
            if query and category and not location:
                return self.query.filter(
                    Business.category == category,
                    Business.name.ilike('%' + query + '%')
                ).paginate(page, limit, error_out=False).items
            if query and category and location:
                return self.query.filter(
                    Business.category == category,
                    Business.location == location,
                    Business.name.ilike('%' + query + '%')
                ).paginate(page, limit, error_out=False).items
        return self.query.order_by(
            Business.created_at.desc()).paginate(
            page, limit, error_out=False).items


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

    def import_data(self, data):
        """Validates request data from user"""
        try:
            if len(data["title"].strip()) == 0:
                return "Invalid"
            else:
                self.title = data["title"]
                self.message = data["message"]
        except KeyError as e:
            raise ValidationError("Invalid: Field required: " + e.args[0])
        return self
