import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import metadata, shops, categories
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

@pytest.fixture(scope="module")
def engine():
    return create_engine(DATABASE_URL)

@pytest.fixture(scope="module")
def tables(engine):
    metadata.create_all(engine)  # create all tables
    yield
    metadata.drop_all(engine)  # drop all tables after tests are done

@pytest.fixture(scope="function")
def db_session(engine, tables):
    """Creates a new database session with a rollback at the end of each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker()(bind=connection)
    yield session
    transaction.rollback()
    connection.close()





