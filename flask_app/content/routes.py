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
        schools = school_client.search_by_name(query)
       
        if len(schools) == 0:
            return "No school found by that name"
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", schools=schools)

#TODO. Give more information about school detail. Copied from P4 to use as starting template. Intend to use the funct
@content.route("/content/<schls>", methods=["GET", "POST"])
def school_detail(schls):
    try:
        result = school_client.display_schools(schls)
        return result
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=str(e))

    # form = MovieReviewForm()

    # if form.validate_on_submit():
    #     review = Review(
    #         commenter=current_user._get_current_object(),
    #         content=form.text.data,
    #         date=current_time(),
    #         imdb_id=movie_id,
    #         movie_title=result.title,
    #     )

    #     review.save()

    #     return redirect(request.path)

    # reviews = Review.objects(imdb_id=movie_id)

    # for review in reviews:
    #     if review.commenter:
    #         reviewer_user = User.objects(username=review.commenter.username).first()
    #         if reviewer_user:
    #             review.image = get_b64_img(reviewer_user.username)
    #         else:
    #             review.image = None  # This is probably already taken care of


    # return render_template(
    #     "movie_detail.html", form=form, movie=result, reviews=reviews
    # )
