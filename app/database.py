from flask_sqlalchemy import SQLAlchemy
from .models import db

def init_database(app):
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	with app.app_context():
		db.create_all()
		print("База данных инициализтрована!") 
