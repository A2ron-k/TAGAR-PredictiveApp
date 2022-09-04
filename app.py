### Running instruction
# 1. Create Virtual Environment => * python -m venv env
# 2. Activate Virtual Environment => * source env/bin/activate (For Mac) | * .\env\Scripts\activate (For Windows)
# 3. Install dependencies and packages => * pip install -r requirements.txt
# 3. Change directory to TAGAR_PDA_REMASTER
# 4. Cmd to config flask app to search for the initaliser location aka inside app => * export FLASK_APP=app (For Mac) | * set FLASK_APP=app (For Windows)
# 5. Cmd to config flask app DEBUG MODE => * export FLASK_DEBUG=1 (For Mac) | * set FLASK_DEBUG=1 (For Windows)
# 6. Run using app while in TAGAR_PDA_REMASTER directory => * flask run 

# For Mac (Single line flask run) -> export FLASK_APP=app; export FLASK_ENV=development; export FLASK_DEBUG=1; flask run 
###

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