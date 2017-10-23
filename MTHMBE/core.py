from MTHMBE import app

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

from contextlib import contextmanager


app.logger.debug("core.py")

db = SQLAlchemy(app)

api_manager = APIManager(app, flask_sqlalchemy_db=db)


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# configure Session class with desired options
Session = sessionmaker()

# later, we create the engine
#engine = create_engine('mysql://ec2-user:test@localhost/MTHMBE')
engine = create_engine(app.config['SQL_ENGINE'])

# associate it with our custom Session class
Session.configure(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

