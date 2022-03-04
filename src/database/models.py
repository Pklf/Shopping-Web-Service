"""Data models for database."""
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from __init__ import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Products {self.desc} #{self.id}: ${self.price}, {self.quantity}>'
    
    def __str__(self):
        return f'<Products {self.desc} #{self.id}: ${self.price}, {self.quantity}>'

    def to_json(self):
        return {
                'id': self.id,
                'desc': self.desc,
                'price': self.price,
                'quantity': self.quantity,
                }