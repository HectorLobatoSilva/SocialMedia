from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import ( DataRequired, ValidationError, Email, Regexp, Length, EqualTo )
from models import User

def name_exist( form, field ):
    if User.select().where( User.username == field.data ).exists():
        raise ValidationError( 'User already exists' )

def email_exists( form, field ):
    if User.select().where( User.email == field.data ).exists():
        raise ValidationError( 'Email already exists' )

class RegisterForm( FlaskForm ):
    username = StringField( 
        'Username', 
        validators = [ 
            DataRequired(), 
            Regexp( r'^[a-zA-Z0-9_]+$' ), 
            name_exist 
        ] )
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            email_exists
        ]
    )

    password2 = PasswordField(
        'Confirm password',
        validators = [
            DataRequired()
        ]
    )

    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length( min = 4 ),
            EqualTo( fieldname = 'password2', message = "Password must coincide" )
        ]
    )

class LoginForm( FlaskForm ):
    email = StringField( 'Email', validators = [ DataRequired(), Email() ] )
    password = PasswordField ( 'Password', validators = [ DataRequired() ] )

class PostsForm ( FlaskForm ):
    content = TextAreaField( "Que piensas", validators = [ DataRequired() ] )