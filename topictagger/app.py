import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from datetime import datetime
import requests
import urllib.parse

# Configure application

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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


@app.route("/item/", methods=["GET", "POST"])
@app.route("/item", methods=["GET", "POST"])
def item_base():

    if request.method == "POST":
        item = request.form.get("item")
        return redirect(f"/item/{item}")

    return render_template("item.html")


@app.route("/item/<item_id>", methods=["GET", "POST"])
def item_id(item_id):

    if request.method == "POST":

        item = request.form.get("item")

        return redirect(f"/item/{item}")

    query = f"SELECT * WHERE {{ OPTIONAL {{wd:{item_id} wdt:P356 ?doi}} }}  "
    query_formatted = "https://query.wikidata.org/sparql?query=" + urllib.parse.quote(
        query, safe=""
    )

    try:
        wikidata_result = requests.get(query_formatted, params={"format": "json"})

        doi = wikidata_result.json()["results"]["bindings"][0]["doi"]["value"]

        query_to_europe_pmc = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:{doi}&format=json&resultType=core"
        print(query_to_europe_pmc)
        r = requests.get(query_to_europe_pmc, params={"format": "json"})

        json_for_article = r.json()["resultList"]["result"][0]
    except:
        flash("Item is not an article or did not have a DOI on Wikidata")
        return redirect(url_for(".item_base"))

    try:
        abstract = json_for_article["abstractText"]
    except:
        abstract = "No abstract."

    title = json_for_article["title"]
    mesh_headings = json_for_article["meshHeadingList"]["meshHeading"]

    try:
        keywords = json_for_article["keywordList"]["keyword"]
    except:
        keywords = {"No keywords."}

    return render_template(
        "item.html",
        message="",
        item=item_id,
        title=title,
        abstract=abstract,
        mesh_headings=mesh_headings,
        keywords=keywords,
    )
