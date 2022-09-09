import asyncio
import socket
from threading import Thread

import aiohttp

from database.crud import insert_data
from .mytypes import URL
from .classes import Parsing
from .helpers import (
    write_to_csv, 
    get_number_pagination, get_page, get_soup,
    write_header, get_data_on_database
)


def generate_urls(number: int) -> list[URL]:
    urls = [f"https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{i}/c37l1700273?ad=offering" for i in range(1,number+1)]
    return urls


async def main(url: URL):
    write_header()
    conn=aiohttp.TCPConnector(ssl=False, family=socket.AF_INET)
    async with aiohttp.ClientSession(connector=conn) as session:
        number = await get_number_pagination(session=session, url=url)
        urls = generate_urls(number=number)
        all_result_on_site = []
        for url in urls:
            data = await get_page(session=session, url=url)
            soup = get_soup(html=data)
            parsing = Parsing(soup=soup)
            all_result_on_site.extend(parsing.parsing())
            print(url)

        for index in all_result_on_site:
            print("i workkkkk!!!!")
            data= get_data_on_database(index)
            write_to_csv_thread = Thread(target=write_to_csv, args=(data,))
            insert_data_thread = Thread(target=insert_data, args=("", data))

            write_to_csv_thread.start()
            insert_data_thread.start()

            write_to_csv_thread.join()
            insert_data_thread.join()
            
        

if __name__ == "__main__":
    url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273?ad=offering"

    results = asyncio.run(main(url=url))
     
