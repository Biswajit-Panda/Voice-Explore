# mongodb+srv://kanha:Tw9RVjiJ7LAmqj3@voice-explore-login.qg20k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority

from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'voiceTravel'
app.config['MONGO_URI'] = 'mongodb+srv://kanha:12345@voice-explore-login.qg20k.mongodb.net/voiceTravel?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
    if session['username'] != None:
        return redirect(url_for('home'))

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():

    users = mongo.db.users
    login_user = users.find_one({'email': request.form['email']})

    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['email']
            return redirect(url_for('home'))
    return render_template('index.html', invalid_data='Invalide Email Id or Password')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email':request.form['email']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'email':request.form['email'], 'name':request.form['name'], 'password': hashpass})
            session['username'] = request.form['email']
            return render_template('profile.html')
        return render_template('register.html', invalid_data='Email Id already present. Choose another one.')
    return render_template('register.html')

@app.route('/profile', methods=['POST','GET'])
def profile():
    if request.method == 'POST':
        relatives = mongo.db.relatives
        relatives.insert({'user': session['username'], 'p1_email':request.form['email1'], 'p1_name':request.form['person1'], 'p1_PhoneNo': request.form['phone1'], 'p2_email':request.form['email2'], 'p2_name':request.form['person2'], 'p2_PhoneNo': request.form['phone2'], 'p3_email':request.form['email3'], 'p3_name':request.form['person3'], 'p3_PhoneNo': request.form['phone3']})

        return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html', result = {})

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect(url_for('index'))

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      print(type(result))
      print(result)
      return render_template("home.html",result = result)

if __name__ == '__main__':
    app.secret_key = 'kanha'
    app.run(debug=True)