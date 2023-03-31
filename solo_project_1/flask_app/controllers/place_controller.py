from webbrowser import get
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.place_model import Place
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/new_place')
def new_place():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('new_place.html')


@app.route('/add_place', methods=['POST'])
def create_place():
    data = {
        'name' : request.form['name'],
        'city' : request.form['city'],
        'cuisine' : request.form['cuisine'],
        'address' : request.form['address'],
        'days' : request.form['days'],
        'opening_time' : request.form['opening_time'],
        'closing_time' : request.form['closing_time'],
        'user_id' : session['user_id']
    }
    Place.save(data)
    return redirect('/home')

@app.route('/view_place/<int:id>')
def view_place(id):
    if 'user_id' not in session:
        return redirect('/')
        Place.get_one_w_user(request.form)
        print(request.form)
    return render_template('/view_place.html', place_w_posted_by = Place.get_one_w_user(id))

@app.route('/edit_place/<int:id>')
def edit_place(id):
    return render_template("edit_place.html", one_user = Place.get_one_w_user(id))

@app.route('/update', methods=['post'])
def update():
    print(request.form)
    place = Place.update(request.form)
    return redirect('/home')

@app.route('/delete/<int:id>')
def destroy(id):
    Place.delete(id)
    return redirect('/home')
