from flask import render_template, request, redirect, url_for, session, flash, Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")

@main.route("/downloads")
def downloads():
    return render_template("downloads.html")

@main.route("/about")
def about():
    return render_template("about.html")