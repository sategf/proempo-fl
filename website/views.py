#Main Views and URL endpoints to frontend of website

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Task, FinishedTask
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/help')
@login_required
def help():
    return render_template("help.html", user=current_user)

@views.route('/FAQ')
@login_required
def faq():
    accordion_items = [
        {"id": "section1", "title": "What is Proempo? What does it stand for?", "content": "Proempo is a mental health and productivity website. Proempo has 3 meanings. Pro for positivity, Em for Empathy, and Po for positivity."},
        {"id": "section2", "title": "How do I get started with the website?", "content": "You can get started by signing up through the blue link below."},
        {"id": "section3", "title": "Is there a tutorial or onboarding process to help me navigate the application for the first time?", "content": "Sorry, the website doesn't offer any process at the moment, come back for future updates."},
        {"id": "section4", "title": "Can I use the website without creating an account or logging in?", "content": "No, you need to create an account or log in in order to access the website."},
        {"id": "section5", "title": "What is the pricing model for your website? Are there any free or trial versions available?", "content": "This website is free, there is no pricing model nor any trial versions."},
        {"id": "section6", "title": "What is the pomodoro technique? How can i use it on the website?", "content": "The pomodoro method is a time management method based on 25-minute stretches of focused work broken by five-minute breaks. You can use the technique located in the Self-Help page."},
        {"id": "section7", "title": "Where can i go to contact support if any of the issues listed above aren't available?", "content": "You can visit the Support page in the navigation bar and list your issues there."},
       
    ]
    return render_template("FAQ.html", user=current_user, accordion_items=accordion_items)

@views.route('/bearMeditation')
@login_required
def bearMeditation():
    return render_template("bearMeditation.html", user=current_user)

@views.route('/regularMeditation')
@login_required
def regularMeditation():
    return render_template("regularMeditation.html", user=current_user)

@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST': 
        task = request.form.get('task')#Gets the task from the HTML 

        if len(task) < 1:
            flash('Task is too short!', category='error') 
        else:
            new_task = Task(data=task, user_id=current_user.id)  #providing the schema for the task 
            db.session.add(new_task) #adding the task to the database 
            db.session.commit()
            flash('Task added!', category='success')

    return render_template("tasks.html", user=current_user)

@views.route('/journal')
@login_required
def journal():
    return render_template("journal.html", user=current_user) 

@views.route('/delete-task', methods=['POST'])
def delete_task():  
    task = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    taskId = task['taskId']
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()

    return jsonify({})

@views.route('/delete-finished-task', methods=['POST'])
def delete_finished_task():  
    task_data = json.loads(request.data)
    taskId = task_data['taskId']
    finished_task = FinishedTask.query.get(taskId)

    if finished_task and finished_task.user_id == current_user.id:
        db.session.delete(finished_task)
        db.session.commit()

    return jsonify({})


@views.route('/mark-task', methods=['POST'])
@login_required
def mark_task():
    task_data = json.loads(request.data)
    task_id = task_data['taskId']

    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        # Create a FinishedTask with the same data
        finished_task = FinishedTask(data=task.data, user_id=current_user.id)

        # Add and commit changes to the database
        db.session.add(finished_task)
        db.session.delete(task)
        db.session.commit()

    return jsonify({})

@views.route('/unmark-task', methods=['POST'])
@login_required
def unMark_task():
    task_data = json.loads(request.data)
    finished_task_id = task_data['finishedTaskId']

    finished_task = FinishedTask.query.get(finished_task_id)

    if finished_task and finished_task.user_id == current_user.id:
        # Create a Task with the same data as the FinishedTask
        task = Task(data=finished_task.data, user_id=current_user.id)

        # Add and commit changes to the database
        db.session.add(task)
        db.session.delete(finished_task)
        db.session.commit()

    return jsonify({})