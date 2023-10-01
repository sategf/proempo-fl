#Main Views and URL endpoints to frontend of website
from flask import Flask
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_mail import Mail, Message
from flask_login import login_required, current_user
from .models import Task, FinishedTask
from . import db
from quote import quote
import json, os

views = Blueprint('views', __name__)


app = Flask(__name__)


# Get the values of the environment variables
mail_username = os.environ.get('MAIL_USERNAME')
mail_password = os.environ.get('MAIL_PASSWORD')




# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # SMTP server
app.config['MAIL_PORT'] = 587  #the SMTP port
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


# Creating the Mail instance
mail = Mail(app)


# Defining the support email address
support_email = "Proempohelpdesk@gmail.com" 




@views.route('/')
@login_required
def home():
    qod = generate_quote()
    return render_template("home.html", user=current_user, qod=qod)

def generate_quote():
    #generates the quote off the keywork Positive from the quote library.
    qod = quote('Positive', limit=1) 
    return qod[0]


@views.route('/help')
@login_required
def help():
    return render_template("help.html", user=current_user)

@views.route('/feynman')
@login_required
def feynman():
    return render_template("feynman.html", user=current_user)

@views.route('/pomodoro')
@login_required
def pomodoro():
    task_id = request.args.get('taskId')
    task_data = request.args.get('taskData')
    uncompleted_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('pomodoro.html', task_id=task_id, task_data=task_data, user=current_user, uncompleted_tasks=uncompleted_tasks)


@views.route('/FAQ')
@login_required
def faq():
    accordion_items = [
        {"id": "section1", "title": "Is there a tutorial or onboarding process to help me navigate the application for the first time?", "content": "Sorry, the website doesn't offer any process at the moment, come back for future updates."},
        {"id": "section2", "title": "Can I use the website without creating an account or logging in?", "content": "No, you need to create an account or log in in order to access the website."},
        {"id": "section3", "title": "What is the pricing model for your website? Are there any free or trial versions available?", "content": "This website is free, there is no pricing model nor any trial versions."},
        {"id": "section4", "title": "What is the pomodoro technique? How can I use it on the website?", "content": "The pomodoro technique is a time management method based on 25-minute stretches of focused work broken by five-minute breaks. You can use the technique located in the Self-Help page."},
        {"id": "section5", "title": "What is the feynman technique? How can I use it on the website?", "content": "The feynman technique is a four-step process for understanding any topic. It rejects automated recall in favor of true comprehension gained through selection, research, writing, explaining, and refining. You can find it located in the self-help page."},
        {"id": "section6", "title": "Where can I go to contact support if any of the issues listed above aren't available?", "content": "You can visit the Support page in the navigation bar and list your issues there."},
       
    ]
    return render_template("FAQ.html", user=current_user, accordion_items=accordion_items)

@views.route('/MentalHealth')
@login_required
def mentalhealth():
    accordion_items = [
        {"id": "section1", "title": "", "content": ""},  #title = header title or question, content = the description of the question or answer
        {"id": "section2", "title": "", "content": ""},
        {"id": "section3", "title": "", "content": ""},
        {"id": "section4", "title": "", "content": ""},
        {"id": "section5", "title": "", "content": ""},
        {"id": "section6", "title": "Where can I go to contact support if any of the issues listed above aren't available?", "content": "You can visit the Support page in the navigation bar and list your issues there."},
       
    ]
    return render_template("MentalHealth.html", user=current_user, accordion_items=accordion_items)

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

@views.route('/About')
@login_required
def about():
    return render_template("About.html", user=current_user)

@views.route('/Support', methods=['GET'])
@login_required
def support():
    return render_template("Support.html", user=current_user)

@app.route('/submit_support', methods=['POST']) #something about routes isn't submitting the form through here, will be fixed soon
def submit_support():
    if request.method == 'POST':
        # Get form data
        issue_title = request.form['issue_title']
        username = request.form['username']
        description = request.form['description']
        
        # Send an email to the support team with the form data
        send_support_email(issue_title, username, description)
        
        # You can also save the form data to a database or perform other actions as needed
        
        # Redirect back to the support page or a thank you page
        return redirect(url_for('thank_you'))


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html') # thank you message for the user after submitting form




def send_support_email(issue_title, username, description):
    # Create a message object for the email
    msg = Message('Support Request: ' + issue_title, sender=support_email, recipients=[support_email])
    
    # Customize the email content with the form data
    msg.body = f"Issue Title: {issue_title}\nUsername: {username}\nDescription: {description}"
    
    # Send the email
    try:
        mail.send(msg)
        print("Support email sent successfully")
    except Exception as e:
        print(f"Error sending support email: {str(e)}")


@views.route('/Flashcards')
@login_required
def flascards():
    return render_template("Flashcards.html", user=current_user)