#Main Views and URL endpoints to frontend of website
from flask import Flask
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_mail import Mail, Message
from email.message import EmailMessage
from flask_login import login_required, current_user
from .models import Goal, Journal, Task, FinishedTask, ArchivedTask, Card, Lesson, Pride, Support
from sqlalchemy.orm import aliased
from . import db
import json, os, smtplib
from datetime import date, datetime
import csv
import plotly.graph_objs as go
from datetime import datetime, timedelta
from sqlalchemy import and_, func, text

views = Blueprint('views', __name__)


app = Flask(__name__)


# Get the values of the environment variables
mail_username = os.environ.get('MAIL_USERNAME')
mail_password = os.environ.get('MAIL_PASSWORD')





# Creating the Mail instance
mail = Mail(app)


# Defining the support email address
support_email = "proempohelpdesk@gmail.com" 




@views.route('/')
@login_required
def home():
    qod = generate_quote()
    currentDay = todays_date()
    print(current_user.language)
    if current_user.language == "ro":
        welcome = "Bun venit la ProEmPo, "
        currentDay = "Astăzi este " + today.strftime("%d.%m.%Y")
        openNoisePlayer = "Deschide playerul de zgomot alb"
    else:
        welcome = "Welcome to ProEmPo, "
        currentDay = currentDay
        openNoisePlayer = "Open Noise Player"

    return render_template("home.html", user=current_user, qod=qod, currentDay=currentDay, welcome=welcome, openNoisePlayer=openNoisePlayer)

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
                if(row[0] == "") :
                    row[0] = "Unknown Author"
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
    if current_user.language == "ro":
        accordion_items = [
    {
        "id": "section1",
        "title": "Începerea",
        "content": "",
        "nested_items": [
            {"id": "nested1", "title": "Există un tutorial sau un proces de inițiere care să mă ajute să navighez în aplicație pentru prima dată?", "content": "Ne pare rău, site-ul nu oferă niciun proces în acest moment. Reveniți pentru actualizări viitoare."},
            {"id": "nested2", "title": "Care este modelul de preț pentru site-ul dvs.? Există versiuni gratuite sau de încercare disponibile?", "content": "Acest site este gratuit, nu există un model de preț sau versiuni de încercare."},
            {"id": "nested3", "title": "Ce este tehnica pomodoro? Cum o pot utiliza pe site?", "content": "Tehnica pomodoro este o metodă de gestionare a timpului bazată pe sesiuni de lucru concentrate de 25 de minute întrerupte de pauze de cinci minute. Puteți utiliza această tehnică în pagina de Ajutor personal."},
            {"id": "nested4", "title": "Ce este tehnica Feynman? Cum o pot utiliza pe site?", "content": "Tehnica Feynman este un proces în patru pași pentru înțelegerea oricărui subiect. Ea respinge reținerea automată în favoarea înțelegerii autentice obținute prin selecție, cercetare, scriere, expunere și rafinare. Puteți găsi această tehnică în pagina de Ajutor personal."},
            {"id": "nested5", "title": "Ce este zgomotul alb? Cum mă poate ajuta zgomotul alb în timp ce utilizez acest site?", "content": "Zgomotul alb este un sunet constant și uniform care conține putere egală la toate frecvențele auzibile. Vă poate ajuta prin mascarea zgomotului de fundal, îmbunătățirea concentrării și a atenției și crearea unui mediu sonor constant."},
            {"id": "nested6", "title": "Unde pot să merg pentru a lua legătura cu suportul dacă nu sunt disponibile problemele listate pe pagină?", "content": "Puteți vizita pagina de Suport din bara de navigație și să vă listați problemele acolo."}
        ],
    },
    {
        "id": "section2",
        "title": "Sănătatea Mintală",
        "content": "",
        "nested_items": [
            {"id": "nested8", "title": "Care este relația dintre sănătatea mintală și productivitate?", "content": "Starea sănătății mintale și nivelul de productivitate au o relație foarte strânsă, însă mulți oameni aleg să ignore această relație. Sănătatea mintală constă în multe aspecte, cum ar fi stresul, anxietatea și depresia. De obicei, o persoană care se confruntă cu aceste provocări va avea niveluri mai scăzute de implicare, creativitate și rezolvare a problemelor. Proempo încearcă să mențină o relație pozitivă între aceste două aspecte ale vieții."},
            {"id": "nested9", "title": "Cum mă va ajuta Proempo să gestionez stresul și anxietatea?", "content": "Ca studenți, noi, la Proempo, avem multă empatie față de oamenii care luptă să-și controleze gândurile și sunt foarte stresați din cauza termenelor limită. Organizarea vieții tale este un mod excelent de a începe să faci față stresului și/sau anxietății. Păstrând toate activitățile, temele școlare sau pur și simplu notele și amintirile generale într-un loc central ușor accesibil. Acest lucru va arăta cât timp ai pentru a face aceste sarcini. Te vei simți în siguranță văzând că ai completat sarcinile. Proempo oferă și o secțiune de jurnalizare pentru a ajuta cu anxietatea trăită în viața ta de zi cu zi."},
            {"id": "nested10", "title": "Care este scopul jurnalizării?", "content": "Jurnalizarea este o activitate excelentă pentru a te ajuta pe tine însuți. În timpul jurnalizării, nu există factori externi de care să-ți faci griji, în afara lui „Eu, eu și eu”. Acesta este un spațiu sigur în care poți elibera toate gândurile și sentimentele acumulate pe o pagină. Pe măsură ce trece timpul, vei avea multe jurnale care îți vor arăta cum te-ai simțit într-o zi anume și motivul pentru care acea zi a avut acel rezultat. Privind înapoi la aceste jurnale, vei vedea cât de mult te-ai dezvoltat ca persoană și vei învăța din trecutul tău."},
            {"id": "nested11", "title": "Ce este epuizarea și ce trebuie să fac dacă o experimentez?", "content": "Epuizarea este o stare de oboseală fizică și/sau emoțională care poate afecta identitatea cuiva și sentimentul de a fi realizat. Pașii pentru a reduce epuizarea încep cu căutarea de sprijin din partea membrilor familiei sau colegilor pentru a vă ajuta să colaborați și să faceți față a ceea ce simțiți. Puteți să încercați să vă dedicați timp unei activități sau hobby pe care îl apreciați și care vă relaxează sau chiar să faceți exerciții. „Leacul” pentru epuizare constă în a lua o pauză de la muncă sau școală sau de la alte factori care ar putea cauza această stare."},
            {"id": "nested12", "title": "Unde pot să merg pentru a cere ajutor?", "content": "Dacă aveți nevoie de ajutor serios sau de suport dincolo de serviciile noastre, iată câteva resurse pe care le puteți verifica: Linia de viață pentru suicid și criză: 988, Terapie."}
        ],
    },
    {
        "id": "section3",
        "title": "Productivitate",
        "content": "",
        "nested_items": [
            {"id": "nested13", "title": "Ce funcționalități oferă site-ul pentru a îmbunătăți productivitatea?", "content": "Funcționalitățile oferite pe site sunt metoda pomodoro și tehnica Feynman, ambele fiind disponibile în pagina de Ajutor personal."},
            {"id": "nested14", "title": "Puteți oferi sfaturi pentru stabilirea și atingerea obiectivelor de productivitate?", "content": "Sfaturile noastre pentru utilizarea acestui site în stabilirea și atingerea obiectivelor includ crearea de sarcini, utilizarea metodei pomodoro, crearea de carduri cu întrebări și realizarea de pauze pentru a preveni epuizarea."},
            {"id": "nested15", "title": "Cum joacă gestionarea timpului un rol în productivitate? Poate site-ul dvs. să ajute în acest sens?", "content": "Gestionarea timpului joacă un rol crucial în productivitate, ajutând persoanele să-și prioritizeze sarcinile, să aloce timp eficient și să minimizeze distragerile. O gestionare eficientă a timpului permite o mai bună organizare și le permite persoanelor să realizeze mai mult în mai puțin timp, ceea ce duce la o productivitate mai mare. Site-ul nostru poate oferi utilizatorilor crearea unei sarcini în pagina de sarcini, utilizarea metodei pomodoro pentru a seta un cronometru, împreună cu finalizarea sarcinilor create din pagina de sarcini, crearea de carduri cu întrebări în pagina de Ajutor personal, etc. Vă rugăm să verificați pagina de Ajutor personal dacă doriți să vă îmbunătățiți productivitatea."},
            {"id": "nested16", "title": "Care sunt câteva strategii pentru a învinge procrastinarea și a menține concentrarea?", "content": "Site-ul nostru poate lista câteva strategii. Descompuneți sarcinile în pași mai mici. Stabiliți obiective specifice și realizabile. Utilizați un cronometru pentru muncă concentrată, precum metoda pomodoro. Minimizați distragerile cu ajutorul player-ului nostru de zgomot alb încorporat. Răsfățați-vă pentru finalizarea sarcinilor. Creați un spațiu de lucru dedicat. Prioritizați sarcinile în funcție de importanță și urgență."},
            {"id": "nested17", "title": "Cum pot să prioritizez eficient sarcinile și proiectele pentru a-ți optimiza productivitatea?", "content": "Această întrebare este în lucru. Reveniți pentru actualizări viitoare."},
            {"id": "nested18", "title": "Cum pot să urmăresc progresul și să măsurăm câștigurile de productivitate folosind site-ul?", "content": "Puteți urmări progresul pe site cu ajutorul graficelor și diagramele furnizate pentru a măsura progresul dvs. actual de productivitate."}
        ],
    },
]
        FAQtitle = "Întrebări frecvente"
        subtitle = "Dacă aveți alte întrebări, vă rugăm să consultați celelalte secțiuni de mai jos."
    else:
        accordion_items = [
            {
                "id": "section1",
                "title": "Getting Started",
                "content": "",
                "nested_items": [
                    {"id": "nested1", "title": "Is there a tutorial or onboarding process to help me navigate the application for the first time?", "content": "Sorry, the website doesn't offer any process at the moment, come back for future updates."},
                    {"id": "nested2", "title": "What is the pricing model for your website? Are there any free or trial versions available?", "content": "This website is free, there is no pricing model nor any trial versions."},
                    {"id": "nested3", "title": "What is the pomodoro technique? How can I use it on the website?", "content": "The pomodoro technique is a time management method based on 25-minute stretches of focused work broken by five-minute breaks. You can use the technique located in the Self-Help page."},
                    {"id": "nested4", "title": "What is the feynman technique? How can I use it on the website?", "content": "The feynman technique is a four-step process for understanding any topic. It rejects automated recall in favor of true comprehension gained through selection, research, writing, explaining, and refining. You can find it located in the self-help page."},
                    {"id": "nested5", "title": "What is white noise? How can white noise help me while using this website?", "content": "White noise is a consistent and uniform sound that contains equal power across all audible frequencies. It can help you by masking background noise, improving focus and concentration,  and having a consistent sound environment."},
                    {"id": "nested6", "title": "Where can I go to contact support if any of the issues listed in the page aren't available?", "content": "You can visit the Support page in the navigation bar and list your issues there."}
                ],
            },
            {
                "id": "section2",
                "title": "Mental Health",
                "content": "",
                "nested_items": [
                    {"id": "nested8", "title": "What is the relationship between mental health and productivity?", "content": "The state of your mental health and how productive you are, have a very interconnected relationship but, many people choose to ignore this relationship. Mental health consists of many things such as stress, anxiety, and depression. Typically, someone who has any of these challenges will experience lower levels of engagement, creativity and problem solving. Proempo looks keep a positive relationship between these two factors of life."},
                    {"id": "nested9", "title": "How will Proempo help me manage my stress and anxiety?", "content": "As students, here at Proempo, we have a lot of empathy towards people struggling to control their thoughts and are very stressed about deadlines. Organizing your life is a great way to get started with handling your stress and/or anxiety. By keeping all your activities, schoolwork, or just general notes and reminders in one centrally located place that is easily accessible. Having this will layout how much time you have to do these tasks. You will be at ease seeing that your tasks are completed. Proempo also offers a journaling section to help with anxiety delt in your daily life."},
                    {"id": "nested10", "title": "What is the point of journaling?", "content": "Journalling is a great activity to help yourself. While journaling there are no outside factors to worry about except “Me, myself and I”. This is a safe space where you can heave all your pent-up thoughts and feelings onto a page. As time goes on you will have many journals telling you how you felt during a particular day and the reason that day followed that outcome. Looking back at these journals will show you how much you have developed as a person and learn from your past self."},
                    {"id": "nested11", "title": "What is burnout and what to do if I experience it?", "content": "Burnout is a state of physical and/or emotional exhaustion that can come to effect someone’s identity and sense of feeling accomplished. Steps to help reduce burnout starts with seeking support from family members or colleagues to help you collaborate and cope with what you are feeling. You could go ahead and try an activity or hobby you really enjoy that gets you relaxed or even exercise. The “cure” to burnout is taking a break from either work or school or other factors that might be causing this."},
                    {"id": "nested12", "title": "Where can I go to seek support?", "content": "If in need of serious help or support beyond our services here are some resources to look into: Suicide and Crisis lifeline: 988, Therapy."}
                
                ],
            },
            {
                "id": "section3",
                "title": "Productivity",
                "content": "",
                "nested_items": [
                    {"id": "nested13", "title": "What features does the website offer to enhance productivity?", "content": "The features offered in the website are the pomodoro method, feynman technique, which are both located in the self-help page."},
                    {"id": "nested14", "title": "Can you provide tips for settings and achieving productivity goals?", "content": "Our tips to utilizing this website for setting and achieving goals are creating tasks, using the pomodoro method, creating flashcards, and taking a break to prevent burnout."},
                    {"id": "nested15", "title": "How does time management play a role in productivity? Can your website assist with this?", "content": "Time management plays a crucial role in productivity by helping individuals prioritize tasks, allocate time efficiently, and minimize distractions. Effective time management enables better organization and allows individuals to accomplish more in less time, leading to increased productivity. Our website can offer users with creating a task withing the tasks page, using the pomodoro method to set a timer along with completing the tasks created from the task page, creating flashcards in the self-help page, etc. Please check the self-help page if you want to enhance your productivity."},
                    {"id": "nested16", "title": "What are some strategies for overcoming procrastination and maintaining focus?", "content": "Our website can list some strategies. Break tasks into smaller steps. Set specific, achievable goals. Use a timer for focused work like the pomodoro method. Minimize distractions with our built-in white noise player. Reward yourself for completing tasks. Create a dedicated workspace. Prioritize tasks based on importance and urgency."},
                    {"id": "nested17", "title": "how can I effectively priortize tasks and projects to optimize my productivity?", "content": "This question is in progress. Come back for future updates."},
                    {"id": "nested18", "title": "How can I track my progress and measure my productivity gains using the website?", "content": "You can track progress in the website with the provided graphs and charts to measure your current productivity progress."},
                ],
            },
        
        ]
        FAQtitle = "Frequently Asked Questions"
        subtitle = "If you have other questions, please check out the other sections below."
    return render_template("FAQ.html", user=current_user, accordion_items=accordion_items, FAQtitle=FAQtitle, subtitle=subtitle)



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
        due_date_str = request.form.get('dueDate')  # Gets the due date string
        due_time_str = request.form.get('dueTime')  # Gets due time

        if len(task_data) < 1:
            flash('You must enter a task!', category='error')
        elif due_time_str and not due_date_str:
            flash('You cannot have a due time without choosing a due date!', category='error')
        else:
            due_date = None  # Default to None if no due date is provided
            due_time = None
            if due_date_str:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

            if due_time_str:
                due_time = datetime.strptime(due_time_str, '%H:%M').time()

            new_task = Task(
                data=task_data,
                due_date=due_date,
                due_time=due_time,
                user_id=current_user.id
            )

            db.session.add(new_task)  # Add the task to the database
            db.session.commit()
            flash('Task added!', category='success')

    selected_sort = request.args.get('sort_method', 'default')

    user_id = current_user.id

    if selected_sort == 'due_date':
        tasks = Task.query.filter(Task.user_id == user_id).order_by(Task.due_date, Task.due_time)
    elif selected_sort == 'data':
        tasks = Task.query.filter(Task.user_id == user_id).order_by(func.lower(Task.data))
    elif selected_sort == 'newest':
        tasks = Task.query.filter(Task.user_id == user_id).order_by(Task.date.desc())
    elif selected_sort == 'oldest':
        tasks = Task.query.filter(Task.user_id == user_id).order_by(Task.date)
    else:
        tasks = Task.query.filter(Task.user_id == user_id).order_by(text(current_user.defaultsort))


    return render_template('tasks.html', user=current_user, tasks=tasks, selected_sort=selected_sort)


