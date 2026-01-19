import math
from collections import defaultdict

class RestaurantSuccessAnalyzer:
    def __init__(self, repository):
        self.repo = repository

    # ---------- CORE METRIC ----------

    # ---------- RANKING ALGORITHM ----------
    def top_restaurants(self, n=10, min_reviews=50):
        scored = []
        for b in self.repo.businesses:
            if b.review_count >= min_reviews:
                score = self.success_score(b)
                scored.append((b, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:n]

    # ---------- CITY ANALYSIS ----------
    def city_performance(self):
        city_map = defaultdict(list)

        for b in self.repo.businesses:
            city_map[b.city].append(b.stars)

        city_scores = []
        for city, ratings in city_map.items():
            avg = sum(ratings) / len(ratings)
            city_scores.append((city, round(avg, 2), len(ratings)))

        city_scores.sort(key=lambda x: x[1], reverse=True)
        return city_scores

    # ---------- CATEGORY ANALYSIS ----------
    def category_performance(self):
        """
        Computes average ratings for food-related restaurant categories only.
        Applies both business-level and category-level filtering.
        """
    
        from collections import defaultdict
    
        # Generic / non-food categories to exclude
        EXCLUDE = set([
            "restaurants", "food", "nightlife", "shopping",
            "education", "event planning & services", "local services",
            "professional services", "pets", "home services",
            "health & medical", "beauty & spas", "active life"
        ])
    
        category_map = defaultdict(list)
    
        for b in self.repo.businesses:
    
            # ---- Level 1 filter: Only restaurant businesses ----
            if not b.categories or "Restaurants" not in b.categories:
                continue
    
            for c in b.categories.split(","):
                c = c.strip()
    
                # ---- Level 2 filter: Remove non-food/generic tags ----
                if c.lower() in EXCLUDE:
                    continue
    
                # Extra safety: skip very generic service words
                if any(x in c.lower() for x in ["class", "rental", "education", "veterinar", "repair"]):
                    continue
    
                category_map[c].append(b.stars)
    
        category_scores = []
        for cat, ratings in category_map.items():
            avg = sum(ratings) / len(ratings)
            category_scores.append((cat, round(avg,2), len(ratings)))
    
        category_scores.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return category_scores
    
    # ---------- STRATEGIC INSIGHT ----------
    def recommended_cities(self, min_businesses=30):
        city_data = self.city_performance()
        filtered = [c for c in city_data if c[2] >= min_businesses]
        return filtered[:10]
    
    def success_score(self, business, sentiment=0):
        rating_component = business.stars / 5
        engagement_component = math.log(1 + business.review_count) / 10
        sentiment_component = (sentiment + 1) / 2

        return round(0.5*rating_component + 0.3*engagement_component + 0.2*sentiment_component, 4)
