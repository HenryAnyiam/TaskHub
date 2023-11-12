#!/usr/bin/python3
"""handle web framework"""

from models.tasks import Task
from models.teams import Team
from models.users import User
from models.notifications import Notification
from models.messages import Message
from models import storage
import uuid
from flask import Flask, render_template, request, flash, redirect, url_for, session
from datetime import date
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from hashlib import md5
from datetime import datetime, timedelta
from flask_mail import Mail, Message as Msg


app = Flask(__name__)


app.secret_key = str(uuid.uuid4())


login = LoginManager(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Use the appropriate port for Gmail
app.config['MAIL_USERNAME'] = 'taskhub2023@gmail.com'
app.config['MAIL_PASSWORD'] = 'Application@email'
app.config['MAIL_USE_TLS'] = True  # Use TLS for Gmail

mail = Mail(app)


@login.user_loader
def load_user(id):
    """load current user"""
    all = storage.all()
    today = datetime.today()
    day = timedelta(seconds=86400)
    tasks = []
    for i in all:
        if 'Task' in i:
            if all[i].get('created_by') == id:
                tasks.append(all[i])
            else:
                team = all[i].get('team')
                team = all.get(f'Team.{team}')
                if team != None:
                    
                    if id in team.members:
                        tasks.append(all[i])
    for i in tasks:
        deadline = i.deadline
        if isinstance(deadline, datetime):
            diff = deadline - today
            if diff <= day:
                dic = {'title': f"Reminder: Your task {i.title} is due by {i.deadline}",
                   'type': 'Task Reminder', 'check': 'False', 'user_id': id}
                new_notification = Notification(**dic)
                new_notification.save()
    return all.get(f"User.{id}")

@login.unauthorized_handler
def unauthorized():
    """redirect when a user tries to access a 
    log in required page"""
    return redirect(url_for('login'))

@app.route("/", strict_slashes=False)
def index():
    """serve landing page"""
    return render_template("index.html")

@app.route("/log_in", methods=['GET', 'POST'],strict_slashes=False)
def login():
    """serve login page"""
    email = request.form.get('email')
    error = "None"
    if email:
        all = storage.all()
        for i in all:
            if email == all[i].get('email'):
                password = request.form.get('password')
                password = md5(password.encode()).hexdigest()
                if password == all[i].get('password'):
                    login_user(user=all[i], remember=True)
                    return redirect(url_for('view_tasks'))
                error = "Incorrect Password"
                return render_template("log_in.html", error=error)
        error = "User does not exist"
        return render_template("log_in.html", error=error)
    return render_template("log_in.html", error=error)

@app.route("/sign_up", methods=['GET', 'POST'], strict_slashes=False)
def signup():
    """serve sign up page"""
    name = request.form.get('name')
    if name:
        email = request.form.get('email')
        all = storage.all()
        for i in all:
            if all[i].get('email') == email:
                flash('Email already in use')
                return redirect(url_for('login'))
        dict = {'name': name, 'email': email,
                'password': request.form.get('password')}
        user = User(**dict)
        user.save()
        login_user(user=user, remember=True)
        return redirect(url_for('view_tasks'))
    return render_template("sign_up.html")

@app.route("/reset", methods=['GET', 'POST'], strict_slashes=False)
def reset():
    """serve reset page"""
    email = request.form.get('email')
    if email:
        msg = Msg("New Password", 
               recipients=[email])
        mail.send(msg)
    return render_template("reset.html")

@app.route("/new_task", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def create_task():
    """serve create task page"""
    user_id = current_user.id
    teams = [current_user]
    all = storage.all()
    notifications = current_user.notifications
    title = request.form.get('title')
    if title:
        team = request.form.get('team', current_user.id)
        if team != user_id:
            team = all[f'Team.{team}'].id
        day = request.form.get('deadline-date')
        time = request.form.get('deadline-time')
        deadline = None
        if day:
            if time:    
                deadline = day + 'T' + time
            else:
                deadline = day + 'T' + '00:00:00'
            deadline = datetime.fromisoformat(deadline)
        parent = request.form.get('parent-task', 'None')
        if parent == '':
            parent = 'None'
        dict = {'title': title, 'parent': parent, 'team': team, 
                'created_by': user_id}
        if deadline:
            dict['deadline'] = deadline
        task = Task(**dict)
        task.save()
        if parent != 'None':
            parent = all.get(f'Task.{parent}')
            if parent:
                hold = parent.child_task
                child_tasks = eval(hold) if isinstance(hold, str) else hold
                child_tasks.append(task.id)
                setattr(parent, 'child_task', str(child_tasks))
        if team != user_id:
            team_obj = all.get(f'Team.{team}')
            if team_obj:
                hold = team_obj.tasks
                str_tasks = eval(hold) if isinstance(hold, str) else hold
                str_tasks.append(task.id)
                setattr(team_obj, 'tasks', str(str_tasks))
        storage.save()
        return redirect(url_for('create_task'))
    for i in all:
        if 'Team' in i:
            members = all[i].get('members')
            if members:
                if user_id in members:
                    teams.append(all[i])
    min_date = date.today().isoformat()
    parent_id = request.form.get('parent_id', "None")
    members = "None"
    if parent_id != "None":
        parent = all.get(f'Task.{parent_id}')
        if (parent is not None) and (parent.created_by != parent.team):
            members = all.get(f'Team.{parent.team}', "None")
        elif (parent is not None) and (parent.created_by == parent.team):
            members = all.get(f'User.{parent.team}')
    return render_template("new_task.html", name=current_user.name, parent_id=parent_id,
                           members=members, file="task_body", teams=teams, date=min_date,
                           notifications=notifications)

@app.route("/view_task", strict_slashes=False)
@login_required
def view_tasks():
    """serve view tasks page"""
    user_id = current_user.id
    tasks = []
    all = storage.all()
    notifications = current_user.notifications
    for i in all:
        if 'Task' in i:
            if all[i].get('created_by') == user_id:
                tasks.append(all[i])
            else:
                team = all[i].get('team')
                team = all.get(f'Team.{team}')
                if team != None:
                    
                    if user_id in team.members:
                        tasks.append(all[i])
    tasks.sort(key=(lambda x: x.updated_at), reverse=True)
    length = len(tasks)
    for i in range(length):
        team_id = tasks[i].team
        team_obj = all.get(f'Team.{team_id}', all.get(f'User.{team_id}'))
        if team_obj:
            team_name = team_obj.name
            tasks[i] = tasks[i].to_dict()
            tasks[i]['team_name'] = team_name
        else:
            tasks[i].team_name = 'None'
    return render_template("view_task.html", name=current_user.name, file="table_body",
                           tasks=tasks, notifications=notifications)



@app.route("/view_team", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def view_teams():
    """serve view teams page"""
    team = storage.all('Team')
    user_id = request.form.get('user_id')
    team_id = request.form.get('team_id')
    if user_id and team_id:
        the_team = team.get(f'Team.{team_id}')
        if the_team:
            hold = the_team.members if isinstance(the_team.members, str) else the_team.members
            if user_id in hold:
                hold.remove(user_id)
                storage.save()
    if (team_id) and (user_id is None):
        the_team = team.get(f'Team.{team_id}')
        if the_team:
            storage.delete(the_team)
    team = storage.all('Team')
    all = storage.all()
    notifications = current_user.notifications
    team = storage.all('Team')
    teams = [team[i].to_dict() for i in team if current_user.id in team[i].members]
    length = len(teams)
    for i in range(length):
        hold = teams[i]['members']
        teams[i]['members'] = eval(hold) if isinstance(hold, str) else hold
        lent = len(teams[i]['members'])
        for j in range(lent):
            userId = teams[i]['members'][j]
            teams[i]['members'][j] = all.get(f'User.{userId}')
    for i in range(length):
        hold = teams[i]['tasks']
        teams[i]['tasks'] = eval(hold) if isinstance(hold, str) else hold
        lent = len(teams[i]['tasks'])
        for j in range(lent):
            taskId = teams[i]['tasks'][j]
            teams[i]['tasks'][j] = all.get(f'Task.{taskId}')
    return render_template("view_teams.html", name=current_user.name, id=current_user.id,
                           file="team_body", teams=teams, notifications=notifications)


@app.route("/new_team", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def create_teams():
    """serve create teams page"""
    error = "None"
    title = request.form.get("title")
    email = request.form.get('email')
    notifications = current_user.notifications
    team = "None"
    if (title is not None) and (email is None):
        dict = {'name': title, 'created_by': current_user.id}
        new_team = Team(**dict)
        new_team.save()
        members = new_team.members
        members.append(current_user.id)
        setattr(new_team, 'members', str(members))
        storage.save()
        return render_template("new_team.html", name=current_user.name, file='new_team', team=new_team)
    done =request.form.get('done')
    if (email is not None) and (done is None):
        team = request.form.get('team_id')
        if team:
            all = storage.all()
            team = all.get(f'Team.{team}')
            if team:
                invited = False
                for i in all:
                    if ('User' in i) and (all[i].email == email):
                        invited = True
                        invite = all[i].id
                        members = team.members
                        new = eval(members) if isinstance(members, str) else members
                        if invite not in new:
                            new.append(invite)
                            setattr(team, 'members', str(new))
                            storage.save()
                            dic = {'title': f"You have been added to a new team 'Team {team.name}'",
                                   'type': "New Team", "check" : "False", "user_id": invite}
                            notification = Notification(**dic)
                            notification.save()
                        else:
                            error = "User already in team"
                if invited is False:
                    error = "User does not exist"
    return render_template("new_team.html", name=current_user.name, file='new_team',
                           team=team, notifications=notifications, error=error)


@app.route('/work_board', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def work_board():
    """serve work board page"""
    taskId = request.args.get('task-id')
    main_task = 'None'
    child_tasks = 'None'
    messages = 'None'
    new_message = request.form.get('message')
    notifications = current_user.notifications
    if new_message:
        taskId = request.form.get('main_task')
        team = request.form.get('team')
        dic = {'text': new_message,
               'sender': current_user.id,
               'receiver': team}
        new_message = Message(**dic)
        new_message.save()
    all = storage.all()
    if new_message:
        team_detail = all.get(f'Team.{team}')
        memb = team_detail.members
        memb = eval(memb) if isinstance(memb, str) else memb
        for i in memb:
            dic = {'title': f"You have a new message from {current_user.name} in Team {team_detail.name}",
                   'type': 'New Message', 'check': 'False', 'user_id': i}
            new_notification = Notification(**dic)
            new_notification.save()
    p_task = request.form.get('task_id')
    if p_task:
        taskId = p_task
        p_task = all.get(f'Task.{p_task}')
        if p_task:
            p_task.progress = 100
            hold = p_task.child_task
            child = eval(hold) if isinstance(hold, str) else hold
            length = len(child)
            for i in range(length):
                child[i] = all.get(f'Task.{child[i]}')
            child_tasks = child if len(child) > 0 else 'None'
            if child_tasks != 'None':
                for i in child_tasks:
                    child_tasks[i].progress = 100
            storage.save()
    c_task = request.form.get('c_task_id')
    if c_task:
        c_task = all.get(f'Task.{c_task}')
        if c_task:
            c_task.progress = 100
            parent = all.get(f'Task.{c_task.parent}')
            if parent:
                taskId = parent.id
                hold = parent.child_task
                children = eval(hold) if isinstance(hold, str) else hold
                length = len(children)
                progress = parent.progress
                parent.progress = progress + ((1 / length) * 100)
                if parent.progress > 100:
                    parent.progress = 100
            storage.save()
    if taskId:
        task = all.get(f'Task.{taskId}')
        if task:
            parent = task.parent
            parent_task = all.get(f'Task.{parent}')
            if parent_task:
                main_task = parent_task
            else:
                main_task = task
            hold = main_task.child_task
            child = eval(hold) if isinstance(hold, str) else hold
            length = len(child)
            for i in range(length):
                child[i] = all.get(f'Task.{child[i]}')
            child_tasks = child if len(child) > 0 else 'None'
            if (main_task.team != current_user.id) and (all.get(f'Team.{main_task.team}')):
                messages = []
                for i in all:
                    if ('Message' in i) and (main_task.team == all[i].receiver):
                        messages.append(all[i])
                length = len(messages)
                if length > 0:
                    messages.sort(key=(lambda x: x.updated_at))
                    messages = [i.to_dict() for i in messages]
                    for i in range(length):
                        messages[i]['sender'] = all.get(f"User.{messages[i]['sender']}")
            if child_tasks != 'None':
                length = len(child_tasks)
                for i in range(length):
                    child_tasks[i] = child_tasks[i].to_dict()
                    child_tasks[i]['team'] = all.get(f"User.{child_tasks[i]['team']}", 
                                                     all.get(f"Team.{child_tasks[i]['team']}"))
            main_task = main_task.to_dict()
            main_task['team'] = all.get(f"User.{main_task['team']}", all.get(f"Team.{main_task['team']}"))
    return render_template("work_board.html", name=current_user.name,
                            file="work_board", main_task=main_task,
                            child_tasks=child_tasks, messages=messages, notifications=notifications)

@app.route('/logout', strict_slashes=False)
def logout():
    """log out current user"""
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
