import datetime
import requests
from flask import Flask, redirect, render_template, abort
from data import db_session
from data.jobs import Jobs
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user
from data.login_form import LoginForm
from data.add_job import AddJobForm
from forms.user import RegisterForm
from data import jobs_api, user_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    """Показывает карту родного города пользователя."""
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404)  # Или обработайте отсутствие пользователя

    if user.city_from:
        # Используем геокодер для получения координат города
        GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"  # <---- Ключ для геокодера
        geocoder_request = f"https://geocode-maps.yandex.ru/1.x/?apikey={GEOCODER_API_KEY}&geocode={user.city_from}&format=json"
        response = requests.get(geocoder_request)
        if response.status_code == 200:
            json_data = response.json()
            try:
                pos_str = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                longitude, latitude = map(float, pos_str.split())  # Разделяем координаты
                print(longitude, latitude)
                return render_template('user_show.html', user=user, longitude=longitude, latitude=latitude)
            except (KeyError, IndexError) as e:
                # Обработка ошибок геокодирования (например, город не найден)
                print(f"Ошибка при геокодировании: {e}")
                return render_template('user_show.html', user=user, error="Не удалось определить координаты города.")
        else:
            print(f"Ошибка запроса геокодера: {response.status_code}")
            return render_template('user_show.html', user=user, error="Ошибка при геокодировании города.")
    else:
        return render_template('user_show.html', user=user)

@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names, title='Work log')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='регистрация', form=form, message='пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='регистрация', form=form,
                                   message='такой пользователь уже есть')
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=int(form.age.data),
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            modified_date=datetime.datetime.now()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    add_form = AddJobForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs(
            job=add_form.job.data,
            team_leader=add_form.team_leader.data,
            work_size=add_form.work_size.data,
            collaborators=add_form.collaborators.data,
            is_finished=add_form.is_finished.data
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Добавление работы', form=add_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