@views.route('/archivedtasks')
@login_required
def archivedtasks():
    archivedtasks = ArchivedTask.query.filter_by(user_id=current_user.id).order_by(ArchivedTask.date).all()
    return render_template('archivedtasks.html', archivedtasks=archivedtasks, user=current_user)
    


@views.route('/reports')
@login_required
def reports():
    #code for the first graph on page
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6) 
    finished_tasks_data = (
        db.session.query(
            func.strftime('%Y-%m-%d', FinishedTask.date).label('date'),
            func.count(FinishedTask.id).label('finished_count')
        )
        .filter(FinishedTask.user_id == current_user.id)
        .filter(FinishedTask.date >= start_date)
        .filter(FinishedTask.date <= end_date)
        .group_by(func.strftime('%Y-%m-%d', FinishedTask.date))
        .all()
    )
    archived_tasks_data = (
        db.session.query(
            func.strftime('%Y-%m-%d', ArchivedTask.date).label('date'),
            func.count(ArchivedTask.id).label('finished_count')
        )
        .filter(ArchivedTask.user_id == current_user.id)
        .filter(ArchivedTask.date >= start_date)
        .filter(ArchivedTask.date <= end_date)
        .group_by(func.strftime('%Y-%m-%d', ArchivedTask.date))
        .all()
    )
    data_dict = {}
    current_day = start_date
    while current_day <= end_date:
        formatted_date = current_day.strftime('%Y-%m-%d')
        data_dict[formatted_date] = 0  # Initialize all days with zero completed tasks
        current_day += timedelta(days=1)

    for row in finished_tasks_data:
        date_str = row.date
        data_dict[date_str] = row.finished_count

    for row in archived_tasks_data:
        date_str = row.date
        data_dict[date_str] += row.finished_count


    finished_tasks_list = [{'date': date, 'finished_count': count} for date, count in data_dict.items()]
    finished_tasks_json = json.dumps(finished_tasks_list)

    # Query to find the most popular day-rating
    most_popular_day_rating = (
        db.session.query(Journal.day_rating, func.count().label('count'))
        .filter(Journal.user_id == current_user.id)
        .group_by(Journal.day_rating)
        .order_by(func.count().desc())
        .limit(1)
        .first()
    )

    most_popular_rating = most_popular_day_rating[0] if most_popular_day_rating else "No data available"
    # !!!!! need to handle what happens when there is a tie




    # Code for the second visualization
    goals_count = Goal.query.filter(
        and_(Goal.user_id == current_user.id, Goal.status == "C")
    ).count()

    latest_completed_goals = Goal.query.filter(
        and_(Goal.user_id == current_user.id, Goal.status == "C")
    ).order_by(Goal.date.desc()).limit(3).all()

    day_ratings = Journal.query.filter_by(user_id=current_user.id).with_entities(Journal.date, Journal.day_rating).all()

    # Map day ratings to numerical values
    converted_ratings = {'horrible': 1, 'bad': 2, 'good': 3, 'excellent': 4}
    day_rating_data = [{'date': str(date), 'rating': converted_ratings.get(rating.lower(), 0)} for date, rating in day_ratings]

    day_rating_json = json.dumps(day_rating_data)
    print(day_rating_json)

    if goals_count > 0:
        return render_template("reports.html", user=current_user, finished_tasks=finished_tasks_json, goals_count=goals_count, latest_completed_goals=latest_completed_goals, most_popular_rating=most_popular_rating, day_rating_json=day_rating_json)
    else:
        return render_template("reports.html", user=current_user, finished_tasks=finished_tasks_json, goals_count=goals_count, no_goals_message="It appears as if you have not set any goals. <a href=/goals>Begin setting goals.</a>", most_popular_rating=most_popular_rating, day_rating_json=day_rating_json)


