from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models.models import users, roles, products, categories, cart_items, shops, bank_accounts, orders

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# engine
engine = create_engine(DATABASE_URL, echo=True)

# session
Session = sessionmaker(bind=engine)
session = Session()

# Insert roles
buyer_role_id = session.execute(roles.insert().values(name='Buyer', permissions=['read'])).inserted_primary_key[0]

# Insert user with the buyer role
buyer_user_id = session.execute(users.insert().values(email='buyer@example.com', username='buyer1', password='password', registered_at=datetime.now(), role_id=buyer_role_id)).inserted_primary_key[0]

# Insert categories and get their IDs
category_a_id = session.execute(categories.insert().values(name='Category A')).inserted_primary_key[0]
category_b_id = session.execute(categories.insert().values(name='Category B')).inserted_primary_key[0]

# Ensure that the shop exists before adding products
shop_id = session.execute(shops.insert().values(name='Shop 1', owner_id=buyer_user_id)).inserted_primary_key[0] # Adding a shop

# Adding products with existing category_id and shop_id
product_a_id = session.execute(products.insert().values(name='Iphone', description='Apple phone', price=1000, quantity=10, shop_id=shop_id, category_id=category_a_id)).inserted_primary_key[0]
product_b_id = session.execute(products.insert().values(name='Glaxy s', description='Samsung phone', price=900, quantity=20, shop_id=shop_id, category_id=category_b_id)).inserted_primary_key[0]
product_c_id = session.execute(products.insert().values(name='Pixel', description='Google phone', price=800, quantity=30, shop_id=shop_id, category_id=category_a_id)).inserted_primary_key[0]

# Adding products to the cart of the created buyer
session.execute(cart_items.insert().values(user_id=buyer_user_id, product_id=product_a_id, quantity=2, added_at=datetime.now()))
session.execute(cart_items.insert().values(user_id=buyer_user_id, product_id=product_c_id, quantity=1, added_at=datetime.now()))

session.commit()
session.close()
