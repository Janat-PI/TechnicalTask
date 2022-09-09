from abc import ABC, abstractmethod


class Request(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def get_page(self):
        pass