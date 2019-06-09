from flask import render_template, url_for, flash, redirect, request
from webapp.forms import RegistrationForm, LoginForm, CompetitionAddForm, TaskAddForm, TaskSubmitForm
from webapp.models import User, Competition, Task, Contains, Submission, Test, ParticipatesIn
from webapp.evaluate import evaluate
from webapp import app, database, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import *
import os
from zipfile import ZipFile


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/calendar')
def calendar():
    competitions = Competition.select().where(Competition.end_time > datetime.now())
    return render_template('calendar.html', title='calendar', competitions=competitions, current_user=current_user)


@app.route('/competition/<competition_id>', methods=['GET', 'POST'])#TODO timer, points
def display_competition(competition_id):
    competition = Competition.get(int(competition_id))
    return render_template('competition.html', title=competition.name, competition=competition, Contains=Contains, evaluate=evaluate)


@app.route('/evaluate/competition/<competition_id>', methods=['GET', 'POST'])   #evaluate a given competition
@app.route('/evaluate/task/<task_id>', methods=['GET', 'POST'])   #evaluate a given task for a given user
def evaluate(competition_id=None, task_id=None):
    if not (current_user and current_user.is_authenticated and current_user.admin):
        flash('You do not have admin privilages', 'danger')
        return redirect(url_for('display_competition', competition_id=competition_id))

    #TODO the actual evaluation takes place here
    if competition_id:
        flash('The competition is being evaluated...', 'info')
        to_evaluate = Submission.select().where(Submission.competition == competition_id)
    if task_id:
        flash('The task is being evaluated...', 'info')
        to_evaluate = Submission.select().where(Submission.task_id == task_id and Submission.user_id == current_user.id and Submission.result == None)

    print('to evaluate:')
    for i in to_evaluate:
        print(i)

    if competition_id:
        return redirect(url_for('display_competition', competition_id=competition_id))
    if task_id:
        return redirect(url_for('display_task', task_id=task_id))




@app.route('/competition/add', methods=['GET', 'POST'])
def add_competition():
    if not (current_user.is_authenticated and current_user.admin):
        flash('You do not have admin privilages!', 'danger')
        return redirect(url_for('home'))
    form = CompetitionAddForm()
    form.tasks.choices=[(t.id, t.title) for t in Task.select()]
    form.participants.choices=[(u.id, u.username) for u in User.select()]
    if form.validate_on_submit():
        competition = Competition(name=form.name.data,
                                  start_time=form.start_time.data,
                                  end_time=form.end_time.data,
                                  public=form.public.data)
        competition.save()

        for task in form.tasks.data:
            contains = Contains(competition=competition.id,
                                task=int(task)).save()
        for participant in form.participants.data:
            ParticipatesIn(competition=competition.id,
                                user=int(participant)).save()
        flash('Competition added seccesfully!', 'success')
        return redirect(url_for('calendar'))
    return render_template('add_competition.html', title='Add competition', form=form, action='add')


#@app.route('/competition/<competition_id>/edit', methods=['GET', 'POST'])       #TODO
#def add_competition():
#    if not (current_user.is_authenticated and current_user.admin):
#        flash('You do not have admin privilages!', 'danger')
#        return redirect(url_for('home'))
#
#    form = CompetitionAddForm()
#    if form.validate_on_submit():
#        competition = Competition(name=form.name.data,
#                                  start_time=form.start_time.data,
#                                  end_time=form.end_time.data,
#                                  public=form.public.data)
#        competition.save()
#        for task in form.tasks.data:
#            contains = Contains(competition=competition.id,
#                                task=int(task)).save()
#        flash('Competition added seccesfully!', 'success')
#        return redirect(url_for('calendar'))
#    return render_template('add_competition.html', title='Add competition', form=form, action='edit')


@app.route('/task')
def task():
    if current_user.is_authenticated and current_user.admin:
        tasks = Task.select()
    else:
        tasks = Task.select().where(Task.public)
    return render_template('list_task.html', title='task', tasks=tasks, current_user=current_user)


def save_text(form):
    _, ext = os.path.splitext(form.text.data.filename)
    filename = form.title.data.replace(' ', '_') + ext
    route = os.path.join(app.root_path, 'static/task_text', filename)
    form.text.data.save(route)
    return os.path.join('static/task_text', filename)


def save_tests(form, task_id):
    filename = form.tests.data.filename.replace(' ', '_')
    route = os.path.join(app.root_path, 'static/tests', filename)
    form.tests.data.save(route)
    #route = os.path.join('static/tests', filename)
    zip_tests = ZipFile(route)
    for file in zip_tests.namelist():
        if not (file.startswith('out/') or file.endswith('/')):
            test = Test(task=task_id,
                        test_name=file.split('/')[1],
                        zip_file=route)
            test.save()
    return os.path.join('static/tests', filename)


@app.route('/task/add', methods=['GET', 'POST'])
def add_task():
    if not (current_user.is_authenticated and current_user.admin):
        flash('You do not have admin privilages!', 'danger')
        return redirect(url_for('home'))
    form = TaskAddForm()
    if form.validate_on_submit():
        relative_path = save_text(form)
        task = Task(title=form.title.data,
                    text=relative_path,
                    maxpoints=form.maxpoints.data,
                    public=form.public.data)
        task.save()
        save_tests(form, task.id)
        flash('Task added seccesfully!', 'success')
        return redirect(url_for('display_task', task_id=task.id))
    return render_template('add_task.html', title='Add task', form=form)


def save_submission(form, id):
    _, ext = os.path.splitext(form.code.data.filename)
    filename = str(id) + ext
    route = os.path.join(app.root_path, 'static/submission', filename)
    form.code.data.save(route)
    return os.path.join('static/submission', filename)


@app.route('/competition/<competition_id>/<task_id>', methods=['GET', 'POST'])        #TODO timer, points
@app.route('/task/<task_id>', defaults={'competition_id':None}, methods=['GET', 'POST'])
def display_task(task_id, competition_id):
    selected_task = Task.get(int(task_id))
    if competition_id:
        competition = Competition.get(int(competition_id))

    if not (current_user and current_user.admin):
        if competition_id:
            if not (ParticipatesIn.select(ParticipatesIn.user_id == current_user.id and ParticipatesIn.competition_id == competition_id).exists() or competition.public):
                flash('You are not in this competition', 'danger')
                return redirect(url_for('task'))
        else:
            if not selected_task.public:
                flash('You cannot view that task', 'danger')
                return redirect(url_for('task'))

    taskSubmitForm = TaskSubmitForm()
    active = True
    if taskSubmitForm.validate_on_submit():
        submission = Submission(competition=competition_id,
                                language=taskSubmitForm.language.data,
                                task=task_id,
                                time=datetime.now(),
                                user=current_user.id)
        submission.save()
        relative_path = save_submission(taskSubmitForm, submission.id)
        submission.code = relative_path
        submission.save(only=[Submission.code])
        #return redirect(url_for(''))

    if competition_id:
        if competition.start_time > datetime.now() or competition.end_time < datetime.now():
            flash('Wait for the competition to start to view the tasks', 'danger')
            return redirect(url_for('display_competition', competition_id=competition_id))

    return render_template('view_task.html', title=selected_task.title, task=selected_task, file=selected_task.text, current_user=current_user, taskSubmitForm=taskSubmitForm)#, active=active)


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



