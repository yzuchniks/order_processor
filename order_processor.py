import asyncio
import random

from constants import DEFAULT_NUM_WORKERS, MAX_SIZE_QUE, RangeDelay, Status
from decorators import retry
from loggers import logger


class Order:
    def __init__(self, order_id, description):
        self.order_id = order_id
        self.description = description
        self.status = Status.PENDING.value

    def __str__(self):
        return f'Заказ {self.order_id}: {self.description} - {self.status}'


class Worker:
    def __init__(self, worker_id):
        self.worker_id = worker_id

    @retry()
    async def _process_order(self, order):
        order.status = Status.IN_PROGRESS.value
        logger.info(f'Worker {self.worker_id} начал обработку заказа: {order}')

        try:
            if random.random() < 0.3:
                raise Exception('Тестовая ошибка!')

            await asyncio.sleep(random.uniform(RangeDelay.MIN_DELAY.value,
                                               RangeDelay.MAX_DELAY.value))
            order.status = Status.DONE.value
            logger.info(
                f'Worker {self.worker_id} завершил обработку заказа: {order}'
            )
        except Exception as e:
            order.status = Status.FAILED.value
            logger.error(
                f'Worker {self.worker_id} ошибка при обработке заказа: '
                f'{order}, {str(e)}',
                exc_info=True
                )

    async def run(self, queue):
        while True:
            order = await queue.get()
            if order is None:
                break
            await self._process_order(order)


class OrderProcessor:
    def __init__(self, num_workers=DEFAULT_NUM_WORKERS):
        self.num_workers = num_workers
        self.queue = asyncio.Queue(maxsize=MAX_SIZE_QUE)
        self.workers = []

    async def _start_workers(self):
        for worker_id in range(self.num_workers):
            worker = Worker(worker_id)
            self.workers.append(asyncio.create_task(worker.run(self.queue)))

    async def _add_order(self, order):
        await self.queue.put(order)

    async def run(self, list_order):
        if not list_order:
            logger.warning('Передан пустой список заказов!')

        await self._start_workers()

        for order in list_order:
            await self._add_order(order)

        for _ in range(self.num_workers):
            await self.queue.put(None)

        await asyncio.gather(*self.workers)


async def main():
    order_list = [Order(i, f'Описание заказа {i}') for i in range(10)]
    order_processor = OrderProcessor()

    await order_processor.run(order_list)


if __name__ == '__main__':
    asyncio.run(main())
