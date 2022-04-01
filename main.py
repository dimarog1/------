import datetime
from flask import Flask, render_template
from werkzeug.utils import redirect

from data import db_session
from forms.film import FilmForm
from data.film import Film

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    films = db_sess.query(Film)
    return render_template("index.html", title='W&F', films=films)


@app.route("/search")
def search():
    db_sess = db_session.create_session()
    return render_template("search.html", title='search')


@app.route("/add_film", methods=['GET', 'POST'])
def add_film():
    form = FilmForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        film = Film()
        film.title = form.title.data
        film.year = form.year.data
        # film.poster = form.poster.data
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
    return render_template("add_film.html", title='Добавление фильма', form=form)


@app.route('/films/<int:id>')
def show_film(id):
    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    return render_template('film.html', title=film.title, film=film)


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()
