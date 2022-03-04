"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import sys
sys.path.append(".") # Adds higher directory to python modules path.
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # load config (SQLALCHEMY_DATABASE_URI, FLASK_ENV)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        import routes                           # import routes of web services 
        from database.models import Product     # import Product model for init database 

        # create Product table if not exist
        createDB(Product)
        print(Product.query.all())
    
        return app

def createDB(Product):
    # create Product table if not exist
    db.create_all()
    # insert Product row if not exist
    if not Product.query.all():
        # id beside 0 is not required, it will be autoincrement (if there is a POST create Product will be useful)
        db.session.add(Product(desc="apple",price=10,quantity=100,id=0))  # id start from 0
        db.session.add(Product(desc="orange",price=20,quantity=200,id=1))
        db.session.add(Product(desc="watermelon",price=30,quantity=300,id=2))
        db.session.add(Product(desc="banana",price=40,quantity=400,id=3))
        db.session.add(Product(desc="cherry",price=50,quantity=500,id=4))
        db.session.add(Product(desc="figs",price=60,quantity=600,id=5))
        db.session.add(Product(desc="lime",price=70,quantity=700,id=6))
        db.session.add(Product(desc="pear",price=80,quantity=800,id=7))
        db.session.add(Product(desc="plum",price=90,quantity=900,id=8))
        db.session.add(Product(desc="olive",price=100,quantity=1000,id=9))
        db.session.add(Product(desc="pineapple",price=110,quantity=1100,id=10))  # total (0 - 10)
        db.session.commit()