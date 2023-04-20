from flask import render_template, redirect, request, flash, session

from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

@app.route('/')
def welcome_page():
    return render_template('index.html')

@app.route('/register', methods = ["POST"])
def register():

    # validating if request form submition
    if not User.validate_registration(request.form):
        # if it doesnt match then boot user back to register route to retry
        return redirect('/')
    
    # if form is valid then create method to send a query into the Database
    User.create(request.form)
    

    # using the given email in the request form to create an User instance to grab the id
    user = User.get_one_by_email(request.form['email'])

    # entering the newly register user id into session so we can route them into the logged in page
    session['user_id'] = user.id

    return redirect('/user_page')

@app.route('/login', methods = ["POST"])
def login():
    # checking if the login info match what we got in the Database
    found_user = User.validate_login(request.form)

    # if match then send the user id into session so they can have access into the logged in page
    if found_user:
        session['user_id'] = found_user.id

        return redirect('/user_page')
    # if it does not match then we redirect them back into the home page to try again
    else:
        return redirect('/')
    
@app.route('/user_page')
def user_page():


    if 'user_id' not in session:
        flash("Might Wanna Log in First Buddy >:(")
        return redirect('/')
    
    user = User.get_one_by_id(session['user_id'])


    recipe_list = Recipe.get_all_recipe()

    # super cool if/elif condition to make sure the page will load even if
    # the get_all_recipe() return nothing or null values due to the DB being empty
    if recipe_list:
        return render_template('user_page.html', user = user, recipe_list = recipe_list)
    
    elif not recipe_list :
        return render_template('user_page.html', user = user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')