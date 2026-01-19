import sqlite3

class YelpDatabase:
    def __init__(self, db_path="../db/yelp.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        business_table = """
        CREATE TABLE IF NOT EXISTS businesses (
            business_id TEXT PRIMARY KEY,
            name TEXT,
            city TEXT,
            stars REAL,
            review_count INTEGER,
            categories TEXT
        );
        """

        review_table = """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id TEXT PRIMARY KEY,
            business_id TEXT,
            stars INTEGER,
            useful INTEGER,
            text TEXT,
            FOREIGN KEY(business_id) REFERENCES businesses(business_id)
        );
        """

        self.cursor.execute(business_table)
        self.cursor.execute(review_table)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_businesses(self, businesses):
        query = """
        INSERT OR REPLACE INTO businesses 
        (business_id, name, city, stars, review_count, categories)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        data = []
        for b in businesses:
            data.append((
                b.business_id,
                b.name,
                b.city,
                b.stars,
                b.review_count,
                str(b.categories)
            ))
        self.cursor.executemany(query, data)
        self.conn.commit()

    def insert_reviews(self, reviews):
        query = """
        INSERT OR REPLACE INTO reviews
        (review_id, business_id, stars, useful, text)
        VALUES (?, ?, ?, ?, ?)
        """
        data = []
        for r in reviews:
            data.append((
                r.review_id,
                r.business_id,
                r.stars,
                r.useful,
                r.text
            ))
        self.cursor.executemany(query, data)
        self.conn.commit()

    def top_cities_by_rating(self, min_reviews=50, limit=10):
        query = """
        SELECT city, ROUND(AVG(stars),2) as avg_rating, COUNT(*) as num_businesses
        FROM businesses
        WHERE review_count >= ?
        GROUP BY city
        ORDER BY avg_rating DESC
        LIMIT ?
        """
        self.cursor.execute(query, (min_reviews, limit))
        return self.cursor.fetchall()

    def top_categories(self, limit=10):
        query = """
        SELECT categories, AVG(stars) as avg_rating, COUNT(*) as cnt
        FROM businesses
        GROUP BY categories
        ORDER BY avg_rating DESC
        LIMIT ?
        """
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()

    def rating_distribution(self):
        query = """
        SELECT stars, COUNT(*) 
        FROM businesses
        GROUP BY stars
        ORDER BY stars
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
