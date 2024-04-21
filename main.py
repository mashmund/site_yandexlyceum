from fileinput import filename

import requests
from flask import Flask, render_template, redirect, make_response, jsonify, abort, request
from flask_wtf import form
from sqlalchemy import create_engine

import data.jobs
from data import db_session
from data.api import jobs_api
from data.forms.LoginForm import LoginForm
from data.forms.add_jobs import JobForm
from data.forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import folium
from data.jobs import Jobs
from data.users import User
from data.gerate_adress import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

engine = create_engine('sqlite:///db/mars.db')

# Создайте все таблицы, определенные в моделях
db_session.SqlAlchemyBase.metadata.create_all(engine)
api_key = '40d1649f-0493-4b70-98ba-98533de7710b'
db_session.global_init("db/mars.db")


@app.route("/about_us")
def about_us():
    return render_template('about_us.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    context = {}
    filtered_ads = []
    context["jobs"] = db_sess.query(Jobs).all()
    if request == 'POST':
        pass
    else:
        print(3)
        age = request.form.get('age')
        spher = request.form.get('spher')
        if age:
            if spher:
                for i in context['jobs']:
                    if str(i.age) == str(age) and str(i.spher) == str(spher):
                        filtered_ads.append(i)
            else:
                for i in context['jobs']:
                    if str(i.age) == str(age):
                        filtered_ads.append(i)
        else:
            if spher:
                for i in context['jobs']:
                    if str(i.spher) == str(spher):
                        filtered_ads.append(i)
            else:
                filtered_ads = context["jobs"]

    print(filtered_ads)
    return render_template('index.html', filtered_ads=filtered_ads, **context)


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
        if form.role.data == 'Участник':
            user_type = 3
        elif form.role.data == 'Организатор':
            user_type = 2
        user = User(
            name=form.name.data,
            email=form.email.data,
            type_of_user=user_type
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    add_form = JobForm()
    location = request.form.get('location')

    # Запрос к API Яндекс.Карт для получения координат по адресу
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&format=json&geocode={location}'
    response = requests.get(url)
    data = response.json()

    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs(
            job=add_form.job.data,
            des=add_form.des.data,
            spher=add_form.spher.data,
            age=add_form.age.data,
            adress=add_form.adress.data,
            contact=add_form.contact.data,
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы',
                           form=add_form)


@app.route("/jobbs/<name>", methods=['GET', 'POST'])
def game(name):
    db_sess = db_session.create_session()
    if request.method == 'GET':
        db_sess = db_session.create_session()

        try:
            job = db_sess.query(Jobs).filter(Jobs.job == name).one()
            return render_template("jobs.html", params=job, adr=get_adress(job.adress))
        except Exception as e:
            print(e)
            return abort(404)


# обработчик страницы редактирования игры
@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_games(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            form.job.data = job.job
            form.des.data = job.des
            form.spher.data = job.spher
            form.age.data = job.age
            form.adress.data = job.adress
            # form.photo.label = job.photo
            form.contact.data = job.contact
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            job.job = form.job.data
            job.des = form.des.data
            job.spher = form.spher.data
            job.age = form.age.data
            job.adress = form.adress.data
            # job.photo = form.photo.label
            job.contact = form.contact.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html',
                           title='Редактирование игры',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def games_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=555, host='127.0.0.1')
