import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from datetime import datetime
import requests
import urllib.parse
import flask
import os
from wbib import wbib
import yaml
from wikidata2df import wikidata2df
from flask import request, redirect, url_for, render_template, flash
import re  # For regex

from wdcuration import lookup_multiple_ids

app = Flask(__name__)


def convert_doi_to_qid(list_of_dois):
    """
    Converts a list of DOI ids to Wikidata QIDs.
    """
    formatted_dois = '{ "' + '" "'.join(list_of_dois) + '"}'
    query = f"""SELECT ?id ?item  ?itemLabel
    WHERE {{
        {{
        SELECT ?item ?id WHERE {{
            VALUES ?unformatted_id {formatted_dois}
            BIND(UCASE(?unformatted_id) AS ?id)
            ?item wdt:P356 ?id.
        }}
        }}
        SERVICE wikibase:label 
        {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}}}
    """

    query_result = wikidata2df(query)

    result = {"qids": set(query_result["item"].values), "missing": set()}
    for doi in list_of_dois:
        if doi.upper() not in list(query_result["id"].values):
            result["missing"].add(doi)

    return result


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
    return flask.render_template("index.html")


# A dashboard that takes a list of QIDs as direct parameters and displays them to the user
@app.route("/dashboard")
def dashboard():
    qids = request.args.get("qids", "")
    if qids:
        qid_list = qids.split(",")
    else:
        return "No qids provided", 400

    dashboard_html = wbib.render_dashboard(qid_list)

    return flask.render_template(
        "dashboard.html",
        dashboard=dashboard_html,
    )


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # Check if DOI text input is provided
        dois = request.form.get("dois", "").split()

        # Check if a file is uploaded
        file = request.files.get("bibtex_file")
        if file and allowed_file(file.filename):
            content = file.read().decode("utf-8")  # Assuming the file is UTF-8 encoded
            extracted_dois = extract_dois_from_bibtex(content)
            dois.extend(extracted_dois)
        elif not dois:
            flash("Please provide DOIs or a BIBTeX file.")
            return redirect(request.url)

        # Remove duplicates
        dois = list(set(dois))
        print(len(dois))
        dois = [doi.upper() for doi in dois]
        if len(dois) > 800:
            flash("Too many DOIs, using only the first 800.")
            dois = dois[:800]
        if dois:
            result = lookup_multiple_ids(
                dois, wikidata_property="P356", return_type="list"
            )
            qids = ",".join(result)
            return redirect(url_for("dashboard", qids=qids))
        else:
            flash("No DOIs found.")
            return redirect(request.url)

    return render_template("upload.html")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"bib", "bibtex"}


def extract_dois_from_bibtex(content):
    """
    Extracts DOIs from a BIBTeX file content using regular expression.
    """
    doi_pattern = re.compile(r"doi\s*=\s*{\s*([^}]+)\s*}", re.IGNORECASE)
    return doi_pattern.findall(content)


@app.route("/search")
def search():

    genders = ["female", "other"]

    return flask.render_template("search.html", genders=genders)


@app.route("/search/<item_id>", methods=["GET", "POST"])
def search_with_topic(item_id):

    query = f"""SELECT  ?topic ?topicLabel WHERE {{ 
    VALUES ?topic {{ wd:{item_id} }} .
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}  """

    query_formatted = "https://query.wikidata.org/sparql?query=" + urllib.parse.quote(
        query, safe=""
    )
    print(query_formatted)
    wikidata_result = requests.get(query_formatted, params={"format": "json"})
    item_label = wikidata_result.json()["results"]["bindings"][0]["topicLabel"]["value"]

    main_subject = {item_id: item_label}
    genders = {"female": "Q6581072", "any": "any"}

    # Query for regions: https://w.wiki/3RWu
    regions = {"latin america": "Q12585", "any": "any"}
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    config["restriction"]["topic_of_work"] = [item_id]
    config["title"] = ""
    config["subtitle"] = "Searchig articles about " + item_label

    if "gender" in request.args:
        print(request.args["gender"])
        gender = request.args["gender"]
        if gender != None and gender != "any":
            config["restriction"]["gender"] = [gender]

    if "region" in request.args:
        print(request.args["region"])
        region = request.args["region"]
        if region != None and region != "any":
            config["restriction"]["institution_region"] = [region]

    html = wbib.render_dashboard(config, mode="advanced", filepath="dashboard.html")

    return flask.render_template(
        "search.html",
        genders=genders,
        main_subject=main_subject,
        regions=regions,
        dashboard=html,
    )


@app.route("/about")
def about():
    return flask.render_template("about.html")


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

    query = f"""SELECT ?doi ?topic ?topicLabel WHERE {{ 
        OPTIONAL {{wd:{item_id} wdt:P356 ?doi}} .
        OPTIONAL {{wd:{item_id} wdt:P921 ?topic}} .
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}  """
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

        main_subjects = {}
        for snak in wikidata_result.json()["results"]["bindings"]:
            main_subjects[snak["topic"]["value"]] = snak["topicLabel"]["value"]

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
        main_subjects=main_subjects,
    )
