import asyncio

COOK_TIME = 3
EXTRAS_TIME = .5
TOTAL_ORDERS = 5


async def cook(order_id: int) -> None:
    print(f"\tCooking order #{order_id}")
    await asyncio.sleep(COOK_TIME)


async def add_extras(order_id: int) -> None:
    print(f"\tAdding extras to order #{order_id}")
    await asyncio.sleep(EXTRAS_TIME)


async def prepare_order(order_id: int) -> None:
    print(f"Preparing order #{order_id}")
    await cook(order_id)
    await add_extras(order_id)
    print(f"Order #{order_id} complete!")


async def main() -> None:
    await asyncio.gather(
        *(prepare_order(i) for i in range(1, TOTAL_ORDERS + 1))
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
