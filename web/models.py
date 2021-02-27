from flask_sqlalchemy import SQLAlchemy
from web import db
from flask_login import LoginManager, UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    items = db.relationship('Item', backref='category', lazy=True)

    def __repr__(self):
        return self.name

    def all(self):
        return [self.id, self.name]

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)
    first_image = db.Column(db.String(200), nullable=False)
    second_image = db.Column(db.String(200), nullable=True)
    images = db.relationship('Image', backref='item', lazy=True)

    def __repr__(self):
        return self.title

    def all(self):
        return [self.id, self.category_id, self.title, self.price, self.isActive, self.text, self.first_image,
         self.second_image]


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
