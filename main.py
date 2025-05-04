from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.news import News
from forms.user import ExtendedRegisterForm  # Импортируем ExtendedRegisterForm
from data.jobs import Jobs
from data.departments import Department

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/jobs")
def jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("jobs.html", jobs=jobs, db_sess=db_sess, User=User)  # передаем User в шаблон


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def register():  # Переименовали функцию в register
    form = ExtendedRegisterForm()  # Используем ExtendedRegisterForm
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
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.db")
    # Создаем тестовый департамент
    db_sess = db_session.create_session()

    # Проверяем, есть ли уже департамент с таким названием
    if not db_sess.query(Department).filter(Department.title == "Research").first():
        department = Department()
        department.title = "Research"
        department.chief = 1  # ID руководителя
        department.members = "2,3,4"  # Список ID участников через запятую
        department.email = "research@mars.org"

        db_sess.add(department)
        db_sess.commit()
        print("Department 'Research' added.")
    else:
        print("Department 'Research' already exists.")
    app.run()


if __name__ == '__main__':
    main()
