import asyncio
import random

from typing import Union


SLEEP_TIME = 2
TASKS = 3
THRESHOLD = 10


async def get_random_number(task_id: int, threshold: Union[float, int]) -> None:
    while True:
        num = random.randint(0, threshold)
        if num > threshold:
            break
        print(f"Task {task_id} failed to find num over threshold ({num})")
        await asyncio.sleep(SLEEP_TIME)

    print(f"Task {task_id} found num over threshold ({num})")


async def main():
    await asyncio.gather(
        *[
            get_random_number(i, random.randint(0, THRESHOLD))
            for i in range(1, TASKS + 1)
        ]
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
