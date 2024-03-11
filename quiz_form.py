from flask_wtf import FlaskForm
from wtforms import RadioField

class QuizForm(FlaskForm):
    answer = RadioField('Wybierz prawidłową odpowiedź', choices=[], coerce=int)

