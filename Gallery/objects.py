class HouseSpec:
    stories = 0
    bedrooms = 0
    baths = 0
    size = 0
    interior_balcony = True
    cathedral_ceiling = True

    def __init__(self, stories, bedrooms, baths, size, interior_balcony=False, cathedral_ceiling=False):
        self.stories = stories
        self.bedrooms = bedrooms
        self.baths = baths
        self.size = size
        self.interior_balcony = interior_balcony
        self.cathedral_ceiling = cathedral_ceiling
