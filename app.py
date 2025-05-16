from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    abort,
    flash)
import os
from article import Article
from database import Database


app = Flask(__name__)
app.config["SECRET_KEY"] = "SHPI"
Database.create_article_table()

# Создаем по умолчанию папку 'uploads/' для загрузки картинок
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    repeat_password = request.form.get("repeat_password")

    if not username:
        flash("имя пользователя не может быть пустым")
        return redirect(request.url)

    
    if not email:
        flash("электронная почта не может быть пустым")
        return redirect(request.url)


    
    if not password:
        flash("повторите пароль")
        return redirect(request.url)
    
    if password != repeat_password:
        flash("пароли не совпадают")
        return redirect(request.url)

    
    
    if not repeat_password:
        ...
    return redirect(url_for("index"))



@app.route("/favicon/")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path,'static/img'),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"

    )



@app.route("/article/<title>")
def get_article(title):

    article = Database.find_article_by_title(title)
    
    Database.increase_views_count(title)
    

    print("GET", article)

    if article is None:
        return "<h1>Такой статьи не существует!</h1>"
    
    
    return render_template(
        "article.html",
        article=article
    )


@app.route("/create_article", methods=["GET", "POST"])
def create_article():
    if request.method == "GET":
        return render_template('create_article.html',error=request.args.get("error"))
    
    # Далее обработка POST-запроса
    title = request.form.get("title")
    content = request.form.get("content")
    image = request.files.get("photo")
    anotation = request.form.get("anotation")
    views = request.form.get("views")
    
    if image is not None and image.filename: # Не надо писать: photo != None
        image_path = image.filename
        print(app.config["UPLOAD_FOLDER"] + image_path)
        image.save(app.config["UPLOAD_FOLDER"] + image_path)
        

    else:
        image_path = None

    Database.save(Article(title, content,image_path,anotation,views))


    
    

    return redirect(url_for('index'))


@app.route("/delete_article/<id>", methods=["POST"])
def delete_article(id):
    if not Database.delete(id):
        abort(404, f"Article id {id} doesn't exist")
    
    return redirect(url_for('index'))


@app.route("/update_article/<id>", methods=["GET", "POST"])
def update_article(id):
    article = Database.find_article_by_id(id)
    if article is None:
        abort(404, f"Article id {id} doesn't exist")

    if request.method == "GET":
        return render_template("update_article.html", article=article)
    
    # Обработка POST-запроса
    title = request.form.get("title")
    if title is None:
        title = article.title

    content = request.form.get("content")
    if content is None:
        content = article.title

    image = request.files.get("photo")
    
    
    if image is not None and image.filename:
        image_path = image.filename
        # Костыль: может вызвать проблемы с сохранением
        # картинок в папку
        image.save(app.config["UPLOAD_FOLDER"] + image_path)
        filename= image_path
    else:
        filename = article.image

    anotation = request.files.get("anotation")
    if anotation is None:
        anotation = article.anotation 

    views = request.files.get("views")
    if views is None:
        views = article.views
    # print(Database.update(id,title,content,filename,anotation))
    Database.update(id,title,content,filename,anotation,views)
    return redirect(url_for('index'))
    
    







@app.route("/")
@app.route("/index")
def index():
    articles = Database.get_all_articles()
    count_in_group = 5

    groups = []
    for i in range(0,len(articles),count_in_group):
        groups.append(articles[i:i + count_in_group])
    
    return render_template("index.html",groups=groups)


@app.route('/uploads/<filename>')
def uploaded_photo(filename):
    print("было получено такое имя файла", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


app.run(debug=True, port=8080)
