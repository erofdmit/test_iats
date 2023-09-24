from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from database.operations import get_lenenergo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import asyncio

async def generate_charts(username,password):
    df = await get_lenenergo(username,password)
    
    # Создание графиков
    charts = {}
    
    # График расположения по району
    for index, row in df.iterrows():
        if "admin_district" in df.columns:
            district_counts = df['admin_district'].value_counts()
            district_chart = sns.barplot(x=district_counts.index, y=district_counts.values)
            district_chart.set(xlabel='Район', ylabel='Количество')
            district_chart.set_title('Расположение по району')
            district_image = plot_to_image(district_chart)
            charts['district'] = district_image
        
        # График времени включения и отключения
        if "start_disconnect_time" in df.columns and "end_disconnect_time" in df.columns:
            time_chart = sns.kdeplot(df['start_disconnect_time'], label='Время включения')
            time_chart = sns.kdeplot(df['end_disconnect_time'], label='Время отключения')
            time_chart.set(xlabel='Время', ylabel='Плотность')
            time_chart.set_title('Время включения и отключения')
            time_image = plot_to_image(time_chart)
            charts['time'] = time_image
        
        # График по РЭС
        if "branch" in df.columns:
            branch_counts = df['branch'].value_counts()
            branch_chart = sns.barplot(x=branch_counts.index, y=branch_counts.values)
            branch_chart.set(xlabel='РЭС', ylabel='Количество')
            branch_chart.set_title('По РЭС')
            branch_image = plot_to_image(branch_chart)
            charts['branch'] = branch_image

        return {"charts": charts}

def plot_to_image(plot):
    buf = io.BytesIO()
    plot.figure.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode()
    buf.close()
    return image_base64


