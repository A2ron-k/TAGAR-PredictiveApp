from flask import Flask, render_template
from flask_session import Session
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)
Session(app)


@app.route('/test')
def index():
    return render_template('index.html')


if __name__ == '__main__': app.run(debug=True)