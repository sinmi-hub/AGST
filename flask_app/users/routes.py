# flask extensions and extra libraries
from flask import Blueprint, redirect, url_for, render_template, request, flash, current_app
from flask_login import current_user, login_required, login_user, logout_user
from .. import bcrypt
from io import BytesIO
from base64 import b64encode
from werkzeug.utils import secure_filename
from base64 import b64encode

import os

# # local imports
from ..models import User, Student, InformalEducator, Educator
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm


users = Blueprint("users", __name__)


# ======================== USER MANAGEMENT VIEWS ==========================
# This function helps users to register for a new account on the website. This could either be a Student, Teacher or informal educator, as stated in models.py
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('content.index')) #TODO

    # creates an instance of the form that is needed to register
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # hashes the user's password after user types it in
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=hashed_pwd)

            # Deciding what instance of user to create based on what user 
            # indicates what role is
            if form.role.data == 'Educator':
                user = Educator(
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=hashed_pwd,
                    institution=form.institution.data
                )
            
            elif form.role.data == 'Student':
                user = Student(
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=hashed_pwd,
                    institution=form.institution.data
                )
            
            else:
                user = InformalEducator(
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=hashed_pwd,
                    institution=form.institution.data
                )
            user.save()
            
            flash('Your account has been created! You are now able to log in', 'success')

            # after logging the user in, we redirect them to login
            return redirect(url_for('users.login'))
       
    return render_template('register.html', title = 'Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # redirect authenticated users
        return redirect(url_for('content.index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Check if user exists and the password is correct
            user = User.objects(username = form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                print("This is user before authenication:", current_user)
                login_user(user)
                print("This is user after authenication:", current_user)
                return redirect(url_for('users.account'))
            
            else:
                # If user is not authenticated, flash a message
                flash("Login Failed. Account might not exist or password might be wrong!")

    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('content.index'))  


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    propic_update = UpdateProfilePicForm()
    username_update = UpdateUsernameForm()
    propic = None

    if request.method == "POST":
        # username update
        if username_update.validate():
            current_user.modify(username = username_update.username.data)
            current_user.save()
            flash('Your username has been updated.', 'success')
            return redirect(url_for('users.account'))

        # profile picture update
        if propic_update.validate():
            image = propic_update.picture.data
            filename = secure_filename(image.filename)
            content_type = f'images/{filename[-3:]}'
            current_user.profile_pic.put(image.stream, content_type=content_type)
            current_user.save()
            flash('Your profile picture has been updated.', 'success')

        return redirect(url_for('users.account'))
    
    # get's the current user's profile picture if it exists
    if current_user.profile_pic:
        print("Profile pic exists:", current_user.profile_pic)
        propic_bytes = BytesIO(current_user.profile_pic.read())
        propic = b64encode(propic_bytes.getvalue()).decode()

    # we use the default profile picture created by the python script -
    # {./static/default_propics/image_gen.py}
    else:
        # print("Using default profile pic")
        first_name = current_user.firstname
        letter = first_name[0]
        # print(first_name)
        # print(letter)
        default_pic_filename = f"{letter}_image.jpg"

        # construct a file path stating from flask_app as current_app in flask is the app directory
        default_pic_path = os.path.join(current_app.root_path,'static', 'default_propics', default_pic_filename)
        # print(default_pic_path)

        # print(os.path.exists(default_pic_path))
        if os.path.exists(default_pic_path):
            
            propic = url_for('static', filename=os.path.join('default_propics', default_pic_filename))

    # print(propic)
    return render_template(
        'account.html',
        image = propic,
        update_username_form = username_update,
        update_profile_picture_form=propic_update
    )

# propic should not return None as the last {if statement} should always update propic. Default image for every character of the alphabet is created already.
