from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from config import base_url


async def parse_data():
    # Создаем список для хранения данных со всех страниц
    all_data = []

    # URL веб-сайта для парсинга данных
    
    
    # Определяем текущую неделю
    today = datetime.now().date()
    end_of_week = today + timedelta(days=(6))  # Конец текущей недели

    # Начинаем с первой страницы (первая страница имеет номер 1)
    page_number = 1

    # Инициализируем DataFrame для хранения данных
    all_data_df = pd.DataFrame()

    # Инициализируем Selenium WebDriver
    driver = webdriver.Chrome()  # Указать путь к драйверу Chrome, если необходимо

    try:
        while True:
             # Формируем параметры фильтрации для текущей страницы
            filters = {
                'PAGEN_1': page_number,
                'date_start': today.strftime("%d.%m.%Y"),
                'date_finish': end_of_week.strftime("%d.%m.%Y")
            }

            # Формируем URL для текущей страницы с учетом параметров фильтрации
            url = f"{base_url}?{urlencode(filters)}"

            # Открываем страницу в браузере с помощью Selenium
            driver.get(url)

            # Ждем несколько секунд для загрузки данных
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "planedwork")))

            # Используем BeautifulSoup для парсинга HTML-страницы после ввода даты
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Находим таблицу с данными
            table_container = soup.select_one('body > div.wrapper > div.wrap.wrap-nosb > div > div > div > div.planedwork.extended')
    
            # Находим таблицу внутри элемента
            table = table_container.find('table')
            
            # Извлекаем данные из таблицы в DataFrame
            data = pd.read_html(str(table))[0]

            # Находим элемент с классом "prev" (предыдущая страница)
            prev_page_link = driver.find_elements(By.CLASS_NAME, "prev")
            # Проверяем, существует ли элемент и его href содержит "?PAGEN_1=0"
            if prev_page_link and "?PAGEN_1=0" in prev_page_link[0].get_attribute("href") and page_number != 1:
                break
            else:
                page_number += 1
                

            # Если на текущей странице есть данные для текущей недели, добавляем их в список
            all_data.append(data)

            
            

            

        # Объединяем все данные из разных страниц в один DataFrame
        if all_data:
            all_data_df = pd.concat(all_data, ignore_index=True)
    finally:
        # Завершаем работу браузера после парсинга
        driver.quit()
    return all_data_df