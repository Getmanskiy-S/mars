from flask import Flask, redirect, render_template, abort
from data import db_session
import datetime
from data.jobs import Jobs
from data.users import User
from data.departaments import Department  # Added
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.login_form import LoginForm
from data.add_job import AddJobForm
from forms.user import RegisterForm
from forms.department import DepartmentForm  # Added

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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
@login_required
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


@app.route('/job/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(id)

    if not job:
        abort(404)

    if job.team_leader != current_user.id and current_user.id != 1:
        abort(403)

    form = AddJobForm(obj=job)

    if form.validate_on_submit():
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data

        db_sess.commit()
        return redirect('/')

    return render_template('addjob.html', title='Редактирование работы', form=form)


@app.route('/job/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(id)

    if not job:
        abort(404)

    if job.team_leader != current_user.id and current_user.id != 1:
        abort(403)

    db_sess.delete(job)
    db_sess.commit()
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template('departments.html', departments=departments, names=names, title='List of Departments')


@app.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('department_form.html', title='Add Department', form=form)


@app.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).get(id)
    if not department:
        abort(404)

    # Права доступа (только капитан может редактировать департаменты)
    if current_user.id != 1:
        abort(403)

    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        db_sess.commit()
        return redirect('/departments')
    return render_template('department_form.html', title='Edit Department', form=form)


@app.route('/departments/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).get(id)
    if not department:
        abort(404)

    # Права доступа (только капитан может удалять департаменты)
    if current_user.id != 1:
        abort(403)

    db_sess.delete(department)
    db_sess.commit()
    return redirect('/departments')


# в main_users.py в функции main()
def main():
    db_session.global_init("db/mars_explorer.db")
    # Добавьте эти строки
    # db_sess = db_session.create_session()
    # db_session.SqlAlchemyBase.metadata.drop_all(db_sess.bind)
    # db_session.SqlAlchemyBase.metadata.create_all(db_sess.bind)
    app.run()


if __name__ == '__main__':
    main()
