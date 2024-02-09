from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Numeric, DateTime, func

metadata = MetaData()

roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey("roles.id")),
)


shops = Table(
    "shops",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("owner_id", Integer, ForeignKey("users.id"), nullable=False),
)

categories = Table(
    "categories",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("price", Integer, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("shop_id", Integer, ForeignKey("shops.id"), nullable=False),
    Column("category_id", Integer, ForeignKey("categories.id"), nullable=False),
)

cart_items = Table(
    "cart_items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("product_id", Integer, ForeignKey("products.id"), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("added_at", TIMESTAMP, default=datetime.utcnow),
)

bank_accounts = Table(
    "bank_accounts",
    metadata,
    Column("account_id", Integer, primary_key=True),
    Column("balance", Numeric, nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
)

orders = Table(
    "orders",
    metadata,
    Column("order_id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("total_amount", Numeric, nullable=False),
    Column("status", String, nullable=False, server_default="new"),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)