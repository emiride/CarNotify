class CarModel:
    def __init__(self, url: str, price: str):
        self.url: str = url
        self.price: str = price

    def __eq__(self, other):
        return self.url == other.url
        # This is a solution to avoid picking up changed title
        # "/".join(self.url.split("/")[:-2]) == "/".join(other.url.split("/")[:-2])