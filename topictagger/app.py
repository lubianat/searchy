import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
import requests
import urllib.parse

# Configure application

app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/item", methods=["GET", "POST"])
def item_base():

    if request.method == "POST":
        pass

    return render_template("item.html")


@app.route("/item/<item_id>", methods=["GET", "POST"])
def item_id(item_id):

    if request.method == "POST":
        pass

    query = f"SELECT * WHERE {{ OPTIONAL {{wd:{item_id} wdt:P356 ?doi}} }}  "
    query_formatted = "https://query.wikidata.org/sparql?query=" + urllib.parse.quote(
        query, safe=""
    )

    r = requests.get(query_formatted, params={"format": "json"})

    return render_template("item.html", item=r.json())

