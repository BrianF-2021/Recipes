# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt

from users_app import app
from users_app.controllers import users_controller

if __name__=="__main__":
    app.run(debug=True)