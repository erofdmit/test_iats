from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from database.database_model import Lenenergo
from database.operations import async_lenenergo_add, get_lenenergo
from scraper import parse_data
from graphs import generate_charts

app = FastAPI()

class AuthData(BaseModel):
    username: str
    password: str


@app.post("/insert-new-data/")
async def insert_data(auth_data: AuthData):
    data = await parse_data()
    await async_lenenergo_add(data=data, login = auth_data.username, password= auth_data.password)
    return data

@app.get("/get-lenenergo/")
async def get_data(auth_data: AuthData):
    
    data = await get_lenenergo(login = auth_data.username, password= auth_data.password)
    return data


@app.get("/charts/")
async def generate_charts_page(auth_data: AuthData):
    data = await get_lenenergo(login = auth_data.username, password= auth_data.password)
    
    charts = generate_charts(data)

    return {"charts": charts}