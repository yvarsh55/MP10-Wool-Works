from flask import Flask, render_template,flash,redirect,url_for,request,json
from form import RegistrationForm,LoginForm,Predictform

# just for now we are adding sqlalchemy here in our main file but later we ill separtate it in the future

from flask_sqlalchemy  import SQLAlchemy 
from datetime import datetime




#inititialize
app=Flask(__name__)
app.config['SECRET_KEY']='07237226efedd71266068bbebefe5618'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)


#table creation 
class User(db.Model):
   id=db.Column(db.Integer, primary_key=True)
   username=db.Column(db.String(20),unique=True,nullable=False)
   email=db.Column(db.String(120),unique=True,nullable=False)
   image_file=db.Column(db.String(120),nullable=False, default='default.jpg')
   password=db.Column(db.String(60),nullable=False)
   post=db.relationship('Post',backref='author',lazy=True)

   #magic method(it is used to know hwo our object is printed when we print it)

   def __repr__(self):
      return f"user('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):

   id=db.Column(db.Integer, primary_key=True)
   title=db.Column(db.String(100),nullable=False)
   date_posted=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
   content= db.Column(db.Text,nullable=False)
   user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

   def __repr__(self):
      return f"Post('{self.title}','{self.date_posted}')"


    

#create our route method where localhost will call
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
   form=RegistrationForm()
   if form.validate_on_submit():
      flash(f'Account successfully created for {form.username.data}!','success')
      return redirect(url_for('index'))
   return render_template('Register.html',title='register', form=form )

@app.route('/login')
def login():
   form=LoginForm()
   return render_template('login.html',title='login', form=form )


import numpy as np 
import pickle
from flask import request



model=pickle.load(open('trained_model2.pkl','rb'))


import pandas as pd

with open('label_encoders.pkl', 'rb') as encoder_file:
    label_encoders = pickle.load(encoder_file)

# Load the target encoder
with open('target_encoder.pkl', 'rb') as target_encoder_file:
    le_target = pickle.load(target_encoder_file)

# Helper function to safely transform categories
def safe_transform(encoder, value):
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        print(f"Warning: Unseen category '{value}' encountered. Using fallback value.")
        return -1 

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = Predictform(request.form)

    if request.method == 'POST' and form.validate():
        
        fd=form.fiber_diameter.data
        fl=form.fiber_length.data
        cc=form.crimp_Characteristics.data
        st=form.strength.data
        el=form.elasticity.data
        ft=form.fitness.data

        
        cce = safe_transform(label_encoders['Crimp Characteristics'], cc)
        ste = safe_transform(label_encoders['Strength'], st)
        ele = safe_transform(label_encoders['Elasticity'], el)
        fte = safe_transform(label_encoders['Fineness'], ft)

        
        feature_names = ['Fiber Diameter (Microns)', 'Fiber Length (mm)', 
                         'Crimp Characteristics', 'Strength', 'Elasticity', 'Fineness']
        feat_df = pd.DataFrame([[fd, fl, cce, ste, ele, fte]], columns=feature_names)

        
        prediction = model.predict(feat_df)[0]

        # decode the target to return the original label instead of a numeric prediction
        prediction_label = le_target.inverse_transform([prediction])[0]

        return render_template('predictform.html', form=form, prediction=prediction_label)

    return render_template('predictform.html', form=form, prediction=None)




#check if app is our main file or not
if __name__=='__main__':
    # run our name object
    app.run(debug=True)







