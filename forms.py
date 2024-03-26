from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Powtórz hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')
    
class LogoutForm(FlaskForm):
    submit = SubmitField('Wyloguj')

class AnswerForm(FlaskForm):
    answer = StringField('Odpowiedź', validators=[DataRequired()])

class QuestionForm(FlaskForm):
    question_content = StringField('Treść pytania', validators=[DataRequired()])
    answers = FieldList(FormField(AnswerForm), min_entries=4, max_entries=4)
    submit = SubmitField('Dodaj pytanie')

