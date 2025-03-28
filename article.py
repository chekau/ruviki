
from dataclasses import dataclass

@dataclass
class Article:
    title: str
    content: str
    image: str| None = None

class Database:
    articles = []

    @staticmethod
    def save(article: Article):
        if Database.find_article_by_title(article.title) is not None:
            return False
        
        Database.articles.append(article)
        return True
    
    @staticmethod
    def get_all_articles():
        return Database.articles
    
    def find_article_by_title(title: str):
        for article in Database.articles:
            if article.title == title:
                return article
        return None
    