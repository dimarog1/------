import datetime
import random

from flask import Flask, render_template, make_response, request
from werkzeug.utils import redirect

from data import db_session
from data.film import Film
from data.user import Role, User

from forms.film import FilmForm

from forms.register import ExtendedRegisterForm, ExtendedLoginForm
from flask_security import SQLAlchemySessionUserDatastore, Security, login_required
from flask_security.utils import hash_password
from flask_security.forms import current_user
from data.db_session import db_sess, global_init

from flask_restful import Api
from rest_api import review_resources
from rest_api.review_resources import ReviewResource


app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECURITY_PASSWORD_SALT'] = 'pbkdf2:sha256:150000'

user_datastore = SQLAlchemySessionUserDatastore(db_sess, User, Role)
security = Security(app, user_datastore, login_form=ExtendedLoginForm)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    films = db_sess.query(Film)
    return render_template("index.html", title='W&F', films=films, css_file='styles/main.css')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route("/random_film")
def random_film():
    db_sess = db_session.create_session()
    films = list(db_sess.query(Film))
    film = random.choice(films)
    return redirect(f'/films/{film.id}')


@app.route("/search")
def search():
    db_sess = db_session.create_session()
    return render_template("search.html", title='search', css_file='styles/search.css')


@app.route("/add_film", methods=['GET', 'POST'])
def add_film():
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
    return render_template("add_film.html", title='Добавление фильма', form=form)


@app.route('/films/<int:id>', methods=['GET', 'POST'])
def show_film(id):
    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    #TODO сделать нормальный html
    return render_template('film.html', title=film.title, film=film, css_file='styles/film.css',
                           is_authenticated=current_user.is_authenticated)


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


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = ExtendedRegisterForm()
    if request.method == 'POST':
        if not user_datastore.find_user(email=request.form.get('email')):
            user_datastore.create_user(
                email=request.form.get('email'),
                password=hash_password(request.form.get('password')),
                roles='',
            )
            db_sess.commit()
        return redirect('/')

    return render_template('register.html', form=form, bootstrapp=True)


def main():
    api.add_resource(review_resources.ReviewListResource, '/api/review')
    api.add_resource(review_resources.ReviewResource, '/api/review/<int:review_id>')

    global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()
