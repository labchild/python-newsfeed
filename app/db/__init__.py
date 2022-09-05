from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g 

load_dotenv()

# connect to database with env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# start db connection
def init_db(app):
    Base.metadata.create_all(engine)

    app.teardown_appcontext(close_db)

# send session object for use with routes
def get_db():
    if 'db' not in g:
        # store db connectin in app context
        g.db = Session()

    return g.db

# close db connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
    