# Thiss folder iss package

from flask import Flask
from config import Config

#importing migrate
from flask_migrate import Migrate

#we are importing routefolder home.py 
from app.routes.home import home_bp
#employefile imported
from app.routes.employee import employee_bp
#department file imported
from app.routes.department import department_bp

from app.models import db
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    #initialized database
    db.init_app(app)

    #flask migrate
    migrate.init_app(app,db)     



    #now wwe are registing home.app
    app.register_blueprint(home_bp)
    #Registered Employee files  :- if the file is not resisted then NOT found will show in web browser  
    app.register_blueprint(employee_bp)
    #registered department file
    app.register_blueprint(department_bp)   

    return app