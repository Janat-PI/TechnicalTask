from sqlalchemy import Integer, String, Column, Date

from database.DB import Base


class DataDB(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    date_of_public = Column(Date)
    price = Column(String)
    desc = Column(String)
    image_url = Column(String)
    bedrooms = Column(String)

    def __repr__(self):
        return f"id:{self.id} titile: {self.title} "