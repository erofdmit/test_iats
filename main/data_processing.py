import re
import asyncio
import pandas as pd

async def parse_addresses(address_str):
    # Регулярное выражение для поиска адресных элементов
    address_pattern = r'(?P<street>[\w\s]+) ул|пер|пр\., д|стр|строение|здание\.(?P<house>[\d/]+)(, к\.(?P<corpus>[\d,]+))?;?'

    # Список для хранения полных адресов
    full_addresses = []

    # Поиск адресов в строке
    matches = re.finditer(address_pattern, address_str)
    for match in matches:
        try:
            street = match.group('street')  # Улица
            house = match.group('house')  # Дом
            corpus = match.group('corpus')          # Корпус
            print(street)
            print(house)
            print(corpus)
            # Формирование полного адреса
            full_address = street + ', д. ' + house
            if corpus is not None:
                full_address += ', к. ' + corpus
            full_addresses.append(full_address)
        except Exception as error:
            print(error)

    return full_addresses


data = pd.read_csv('output.csv', encoding='utf-8').fillna('')
for index, row in data.iterrows():
    street = asyncio.run(parse_addresses(row['Улица']))
    #print(street)