from distutils.log import error
from flask import Blueprint, request,render_template, request, session, url_for, redirect, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import db as db
from datetime import datetime


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("/auth/login.html")

@auth.route('/login', methods=['POST'])
def login_request():
    email = request.form.get('email')
    password = request.form.get('password')
    
    #   Retrieve existing user record for validation
    user_query = db.TAGAR_DB.User.find_one({"email":email})
    if user_query == None:
        #   Email not tagged to user, redirect to login
        flash("There is no account tagged to this email")
        redirect_url = "auth.login"
    else:
        #   Password validation
        stored_hash = user_query["hashed_password"]
        
        if check_password_hash(stored_hash,password):
            #   Password matches -> Log user in and save session data
            session["email"] = request.form['email']
            session["username"] = user_query["username"]
            redirect_url = "pda.home"
        else:
            #   Password not match -> redirect to login and flash error 
            redirect_url = "auth.login"
            flash("Incorrect Password")

    return redirect(url_for(redirect_url))

@auth.route('/register')
def register():
    return render_template("/auth/register.html")

@auth.route('/register', methods=['POST'])
def register_request():

    username = request.form.get('username')
    password = request.form.get('password')
    verify_password = request.form.get('verify_password')
    email = request.form.get('email') # Unqiue Key/Index
    phone_num = request.form.get('phone_num')
    date_created = datetime.now()

    #   Password validation
    password_verification_flag = True

    if password != verify_password:
        flash("The passwords didn’t match. Try again.")
        password_verification_flag= False

    else:
        #   Password Hashing
        hashed_password = generate_password_hash(password)
    
    #   Phone Number validation
    phone_verification_flag = True
    if len(phone_num) != 8:
        flash("The phone number must be 8 digits. Try again.")
        phone_verification_flag = False

    if not (phone_num.isdigit()):
        flash("The phone number must made up of digits only. Try again.")
        phone_verification_flag = False

    #   Email validation
    email_verification_flag = True
    if email.find("@",0) == -1:
        flash("Invaild email. Try again.")
        email_verification_flag = False

    #   When all condition clear, proceed to check if user exist
    if password_verification_flag and phone_verification_flag and email_verification_flag:

        #   Check if the data exist already
        user_query = db.TAGAR_DB.User.find_one({"email":email})

        if user_query == None:
            #   If record does not exist, 
            #   add into a JSON Object, Perform insert function 
            record = {
                "username": username,
                "email": email,
                "phone_num": phone_num,
                "password": password,
                "hashed_password": hashed_password,
                "date_created": date_created 
            }

            db.insert_record(db.TAGAR_DB.User, record)
            redirect_url = "auth.login"
            return redirect(url_for(redirect_url))

        else:
            #   If record exist, return error 
            flash("An account has already been assigned to this email")

    # Any error, redirect back to register page 
    redirect_url = "auth.register"
    return redirect(url_for(redirect_url))


@auth.route('/logout')
def logout():
    session.clear()
    return render_template("/auth/login.html")
