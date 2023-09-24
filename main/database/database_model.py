from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.ext.asyncio import create_async_engine
import pandas as pd
import asyncio

Base = declarative_base()
class Lenenergo(Base):
    __tablename__ = 'lenenergo_table'

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(Text, nullable=True)  # Теперь допускаются значения None (NaN)
    admin_district = Column(Text, nullable=True)
    locality = Column(Text, nullable=True)
    street = Column(Text, nullable=True)
    start_disconnect_date = Column(Text, nullable=True)
    start_disconnect_time = Column(Text, nullable=True)
    end_disconnect_date = Column(Text, nullable=True)
    end_disconnect_time = Column(Text, nullable=True)
    branch = Column(Text, nullable=True)
    substation = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    def __repr__(self):
        return f"<Lenenergo(row_id={self.row_id}, region='{self.region}', admin_district='{self.admin_district}', " \
               f"locality='{self.locality}', street='{self.street}')>"
    @classmethod
    async def to_dataframe(cls, session: Session):
        async with session.begin():
            results = await session.execute(cls.__table__.select())
            records = results.fetchall()

        # Создайте DataFrame из результатов запроса
        data = {
            'row_id': [r.row_id for r in records],
            'region': [r.region for r in records],
            'admin_district': [r.admin_district for r in records],
            'locality': [r.locality for r in records],
            'street': [r.street for r in records],
            'start_disconnect_date': [r.start_disconnect_date for r in records],
            'start_disconnect_time': [r.start_disconnect_time for r in records],
            'end_disconnect_date': [r.end_disconnect_date for r in records],
            'end_disconnect_time': [r.end_disconnect_time for r in records],
            'branch': [r.branch for r in records],
            'substation': [r.substation for r in records],
            'comment': [r.comment for r in records],
        }

        df = pd.DataFrame(data)
        return df








# Класс Address
class Address(Base):
    __tablename__ = 'address_table'  # Изменено на __tablename__ для указания имени таблицы

    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, nullable=False)
    street = Column(String(100))
    house_number = Column(String(20))

