import sqlite3
from article import Article
 
 
class Database:
     db_path = "database.db"
     schema_path = "schema.sql"
 
     @staticmethod
     def execute(sql_code: str, params: tuple = ()):
         conn = sqlite3.connect(Database.db_path)
         
         cursor = conn.cursor()
         cursor.execute(sql_code, params)
 
         conn.commit()
 
     @staticmethod
     def create_article_table():
         with open(Database.schema_path) as schema_file:
            sql_code = schema_file.read()
            Database.execute(sql_code)
 
     @staticmethod
     def save(article: Article):
         if Database.find_article_by_title(article.title) is not None:
             return False


         Database.execute(f"""
         INSERT INTO articles (title, content, filename,anotation) VALUES (?, ?, ?, ?)
         """, (article.title, article.content, article.image,article.anotation))
         return True
 
     @staticmethod
     def fetchall(sql_code: str,params: tuple =()):
         conn = sqlite3.connect(Database.db_path)
         
         cursor = conn.cursor()
         cursor.execute(sql_code,params)
 
         return cursor.fetchall()
 
     @staticmethod
     def get_all_articles():
        articles = []
        

        for (id,title,content,image,anotation) in Database.fetchall(

            "SELECT * FROM articles"):
            articles.append(Article(title=title,
                                    content=content,
                                    anotation=anotation,
                                    image=image,
                                    id=id))

        return articles




     @staticmethod
     def find_article_by_title(title: str):
         articles = Database.fetchall(
        "SELECT * FROM articles WHERE title = ?", [title]                              
        )
         
         if not articles:
          return None
         
         id,title,content,image,anotation = articles[0]
         return Article(id,title,content,image,anotation)
 
 
class SimpleDatabase:
     articles = []
 
     @staticmethod
     def save(article: Article):
         if SimpleDatabase.find_article_by_title(article.title) is not None:
             return False
 
         SimpleDatabase.articles.append(article)
         return True
 
     @staticmethod
     def get_all_articles():
         return SimpleDatabase.articles
     
     @staticmethod
     def find_article_by_title(title: str):
         for article in SimpleDatabase.articles:
             if article.title == title:
                 return article
         return None