#this home .py will maint thee homee pagee off all html page

from flask import Flask    # import 
from flask import Blueprint # for declaring files as a routing
from flask import render_template #
home_bp = Blueprint("home",__name__)

#rendering html home page
@home_bp.route("/home")
def home():
    return render_template("home.html",name= "Python Programming")