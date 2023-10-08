#Main Views and URL endpoints to frontend of website
from flask import Flask
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_mail import Mail, Message
from flask_login import login_required, current_user
from .models import Journal, Task, FinishedTask, Card, Lesson
from sqlalchemy.orm import aliased
from . import db
import json, os, smtplib
from datetime import date, datetime
import csv

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
    currentDay = todays_date()
    return render_template("home.html", user=current_user, qod=qod, currentDay=currentDay)

today = date.today()

def todays_date():
    day_str = today.strftime('%d')
    day_int = int(day_str)
    
    
    if day_int < 10:
        day = (today.strftime('%d')).lstrip('0')
    else:
        day = (today.strftime('%d'))
    
    if (day_int % 10 == 1):
        day = day + 'st'
    elif (day_int % 10 == 2):
        day = day + 'nd'
    elif (day_int % 10 == 3):
        day = day + 'rd'
    else:
        day = day + 'th'

    currentDay = today.strftime('%A, %B ' + day + ', %Y')

    return currentDay
def generate_quote():
    csv_file_path = os.path.join(app.root_path, 'static', 'list.csv')
    with open(csv_file_path, 'r') as f:

        reader = csv.reader(f, delimiter=',')
        epoch = datetime(2023, 10, 1)
        today = datetime.now()
        currentDay = (today - epoch).days
        num_lines = sum(1 for _ in reader)
        index = currentDay % num_lines
        f.seek(0)
        

        for i, row in enumerate(reader):
            if i == index:
                qod = (row[1], row[0]) 
                break
        else:
            qod = "Error: Quote not found."

    return qod

@app.route('/toggle_white_noise', methods=['POST'])
@login_required
def toggle_white_noise():
    print("Form submitted")
    # Handle the white noise play/pause action based on the form submission (your implementation)
    return redirect(url_for('views.home'))  # Redirect back to the home page after handling the action






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
        {
            "id": "section1",
            "title": "Getting Started",
            "content": "",
            "nested_items": [
                {"id": "nested1", "title": "Is there a tutorial or onboarding process to help me navigate the application for the first time?", "content": "Sorry, the website doesn't offer any process at the moment, come back for future updates."},
                {"id": "nested2", "title": "Can I use the website without creating an account or logging in?", "content": "No, you need to create an account or log in in order to access the website."},
                {"id": "nested3", "title": "What is the pricing model for your website? Are there any free or trial versions available?", "content": "This website is free, there is no pricing model nor any trial versions."},
                {"id": "nested4", "title": "What is the pomodoro technique? How can I use it on the website?", "content": "The pomodoro technique is a time management method based on 25-minute stretches of focused work broken by five-minute breaks. You can use the technique located in the Self-Help page."},
                {"id": "nested5", "title": "What is the feynman technique? How can I use it on the website?", "content": "The feynman technique is a four-step process for understanding any topic. It rejects automated recall in favor of true comprehension gained through selection, research, writing, explaining, and refining. You can find it located in the self-help page."},
                {"id": "nested6", "title": "Where can I go to contact support if any of the issues listed in the page aren't available?", "content": "You can visit the Support page in the navigation bar and list your issues there."}
            ],
        },
        {
            "id": "section2",
            "title": "Mental Health",
            "content": "",
            "nested_items": [
                {"id": "nested7", "title": "What is the relationship between mental health and productivity?", "content": "The state of your mental health and how productive you are, have a very interconnected relationship but, many people choose to ignore this relationship. Mental health consists of many things such as stress, anxiety, and depression. Typically, someone who has any of these challenges will experience lower levels of engagement, creativity and problem solving. Proempo looks keep a positive relationship between these two factors of life."},
                {"id": "nested8", "title": "How will Proempo help me manage my stress and anxiety?", "content": "As students, here at Proempo, we have a lot of empathy towards people struggling to control their thoughts and are very stressed about deadlines. Organizing your life is a great way to get started with handling your stress and/or anxiety. By keeping all your activities, schoolwork, or just general notes and reminders in one centrally located place that is easily accessible. Having this will layout how much time you have to do these tasks. You will be at ease seeing that your tasks are completed. Proempo also offers a journaling section to help with anxiety delt in your daily life."},
                {"id": "nested9", "title": "What is the point of journaling?", "content": "Journalling is a great activity to help yourself. While journaling there are no outside factors to worry about except “Me, myself and I”. This is a safe space where you can heave all your pent-up thoughts and feelings onto a page. As time goes on you will have many journals telling you how you felt during a particular day and the reason that day followed that outcome. Looking back at these journals will show you how much you have developed as a person and learn from your past self."},
                {"id": "nested10", "title": "What is burnout and what to do if I experience it?", "content": "Burnout is a state of physical and/or emotional exhaustion that can come to effect someone’s identity and sense of feeling accomplished. Steps to help reduce burnout starts with seeking support from family members or colleagues to help you collaborate and cope with what you are feeling. You could go ahead and try an activity or hobby you really enjoy that gets you relaxed or even exercise. The “cure” to burnout is taking a break from either work or school or other factors that might be causing this."},
                {"id": "nested11", "title": "Where can I go to seek support?", "content": "If in need of serious help or support beyond our services here are some resources to look into: Suicide and Crisis lifeline: 988, Therapy."}
            
            ],
        },
        {
            "id": "section3",
            "title": "Productivity",
            "content": "",
            "nested_items": [
                {"id": "nested12", "title": "What features does the website offer to enhance productivity?", "content": "The features offered in the website are the pomodoro method, feynman technique, which are both located in the self-help page."},
                {"id": "nested13", "title": "Can you provide tips for settings and achieving productivity goals?", "content": "Our tips to utilizing this website for setting and achieving goals are creating tasks, using the pomodoro method, creating flashcards, and taking a break to prevent burnout."},
                {"id": "nested14", "title": "How does time management play a role in productivity? Can your website assist with this?", "content": "Time management plays a crucial role in productivity by helping individuals prioritize tasks, allocate time efficiently, and minimize distractions. Effective time management enables better organization and allows individuals to accomplish more in less time, leading to increased productivity. Our website can offer users with creating a task withing the tasks page, using the pomodoro method to set a timer along with completing the tasks created from the task page, creating flashcards in the self-help page, etc. Please check the self-help page if you want to enhance your productivity."},
                {"id": "nested15", "title": "What are some strategies for overcoming procrastination and maintaining focus?", "content": "Our website can list some strategies. Break tasks into smaller steps. Set specific, achievable goals. Use a timer for focused work like the pomodoro method. Minimize distractions with our built-in white noise player. Reward yourself for completing tasks. Create a dedicated workspace. Prioritize tasks based on importance and urgency."},
                {"id": "nested16", "title": "how can I effectively priortize tasks and projects to optimize my productivity?", "content": "This question is in progress. Come back for future updates."},
                {"id": "nested17", "title": "How can I track my progress and measure my productivity gains using the website?", "content": "You can track progress in the website with the provided graphs and charts to measure your current productivity progress."},
            ],
        },
       
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
        task_data = request.form.get('task')  # Gets the task from the HTML
        due_date_str = request.form.get('dueDate')  # Gets the due date string from the HTML

        if len(task_data) < 1:
            flash('Task is too short!', category='error')
        else:
            due_date = None  # Default to None if no due date is provided
            if due_date_str:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

            new_task = Task(data=task_data, due_date=due_date, user_id=current_user.id)  # Provide the schema for the task
            db.session.add(new_task)  # Add the task to the database
            db.session.commit()
            flash('Task added!', category='success')

    return render_template("tasks.html", user=current_user)




