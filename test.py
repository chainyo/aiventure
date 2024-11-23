import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import selectinload
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from aiventure.models import Lab, Player


sqlite_file_name = "aiventure.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = create_async_engine(sqlite_url)


async def select_players():
    async with AsyncSession(engine) as session:
        statement = select(Player).where(col(Player.user_id) == "3d89030b-d67f-4c50-a635-aaef6c2f1af7")
        result = await session.exec(statement)
        player = result.one()

    print(f"Player: {player}")
    print(f"Player labs: {player.labs}")

    async with AsyncSession(engine) as session:
        statement = (
            select(Player)
            .where(Player.user_id == "3d89030b-d67f-4c50-a635-aaef6c2f1af7")
            .options(
                selectinload(Player.labs).selectinload(Lab.investors),
                selectinload(Player.labs).selectinload(Lab.employees),
                selectinload(Player.labs).selectinload(Lab.models),
                selectinload(Player.labs).selectinload(Lab.player),
            )
        )
        result = await session.exec(statement)
        player = result.one()

    print(f"Player: {player}")
    print(f"Player labs: {player.labs}")
    print(f"Player investments: {player.investments}")
    print(f"Player labs 0 investors: {player.labs[0].investors}")
    print(f"Player labs 0 employees: {player.labs[0].employees}")
    print(f"Player labs 0 models: {player.labs[0].models}")
    print(f"Player labs 0 player: {player.labs[0].player}")


async def main():
    await select_players()

if __name__ == "__main__":
    asyncio.run(main())
