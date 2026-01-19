import json

class YelpDataLoader:
    def __init__(self, business_path, review_path):
        self.business_path = business_path
        self.review_path = review_path
        self.businesses = []
        self.reviews = []

    def load_businesses(self, limit=None):
        with open(self.business_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if limit and i >= limit:
                    break
                self.businesses.append(json.loads(line))
        return self.businesses

    def load_reviews(self, limit=None):
        with open(self.review_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if limit and i >= limit:
                    break
                self.reviews.append(json.loads(line))
        return self.reviews
    
    def filter_restaurants(self):
        restaurants = []
        for b in self.businesses:
            if b.get("categories") and "Restaurant" in b["categories"]:
                restaurants.append(b)
        self.businesses = restaurants
        return restaurants
