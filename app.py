from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory)
import os
import article


app = Flask(__name__)

# Создаем по умолчанию папку 'uploads/' для загрузки картинок
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

database = {
    "spacex": {
        "article_title": "SpaceX Crew-10",
        "article_text": """
SpaceX Crew-10 — планируемый десятый пилотируемый полёт американского космического корабля
Crew Dragon компании SpaceX в рамках программы NASA Commercial Crew Program.
Корабль доставит четырёх членов экипажа миссии Crew-10 и космических экспедиций МКС-72/73 на Международную космическую станцию (МКС).
Запуск планируется провести 12 марта 2025 года.
""",
        "article_image": "SpaceX_Crew_Dragon.jpg"
    },

    "cosmos": {
        "article_title": "Космос (философия)",
        "article_text": """
Ко́смос (др.-греч. κόσμος «порядок, гармония») — понятие древнегреческой философии и культуры,
представление о природном мире как о пластически упорядоченном гармоническом целом.
Противопоставлялся хаосу.
Греки соединяли в понятии «космос» две функции — упорядочивающую и эстетическую.
""",
        "article_image": "Cosmos.png"
    }
}

@app.route("/article/<name>")
def get_article(name):
    if name not in database:
        return "<h1>Такой статьи не существует!</h1>"

    article = database[name]
    return render_template(
        "article.html",
        article=article
    )


@app.route("/create_article", methods=["GET", "POST"])
def create_article():
    if request.method == "GET":
        return render_template('create_article.html')
    
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



    print(dir(article))
    database[title] = article.Article(title,content,image_path)

    return redirect(url_for('index'))

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route('/uploads/<filename>')
def uploaded_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


app.run(debug=True, port=8080)
