#server py file

from os import environ
from flask import Flask, render_template, render_template, url_for, redirect, request, flash, abort

from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt

from model import Loans, Users, db, database_connection

from forms import LoanForm, OtherForm, CCForm, DelForm, UpdateForm, LoginForm, RegistrationForm




app = Flask(__name__, template_folder='pages')

app.secret_key = environ["SECRET_KEY_FTW"]

migrate = Migrate(app,db)


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'




@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out")
    return redirect(url_for('home'))

@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)

    return render_template('login.html',form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Users(email      =form.email.data,
                    username    =form.username.data,
                    password    =form.password.data,
                    state       =form.state.data)

        db.session.add(user)
        db.session.commit()
        flash("Thank you for registering.")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/overview', methods=['GET','POST'])
def overview():
    loan_form = LoanForm()

    if loan_form.validate_on_submit():
        loan = Loans(loan_name      =loan_form.loan_name.data,
                    current_owed    =loan_form.current_owed.data,
                    interest_rate   =loan_form.interest_rate.data,
                    min_payment     =loan_form.min_payment.data,
                    due_date        =loan_form.due_date.data,
                    payoff_date     =loan_form.payoff_date.data)

        db.session.add(loan)
        db.session.commit()
        flash("Loan has been added to your list.")
        return redirect(url_for('overview'))

    return render_template('overview.html', loan_form=loan_form)


if __name__ == '__main__':
    database_connection(app)
    app.run(debug=True, port=8000)


