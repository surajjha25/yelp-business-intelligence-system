from collections import defaultdict

class MarketStructureAnalyzer:
    def __init__(self, repository):
        self.repo = repository

    def city_category_map(self):
        market = defaultdict(lambda: defaultdict(list))

        for b in self.repo.businesses:
            if b.categories:
                for c in b.categories.split(","):
                    market[b.city][c.strip()].append(b)

        return market

    def saturation_index(self, city, category):
        market = self.city_category_map()
        businesses = market.get(city, {}).get(category, [])

        if len(businesses) == 0:
            return 0, 0

        avg_rating = sum(b.stars for b in businesses) / len(businesses)
        density = len(businesses)

        saturation = density / avg_rating
        return round(saturation, 2), density

    def white_space_opportunities(self, min_density=5):
        market = self.city_category_map()
        opportunities = []

        for city in market:
            for cat in market[city]:
                sat, density = self.saturation_index(city, cat)
                if density >= min_density and sat < 3:
                    opportunities.append((city, cat, sat, density))

        opportunities.sort(key=lambda x: x[2])
        return opportunities[:10]
