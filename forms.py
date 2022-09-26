
from tokenize import String
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, email_validator, Length
from wtforms import ValidationError
import email_validator

from model import Users

class LoginForm(FlaskForm):
    username    = StringField('Username',validators=[DataRequired()])
    password    = PasswordField('Password',validators=[DataRequired()])
    submit      = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email               = StringField('Email',validators=[DataRequired(),Email()])
    username            = StringField('Username', validators=[DataRequired()])
    password            = PasswordField('Password', validators=[DataRequired(),EqualTo('password_confirm',message="Passwords don't match")])
    password_confirm    = PasswordField('Confirm Password',validators=[DataRequired()])
    state               = StringField('State', validators=[Length(max=2)])
    submit              = SubmitField('Register')

    def check_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has already been registered')

    def check_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has already been registered')

class LoanForm(FlaskForm):
    loan_name       = StringField('Loan Name',validators=[DataRequired()])
    current_owed    = StringField('Current Amount Owed', validators=[DataRequired()])
    interest_rate   = StringField('Interest Rate',validators=[DataRequired()])
    min_payment     = StringField('Minimum Payment Amount',validators=[DataRequired()])
    due_date        = StringField('Due Date',validators=[DataRequired()])
    payoff_date     = StringField('Payoff Date',validators=[DataRequired()])
    submit          = SubmitField('Track Loan')

class OtherForm(FlaskForm):
    debt_name       = StringField('Debt Name', validators=[DataRequired()])
    current_owed    = StringField('Current Owed Amount', validators=[DataRequired()])
    interest_rate   = StringField('Interest Rate', validators=[DataRequired()])
    min_payment     = StringField('Minimum Payment Amount')
    due_date        = StringField('Due Date', validators=[DataRequired()])
    payoff_date     = StringField('Payoff Date (if applicable)', validators=[DataRequired()])
    submit          = SubmitField('Track Debt')

class CCForm(FlaskForm):
    card_name       = StringField('CreditCard Name', validators=[DataRequired()])
    card_max        = StringField('Card Max Amount', validators=[DataRequired()])
    current_owed    = StringField('Current Owed Amount', validators=[DataRequired()])
    interest_rate   = StringField('Card Interest Rate', validators=[DataRequired()])
    due_date        = StringField('Due Date', validators=[DataRequired()])
    min_calc        = StringField('Minimum Calculation Amount')
    submit          = SubmitField('Track CreditCard')

class DelForm(FlaskForm):
    id      = IntegerField('ID number of debt to remove: ')
    submit  = SubmitField("Remove Debt")

class UpdateForm(FlaskForm):
    id      = IntegerField('ID of debt to update: ')
    submit  = SubmitField("Update Debt")
    