from flask import render_template, redirect, request, flash, session

from flask_app import app
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User

@app.route('/add_recipe_page')
def add_recipe_page():

    #if condition the user is logged in before being able to add a new recipe
    if 'user_id' not in session:
        flash("Might Wanna Log in First Buddy >:(")
        return redirect('/')
    
    return render_template('add_recipe_page.html')

@app.route('/add_recipe', methods=["POST"])
def add_recipe():
    
    #checking if the recipe sumbition is valid
    if not Recipe.recipe_validation(request.form):
        return redirect('/add_recipe_page')
    
    #calling the create class method
    Recipe.create(request.form)

    return redirect('/user_page')

@app.route('/recipe_page/<int:id>')
def recipe_page(id):

    # an if condition to make sure user is logged in before viewing the recipe page
    if 'user_id' not in session:
        flash("Might Wanna Log in First Buddy >:(")
        return redirect('/')
    
    user = User.get_one_by_id(session['user_id'])
    
    recipe = Recipe.get_one_by_id(id)

    return render_template('recipe_page.html',user = user, recipe = recipe )


@app.route('/edit_recipe_page/<int:id>')
def edit_page(id):

    # an if conidtion to make sure the logged in user can only edit their own recipe and not someone else
    if Recipe.get_one_by_id(id).user_id != session['user_id']:
        flash(" Not yours to edit!")
        return redirect('/user_page')

    # an if conidtion to make sure the user is actually logged in
    if 'user_id' not in session:
        flash("Might Wanna Log in First Buddy >:(")
        return redirect('/')
    
    user = User.get_one_by_id(session['user_id'])
    
    recipe = Recipe.get_one_by_id(id)

    return render_template('edit_recipe_page.html', user = user, recipe = recipe )

@app.route('/save_recipe', methods = ["POST"])
def save_recipe():

    # if condition to check if the edit submition of the recipe is valid
    if not Recipe.recipe_validation(request.form):
        return redirect('/add_recipe_page')

    Recipe.save(request.form)

    return redirect('/user_page')

@app.route('/delete_recipe/<int:id>')
def delete_route(id):

    # if condition to make sure the user actually logged in
    if 'user_id' not in session:
        flash("Might Wanna Log in First Buddy >:(")
        return redirect('/')

    # to make sure the user is only able to delete their own recipe and not other's recipe
    if Recipe.get_one_by_id(id).user_id != session['user_id']:
        flash(" Not yours to delete!")
        return redirect('/user_page')
    
    Recipe.delete(id)
    return redirect('/user_page')