from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models.models import orders
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def test_orders_operations() :
    try:
        # Start of transaction
        with session.begin():
            # Inserting a new order specifying customer_id
            new_order_id = \
                session.execute(orders.insert().values(customer_id=1, total_amount=1500.0)).inserted_primary_key[0]
            print(f"A new order with ID {new_order_id} was successfully created.")

            # Trying to insert an order without specifying customer_id (should cause an error)
            session.execute(orders.insert().values(total_amount=1000.0))

        # This line will only be executed if there were no errors
        print("All orders were inserted successfully.")
    except exc.IntegrityError as e:
        # Handle an integrity constraint violation exception
        print("Data integrity error:", e)
    except Exception as e:
        # Handle all other exceptions
        print("An error occurred:", e)
    finally :
        # Closing the session
        session.close()


# Running test function
test_orders_operations()