@views.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    selected_entry = None  #Initialize selected_entry to None

    today = datetime.now().date()
    entry_for_today = Journal.query.filter(Journal.date == today, Journal.user_id == current_user.id).first()
    if entry_for_today:
        selected_entry = entry_for_today


    if request.method == 'POST':
        if is_entry_exists_for_today():
            flash('Entry already exists for today. Cannot check-in again today.', category='error')
        else:

            #Handle form submission
            date = datetime.now().date()
            dear_journal_content = request.form.get('dear_journal_content')
            grateful_contents = [request.form.get('grateful1'), request.form.get('grateful2'), request.form.get('grateful3')]
            day_rating = request.form.get('day_rating')

            

            #Create a new journal entry
            journal_entry = Journal(
                date=date,
                user_id=current_user.id,
                dear_journal_content=dear_journal_content,
                grateful_content=','.join(grateful_contents),
                day_rating=day_rating
            )
            
            db.session.add(journal_entry)
            db.session.commit()
            
            list = ["suicide", "murder", "kill", "hurt"]
            if any(word in dear_journal_content for word in list):
                db.session.commit()
                flash('Your journal contained concerning words. What is hurting you?', category='error')
                flash('If you are feeling unwell, please dont''t heisitate to contact 988 hotline.', category='error')
            elif any(word in grateful_contents for word in list):
                db.session.commit()
                flash('Your journal contained concerning words. What is hurting you?', category='error')
                flash('If you are feeling unwell, please dont''t heisitate to contact 988 hotline.', category='error')
            return redirect(url_for('views.journal'))
    elif request.method == 'GET':
        previous_entries = Journal.query.filter(Journal.user_id == current_user.id).all()

        previous_entry_id = request.args.get('previous_entry')

        if previous_entry_id:
            selected_entry = Journal.query.get(previous_entry_id)
    date = (datetime.now().date())
    
    return render_template('journal.html', user=current_user, previous_entries=previous_entries, selected_entry=selected_entry, date=date)
