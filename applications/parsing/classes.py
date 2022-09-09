from datetime import datetime
from datetime import date

from bs4 import BeautifulSoup

from .helpers import check_on_except, Data


class Parsing:

    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def _get_all_tags(self, tag: str, **kwargs) -> list[BeautifulSoup]:
        class_ = kwargs.get("class_")
        return self.soup.find_all(tag, class_=class_)

    @staticmethod
    @check_on_except
    def get_data(data: BeautifulSoup, tag: str, **kwargs) -> BeautifulSoup:
        if kwargs.get("class_"):
            title = data.find(tag, {"class": kwargs.get("class_")})
        else:
            title = data.find(tag)

        if kwargs.get("strip"):
            title = title.text.strip()
        return title


    def get_image(self, data: BeautifulSoup) -> str:
        try:
            image = data.find("div", {"class":"image"}).find("img").get("data-src")
        except:
            image = ""
        else:
            if image is None:
                image = ""
        return image

    def get_bedrooms(self, data: BeautifulSoup) -> str:
        bedrooms = data.find("span", {"class": "bedrooms"}).text.strip().split(":")
        count: str = bedrooms[-1].strip()
        return count

    def get_desc(self, data: BeautifulSoup):
        desc: str = self.get_data(data=data, tag="div", class_="description", strip=True)
        if not desc.endswith("..."):
            desc = desc.split("...")[0]

        return desc

    @staticmethod
    def converte_date(datee: str) -> date:
        # dd-mm-yy
        # strftime("%d/%m/%Y")
        try:
            if datee.startswith("<"):
                datee = datetime.now().date()
            else:
                day, month, year =map(int, datee.split("/"))
                datee = datetime(day=day, month=month, year=year)
        except:
            datee = datetime.now().date()
        return datee

    def parsing(self) -> list[Data]:
        all_data = self._get_all_tags(tag="div", class_="search-item")
        print(len(all_data))
        results = []
        for data in all_data:
            info_container = self.get_data(data=data, tag="div", class_="info-container", strip=False)
            title = self.get_data(data=info_container, tag="div", class_="title", strip=True)
            price = self.get_data(data=info_container, tag="div", class_="price", strip=True)
            location_and_date = self.get_data(data=info_container, tag="div", class_="location", strip=False)
            location = self.get_data(data=location_and_date, tag="span", strip=True)
            datee = self.get_data(data=location_and_date, tag="span", class_="date-posted", strip=True)
            description = self.get_desc(data=info_container)
            
            image = self.get_image(data=data)
            rental_info = self.get_data(data=data, tag="div", class_="rental-info", strip=False)
            bedrooms = self.get_bedrooms(data=rental_info)

            result = Data(
                title=title,
                desc=description,
                price=price,
                location=location,
                datee=self.converte_date(datee),
                image_url=image,
                bedrooms=bedrooms      
            )

            results.append(result)
            
        return results
    