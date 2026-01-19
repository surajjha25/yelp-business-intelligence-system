class YelpRepository:
    def __init__(self, businesses, reviews):
        self.businesses = businesses
        self.reviews = reviews
        
        self.business_index = {}
        self.reviews_by_business = {}

        self._build_indexes()

    def _build_indexes(self):
        for b in self.businesses:
            self.business_index[b.business_id] = b
            self.reviews_by_business[b.business_id] = []

        for r in self.reviews:
            if r.business_id in self.reviews_by_business:
                self.reviews_by_business[r.business_id].append(r)

    def get_business(self, business_id):
        return self.business_index.get(business_id)

    def get_reviews_for_business(self, business_id):
        return self.reviews_by_business.get(business_id, [])
