import sqlite3
import hashlib
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
     def create_tables():
         with open(Database.schema_path) as schema_file:
            sql_code = schema_file.read()
            conn = sqlite3.connect(Database.db_path)

            cursor = conn.cursor()
            cursor.executescript(sql_code)

            conn.commit()

     @staticmethod
     def update(article_id: int, title: str, content: str, image: str,anotation: str,views: int, author_id: int) -> bool:
        # Если статьи с таким id нет, ничего не делаем и возвращаем False
        if Database.find_article_by_id(article_id) is None:
            return False
        
        Database.execute(
            """
            UPDATE articles
            SET title = ?,
                content = ?,
                filename = ?,
                anotation = ?,
                views = ?
                author_id = ?
            WHERE id = ?
            """,
            [title, content, image,anotation,article_id,views,article_id]
        )
        return True

     @staticmethod
     def delete(article_id: int) -> bool:
        # Если статьи с таким id нет, ничего не делаем и возвращаем False
        if Database.find_article_by_id(article_id) is None:
            return False

        Database.execute("DELETE FROM articles WHERE id = ?", [article_id])
        return True

     @staticmethod
     def find_article_by_id(article_id: int) -> Article | None:
        articles = Database.fetchall("SELECT * FROM articles WHERE id = ?", [article_id])

        if not articles: # if len(articles) == 0
            return None

        id, title, content, image, anotation, views, author_id = articles[0]
        article = Article(id=id, title=title, content=content,anotation=anotation, image=image, views=views, author_id=author_id)
        print(article)

        return article
 
     @staticmethod
     def save(article: Article):
         if Database.find_article_by_title(article.title) is not None:
             return False


         Database.execute(f"""
         INSERT INTO articles (title, content, filename,anotation,views,author_id) VALUES (?, ?, ?, ?,?,?)
         """, (article.title, article.content, article.image,article.anotation,article.views, article.author_id))
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
        

        for (id,title,content,image,anotation,views,author_id) in Database.fetchall(

            "SELECT * FROM articles"):
            author = Database.find_user_id_by_name(author_id)
            articles.append(Article(title=title,
                                    content=content,
                                    anotation=anotation,
                                    image=image,
                                    views=views,
                                    id=id,
                                    author=author))

        return articles
     
     @staticmethod
     def find_article_by_id(article_id: int) -> Article | None:
        articles = Database.fetchall("SELECT * FROM articles WHERE id = ?", [article_id])

        if not articles: # if len(articles) == 0
            return None
        
        id,title,content,image,anotation,views, author_id = articles[0]
        
        print(articles[0])
        article = Article(id=id,title=title,content=content,image=image,anotation=anotation,views=views,author=author_id)

        return article




     @staticmethod
     def find_article_by_title(title: str):
         articles = Database.fetchall(
        "SELECT * FROM articles WHERE title = ?", [title]                              
        )
         
         if not articles:
          return None
         
        #  print(articles)
         id,title,content,image,anotation,views,author_id = articles[0]
         author = Database.find_user_id_by_name(author_id)


         
         
         
         return Article(title,content,image,anotation,views,id,author_id)
     
     @staticmethod
     def increase_views_count(title: str):
        if Database.find_article_by_title(title) is not None:
             return False


        Database.execute(f""" UPDATE `article` SET `views` = `views` + 1;""")


     @staticmethod
     def register_user(user_name,email,password):
         #есть ли пользователи у которых уже указан такой никнейм или электронная почта
         users = Database.fetchall(
             "SELECT * FROM users WHERE user_name = ? OR email = ?",
             [user_name, email]
         )
         print(users)
         if users:
             return False
         
         password_hash = hashlib.md5(password.encode()).hexdigest()

         Database.execute("INSERT INTO users (user_name, email, password_hash)"
                          "VALUES (?,?,?)",
                          [user_name,email,password_hash]
        )
         return True
     
     @staticmethod
     def get_count_of_users():
         count = Database.fetchall(
            "SELECT COUNT(*) FROM users"
            )[0][0]        
         return count
     
     @staticmethod
     def can_be_logged_in(user_or_email: str,password: str) -> bool:
         print(Database.fetchall("SELECT * FROM users"))
         print(user_or_email, password)
         #1 проверить что пользователь с таким именем или эл почтой есть
         users = Database.fetchall("SELECT * FROM users WHERE user_name = ? OR email = ?",[user_or_email,user_or_email])
         print(users)
         if not users:
             return False
         
         #2 берем хэш пароль заданного пользователя
         
         user = users[0]
         real_password_hash = user[3]

         #3 сравниваем хэш хранящийся в бд и хэш пароля который попытались внести
         password_hash = hashlib.md5(password.encode()).hexdigest()
         print(password_hash)
         if real_password_hash != password_hash:
             return False
         return True
        
     def find_user_id_by_name(user_or_email):
        users = Database.fetchall('SELECT id FROM users WHERE user_name = ? OR email = ?',[user_or_email,user_or_email])

        if not users:
            return None
        
        id = users[0][0]
        return id
     

     @staticmethod
     def get_articles_count_of_users(user_name):
         user = Database.find_user_id_by_name(user_name)
         #проверить есть ли такой пользователь если нет return 0
         if user is None:
             return 0
         
         article_count = Database.fetchall(
             "SELECT COUNT(*) FROM articles WHERE author_id = %s", [user.id]
         )

         return article_count[0][0]
         
         
    
         
 
 
