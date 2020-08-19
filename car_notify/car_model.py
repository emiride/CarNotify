class CarModel:
    def __init__(self, url: str, price: str):
        self.url: str = url
        self.price: str = price

    def __eq__(self, other):
        return self.url == other.url
