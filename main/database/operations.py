import asyncio
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine
from database.database_model import Lenenergo
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select


# Создайте асинхронное подключение к базе данных PostgreSQL
async def create_postgr_engine(username, password):
    engine = create_async_engine(f'postgresql+asyncpg://{username}:{password}@localhost:5432/adresses', echo=True)
    async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Lenenergo.metadata.create_all)
    return engine


async def async_lenenergo_add(data, username, password) -> None:
    engine = await create_postgr_engine(username=username, password=password)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    data = data.fillna('')

    async with async_session() as session:
        async with session.begin():
            for index, row in data.iterrows():
                lenenergo_entry = Lenenergo(
                    region=row['Регион РФ (область, край, город фед. значения, округ)'],
                    admin_district=row['Административный район'],
                    locality=row['Населённый пункт'],
                    street=row['Улица'],
                    start_disconnect_date=row['Плановое время начала отключения электроснабжения'],
                    start_disconnect_time=row['Плановое время начала отключения электроснабжения'],
                    end_disconnect_date=row['Плановое время восстановления отключения электроснабжения'],
                    end_disconnect_time=row['Плановое время восстановления отключения электроснабжения'],
                    branch=row['Филиал'],
                    substation=row['РЭС'],
                    comment=row['Комментарий']
                )
                session.add(lenenergo_entry)
        await session.commit()

    await engine.dispose()

async def get_lenenergo(username: str, password: str):
    engine = await create_postgr_engine(username=username, password=password)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        data = await Lenenergo.to_dataframe(session)

    await engine.dispose()
    return data