'''
@views.route('/scanJournal', methods=['POST'])
@login_required
def scan_Journal():
    journal_entry = Journal.query.filter(Journal.date == today, Journal.user_id == current_user.id).first()
    list = ["suicide", "murder", "kill", "hurt"]
    if is_entry_exists_for_today():
        if any(word in journal_entry for word in list):
            db.session.commit()
            return flash('Your journal contained concerning words. What is hurting you?', category='error')
    return jsonify({})
'''
def is_entry_exists_for_today():
    today = date.today()

    entry_for_today = Journal.query.filter(Journal.date == today, Journal.user_id == current_user.id).first()

    return entry_for_today is not None


@views.route('/delete-task', methods=['POST'])
def delete_task():  
    task_data = json.loads(request.data)
    task_id = task_data['taskId']

    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        # Create a archived with the same data and due date as the original task
        archivedtask = ArchivedTask(data=task.data, user_id=current_user.id, due_date=task.due_date, due_time=task.due_time, date=task.date, was_completed=0)

        # Add and commit changes to the database
        db.session.add(archivedtask)
        db.session.delete(task)
        db.session.commit()

    return jsonify({})

@views.route('/delete-finished-task', methods=['POST'])
def delete_finished_task():  
    task_data = json.loads(request.data)
    finished_task_id = task_data['finishedTaskId']

    finished_task = FinishedTask.query.get(finished_task_id)

    if finished_task and finished_task.user_id == current_user.id:
        # Create a Task with the same data and due date as the FinishedTask
        archivedtask = ArchivedTask(data=finished_task.data, user_id=current_user.id, due_date=finished_task.due_date, due_time=finished_task.due_time, date=finished_task.date, was_completed=1)

        # Add and commit changes to the database
        db.session.add(archivedtask)
        db.session.delete(finished_task)
        db.session.commit()

    return jsonify({})

