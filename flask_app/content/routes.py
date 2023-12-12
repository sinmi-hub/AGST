from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import school_client
from ..forms import SearchForm, ReviewEducatorsForm


content = Blueprint("content", __name__)

# ========================= CONTENT MANAGEMENT VIEWS ========================

# home page
@content.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    # if search button is used..
    if form.validate_on_submit():
        return redirect(url_for("content.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)

# when the search bar is used, this would route will execute and try to return the queried school
@content.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = school_client.search_by_name(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)