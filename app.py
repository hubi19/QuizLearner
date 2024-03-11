from flask import Flask, redirect, render_template, request, flash, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import DataRequired, Email
from wtforms import StringField, PasswordField, SubmitField

from quiz_form import QuizForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ROMH85C34XRGOXJ9OM7OBDV3CZLI41R3'
app.config["SQLALCHEMY_DATABASE_URI"] = r'mssql+pyodbc://@DESKTOP-HTLQBNC\MSSQLSERVER01/users?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_menager = LoginManager(app)
login_menager.login_view = 'login'

from models import create_model
Question, Answer, QuizForm =  create_model(db)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(60), nullable=False)

class YourForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

@login_menager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')


def get_next_question():
    current_question_id = 1

    current_question = Question.query.get(current_question_id)

    return current_question

def selected_answer_is_correct(question_id, selected_anser_id):
    selected_answer = Answer.query.get(selected_anser_id)

    return selected_answer_is_correct

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = QuizForm()

    current_question = get_next_question()


    if form.validate_on_submit():
        selected_anser_id = form.answer.data

        if selected_answer_is_correct(current_question.id, selected_anser_id):
            flash("Poprawna odpowiedź")
        else:
            flash("Błędna odpowiedź")
        return redirect(url_for('quiz'))
    return render_template('quiz.html', current_question=current_question, form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/statute')
def statute():
    return render_template('statute.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = YourForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email, password=password).first()        
        if user:
            login_user(user)
            flash("zalogowano")
        else:
            flash("Nieprawidłowe dane logowania")
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = YourForm()

    if request.method == 'POST' and form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Użytkownik o podanym adresie email już istenieje, wybierz inny email!")
        else: 
            user = User(email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Poprawnie zarejestrowano!")
    return render_template('register.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)