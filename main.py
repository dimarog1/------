import base64
import datetime
import random

from flask import Flask, render_template, make_response, request
from flask_restful import abort
from flask import Flask, render_template, make_response, request
from flask_security.utils import hash_password
from werkzeug.utils import redirect

from data import db_session
from data.film import Film
from data.user import Role, User
from data.review import Review

from forms.film import FilmForm
from forms.search import SearchForm
from forms.review import ReviewForm

from forms.register import ExtendedRegisterForm, ExtendedLoginForm
from flask_security import SQLAlchemySessionUserDatastore, Security, login_required, user_registered
from flask_security.forms import current_user
from data.db_session import db_sess, global_init

from flask_restful import Api
from rest_api import review_resources, film_resources, user_resources

from requests import get, post

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECURITY_PASSWORD_SALT'] = 'pbkdf2:sha256:150000'

user_datastore = SQLAlchemySessionUserDatastore(db_sess, User, Role)
security = Security(app, user_datastore, login_form=ExtendedLoginForm)


def create_search_form():
    form = SearchForm()
    if form.validate_on_submit():
        search_input = form.search_info.data
        return redirect(f"/search/{search_input}")


@app.context_processor
def login_context():
    form = SearchForm()
    if form.validate_on_submit():
        search_input = form.search_info.data
        return redirect(f"/search/{search_input}")
    return {
        'css_file': 'styles/reg.css'
    }


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    films = db_sess.query(Film)
    form = SearchForm()
    if form.validate_on_submit():
        search_input = form.search_info.data
        return redirect(f"/search/{search_input}")
    return render_template("index.html", title='W&F', films=films, is_admin=current_user.has_role('admin'),
                           css_file='styles/main.css', search_form=form)


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


@app.route("/search/<string:search_info>")
def search(search_info):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_input = search_form.search_info.data
        return redirect(f"/search/{search_input}")

    db_sess = db_session.create_session()
    films = db_sess.query(Film).all()
    return render_template("search.html", title='search', css_file='styles/search.css',
                           search_form=search_form, films=films, search_info=search_info)


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
            film.rating = form.rating.data
            film.poster = form.poster.data.stream.read()
            film.frame_1 = form.frame_1.data.stream.read()
            film.frame_2 = form.frame_2.data.stream.read()
            film.frame_3 = form.frame_3.data.stream.read()
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
    return render_template("add_film.html", title='Добавление фильма', css_file="styles/add_film.css", form=form, search_form=search_form)


@app.route("/edit_film/<int:id>", methods=['GET', 'POST'])
def edit_film(id):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_input = search_form.search_info.data
        return redirect(f"/search/{search_input}")

    form = FilmForm()

    if request.method == "GET":
        db_sess = db_session.create_session()
        film = db_sess.query(Film).filter(Film.id == id).first()
        if film:
            form.title.data = film.title
            form.year.data = film.year
            form.rating.data = film.rating
            form.poster.data = film.poster
            form.frame_1.data = film.frame_1
            form.frame_2.data = film.frame_2
            form.frame_3.data = film.frame_3
            form.trailer.data = film.trailer
            form.country.data = film.country
            form.genre.data = film.genre
            form.slogan.data = film.slogan
            form.director.data = film.director
            form.scenario.data = film.scenario
            form.producer.data = film.producer
            form.operator.data = film.operator
            form.composer.data = film.composer
            form.designer.data = film.designer
            form.montage.data = film.montage
            form.budget.data = film.budget
            form.fees_in_the_world.data = film.fees_in_the_world
            form.audience.data = film.audience
            form.fees_in_russia.data = film.fees_in_russia
            form.world_premiere.data = film.world_premiere
            form.age.data = film.age
            form.time.data = film.time
            form.short_description.data = film.short_description
            form.long_description.data = film.long_description
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        film = db_sess.query(Film).filter(Film.id == id).first()
        if film:
            film.title = form.title.data
            film.year = form.year.data
            film.rating = form.rating.data
            film.poster = form.poster.data.stream.read()
            film.frame_1 = form.frame_1.data.stream.read()
            film.frame_2 = form.frame_2.data.stream.read()
            film.frame_3 = form.frame_3.data.stream.read()
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
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_film.html', title='Изменение фильма', css_file="styles/add_film.css", form=form, search_form=search_form)


@app.route("/delete_film/<int:id>", methods=['GET', 'POST'])
def delete_film(id):
    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    if film:
        db_sess.delete(film)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/films/<int:id>', methods=['GET', 'POST'])
def show_film(id):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_input = search_form.search_info.data
        return redirect(f"/search/{search_input}")

    review_form = ReviewForm()
    if review_form.is_submitted():
        review = Review()
        review.user = current_user.id
        review.film = id
        review.text = review_form.text.data
        review.mark = int(review_form.mark.data)
        db_sess = db_session.create_session()
        db_sess.add(review)
        db_sess.commit()

        film = db_sess.query(Film).filter(Film.id == review.film).first()
        film.rating = round(((film.review_count * film.rating) + review.mark) / (film.review_count + 1), 1)
        film.review_count += 1
        db_sess.commit()

        return redirect(f'/films/{id}')

    review_data = get('http://localhost:5000/api/review').json()['review']
    user_data = get('http://localhost:5000/api/users').json()['user']
    id_nickname = dict()
    for data_elem in user_data:
        id_nickname[data_elem['id']] = data_elem['nickname']

    review_info = []
    for data_elem in review_data:
        if data_elem['film'] == 1:
            data_block = {
                'username': id_nickname[data_elem['user']],
                'mark': str(data_elem['mark']),
                'text': data_elem['text'],
            }
            review_info.append(data_block)

    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    return render_template('film.html', title=film.title, film=film, css_file='styles/film.css',
                           search_form=search_form, review_info=review_info,
                           review_form=review_form, is_authenticated=current_user.is_authenticated,
                           is_admin=current_user.has_role('admin'))


@app.route('/films/<int:id>/get_poster')
def get_poster(id):
    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    image = film.poster
    h = make_response(image)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/films/<int:id>/get_frame/<int:frame>')
def get_frame(id, frame):
    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    vals = {
        'frame_1': film.frame_1,
        'frame_2': film.frame_2,
        'frame_3': film.frame_3
    }
    res_frame = vals[f'frame_{frame}']
    h = make_response(res_frame)
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
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_input = search_form.search_info.data
        return redirect(f"/search/{search_input}")

    form = ExtendedRegisterForm()
    if request.method == 'POST':
        if not user_datastore.find_user(email=request.form.get('email')):
            user = user_datastore.create_user(
                email=request.form.get('email'),
                password=hash_password(request.form.get('password')),
                nickname=request.form.get('nickname')
            )
            default_role = user_datastore.find_role('user')
            user_datastore.add_role_to_user(user, default_role)
            db_sess.commit()
        return redirect('/')

    return render_template('register.html', form=form, search_form=search_form,
                           css_file='styles/reg.css')


def main():
    api.add_resource(review_resources.ReviewListResource, '/api/review')
    api.add_resource(review_resources.ReviewResource, '/api/review/<int:review_id>')
    api.add_resource(film_resources.FilmListResource, '/api/films')
    api.add_resource(film_resources.FilmResource, '/api/films/<int:film_id>')
    api.add_resource(user_resources.UserListResource, '/api/users')
    api.add_resource(user_resources.UserResource, '/api/users/<int:user_id>')

    global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()
