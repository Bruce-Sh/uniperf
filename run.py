# -*- encoding: utf-8 -*-
from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config

from config import config_dict
from app import create_app, db
from app.base.dbthread import DBThread

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

application = create_app( app_config ) 
Migrate(application, db)


@application.before_request
def start_DB_thread():
    print("starting DB thread")
    db_thrd = DBThread("UpdateDBThread", app=application)
    db_thrd.start()

if __name__ == "__main__":
    application.run()
