from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import users, roles

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# engine
engine = create_engine(DATABASE_URL, echo=True)

# session
Session = sessionmaker(bind=engine)
session = Session()


# Insertion
session.execute(users.insert().values(email='user@example.com', username='user1', password='password', registered_at=datetime.now()))
session.execute(roles.insert().values(name='Admin', permissions=['create', 'read', 'update', 'delete']))


session.commit()


session.close()
