# common_store
This is a common store FastAPI webapp
Эндпоинты
Создание пользователя
Метод: POST
URL: /users/
Тело запроса: {"email": "user@example.com", "username": "user", "password": "password"}
Ответ: {"status": "user created"}
Чтение информации о пользователе
Метод: GET
URL: /users/{user_id}
Ответ: {"status": "success", "data": { информация о пользователе }}
Обновление информации о пользователе
Метод: PUT
URL: /users/{user_id}
Тело запроса: {"email": "newemail@example.com", "username": "newuser", "password": "newpassword"}
Ответ: {"status": "success", "data": { обновленная информация о пользователе }}
Удаление пользователя
Метод: DELETE
URL: /users/{user_id}
Ответ: {"status": "user deleted"}
Создание продукта
Метод: POST
URL: /products/
Тело запроса: {"name": "Product Name", "description": "Product Description", "price": 100, "quantity": 10, "shop_id": 1, "category_id": 1}
Ответ: {"status": "product created"}
Чтение информации о продукте
Метод: GET
URL: /products/{product_id}
Ответ: { информация о продукте }
Обновление информации о продукте
Метод: PUT
URL: /products/{product_id}
Тело запроса: {"name": "New Product Name", "description": "New Description", "price": 150, "quantity": 20}
Ответ: {"status": "product updated"}
Удаление продукта
Метод: DELETE
URL: /products/{product_id}
Ответ: {"status": "product deleted"}
Создание заказа
Метод: POST
URL: /orders/
Тело запроса: {"customer_id": 1, "total_amount": 500}
Ответ: {"status": "order created"}
Чтение информации о заказе
Метод: GET
URL: /orders/{order_id}
Ответ: { информация о заказе }
Обновление статуса заказа
Метод: PUT
URL: /orders/{order_id}/status
Тело запроса: {"status": "processed"}
Ответ: {"status": "order status updated"}
Чтение заказов пользователя
Метод: GET
URL: /orders/user/{customer_id}
Ответ: [ список заказов пользователя ]
Модуль RabbitMQ
Используется для асинхронной обработки сообщений о создании и обновлении статусов заказов.

Очередь новых заказов (new_orders): Сообщения в эту очередь отправляются при создании новых заказов. Сообщение содержит данные о заказе.
Очередь обновлений заказов (order_updates): Сообщения об обновлении статусов заказов отправляются в эту очередь. Сообщение содержит идентификатор заказа и новый статус.
