from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import DATABASE, BCRYPT
from flask import flash
import re

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, form):

        query = """

                INSERT INTO recipes (user_id, name, description, instruction, under_30, created_at)
                VALUE(%(user_id)s, %(name)s, %(description)s, %(instruction)s, %(under_30)s, %(created_at)s)
        """
        return connectToMySQL(DATABASE).query_db(query,form)
    
    @classmethod
    def save(cls,form):
        
        query = """
                UPDATE recipes
                SET
                name = %(name)s,
                description = %(description)s,
                instruction = %(instruction)s,
                under_30 = %(under_30)s
                WHERE id = %(id)s
        """
        connectToMySQL(DATABASE).query_db(query,form)
    
    @classmethod
    def delete(cls, id):

        data = {
            'id': id
        }

        query = """
                DELETE FROM
                recipes
                WHERE id = %(id)s;
        """
        connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_all_recipe(cls):

        #sending a join query so we can get all of the recipes along with the user first and last name back
        query = """

                SELECT first_name, last_name, recipes.id, recipes.user_id, recipes.name, under_30, description, instruction, recipes.created_at,  recipes.updated_at
                FROM users
                JOIN recipes
                ON users.id = recipes.user_id               
            """
        results = connectToMySQL(DATABASE).query_db(query)

        #taking the result from the query and itterating through each of the row or "recipe" and
        #creating a class intance of it. Then adding abtributes of first and last name to that recipe
        #class intance. Finally, append the recipe class intance into the recipe list
        if results:
            recipe_list = []
            for recipe in results:
                the_recipe = cls(recipe)
                the_recipe.user_first_name = recipe['first_name']
                the_recipe.user_last_name = recipe['last_name']
                recipe_list.append(the_recipe)
            
            return (recipe_list)
        
    @classmethod
    def get_one_by_id(cls,id):

        #same thing as the get all but now we're limiting the query to just the recipe id

        data ={
            "id": id
        }

        query = """

                SELECT * FROM recipes
                LEFT JOIN users
                ON recipes.user_id = users.id
                WHERE recipes.id = %(id)s
        """
        results = connectToMySQL(DATABASE).query_db(query, data)


        if results:
            recipe = cls(results[0])
            recipe.first_name = results[0]['first_name']
            return recipe
        else:
            return False


    # Some classmethods that I was playing around with 
    # @classmethod
    # def get_recipe_of_others(cls, id):
    #     data = {
    #         'id': id
    #         }

    #     query = """

    #             SELECT first_name, last_name, recipes.id, recipes.user_id, recipes.name, under_30, description, instruction, recipes.created_at,  recipes.updated_at
    #             FROM users
    #             JOIN recipes
    #             ON users.id = recipes.user_id               
    #             WHERE users.id != %(id)s

    #         """

    #     results = connectToMySQL(DATABASE).query_db(query,data)


    #     if results:
    #         recipe_list_other = []

    #         for recipe in results:
    #             other_recipe = cls(recipe)
    #             other_recipe.user_first_name = recipe['first_name']
    #             other_recipe.user_last_name = recipe['last_name']
    #             recipe_list_other.append(other_recipe)
            
    #         return (recipe_list_other)
    
    # @classmethod
    # def get_recipe_of_user(cls, id):

    #     data = {
    #         'id': id
    #     }

    #     query = """

    #             SELECT first_name, last_name, recipes.id, recipes.user_id, recipes.name, under_30, description, instruction, recipes.created_at,  recipes.updated_at
    #             FROM users
    #             Left JOIN recipes
    #             ON users.id = recipes.user_id               
    #             WHERE users.id = %(id)s

    #     """

    #     results = connectToMySQL(DATABASE).query_db(query,data)

    #     if results:
    #         recipe_list = []
    #         for recipe in results:
    #             user_recipe = cls(recipe)
    #             user_recipe.user_first_name = recipe['first_name']
    #             user_recipe.user_last_name = recipe['last_name']
    #             recipe_list.append(cls(recipe))
    #         return recipe_list

    @classmethod
    def recipe_validation(cls, form):

        #to validate the recipe submitions

        is_valid = True    

        if len(form['name']) < 1:
            flash('Please give the recipe a name!')
            is_valid = False

        if len(form['description']) < 1:
            flash('Please have a decription of your dish!')
            is_valid = False

        if len(form['instruction']) < 1:
            flash('Please explain how to prepare your dish!')
            is_valid = False

        if len(form['created_at'])< 4:
            flash('When did you come up with this recipe?')
            is_valid = False

        return is_valid
