#contains all routes for app. will flask what to display on what path

from flask import render_template

from app import app

#this decorator is used to specify the path for this view to be displayed on
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    #render template is used to specify which html file to load in a view
    return render_template("about.html")