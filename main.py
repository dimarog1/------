import base64
import datetime
import random

from flask import Flask, render_template, make_response
from werkzeug.utils import redirect

from data import db_session
from data.film import Film
from forms.film import FilmForm
from forms.search import SearchForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


def create_search_form():
    form = SearchForm()
    if form.validate_on_submit():
        search_input = form.search_info.data
        return redirect(f"/search/{search_input}")


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    films = db_sess.query(Film)
    form = SearchForm()
    if form.validate_on_submit():
        search_input = form.search_info.data
        return redirect(f"/search/{search_input}")
    return render_template("index.html", title='W&F', films=films, css_file='styles/main.css', search_form=form)


@app.route("/random_film")
def random_film():
    db_sess = db_session.create_session()
    films = list(db_sess.query(Film))
    film = random.choice(films)
    return redirect(f'/films/{film.id}')


@app.route("/search/<string:search_info>")
def search(search_info):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_input = search_form.search_info.data
        return redirect(f"/search/{search_input}")

    db_sess = db_session.create_session()
    films = db_sess.query(Film).all()
    return render_template("search.html", title='search', css_file='styles/search.css', search_form=search_form, films=films, search_info=search_info)


@app.route("/add_film", methods=['GET', 'POST'])
def add_film():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_input = search_form.search_info.data
        return redirect(f"/search/{search_input}")

    form = FilmForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        film = Film()
        if form.poster:
            film.title = form.title.data
            film.year = form.year.data
            film.poster = form.poster.data.stream.read()
            film.trailer = form.trailer.data.stream.read()
            film.country = form.country.data
            film.genre = form.genre.data
            film.slogan = form.slogan.data
            film.director = form.director.data
            film.scenario = form.scenario.data
            film.producer = form.producer.data
            film.operator = form.operator.data
            film.composer = form.composer.data
            film.designer = form.designer.data
            film.montage = form.montage.data
            film.budget = form.budget.data
            film.fees_in_the_world = form.fees_in_the_world.data
            film.audience = form.audience.data
            film.fees_in_russia = form.fees_in_russia.data
            film.world_premiere = form.world_premiere.data
            film.age = form.age.data
            film.time = form.time.data
            film.short_description = form.short_description.data
            film.long_description = form.long_description.data

            db_sess.add(film)
            db_sess.commit()
            return redirect('/')
    return render_template("add_film.html", title='Добавление фильма', form=form, search_form=search_form)


@app.route('/films/<int:id>', methods=['GET', 'POST'])
def show_film(id):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_input = search_form.search_info.data
        return redirect(f"/search/{search_input}")

    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    return render_template('film.html', title=film.title, film=film, css_file='styles/film.css', search_form=search_form)


@app.route('/films/<int:id>/get_poster')
def get_poster(id):
    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    image = film.poster
    h = make_response(image)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/films/<int:id>/get_trailer')
def get_trailer(id):
    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    video = film.trailer
    h = make_response(video)
    h.headers['Content-Type'] = 'video/webm'
    return h


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()
