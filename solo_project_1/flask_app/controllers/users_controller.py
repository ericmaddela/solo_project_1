from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.place_model import Place
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "username": request.form['username'], 
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['first_name'] = data['first_name']
    session['user_id'] = user_id

    return redirect('/home')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect('/home')


@app.route('/home')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'user_id': session['user_id'],
        'first_name': session['first_name']
    }
    return render_template("home.html", user = data['user_id'] , places = Place.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')