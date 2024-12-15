from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import uuid


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    seeker_profile = db.relationship(
        'SeekerProfile', uselist=False, backref='user')
    provider_profile = db.relationship(
        'ProviderProfile', uselist=False, backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'


class SeekerProfile(db.Model):
    __tablename__ = "seeker_profile"
    id = db.Column(db.Integer, primary_key=True)
    emergency_contact = db.Column(db.String(255), nullable=True)
    current_location = db.Column(db.String(255), nullable=True)
    preferred_radius = db.Column(db.Float, default=10.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<SeekerProfile for user {self.user_id}>'


class ProviderProfile(db.Model):
    __tablename__ = "provider_profile"
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    shelters = db.relationship('Shelter', backref='provider', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<ProviderProfile for user {self.user_id} - Organization: {self.organization_name}>'


class Flood_Alert(db.Model):
    __tablename__ = "flood_alert"
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    event = db.Column(db.String(100), nullable=False)
    area_desc = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    certainty = db.Column(db.String(50), nullable=False)
    urgency = db.Column(db.String(50), nullable=False)
    headline = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    coordinates = db.Column(db.Text, nullable=False)
    effective = db.Column(db.DateTime, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Alert {self.event}>"


class Shelter(db.Model):
    __tablename__ = "shelters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    current_occupancy = db.Column(db.Integer, default=0)
    provider_profile_id = db.Column(
        db.Integer, db.ForeignKey('provider_profile.id'), nullable=False)

    def __repr__(self):
        return f'<Shelter {self.name}>'
