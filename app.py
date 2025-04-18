from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory)
import os
from article import Article
from database import Database


app = Flask(__name__)
Database.create_article_table()

# Создаем по умолчанию папку 'uploads/' для загрузки картинок
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
    
    if image is not None and image.filename: # Не надо писать: photo != None
        image_path = image.filename
        print(app.config["UPLOAD_FOLDER"] + image_path)
        image.save(app.config["UPLOAD_FOLDER"] + image_path)
        

    else:
        image_path = None



    
    saved = Database.save(Article(title, content,anotation,image_path))
    if not saved:
        return redirect(url_for("create_article",error=True))

    return redirect(url_for('index'))


@app.route("/delete_article",methods=["DELETE"])
def delete_article():
    ...





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
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


app.run(debug=True, port=8080)
