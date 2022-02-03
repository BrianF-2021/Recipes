# from flask_app import app
# from flask import render_template,redirect,request,session,flash
from users_app.config.mysqlconnection import connectToMySQL
# from flask_app.models.user import User
from users_app import app
from flask import render_template, redirect, request, session
from users_app.models import user, recipe


@app.route('/')
def index():
    session.clear()
    #return render_template('main.html')
    return redirect('/main')

@app.route('/main')
def user_main():
    return render_template("users_login_registration_main.html")


@app.route('/create')
def user_create():
    return render_template('users_new_form.html')


@app.route('/login')
def user_login():
    return render_template('users_login_form.html')


@app.route("/users/creating", methods = ["POST"])
def user_creating():
    print("request.form:",request.form)
    if not user.User.validate_registration(request.form):
        return redirect('/create')
    session['id'] = user.User.save_new_user(request.form)
    print('session id:', session['id'])
    return redirect('/user/home')


@app.route('/user/home')
def user_home():
    user_id = session['id']
    data ={
        'id': user_id
        }
    this_user = user.User.get_one(data)
    recipes = recipe.Recipe.get_all()
    return render_template('user_home_page.html',recipes = recipes, user = this_user)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/main')


@app.route('/users/validation', methods = ['POST'])
def login_validation():
    session['pw'] = request.form['password']
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':request.form['password']
    }
    result = user.User.validate_login(data)
    if result == False:
        return redirect('/login')

    this_user = user.User.get_one_by_email(data)
    session['id'] = this_user[0]['id']
    print('session id:', session['id'])
    return redirect('/user/home')


@app.route('/recipe/create')
def recipe_create():
    if 'id' not in session:
        return redirect('/user/home')
    return render_template('recipes_create_form.html')


@app.route("/recipe/creating", methods = ["POST"])
def recipe_creating():
    if 'id' not in session:
        return redirect('/user/home')
#    print("request.form:",request.form)
    user_id = session['id']
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/recipe/create')
    recipe.Recipe.save(request.form, user_id)
    return redirect('/user/home')


@app.route("/recipe/edit/<int:recipe_id>")
def recipe_edit(recipe_id):
    recipe_data = { 'id' :recipe_id}
    this_recipe = recipe.Recipe.get_one(recipe_data)
    return render_template("recipe_edit_form.html", recipe = this_recipe)


@app.route("/recipe/editing/<int:recipe_id>", methods = ["POST"])
def recipe_editing(recipe_id):
    if 'id' not in session:
        return redirect('/user/home')
#    print("request.form:",request.form)
    user_id = session['id']
    print("user_id", user_id)
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f'/recipe/edit/{recipe_id}')
    recipe.Recipe.update(request.form, user_id, recipe_id)
    return redirect('/user/home')


@app.route("/recipe/view/<int:recipe_id>")
def view_recipe(recipe_id):
    id = { 'id': recipe_id}
    this_recipe = recipe.Recipe.get_one(id)
    return render_template('recipe_view.html', recipe = this_recipe)



@app.route("/users/destroy/<int:user_id>")
def user_destroy(user_id):
    data = {
        'id':user_id
    }
    session.pop('id')
    user.User.delete(data)
    return redirect('/main')


@app.route("/recipe/destroy/<int:recipe_id>")
def recipe_destroy(recipe_id):
    data = {
        'id':recipe_id
    }
    recipe.Recipe.delete(data)
    return redirect('/user/home')


@app.route("/show_joined_users")
def show_joined_users():
    all = user.User.get_all_with_recipes()
    return render_template('show_joined_users.html', all = all)

@app.route("/show_joined_recipes")
def show_joined_recipes():
    all = recipe.Recipe.get_all_with_users()
    return render_template('show_joined_recipes.html', all = all)


@app.route("/show_joined")
def show_all_user():
    all = recipe.Recipe.get_all_with_user()
    names = []
    for user, values in all.items():
        print('user', user)
        for recipes in values:
            names.append(f'{recipes.users.first_name} + {recipes.users.last_name}')
    return render_template('show_joined.html', names = names, all = all)







# @app.route('/users/<int:user_id>')
# def user_show(user_id):
#     data = {
#         'id':user_id
#     }
#     user = User.get_one(data)
#     return render_template('users_view.html', user = user)


# @app.route("/users/<int:user_id>/edit")
# def user_edit(user_id):
#     data = {
#         'id':user_id
#     }
#     user = User.get_one(data)
#     return render_template('users_edit.html', user = user)


# @app.route("/users/<int:user_id>/update", methods=['POST'])
# def user_update(user_id):
#     if not User.validate_registration:
#         return redirect(f'/users/{user_id}/edit')
#     data = {
#         'id':user_id,
#         'first_name':request.form['first_name'],
#         'last_name':request.form['last_name'],
#         'email':request.form['email'],
#         'password':request.form['password']
#     }
#     #confirmed_pw = request.form['confirm_password']
#     print('update data:', data)
#     User.update(data)
#     return redirect(f'/users/{user_id}')


# @app.route('/users/new')
# def new_users():
#     return render_template('new_user.html')#show form


# @app.route('/users/create', methods = ['POST'])
# def create_user():
#     print("request.form:",request.form)
#     if not User.validate_registration(request.form):
#         return redirect('/users/new')
#     session['id'] = User.save_new_user(request.form)
#     return redirect('/users/loggedin')


# @app.route('/users/login')
# def users_login_form():
#     return render_template('users_login.html')#show form


# @app.route('/users/loggedin')
# def users_home():
#     return redirect('/users/home')


# @app.route('/users/home')
# def user_home():
#     user_id ={'id':session['id']}
#     user = User.get_one(user_id)
#     return render_template('user_home.html', user = user)




# @app.route('/show_user')
# def show_user():
#     user = User.get_user(session['id'])
#     print("user", user)
#     render_template('show_user.html', user = user)


# @app.route('/delete_users', methods =['POST'])
# def delete_users():
#     User.delete_users(request.form)
#     return redirect('/main')
#     # users = User.create_user()
#     # return connectToMySQL('users_db').query_db(query, data)




# @app.route('/pastries/<int:id>/edit')
# def show_pastry(id):
#     data = {
#     'id': id
#     }
#     pastry = Pastry.get_one(data)
#     return render_template('edit_pastry.html', pastry = pastry)


# @app.route('/users/create', methods = ['POST'])
# def create_user():
#     print("request.form:",request.form)
#     if not User.validate_registration(request.form):
#         return redirect('/users/new')
#     session['id'] = User.save_new_user(request.form)
#     print('session id:', session['id'])
#     return redirect('/user/home/')







