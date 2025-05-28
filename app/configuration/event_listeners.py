from pgvector.psycopg2 import register_vector
from sqlalchemy import event
from app import db

@event.listens_for(db.engine, "connect")
def _register_vector(dbapi_connection):
    register_vector(dbapi_connection)