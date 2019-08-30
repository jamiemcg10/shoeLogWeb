from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    activities = db.relationship('Activity', backref='athlete', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
        
        
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    walk_miles = db.Column(db.Float)
    run_miles = db.Column(db.Float)
    total_miles = db.Column(db.Float)
    type = db.Column(db.String(50))
    shoe = db.Column(db.String(75), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)
    
    def __repr__(self):
        return '<{} miles on {}.>'.format(self.total_miles, self.shoe)