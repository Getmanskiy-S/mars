from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    db_sess.commit()
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "Ridley_chief@mars.org"

    user2 = User()
    user2.surname = "мужик"
    user2.name = "1"
    user2.age = 21
    user2.position = "colonist"
    user2.speciality = "research engineer"
    user2.address = "module_1"
    user2.email = "muzik1@mars.org"

    user3 = User()
    user3.surname = "мужик"
    user3.name = "2"
    user3.age = 21
    user3.position = "colonist"
    user3.speciality = "research engineer"
    user3.address = "module_1"
    user3.email = "muzik2@mars.org"

    user4 = User()
    user4.surname = "мужик"
    user4.name = "2"
    user4.age = 21
    user4.position = "colonist"
    user4.speciality = "research engineer"
    user4.address = "module_1"
    user4.email = "muzik3@mars.org"

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.add(user2)
    db_sess.add(user3)
    db_sess.add(user4)
    db_sess.commit()
    # app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
