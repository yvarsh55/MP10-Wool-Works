from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField,SelectField,DecimalField,TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo,NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
 

class Predictform(FlaskForm):
    fiber_diameter=DecimalField('fiber diameter',validators=[DataRequired(), NumberRange(min=5,max=40)])
    fiber_length=DecimalField('fiber length',validators=[DataRequired(),NumberRange(min=50,max=200)])
    crimp_Characteristics=SelectField('Crimp Characteristics', choices=['Tight','Moderate','Looser'], validators=[DataRequired()])
    strength=SelectField('Strength', choices=['Moderate','High','Very High'], validators=[DataRequired()])
    elasticity=SelectField('Elasticity', choices=['High','Less Elastic','Good'], validators=[DataRequired()])
    fitness=SelectField('Fitness', choices=[('Soft and smooth'),('Rougher texture'),'Soft'], validators=[DataRequired()])
    submit=SubmitField('Predict')



class feedback(FlaskForm):
    fname=StringField(validators=[DataRequired()])
    femail=StringField(validators=[DataRequired(),Email()])
    fcomment=TextAreaField(validators=[DataRequired()])