@views.route('/delete-archived-task', methods=['POST'])
def delete_archivedtask():  
    archivedtask_data = json.loads(request.data)
    archivedTaskId = archivedtask_data['archivedTaskId']
    archivedtask = ArchivedTask.query.get(archivedTaskId)

    if archivedtask and archivedtask.user_id == current_user.id:
        db.session.delete(archivedtask)
        db.session.commit()

    return jsonify({})


@views.route('/mark-task', methods=['POST'])
@login_required
def mark_task():
    task_data = json.loads(request.data)
    task_id = task_data['taskId']

    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        # Create a FinishedTask with the same data and due date as the original task
        finished_task = FinishedTask(data=task.data, user_id=current_user.id, due_date=task.due_date, due_time=task.due_time, date=task.date)

        # Add and commit changes to the database
        db.session.add(finished_task)
        db.session.delete(task)
        db.session.commit()

    return jsonify({})

@views.route('/star-task', methods=['POST'])
@login_required
def star_task():
    task_data = json.loads(request.data)
    task_id = task_data['taskId']

    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        # Toggle the starred status
        task.starred = 1 if task.starred != 1 else 0
        db.session.commit()

    return jsonify({})

@views.route('/unmark-task', methods=['POST'])
@login_required
def unmark_task():
    task_data = json.loads(request.data)
    finished_task_id = task_data['finishedTaskId']

    finished_task = FinishedTask.query.get(finished_task_id)

    if finished_task and finished_task.user_id == current_user.id:
        # Create a Task with the same data and due date as the FinishedTask
        task = Task(data=finished_task.data, user_id=current_user.id, due_date=finished_task.due_date, due_time=finished_task.due_time, date=finished_task.date)

        # Add and commit changes to the database
        db.session.add(task)
        db.session.delete(finished_task)
        db.session.commit()

    return jsonify({})


