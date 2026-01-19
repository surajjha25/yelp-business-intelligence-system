class Business:
    def __init__(self, business_id, name, city, stars, review_count, categories, attributes):
        self.business_id = business_id
        self.name = name
        self.city = city
        self.stars = stars
        self.review_count = review_count
        self.categories = categories
        self.attributes = attributes

    def is_high_rated(self):
        return self.stars >= 4.0


class Review:
    def __init__(self, review_id, business_id, stars, text, useful):
        self.review_id = review_id
        self.business_id = business_id
        self.stars = stars
        self.text = text
        self.useful = useful
