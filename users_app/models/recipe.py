from users_app.config.mysqlconnection import connectToMySQL
from users_app.models import user
from flask import flash
import re	# the regex module
from users_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Recipe:
    db = "users_db"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.time = data['time']
        self.instructions = data['instructions']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = None


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        recipes_from_db = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for recipe in recipes_from_db:
            recipes.append(recipe)
        return recipes


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]



    @classmethod
    def save(cls, data, id):
        print("data:", data)
        query = "INSERT INTO recipes(name, date, time, description, instructions, user_id, created_at, updated_at) VALUES(%(name)s, %(date)s, %(time)s, %(description)s, %(instructions)s,%(user_id)s, NOW(), NOW());"

        data = {
            'name':data['name'],
            'date':data['date'],
            'time':data['time'],
            'description':data['description'],
            'instructions':data['instructions'],
            'user_id': id,
        }
        return connectToMySQL(cls.db).query_db(query, data) # returns id of object created/inserted


    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) <= 3:
            is_valid = False
            flash("Name must be longer than 3 characters.")

        if len(data['description']) <= 3:
            is_valid = False
            flash("Name must be longer than 3 characters.")

        if len(data['instructions']) <= 3:
            is_valid = False
            flash("Name must be longer than 3 characters.")

        if not data['date']:
            is_valid = False
            flash("Please enter date")
        return is_valid


    @classmethod
    def update(cls, data, user_id, recipe_id):
        recipe_data = {
            'id':recipe_id,
            'name':data['name'],
            'date':data['date'],
            'time':data['time'],
            'description':data['description'],
            'instructions':data['instructions'],
            'user_id': user_id,
        }
        query = "UPDATE recipes SET name = %(name)s, date = %(date)s, time = %(time)s, description = %(description)s, instructions = %(instructions)s, user_id = %(user_id)s, updated_at = NOW() WHERE recipes.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, recipe_data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)



    @classmethod
    def save_new_recipe(cls, data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        print("pw_hash", pw_hash)
        data = {
            "first_name": data['first_name'],
            "last_name" : data['last_name'],
            "email" : data['email'],
            "password" : pw_hash,
        }
        query = "INSERT INTO recipes(first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def get_all_with_users(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.user_id=users.id;"
        #query = "SELECT * FROM users JOIN recipes ON users.id = recipes.user_id WHERE users.id = recipes.user_id;"
        recipes_from_db = connectToMySQL(cls.db).query_db(query)
        all = []
        print("JOIN QUERY", recipes_from_db)
        if not recipes_from_db:
            print("NO RESULTS FROM JOIN QUERY")
            return False

            # print("USER_INSTANCE:", user_instance)
            # print("USERS_FROM_DB:", users_from_db)
            # return user_instance

        for recip in recipes_from_db:
            recipe_data = {
                'id':recip['id'],
                'name':recip['name'],
                'date':recip['date'],
                'time':recip['time'],
                'description':recip['description'],
                'instructions':recip['instructions'],
                'user_id':recip['user_id'],
                'created_at':recip['created_at'],
                'updated_at':recip['updated_at']
            }

            user_data= {
                'id':recip['users.id'],
                'first_name':recip['first_name'],
                'last_name':recip['last_name'],
                'email':recip['email'],
                'password':recip['password'],
                'created_at':recip['users.created_at'],
                'updated_at':recip['users.updated_at']
            }
            recipe_inst = cls(recipe_data)
            recipe_inst.users = user.User(user_data)
            all.append(recipe_inst)
        return all




    @classmethod
    def get_all_with_user(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.user_id=users.id;"
        #query = "SELECT * FROM users JOIN recipes ON users.id = recipes.user_id WHERE users.id = recipes.user_id;"
        recipes_from_db = connectToMySQL(cls.db).query_db(query)
        all = []
        print("JOIN QUERY", recipes_from_db)
        if not recipes_from_db:
            print("NO RESULTS FROM JOIN QUERY")
            return False
            # print("USER_INSTANCE:", user_instance)
            # print("USERS_FROM_DB:", users_from_db)
            # return user_instance
        user_list = []
        user_dic = {}
        for recip in recipes_from_db:
            recipe_data = {
                'id':recip['id'],
                'name':recip['name'],
                'date':recip['date'],
                'time':recip['time'],
                'description':recip['description'],
                'instructions':recip['instructions'],
                'user_id':recip['user_id'],
                'created_at':recip['created_at'],
                'updated_at':recip['updated_at']
            }

            user_data= {
                'id':recip['users.id'],
                'first_name':recip['first_name'],
                'last_name':recip['last_name'],
                'email':recip['email'],
                'password':recip['password'],
                'created_at':recip['users.created_at'],
                'updated_at':recip['users.updated_at']
            }
            # recipe_inst = cls(recipe_data)
            # recipe_inst.users = user.User(user_data)
            # if recip['users.id'] in user_list:
            #     user_list[recip['users.id']].append(recipe_inst)
            # else:
            #     user_list[recip['users.id']] = [recipe_inst]

            recipe_inst = cls(recipe_data)
            recipe_inst.users = user.User(user_data)
            if recip['users.id'] in user_dic:
                user_dic[recip['users.id']].append(recipe_inst)
            else:
                user_dic[recip['users.id']] = [recipe_inst]

        return user_dic




    # @staticmethod
    # def recipe_edit_validation(data):
    #     is_valid = True # we assume this is true
    #     if len(data['first_name']) < 2 or len( data['last_name']) < 2:
    #         flash("First and Last Name  must be at least 2 characters.")
    #         is_valid = False

    #     if not data['first_name'].isalpha() or not data['last_name'].isalpha():
    #         flash("First and Last Name can not contain numbers")
    #         is_valid = False

    #     if not data['password']:
    #         query = "SELECT * FROM recipes WHERE id = %(id)s"
    #         result = connectToMySQL(Recipe.db).query_db(query, data)
    #         data['password'] = result['password']

    #     if (1 < len(data['password']) < 8) or(1 < len(data['confirm_password']) < 8):
    #         flash("Password must be at least 8 characters")
    #         is_valid = False

    #     if data['password'] != data['confirm_password']:
    #         flash("Passwords do not match")
    #         is_valid = False

    #     if not EMAIL_REGEX.match(data['email']):
    #         flash("Invalid email address!")
    #         is_valid = False

    #     email = {'email' : data['email']}
    #     recipe = User.get_one_by_email(email)
    #     if len(recipe) > 0:
    #         flash("The email you entered is already associated with an account.")
    #         is_valid = False

    #     return is_valid



    # @staticmethod
    # def validate_registration(data):
    #     is_valid = True # we assume this is true
    #     if len(data['first_name']) < 2 or len( data['last_name']) < 2:
    #         flash("First and Last Name  must be at least 2 characters.")
    #         is_valid = False

    #     if not data['first_name'].isalpha() or not data['last_name'].isalpha():
    #         flash("First and Last Name can not contain numbers")
    #         is_valid = False

    #     if len(data['password']) < 8 or len(data['confirm_password']) < 8:
    #         flash("Password must be at least 8 characters")
    #         is_valid = False

    #     if data['password'] != data['confirm_password']:
    #         flash("Passwords do not match")
    #         is_valid = False

    #     if not EMAIL_REGEX.match(data['email']):
    #         flash("Invalid email address!")
    #         is_valid = False

    #     email = {'email' : data['email']}
    #     recipe = User.get_one_by_email(email)
    #     if len(recipe) > 0:
    #         flash("The email you entered is already associated with an account.")
    #         is_valid = False

    #     return is_valid


    # @classmethod
    # def get_one_by_email(cls, data):
    #     print('get_one_by_email  email:', data['email'])
    #     data={
    #         'email' : data['email'],
    #     }
    #     query = "SELECT * FROM recipes where email = %(email)s;"
    #     print(connectToMySQL(cls.db).query_db(query, data))
    #     return (connectToMySQL(cls.db).query_db(query, data))


    # @staticmethod
    # def validate_login(data):
    #     is_valid = True
    #     email = {'email' : data['email']}
    #     print(email)
    #     recipe = User.get_one_by_email(email)
    #     print('recipe', recipe)
    #     if len(recipe) != 1:
    #         flash("Invalid login credentials1")
    #         is_valid = False
    #     elif is_valid and not bcrypt.check_password_hash(recipe[0]['password'], data['password']):
    #         flash("Invalid login credentials2")
    #         is_valid = False
    #     return is_valid





    # @classmethod
    # def get_recipe(cls, data):
    #     query = "SELECT * FROM recipes WHERE id = %(id)s"
    #     recipe_from_db = connectToMySQL(cls.db).query_db(query,data)
    #     return cls(recipe_from_db[0])


    # # @classmethod
    # # def save(cls, data):
    # #     query = "INSERT INTO recipes(first_name, last_name, email) VALUES(%(first_name)s, %(last_name)s,%(email)s);"
    # #     return connectToMySQL(cls.db).query_db(query,data)



    # @classmethod
    # def edit_recipe(cls, data):
    #     query = "UPDATE recipes SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s;"
    #     data = {
    #         'first_name' : data['first_name'],
    #         'last_name' : data['last_name'],
    #         'email' : data['email']
    #     }
    #     return connectToMySQL(cls.db).query_db(query,data)





    # @classmethod
    # def delete_recipe(cls, data):
    #     query = "DELETE FROM recipes WHERE id = %()s"
    #     return connectToMySQL(cls.db).query_db(query,data)


    # @classmethod
    # def delete_recipes(cls, data):
    #     query = "TRUNCATE TABLE recipes"
    #     return connectToMySQL(cls.db).query_db(query, data)