@views.route('/return-task', methods=['POST'])
@login_required
def return_task():
    task_data = json.loads(request.data)
    archived_task_id = task_data['archivedTaskId']

    archived_task = ArchivedTask.query.get(archived_task_id)

    if archived_task and archived_task.user_id == current_user.id and archived_task.was_completed == 0:
        # Create a Task with the same data and due date as the FinishedTask
        task = Task(data=archived_task.data, user_id=current_user.id, due_date=archived_task.due_date, due_time=archived_task.due_time, date=archived_task.date)

        # Add and commit changes to the database
        db.session.add(task)
        db.session.delete(archived_task)
        db.session.commit()

    elif archived_task and archived_task.user_id == current_user.id and archived_task.was_completed == 1:
        finished_task = FinishedTask(data=archived_task.data, user_id=current_user.id, due_date=archived_task.due_date, due_time=archived_task.due_time, date=archived_task.date)

        # Add and commit changes to the database
        db.session.add(finished_task)
        db.session.delete(archived_task)
        db.session.commit()


    return jsonify({})

'''
@views.route('/archive-task', methods=['POST'])
@login_required
def archive_task():
    task_data = json.loads(request.data)
    task_id = task_data['taskId']

    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        # Create an ArchivedTask with the same data, date, and due date as the original task
        archivedtask = ArchivedTask(data=task.data, user_id=current_user.id, due_date=task.due_date, date=task.date)

        # Delete the original task
        db.session.delete(task)
        db.session.commit()

    return jsonify({})
'''
@views.route('/About')
@login_required
def about():
    return render_template("About.html", user=current_user)

@views.route('/settings')
@login_required
def setting():
    
    if current_user.language == "ro":
        selectLanguage = "Selectați limba preferată:"
        title = "Setări"
        save = "Salvează "
        Categories = "Categorii"
        General = "General"
        Accessibility = "Accesibilitate"
        changeuser = "Schimbă Utilizator"
        username = "Utilizator:"
        changepass = "Schimbare Parolă"
        currentpass = "Parolă Curentă"
        newpass = "Parolă Nouă"
        confirmnewpass = "Confirmare Parolă Nouă"
        hidefeatures = "Ascundeți Caracteristici"
        selfhelp = "Ajoutor Personal"
        tasks = "Sarcini"
        dailycheckin = "Verificare Zilnică"
        reports = "Rapoarte"
        language = "Limba"
        oldesttonewest = "Cel mai vechi la cel mai nou"
        newesttooldest = "Cel mai nou la cel mai vechi"
        duedate = "Data scadentă"
        alphabetically = "Alfabetic"
        defaultsort = "Sortare Implicită"
        taskpage = "Pagina de Sarcini"
        starredAtTop = "Afișați Sarcinile Cu Stea În Partea De Sus"
        makeAllButtonsPurple = "Faceți Toate Butoanele Violet"
        player = "Zgomot Alb"
    else:
        selectLanguage = "Select your preferred language:"
        title = "Settings"
        save = "Save"
        Categories = "Categories"
        General = "General"
        Accessibility = "Accessibility"
        changeuser = "Change Username"
        username = "Username:"
        changepass = "Change Password"
        currentpass = "Current Password"
        newpass = "New Password"
        confirmnewpass = "Confirm New Password"
        hidefeatures = "Hide Features"
        selfhelp = "Self Help"
        tasks = "Tasks"
        dailycheckin = "Daily Check-In"
        reports = "Reports"
        language = "Language"
        oldesttonewest = "Oldest to Newest"
        newesttooldest = "Newest to Oldest"
        duedate = "Due Date"
        alphabetically = "Alphabetically"
        defaultsort = "Default Sort"
        taskpage = "Task Page"
        starredAtTop = "Show Starred Tasks at Top"
        makeAllButtonsPurple = "Make All Buttons Purple"
        player = "Noise Player"
    return render_template("settings.html",user=current_user, 
                           selectLanguage=selectLanguage, title=title, save=save, Categories=Categories, General=General, Accessibility=Accessibility,
                            changepass=changepass, currentpass=currentpass, newpass=newpass, confirmnewpass=confirmnewpass, 
                            selfhelp=selfhelp, tasks=tasks, dailycheckin=dailycheckin, reports=reports, hidefeatures=hidefeatures,
                            language=language, changeuser=changeuser, username=username, oldesttonewest=oldesttonewest, 
                            newesttooldest=newesttooldest, duedate=duedate, alphabetically=alphabetically, taskpage=taskpage, defaultsort=defaultsort, 
                            starredAtTop=starredAtTop, makeAllButtonsPurple=makeAllButtonsPurple, player=player)


