from users_app.config.mysqlconnection import connectToMySQL
from flask import flash
from users_app.models import recipe
import re	# the regex module
from users_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "users_db"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = None


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        users_from_db = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in users_from_db:
            users.append(user)
        return users


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]



    @classmethod
    def save(cls, data):
        print("data:", data)
        query = "INSERT INTO users(first_name, last_name, email, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"

        data = {
            'first_name':data['first_name'],
            'last_name':data['last_name'],
            'email':data['email']
        }
        return connectToMySQL(cls.db).query_db(query, data) # returns id of object created/inserted


    @classmethod
    def update(cls, data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        print("pw_hash", pw_hash)
        data = {
            "first_name": data['first_name'],
            "last_name" : data['last_name'],
            "email" : data['email'],
            "password" : pw_hash,
        }
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, updated_at = NOW() WHERE users.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)



    @classmethod
    def get_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("mydb").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])



    @classmethod
    def save_new_user(cls, data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        print("pw_hash", pw_hash)
        data = {
            "first_name": data['first_name'],
            "last_name" : data['last_name'],
            "email" : data['email'],
            "password" : pw_hash,
        }
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def user_edit_validation(data):
        is_valid = True # we assume this is true
        if len(data['first_name']) < 2 or len( data['last_name']) < 2:
            flash("First and Last Name  must be at least 2 characters.")
            is_valid = False

        if not data['first_name'].isalpha() or not data['last_name'].isalpha():
            flash("First and Last Name can not contain numbers")
            is_valid = False

        if not data['password']:
            query = "SELECT * FROM users WHERE id = %(id)s"
            result = connectToMySQL(User.db).query_db(query, data)
            data['password'] = result['password']

        if (1 < len(data['password']) < 8) or(1 < len(data['confirm_password']) < 8):
            flash("Password must be at least 8 characters")
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash("Passwords do not match")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False

        email = {'email' : data['email']}
        user = User.get_one_by_email(email)
        if len(user) > 0:
            flash("The email you entered is already associated with an account.")
            is_valid = False

        return is_valid



    @staticmethod
    def validate_registration(data):
        is_valid = True # we assume this is true
        if len(data['first_name']) < 2 or len( data['last_name']) < 2:
            flash("First and Last Name  must be at least 2 characters.")
            is_valid = False

        if not data['first_name'].isalpha() or not data['last_name'].isalpha():
            flash("First and Last Name can not contain numbers")
            is_valid = False

        if len(data['password']) < 8 or len(data['confirm_password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash("Passwords do not match")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False

        email = {'email' : data['email']}
        user = User.get_one_by_email(email)
        if len(user) > 0:
            flash("The email you entered is already associated with an account.")
            is_valid = False

        return is_valid


    @classmethod
    def get_one_by_email(cls, data):
        print('get_one_by_email  email:', data['email'])
        data={
            'email' : data['email'],
        }
        query = "SELECT * FROM users where email = %(email)s;"
        print(connectToMySQL(cls.db).query_db(query, data))
        return (connectToMySQL(cls.db).query_db(query, data))


    @staticmethod
    def validate_login(data):
        is_valid = True
        email = {'email' : data['email']}
        print(email)
        user = User.get_one_by_email(email)
        print('user', user)
        if len(user) != 1:
            flash("Invalid login credentials1")
            is_valid = False
        elif is_valid and not bcrypt.check_password_hash(user[0]['password'], data['password']):
            flash("Invalid login credentials2")
            is_valid = False
        return is_valid


    @classmethod
    def get_all_with_recipes(cls):
        # query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE users.id = recipes.user_id;"
        query = "SELECT * FROM users JOIN recipes ON users.id = recipes.user_id WHERE users.id = recipes.user_id;"
        users_from_db = connectToMySQL(cls.db).query_db(query)
        all = []
        print("JOIN QUERY", users_from_db)
        #user_instance = cls(users_from_db[0])
        if not users_from_db:
            print("NO RESULTS FROM JOIN QUERY")
            return False

            # print("USER_INSTANCE:", user_instance)
            # print("USERS_FROM_DB:", users_from_db)
            # return user_instance

        for usr in users_from_db:
            recipe_data = {
                'id':usr['recipes.id'],
                'name':usr['name'],
                'date':usr['date'],
                'time':usr['time'],
                'description':usr['description'],
                'instructions':usr['instructions'],
                'user_id':usr['user_id'],
                'created_at':usr['recipes.created_at'],
                'updated_at':usr['recipes.updated_at']
            }

            user_data= {
                'id':usr['id'],
                'first_name':usr['first_name'],
                'last_name':usr['last_name'],
                'email':usr['email'],
                'password':usr['password'],
                'created_at':usr['created_at'],
                'updated_at':usr['updated_at']
            }
            user_inst = cls(user_data)
            user_inst.recipes = recipe.Recipe(recipe_data)
            all.append(user_inst)
        return all






    # @classmethod
    # def get_user(cls, data):
    #     query = "SELECT * FROM users WHERE id = %(id)s"
    #     user_from_db = connectToMySQL(cls.db).query_db(query,data)
    #     return cls(user_from_db[0])


    # # @classmethod
    # # def save(cls, data):
    # #     query = "INSERT INTO users(first_name, last_name, email) VALUES(%(first_name)s, %(last_name)s,%(email)s);"
    # #     return connectToMySQL(cls.db).query_db(query,data)



    # @classmethod
    # def edit_user(cls, data):
    #     query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s;"
    #     data = {
    #         'first_name' : data['first_name'],
    #         'last_name' : data['last_name'],
    #         'email' : data['email']
    #     }
    #     return connectToMySQL(cls.db).query_db(query,data)





    # @classmethod
    # def delete_user(cls, data):
    #     query = "DELETE FROM users WHERE id = %()s"
    #     return connectToMySQL(cls.db).query_db(query,data)


    # @classmethod
    # def delete_users(cls, data):
    #     query = "TRUNCATE TABLE users"
    #     return connectToMySQL(cls.db).query_db(query, data)