import math


class RandomValueCollection:
    def __init__(self, values: [], page: int, pageSize: int, totalNumberOfItems: int):
        self.values = values
        self.page = page
        self.pageSize = pageSize
        self.numberOfPages = math.ceil(float(totalNumberOfItems) / float(pageSize))