@views.route('/update_starred_at_top', methods=['POST'])
@login_required
def update_starred_at_top():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.starred_at_top = new_value
    db.session.commit()

@views.route('/update_make_all_buttons_purple', methods=['POST'])
@login_required
def update_make_all_buttons_purple():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.make_all_buttons_purple = new_value
    db.session.commit()

@views.route('/update_hide_self_help', methods=['POST'])
@login_required
def update_hide_self_help():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_self_help = new_value
    db.session.commit()

@views.route('/update_hide_player', methods=['POST'])
@login_required
def update_hide_player():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_player = new_value
    db.session.commit()

@views.route('/update_hide_tasks', methods=['POST'])
@login_required
def update_hide_tasks():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_tasks = new_value
    db.session.commit()


@views.route('/update_hide_journal', methods=['POST'])
@login_required
def update_hide_journal():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_journal = new_value
    db.session.commit()


@views.route('/update_hide_reports', methods=['POST'])
@login_required
def update_hide_reports():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_reports = new_value
    db.session.commit()


@views.route('/update_language', methods=['POST'])
@login_required
def update_language():
    user = current_user
    data = request.get_json()
    new_language = data.get('language')
    user.language = new_language
    db.session.commit()

@views.route('/update_defaultsort', methods=['POST'])
@login_required
def update_defaultsort():
    user = current_user
    data = request.get_json()
    new_defaultsort = data.get('defaultsort')
    user.defaultsort = new_defaultsort
    db.session.commit()


@views.route('/General')
@login_required
def general():


    return render_template("General.html", user=current_user)

@views.route('/Accessibility')
@login_required
def accessibility():
    return render_template("Accessibility.html", user=current_user)


@views.route('/Support', methods=['GET'])
@login_required
def support():
    support = Support.query.all()
    return render_template("Support.html", user=current_user, support=support)

@views.route('/submit_support', methods=['GET','POST'])
def submit_support_form():

    support_entries = []

    if request.method == 'POST':
        try:
            # Get form data
            new_title = request.form['issue_title']
            new_email = request.form['email']
            new_description = request.form['description']
            
            new_form= Support(user_id=current_user.id,issue_title=new_title, email=new_email,description=new_description)
            
            db.session.add(new_form)
            db.session.commit()
            
            return render_template('/thank_you.html', user=current_user)
        except Exception as e:
            print("An error occurred while saving the support submission:", e)
            # Handle the error, log it, or take appropriate action
            flash('Failed to submit the support request', category='error')

    return render_template("Support.html", support_entries=support_entries, user=current_user)




@views.route('/ViewFlashcards', methods=["GET", "POST"])
@login_required
def show_flashcard():
    #gets all the cards from the selected user
    lesson_alias = aliased(Lesson)
    user_flashcards = (Card.query.join(lesson_alias).filter(lesson_alias.user_id == current_user.id))

    selected_lesson_id=request.args.get("lesson")
#gets the leasson associated with the card
    if request.method == 'POST':
        selected_lesson_id = request.form.get('lesson')
        if selected_lesson_id and selected_lesson_id != "all":
             user_flashcards=user_flashcards.filter(Card.lesson_id == selected_lesson_id)
#lists out all the cards
    user_flashcards=user_flashcards.all()
#filters all the available lessons by the user
    all_lessons=Lesson.query.filter_by(user_id=current_user.id)
    return render_template("viewFlashcards.html", user=current_user, cards=user_flashcards, all_lessons=all_lessons, select_lesson=selected_lesson_id)


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

@views.route('/DeleteFlashcard/<int:flashcard_id>', methods=["POST"])
@login_required
def delete_flashcard(flashcard_id):

    flashcard=Card.query.get(flashcard_id)

    db.session.delete(flashcard)
    db.session.commit()

    return redirect("/ViewFlashcards")


@views.route('/ViewFlashcards/<int:flashcard_id>')
@login_required
def get_flashcard(flashcard_id):

    flashcard_id=request.view_args.get('flashcard_id')

    if flashcard_id is None:
        return "Invalid request"

    flashcard=Card.query.get(flashcard_id)

    if not flashcard:
        print('Flashcard not found')
        return redirect('/ViewFlashcards')
    
    return render_template("showFlashcard.html", card=flashcard, user=current_user)



@views.route('/EditFlashcard/<int:flashcard_id>', methods=["GET", "POST"])
@login_required
def edit_flashcard(flashcard_id):

    flashcard = Card.query.get(flashcard_id)

    if flashcard is None:
        flash("Flashcard not found", "error")
        return redirect('/ViewFlashcards')

    if request.method == "POST":
        #get the new values and store them
        lesson_id = request.form.get("lesson")
        question = request.form.get("question")
        answer = request.form.get("answer")

        #new flashcard values assigned 
        flashcard.lesson_id = lesson_id
        flashcard.question = question
        flashcard.answer = answer

        db.session.commit()
        return redirect('/ViewFlashcards/' + str(flashcard_id))
    
    lessons = Lesson.query.filter_by(user_id=current_user.id).all()
    return render_template("editFlashcards.html", card=flashcard, lessons=lessons, user=current_user)