@views.route('/journal', methods = ['GET', 'POST'])
@login_required
def journal():
    if request.method == 'POST':
        journal_content = request.form.get('dearJournalContent')  
        journal_gratitude = request.form.get('gratitudeContent')
        journal_rating = request.form.get('dayRating')
        
       

        new_journal = Journal(data=journal_content, user_gratitude=journal_gratitude, user_rating=journal_rating, user_id=current_user.id)  # Provide the schema for the task
        db.session.add(new_journal)  
        db.session.commit()
        flash('Journal added!', category='success')
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


@views.route('/ViewFlashcards')
@login_required
def show_flashcard():
    lesson_alias = aliased(Lesson)
    user_flashcards = (Card.query.join(lesson_alias).filter(lesson_alias.user_id == current_user.id).all())
    return render_template("viewFlashcards.html", user=current_user, cards=user_flashcards, select_lesson=None)


@views.route('/CreateFlashcards', methods=["GET", "POST"])
@login_required
def new_flashcard():
     # gets all the lessons from the user
    if request.method == "GET":
        all_lessons=current_user.lessons
        return render_template("createFlashcards.html", all_lessons=all_lessons, user=current_user)
    else:
        #Get the data from the form
        lesson_id=request.form["lesson"]
        question=request.form["question"]
        answer=request.form["answer"]
        new_lesson_name=request.form["new_lesson_name"]

        if lesson_id:
            # Gets the selected lesson from the user
            selected_lesson=Lesson.query.get(lesson_id)
            if not selected_lesson or selected_lesson.user_id != current_user.id:
                print("The selected lesson doesnt exist.")
                return redirect("/CreateFlashcards")
        elif new_lesson_name:
            #Create a new lesson if needed
            new_lesson=Lesson(name=new_lesson_name, user_id=current_user.id)
            db.session.add(new_lesson)
            db.session.commit()
            selected_lesson=new_lesson
        else:
            print("no lesson provided")
            return redirect("/CreateFlashcards")
    
        card=Card(question=question, lesson_id=selected_lesson.id,  answer=answer)
        db.session.add(card)
        db.session.commit()

        return redirect("/CreateFlashcards")


@views.route('/clear-all-completed-tasks', methods=['POST'])
@login_required
def clear_all_completed_tasks():
    # Perform the action to clear all completed tasks
    completed_tasks = FinishedTask.query.filter_by(user_id=current_user.id).all()
    for task in completed_tasks:
        db.session.delete(task)
    db.session.commit()
    return jsonify({})



@views.route('/save-journal-entry', methods=['POST'])
def save_journal_entry():
    try:
        data = request.json
        user_id = current_user.id
        dear_journal_content = data['dearJournalContent']
        grateful_content = ', '.join(data['gratitudeContent'])
        day_rating = data['dayRating']

        journal_entry = Journal(
            user_id= user_id,
            dear_journal_content=dear_journal_content,
            grateful_content=grateful_content,
            day_rating=day_rating
        )

        db.session.add(journal_entry)
        db.session.commit()

        return jsonify({'message': 'Journal entry saved successfully'})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to save journal entry'}), 500
