#Database models
import pytz
import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

def get_current_time_in_et():
    eastern_tz = pytz.timezone('US/Eastern')
    current_time = datetime.datetime.now(eastern_tz)
    return current_time

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=get_current_time_in_et)
    due_time = db.Column(db.Time)
    due_date = db.Column(db.Date)
    starred = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class FinishedTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=get_current_time_in_et)
    due_time = db.Column(db.Time)
    due_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ArchivedTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=get_current_time_in_et)
    due_time = db.Column(db.Time)
    due_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    was_completed = db.Column(db.Boolean)

class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) #, default=datetime.date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dear_journal_content = db.Column(db.String(1000)) 
    grateful_content = db.Column(db.String(500))  
    day_rating = db.Column(db.String(20))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    language = db.Column(db.String(2))
    defaultsort = db.Column(db.String(10))
    hide_second_hand = db.Column(db.Boolean)
    make_all_buttons_purple = db.Column(db.Boolean)
    starred_at_top = db.Column(db.Boolean)
    hide_self_help = db.Column(db.Boolean)
    hide_tasks = db.Column(db.Boolean)
    hide_journal = db.Column(db.Boolean)
    hide_reports = db.Column(db.Boolean)
    hide_player = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)
    tasks = db.relationship('Task')
    finished_tasks = db.relationship('FinishedTask')
    archivedtasks = db.relationship('ArchivedTask')
    journals = db.relationship('Journal')
    lessons = db.relationship('Lesson')
    pride = db.relationship('Pride')
    Support = db.relationship('Support')


class Card(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(1000))
    answer = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime(timezone=True), index=True, default=get_current_time_in_et)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    lessons = db.relationship('Lesson', back_populates='cards')

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cards = db.relationship('Card')
    
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    specific = db.Column(db.String(1000)) 
    measurable = db.Column(db.String(1000))
    achievable = db.Column(db.String(1000))
    relevant = db.Column(db.String(1000))
    timely = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=get_current_time_in_et)
    status = db.Column(db.String(1))


class Pride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    moment = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=get_current_time_in_et)
    status = db.Column(db.Boolean, default=False)
    week_number = db.Column(db.Integer)
    year = db.Column(db.Integer)

class Support(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_title = db.Column(db.String(100))
    email = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Feynman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(1000)) 
    description = db.Column(db.String(10000)) 