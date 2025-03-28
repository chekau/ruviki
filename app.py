from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory)
import os
from article import Database,Article


app = Flask(__name__)

# Создаем по умолчанию папку 'uploads/' для загрузки картинок
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)






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
    
    if image is not None and image.filename: # Не надо писать: photo != None
        image_path = image.filename
        print(app.config["UPLOAD_FOLDER"] + image_path)
        image.save(app.config["UPLOAD_FOLDER"] + image_path)
        

    else:
        image_path = None



    
    saved = Database.save(Article(title, content, image_path))
    if not saved:
        return redirect(url_for("create_article",error=True))

    return redirect(url_for('index'))

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",articles=Database.get_all_articles())


@app.route('/uploads/<filename>')
def uploaded_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


app.run(debug=True, port=8080)
