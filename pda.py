from pprint import pprint
from flask import Blueprint, request,render_template, request, url_for, redirect,session
from flask_session import Session
import db
import pprint

printer = pprint.PrettyPrinter()


pda = Blueprint('pda', __name__)

def pageProtector(template_to_render,data="default"):
    """
    If the user is logged in, then render the template, otherwise redirect to the login page
    
    :param template_to_render: This is the template that you want to render
    :param data: This is the data that you want to pass to the template, defaults to default (optional)
    :return: The location is being returned.
    """

    location = render_template(template_to_render, context = data )

    try:
        session["email"]

    except KeyError:
        # if not there in the session then redirect to the login page
        location = redirect(url_for("auth.login"))

    return location

@pda.route("/")
@pda.route("/home")
def home():

    location = pageProtector("/pda/home.html")

    return location


@pda.route("/dispatch")
def dispatch():
    
    location = pageProtector("/pda/dispatch.html")    
    
    return location


@pda.route("/cases")
def cases():

    cases_obj = db.find_all_cases()
    
    location = pageProtector("/pda/cases.html", cases_obj)    
    
    return location

@pda.route("/cases/<_id>",methods=['GET'])
def case_detail(_id):
    """
    It takes the id of a case, finds the case in the database, and then returns the location of the case
    detail page.
    
    :param _id: the id of the case you want to view
    :return: The location of the case_detail.html page.
    """
    
    specific_case_obj = db.find_one_case(_id)
    
    location = pageProtector("/pda/case_detail.html", specific_case_obj)    
    
    return location