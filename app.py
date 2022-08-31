from distutils.command.config import config
from flask import Flask, render_template
from flask_session import Session
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
### A blueprint is a collection of routes for a specific portion of the application

# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from pda import pda as main_blueprint
app.register_blueprint(main_blueprint)

@app.route('/test')
def index():
    return render_template('index.html')


if __name__ == '__main__': app.run(debug=True)