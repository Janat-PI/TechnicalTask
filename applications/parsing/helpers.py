from datetime import date
import csv
import asyncio

from pydantic import BaseModel
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from .mytypes import URL
from database.models import DataDB


async def get_page(session: ClientSession, url: URL):
    """
    it is function return response view Coroutine(str)
    """
    async with session.get(url) as response:
        print(response.status)
        return await response.text()


async def get_all(session: ClientSession, urls: list[URL]):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

def get_soup(html) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


async def get_number_pagination(session: ClientSession, url: URL):
    import math
    async with session.get(url) as response:
        r = await response.text()
        soup = get_soup(r)
        result = soup.find("span", class_="resultsShowingCount-1707762110").text.split()
        all_data_on_site = convert_str_to_int(result[-2])
        number_inline_site = convert_str_to_int(result[3])
        result = math.ceil(all_data_on_site / number_inline_site)
        return result


def convert_str_to_int(number: str) -> int:
    """
    function give number string and convert here and return int_number
    """
    try:
        number = int(number)
    except ValueError:
        raise ValueError("Convert not success")
    else:
        return number


class Data(BaseModel):
    title: str
    location: str
    datee: date
    price: str
    desc: str
    image_url: str
    bedrooms: str


def check_on_except(func):

    def infunc(data, tag, **kwargs):

        try:
            result = func(data, tag, **kwargs)
        except:
            result = "not data"
        finally:
            return result
        
    return infunc


def write_to_csv(data: DataDB):
    with open('files/parsing_site.csv', 'a') as file:
        try:
            writer = csv.writer(file)
            writer.writerow([
                data.title,
                data.desc,
                data.location,
                data.date_of_public,
                data.price,
                data.image_url,
                data.bedrooms
            ])
        except Exception as e:
            print(f'it is error {e}')



def write_header():
    with open('files/parsing_site.csv', 'a') as file:
        try:
            fieldnames = ['title', 'desc', 'location', 'date_of_public', 'price', 'image_url', 'bedrooms']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
        except Exception as e:
            print(f'it is error {e}')


def get_data_on_database(data: Data) -> DataDB:
    
    data_ = DataDB(
                title=data.title,
                location=data.location,
                desc=data.desc,
                date_of_public=data.datee,
                price=data.price,
                image_url=data.image_url,
                bedrooms=data.bedrooms
            )
    return data_