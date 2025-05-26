# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")


class NewsletterForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')
    
class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class QueryForm(FlaskForm):
    title = StringField('Query Title', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Describe Your Query', validators=[DataRequired(), Length(min=10)])
    domain = SelectField('Domain', choices=[
        ('civil', 'Civil Law'),
        ('criminal', 'Criminal Law'),
        ('family', 'Family Law'),
        ('corporate', 'Corporate Law'),
        ('property', 'Property Law'),
        ('cyber crime', 'Cyber Law'),
        ('others', 'Others')
    ], validators=[DataRequired()])
    submit = SubmitField("Post Query")

class ReplyForm(FlaskForm):
    reply_text = TextAreaField('Your Reply', validators=[DataRequired()], render_kw={"placeholder": "Write your reply here..."})
    submit = SubmitField('Post Reply')

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class NewsletterForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')