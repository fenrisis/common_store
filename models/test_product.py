import pytest
from models import products, users, roles, shops, categories


def setup_prerequisite_data(session) :
    # Insert role
    role_id = session.execute(roles.insert().values(name='Owner', permissions=['all'])).inserted_primary_key[0]

    # Insert user
    user_id = session.execute(
        users.insert().values(email='owner@example.com', username='shopowner', password='password',
                              role_id=role_id)).inserted_primary_key[0]

    # Insert category
    category_id = session.execute(categories.insert().values(name='Electronics')).inserted_primary_key[0]

    # Insert shop
    shop_id = session.execute(shops.insert().values(name='Electronics Shop', owner_id=user_id)).inserted_primary_key[0]

    return shop_id, category_id


def insert_product(session, name, description, price, quantity, shop_id, category_id) :
    product_id = session.execute(
        products.insert().values(
            name=name, description=description, price=price,
            quantity=quantity, shop_id=shop_id, category_id=category_id
        )
    ).inserted_primary_key[0]
    session.commit()
    return product_id


@pytest.mark.parametrize("name, description, price, quantity, expected_exception",
                         [
                             ('Iphone', 'Apple phone', 1000, 10, None),
                             ('Glaxy s', 'Samsung phone', 900, 20,  None),
                             ('', '', -10, 0, 1, 1, ValueError),

                         ]
                         )
def test_insert_product(db_session, name, description, price, quantity, expected_exception) :
    shop_id, category_id = setup_prerequisite_data(db_session)

    if expected_exception :
        with pytest.raises(expected_exception) :
            insert_product(db_session, name, description, price, quantity, shop_id, category_id)
    else:
        product_id = insert_product(db_session, name, description, price, quantity, shop_id, category_id)
        assert product_id is not None
