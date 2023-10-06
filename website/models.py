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
    due_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class FinishedTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=get_current_time_in_et)
    due_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=get_current_time_in_et)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dear_journal_content = db.Column(db.String(1000)) 
    grateful_content = db.Column(db.String(500))  
    day_rating = db.Column(db.String(20))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    tasks = db.relationship('Task')
    finished_tasks = db.relationship('FinishedTask')
    journals = db.relationship('Journal')
    lessons = db.relationship('Lesson')

class Card(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(1000))
    answer = db.Column(db.String(100000))
    timestamp = db.Column(db.DateTime(timezone=True), index=True, default=get_current_time_in_et)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    lessons = db.relationship('Lesson', back_populates='cards')

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cards = db.relationship('Card')
    
