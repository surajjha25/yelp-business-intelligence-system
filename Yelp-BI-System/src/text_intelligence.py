from collections import defaultdict
from textblob import TextBlob

class ReviewTextAnalyzer:
    def __init__(self, repository):
        self.repo = repository
        self.sentiment_by_business = {}

    def compute_sentiments(self, min_reviews=5):
        sentiment_map = defaultdict(list)

        for bid, reviews in self.repo.reviews_by_business.items():
            for r in reviews:
                try:
                    polarity = TextBlob(r.text).sentiment.polarity
                    sentiment_map[bid].append(polarity)
                except:
                    continue

        for bid, scores in sentiment_map.items():
            if len(scores) >= min_reviews:
                self.sentiment_by_business[bid] = sum(scores) / len(scores)

        return self.sentiment_by_business

    def get_sentiment(self, business_id):
        return self.sentiment_by_business.get(business_id, 0)
