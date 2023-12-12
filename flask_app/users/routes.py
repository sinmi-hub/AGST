# flask extensions and extra libraries
from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_required, login_user, logout_user
from .. import bcrypt
from io import BytesIO
from werkzeug.utils import secure_filename
from base64 import b64encode

# local imports
from ..models import User, Student, InformalEducator, Educator
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm


users = Blueprint("users", __name__)


# ======================== USER MANAGEMENT VIEWS ==========================
# This function helps users to register for a new account on the website. This could either be a Student, Teacher or informal educator, as stated in models.py
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/')) #TODO

    # creates an instance of the form that is needed to register
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # hashes the user's password after user types it in
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

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
                login_user(user)
                return redirect(url_for('users.account'))
            
            else:
                # If user is not authenticated, flash a message
                flash("Failed to log in!")

    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('content.index'))  

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    profile_pic_form = UpdateProfilePicForm()
    user_reviews = url_for('users.user_detail', username=current_user.username)
    
    profile_pic_data = None

    if request.method == "POST":
        if update_username_form.validate():
            # username update
            current_user.modify(username = update_username_form.username.data)
            current_user.save()
            flash('Your username has been updated.', 'success')
            return redirect(url_for('users.account'))


        if profile_pic_form.validate():
            image = profile_pic_form.picture.data
            filename = secure_filename(image.filename)
            content_type = f'images/{filename[-3:]}'

            if current_user.profile_pic.get() is None:
            # user doesn't have a profile picture => add one
                current_user.profile_pic.put(image.stream, content_type=content_type)
            else:
            # user has a profile picture => replace it
                current_user.profile_pic.replace(image.stream, content_type=content_type)

            current_user.save()
            flash('Your profile picture has been updated.', 'success')

        return redirect(url_for('users.account'))

    # get's the current user's profile picture if it exists
    if current_user.profile_pic:
        profile_pic_bytes = BytesIO(current_user.profile_pic.read())
        profile_pic_data = b64encode(profile_pic_bytes.getvalue()).decode()
    else:
        profile_pic_data = None  # Or set a default image in base64 format


    return render_template(
        'account.html',
        update_username_form = update_username_form,
        update_profile_picture_form = profile_pic_form,
        image = profile_pic_data,  
        user_reviews_url = user_reviews
    )


