from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import users, roles,  bank_accounts
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def test_bank_accounts_operations():
    # Add a role if it doesn't already exist
    buyer_role_id = session.query(roles.c.id).filter_by(name='Buyer').scalar()
    if not buyer_role_id:
        buyer_role_id = session.execute(roles.insert().values(name='Buyer', permissions=['read'])).inserted_primary_key[
            0]
        session.commit()

    # Checking and adding users
    if not session.query(users).filter_by(id=1).scalar():
        session.execute(users.insert().values(id=1, email='user1@example.com', username='user1', password='password1',
                                              registered_at=datetime.utcnow(), role_id=buyer_role_id))
    if not session.query(users).filter_by(id=2).scalar():
        session.execute(users.insert().values(id=2, email='user2@example.com', username='user2', password='password2',
                                              registered_at=datetime.utcnow(), role_id=buyer_role_id))
    session.commit()

    # Start of transaction
    with session.begin():
        # Insert two entries into bank_accounts
        account_id_1 = session.execute(bank_accounts.insert().values(balance=1000.0, user_id=1)).inserted_primary_key[0]
        account_id_2 = session.execute(bank_accounts.insert().values(balance=500.0, user_id=2)).inserted_primary_key[0]

        # Update the balance of one of the accounts
        session.execute(bank_accounts.update().where(bank_accounts.c.account_id == account_id_2).values(balance=600.0))

        # Deleting one of the accounts
        session.execute(bank_accounts.delete().where(bank_accounts.c.account_id == account_id_1))


# Execute the fixture
test_bank_accounts_operations()
session.close()
