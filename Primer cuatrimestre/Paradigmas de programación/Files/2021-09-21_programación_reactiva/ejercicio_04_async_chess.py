import asyncio


AMATEUR_TIME = 0.03
AVERAGE_MOVES = 30
PRO_TIME = 0.005
TOTAL_PLAYERS = 24

pro_lock = asyncio.Lock()


async def play_chess(player_id: int) -> None:
    moves_done = 1
    while moves_done < AVERAGE_MOVES + 1:
        async with pro_lock:
            print(f"Pro player is making move {moves_done} for player {player_id}")
            await asyncio.sleep(PRO_TIME)
        print(f"Amateur player {player_id} is making move {moves_done}")
        await asyncio.sleep(AMATEUR_TIME)
        moves_done += 1


async def main():
    await asyncio.gather(
        *[
            play_chess(i)
            for i in range(1, TOTAL_PLAYERS)
        ]
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
