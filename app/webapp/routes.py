from flask import render_template, url_for, flash, redirect, request
from webapp.forms import RegistrationForm, LoginForm, CompetitionAddForm
from webapp.models import *
from webapp import app, database, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import *


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/calendar')
def calendar():
    competitions = Competition.select().where(Competition.end_time > datetime.now())
    return render_template('calendar.html', title='calendar', competitions=competitions)


@app.route('/competition/<competition_id>')
def display_competition(competition_id):
    competition = Competition.get(competition_id)
    return render_template('competition.html', title=competition.name, competition=competition, Contains=Contains)


@app.route('/competition/add')
def add_competition():      #TODO popravim template
    if not (current_user.is_authenticated and current_user.admin):
        flash('You do not have admin privilages!', 'danger')
        return redirect(url_for('home'))
    form = CompetitionAddForm()
    return render_template('add-competition.html', title='Add competition', form=form)


@app.route('/task/add')
def add_task():
    if not (current_user.is_authenticated and current_user.admin):
        flash('You do not have admin privilages!', 'danger')
        return redirect(url_for('home'))
    form = TaskAddForm()
    return render_template('add_task.html', title='Add task', form=form)


@app.route('/task/<task_id>')
def display_task(task_id):
    selected_task = Task.get(int(task_id))
    return render_template('task.html', title=selected_task.title, task=selected_task)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    password_hash=hashed_pw,
                    email=form.email.data,
                    admin=False).save()
        flash('Account for ' + form.username.data + ' created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.select().where(User.username == form.username.data).get()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Welcome ' + form.username.data, 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        flash('Login failed. Invalid username or password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



