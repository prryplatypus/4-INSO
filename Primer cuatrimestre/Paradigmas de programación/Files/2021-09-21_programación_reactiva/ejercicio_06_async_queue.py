import asyncio
import random

AVG_COOK_TIME = 1
AVG_ORDER_TIME = 1
NUMBER_OF_COOKS = 2
NUMBER_OF_MACHINES = 2

queue = asyncio.Queue()


async def cook(id: int):
    while True:
        print(f"Empleado #{id} esperando para recibir orden")
        order = await queue.get()
        print(f"Empleado #{id} preparando nueva orden")
        await asyncio.sleep(order)
        queue.task_done()
        print(f"--- There's {queue.qsize()} items in the queue ---")


async def order(id: int):
    while True:
        print(f"Realizando nueva orden en máquina #{id}")
        await asyncio.sleep(random.uniform(AVG_ORDER_TIME / 2, AVG_ORDER_TIME * 2))
        print(f"Enviando orden a cocina desde máquina #{id}")
        queue.put_nowait(random.uniform(AVG_COOK_TIME / 2, AVG_COOK_TIME * 2))
        print(f"--- There's {queue.qsize()} items in the queue ---")


async def main():
    await asyncio.gather(
        *(asyncio.create_task(order(i)) for i in range(1, NUMBER_OF_MACHINES + 1)),
        *(asyncio.create_task(cook(i)) for i in range(1, NUMBER_OF_COOKS + 1)),
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
