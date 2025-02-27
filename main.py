import asyncio

from src.orders.order_processor import Order, OrderProcessor


async def main():
    order_list = [Order(i, f"Описание заказа {i}") for i in range(10)]
    order_processor = OrderProcessor()

    await order_processor.run(order_list)


if __name__ == "__main__":
    asyncio.run(main())
