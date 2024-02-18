from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import select, insert, update, delete
from rabbitmq import send_order_to_queue, send_update_order_to_queue
from sqlalchemy.orm import Session
from schemas import ProductCreate, ProductUpdate, OrderCreate, OrderStatusUpdate, CartItemCreate, CartItem, CartItemUpdate
from models.models import users, metadata, products, orders, cart_items
from typing import Optional
from database import engine
from telegram_utils import send_telegram_message
from notification_utils import get_telegram_chat_id_by_id, get_telegram_chat_id_by_order_id

metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/")
def create_user(user_data: dict):
    with Session(engine) as session:
        stmt = insert(users).values(user_data)
        session.execute(stmt)
        session.commit()
        return {"status": "user created"}


@app.get("/users/{user_id}")
def read_user(user_id: int):
    with Session(engine) as session:
        stmt = select(users).where(users.c.id == user_id)
        result = session.execute(stmt).first()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = dict(result._mapping)
        return {"status": "success", "data": user_data}


@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: dict):
    with Session(engine) as session:
        stmt = (
            update(users)
            .where(users.c.id == user_id)
            .values(user_data)
        )
        result = session.execute(stmt)
        session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success", "data": user_data}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        stmt = delete(users).where(users.c.id == user_id)
        result = session.execute(stmt)
        session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "user deleted"}


@app.post("/products/")
def create_product(product_data: ProductCreate):
    with Session(engine) as session:
        # Использование model_dump для преобразования модели Pydantic в словарь
        product_dict = product_data.dict()
        stmt = insert(products).values(**product_dict)
        session.execute(stmt)
        session.commit()
        return {"status": "product created"}


@app.get("/products/")
def read_products(category_id: Optional[int] = None, shop_id: Optional[int] = None):
    with Session(engine) as session:
        query = select(products)
        if category_id:
            query = query.where(products.c.category_id == category_id)
        if shop_id:
            query = query.where(products.c.shop_id == shop_id)
        result = session.execute(query).fetchall()
        return [{"name": item.name, "description": item.description, "price": item.price, "quantity": item.quantity} for item in result]


@app.get("/products/{product_id}")
def read_product(product_id: int):
    with Session(engine) as session:
        result = session.execute(select(products).where(products.c.id == product_id)).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Product not found")

        # Преобразование результата запроса в словарь
        product_data = {key: value for key, value in result._mapping.items()}
        return product_data


@app.put("/products/{product_id}")
def update_product(product_id: int, product_data: ProductUpdate) :
    update_data = product_data.dict(exclude_none=True)

    if not update_data :
        raise HTTPException(status_code=400, detail="No data provided to update")

    with Session(engine) as session :
        stmt = update(products).where(products.c.id == product_id).values(**update_data)
        result = session.execute(stmt)
        if result.rowcount == 0 :
            session.rollback()  # Откатываем изменения, если продукт не найден
            raise HTTPException(status_code=404, detail="Product not found")
        session.commit()
        return {"status" : "product updated"}


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    with Session(engine) as session:
        stmt = delete(products).where(products.c.id == product_id)
        result = session.execute(stmt)
        session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"status": "product deleted"}


@app.post("/orders/")
async def create_order(order_data: OrderCreate):
    with Session(engine) as session:
        stmt = insert(orders).values(customer_id=order_data.customer_id, total_amount=order_data.total_amount)
        session.execute(stmt)
        session.commit()
        chat_id = get_telegram_chat_id_by_id(order_data.customer_id)
        if chat_id:
            await send_telegram_message(chat_id, "Ваш заказ принят. Спасибо за ваш заказ!")
        send_order_to_queue(order_data.dict())
        return {"status": "order created"}

@app.get("/orders/{order_id}")
def read_order(order_id: int):
    with Session(engine) as session:
        result = session.execute(select(orders).where(orders.c.order_id == order_id)).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Order not found")
        order_data = {key: value for key, value in result._mapping.items()}
        return order_data


@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: int, order_status: OrderStatusUpdate):
    with Session(engine) as session:
        stmt = update(orders).where(orders.c.order_id == order_id).values(status=order_status.status)
        result = session.execute(stmt)
        if result.rowcount == 0:
            session.rollback()
            raise HTTPException(status_code=404, detail="Order not found")
        else:
            session.commit()
            chat_id = get_telegram_chat_id_by_order_id(order_id)
            if chat_id:
                await send_telegram_message(chat_id, f"Статус вашего заказа изменен: {order_status.status}.")
            send_update_order_to_queue(order_id, order_status.status)
            return {"status": "Order status updated"}

@app.get("/orders/user/{customer_id}")
def read_orders_by_customer(customer_id: int):
    with Session(engine) as session:
        result = session.execute(select(orders).where(orders.c.customer_id == customer_id)).fetchall()
        orders_list = [{key: value for key, value in row._mapping.items()} for row in result]
        return orders_list


@app.post("/cart-items/")
def add_product_to_cart(cart_item: CartItemCreate):
    with Session(engine) as session:
        db_item = cart_items.insert().values(
            user_id=cart_item.user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        session.execute(db_item)
        session.commit()
        return {"status": "Product added to cart"}


@app.get("/cart-items/{user_id}")
def get_cart_items(user_id: int):
    with Session(engine) as session:
        result = session.execute(select(cart_items).where(cart_items.c.user_id == user_id)).fetchall()
        items_list = [
            {
                "id": item.id,
                "user_id": item.user_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "added_at": item.added_at.isoformat() if item.added_at else None,
            } for item in result
        ]
        return items_list


@app.put("/cart-items/{item_id}")
def update_cart_item_quantity(item_id: int, cart_item: CartItemUpdate):
    with Session(engine) as session:
        db_item = update(cart_items).where(cart_items.c.id == item_id).values(quantity=cart_item.quantity)
        result = session.execute(db_item)
        if result.rowcount == 0:
            session.rollback()
            raise HTTPException(status_code=404, detail="Cart item not found")
        session.commit()
        return {"status": "Cart item quantity updated"}


@app.delete("/cart-items/{item_id}")
def delete_cart_item(item_id: int):
    with Session(engine) as session:
        db_item = delete(cart_items).where(cart_items.c.id == item_id)
        result = session.execute(db_item)
        if result.rowcount == 0:
            session.rollback()
            raise HTTPException(status_code=404, detail="Cart item not found")
        session.commit()
        return {"status": "Cart item deleted"}