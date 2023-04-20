from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import DATABASE, BCRYPT
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data ['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, form):
        #using BCRYPT to hash of pasword from request form before querying it into the Database
        pw_hash = BCRYPT.generate_password_hash(form['password'])

        #setting up a dictionary to change 'password' into its hashed value
        data = {
            **form,
            'password': pw_hash
        }

        query = """

                INSERT INTO users(first_name, last_name, email, password)
                VALUE(%(first_name)s,%(last_name)s,%(email)s,%(password)s)
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_one_by_id(cls,id):

        data =  {
            'id': id
        }
        #getting an User intance base on submitted id
        query = 'SELECT * FROM users WHERE id = %(id)s'

        return cls(connectToMySQL(DATABASE).query_db(query,data)[0])
    
    @classmethod
    def get_one_by_email(cls, email):
        #getting an User intance base on submitted email
        data ={
            "email" : email
        }

        query = """

                SELECT * FROM users
                WHERE email = %(email)s
        """

        results = connectToMySQL(DATABASE).query_db(query,data)

        if results:
            return cls(results[0])
        else:
            return False
    
    

    @classmethod
    def validate_registration(cls, form):

        is_valid = True

        if len(form['first_name']) < 2:
            flash('Please enter a First Name')
            is_valid = False

        if len(form['last_name']) < 2:
            flash('Please enter a Last Name')
            is_valid = False

        if len(form['email']) < 1:
            flash('Please enter an Email')
            is_valid = False

        elif not EMAIL_REGEX.match(form['email']):
            flash("Invalid email address!")
            is_valid = False

        elif cls.get_one_by_email(form['email']):
            flash("Email been taken!")
            is_valid = False

        if len(form['password']) < 1:
            flash('Please enter a password!')
            is_valid = False
        
        elif not re.search('[A-Z]', form['password']):
            flash("Please include at least 1 Uppercase letter for your password!")
            is_valid = False

        elif not re.search('[a-z]', form['password']):
            flash("Please include at least 1 Lowercase letter for your password!")
            is_valid = False

        elif not re.search('[0-9]', form['password']):
            flash("Please include at least 1 digit for your password!")
            is_valid = False

        # '\s' to check for space and ['!@#$%^&*()_+'] for special characters

        elif form['password'] != form['confirm_password']:
            flash('Passwords did not match!')
        
        return is_valid
    
    @classmethod
    def validate_login(cls,form):

        # using get_one_by_email to send a query and return an User intance with the sumbited email
        # and with that User intance hashed password, we compare it with the submitted password
        found_user = cls.get_one_by_email(form['email'])

        if found_user:
            
            if BCRYPT.check_password_hash(found_user.password, form['password']):
                return found_user
            else:
                flash("Invalid Password")
                return False
        # if the get_one_by_email method doesn't return anything, then the submitted email was not
        # in the system and there fore invalid
        else:
            flash("Invalid Email")
            return False