from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import DataRequired, Email
from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ROMH85C34XRGOXJ9OM7OBDV3CZLI41R3'
app.config["SQLALCHEMY_DATABASE_URI"] = r'mssql+pyodbc://@DESKTOP-HTLQBNC\MSSQLSERVER01/users?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_menager = LoginManager(app)
login_menager.login_view = 'login'

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

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/statute')
def statute():
    return render_template('statute.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = YourForm()

    if form.validate():
        email = form.email.data
        password = form.password.data
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
    else: 
        flash('Niepoprawne dane')
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
    return render_template('register.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)