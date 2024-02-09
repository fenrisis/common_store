from sqlalchemy import select
from database import SessionLocal
from models.models import users, orders

def get_user_email_by_id(user_id: int):
    with SessionLocal() as session:
        result = session.execute(select(users.c.email).where(users.c.id == user_id)).first()
        return result[0] if result else None

def get_user_email_by_order_id(order_id: int):
    with SessionLocal() as session:
        result = session.execute(
            select(users.c.email)
            .join(orders, orders.c.customer_id == users.c.id)
            .where(orders.c.order_id == order_id)
        ).first()
        return result[0] if result else None