from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length

from twittor.models.user import User

class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField("Username", validators = [DataRequired()]) # username:方法, "Username":lable
    password = PasswordField("Password", validators = [DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email Address", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Repeat Password", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("Please use different username.")
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("Please use different email address.")

class EditProfileForm(FlaskForm):
    about_me = TextAreaField("About me", validators = [Length(min = 0, max = 120)])
    submit = SubmitField("Save")

class TweetForm(FlaskForm):
    tweet = TextAreaField("Tweet", validators = [DataRequired(), Length(min = 0, max = 140)])
    submit = SubmitField("Tweet")

class EditTweetForm(FlaskForm):
    tweet = TextAreaField("Tweet", validators = [DataRequired(), Length(min = 0, max = 140)])
    submit = SubmitField("Save")

class PasswordResetRequestForm(FlaskForm):
    email = StringField("Email Address", validators = [DataRequired(), Email()])
    submit = SubmitField("Reset Password")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if not user:
            raise ValidationError("You don't have an account for this email address.")

class PasswdRestForm(FlaskForm):
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Password Repeat", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")