@views.route('/clear-all-completed-tasks', methods=['POST'])
@login_required
def clear_all_completed_tasks():
    completed_tasks = FinishedTask.query.filter_by(user_id=current_user.id).all()

    for task in completed_tasks:
        archived_task = ArchivedTask(
            data=task.data,
            user_id=current_user.id,
            due_date=task.due_date,
            due_time=task.due_time,
            date=task.date,
            was_completed=1
        )

        db.session.add(archived_task)
        db.session.delete(task)

    db.session.commit()

    return jsonify({})




@views.route('/player')
def player():
    playIcon='<i class="fas fa-play"></i>'
    pauseIcon='<i class="fas fa-pause"></i>'

    return render_template('player.html', user=current_user, playIcon=playIcon, pauseIcon=pauseIcon)









@views.route('/goals')
@login_required
def goals():
    user_id = current_user.id
    previous_goals = Goal.query.filter_by(user_id=user_id).all()
    if previous_goals is None:
        previous_goals = [] 

    return render_template('goals.html', user=current_user, previous_goals=previous_goals)



@views.route('/save_goal', methods=['POST'])
def save_goal():
    try:
        data = request.json
        user_id = current_user.id
        specific = data.get('specific')
        measurable = data.get('measurable')
        achievable = data.get('achievable')
        relevant = data.get('relevant')
        timely = data.get('timely')
        status = data.get('status')

        goal_entry = Goal(
            user_id=user_id,
            specific=specific,
            measurable=measurable,
            achievable=achievable,
            relevant=relevant,
            timely=timely,
            status=status
        )

        db.session.add(goal_entry)
        db.session.commit()

        return jsonify({'message': 'Goal entry saved successfully'})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to save goal entry'}), 500


@views.route('/complete_goal/<int:goal_id>', methods=['PUT'])
def complete_goal(goal_id):
    try:
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()

        if goal:
            goal.status = "C"
            db.session.commit()
            return jsonify({'message': 'Goal marked as completed successfully'})
        else:
            return jsonify({'message': 'Goal not found or does not belong to the current user'}), 404
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to mark goal as completed'}), 500
    


@views.route('/fetch_goals', methods=['GET'])
@login_required
def fetch_goals():
    user_id = current_user.id
    goals = Goal.query.filter_by(user_id=user_id).all()

    # Serialize the goals to JSON
    serialized_goals = []
    for goal in goals:
        serialized_goal = {
            'id': goal.id,
            'specific': goal.specific,
            'measurable': goal.measurable,
            'achievable': goal.achievable,
            'relevant': goal.relevant,
            'timely': goal.timely,
            'status': goal.status
        }
        serialized_goals.append(serialized_goal)

    return jsonify({'goals': serialized_goals})


def get_iso_year_week(date):
    year, week, _ = date.isocalendar()
    return year, week

@views.route('/accomplishments', methods=['GET', 'POST'])
@login_required
def pride():

    current_year, current_week_number = get_iso_year_week(today)

    recent_accomplishments = Pride.query.filter(
        Pride.user_id == current_user.id,
        Pride.year == current_year,
        Pride.week_number == current_week_number,
        Pride.status == False
    ).all()


    for accomplishment in recent_accomplishments:
        #Update the status once it lands outside the current week
        if current_week_number - accomplishment.week_number > 0:
            accomplishment.status = True 
    
    if request.method == 'POST':
        #max entries for the week check
        maximum_entries = 5
        entries_for_week = len(recent_accomplishments)

        if entries_for_week >= maximum_entries:
            flash("You have entered the maximum number of entries. Only 5 per week")
        else:
            new_moment = request.form.get('moment')
            pride_entry = Pride(
            user_id=current_user.id,
            moment=new_moment,
            year=current_year,
            week_number=current_week_number,
            status=False,
        )

            db.session.add(pride_entry)
            db.session.commit()
            
    recent_accomplishments = Pride.query.filter(
        Pride.user_id == current_user.id,
        Pride.year == current_year,
        Pride.week_number == current_week_number,
        Pride.status == False
    ).all()
    
    return render_template('pride.html', recent_accomplishments=recent_accomplishments, user=current_user)
    

@views.route('/DeletePride/<int:pride_id>', methods=["POST"])
@login_required
def delete_pride(pride_id):

    moment=Pride.query.get(pride_id)
    db.session.delete(moment)
    db.session.commit()

    return redirect("/accomplishments")
    
@views.route('/past-accomplishments', methods=['GET', 'POST'])
@login_required
def past_week_accomplishments():

    error_message = ""

    past_accomplishments = Pride.query.filter(
        Pride.user_id == current_user.id,
        Pride.status == True
    ).order_by(Pride.date.desc()).limit(5).all()

    if not past_accomplishments:
        error_message = "You havent listed any accomplishments in the past week"

    return render_template('pastAccomplishments.html', past_accomplishments=past_accomplishments,error_message=error_message, user=current_user)