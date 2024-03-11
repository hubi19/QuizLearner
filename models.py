from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email

def create_model(db):

    class Question(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String(255), nullable=False)
        answers = db.relationship('Answer', backref='question', lazy=True)

    class Answer(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String(255), nullable=False)
        is_correct = db.Column(db.Boolean, default=False)
        question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    class QuizForm(FlaskForm):
        answer = RadioField('Answer', choices=[], validators=[DataRequired()])
        submit = SubmitField('Submit')

    return Question, Answer, QuizForm