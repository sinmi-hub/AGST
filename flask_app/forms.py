# ------------------ LIBRARIES AND PACKAGES NEEDED------------------------------
from .models import User

# this setup is crucial for creating secure, functional, and user-friendly web
# forms. Flaskform also provide CSRF protection
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import ( # validators for each
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

# This allows educator to upload files as required and stipulates types of file that can be uploaded
from flask_wtf.file import FileAllowed, FileRequired, FileField

#---------------------- CLASSES FOR THE WEBSITE FORMS------------------------
# represents the search form. Will most likely go on a search bar
class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")

# represents what the registration form should look like, when educators need 
# to register for the first time
class RegistrationForm(FlaskForm):
    firstname =  StringField(
        "First name", validators=[InputRequired(), Length(min=1, max=40)]
    )
    lastname =  StringField(
        "Last name", validators=[InputRequired(), Length(min=1, max=40)]
    )
    institution =  StringField(
        "Institution", validators=[InputRequired(), Length(min=1, max=40)]
    )
    role = SelectField(
        "Role", 
        choices=[('Educator', 'Educator'), ('Student', 'Student'), ('Life Coach', 'Informal Educator')]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

# represents the login form for possible educator      
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

# represents the form to update username for possible educator
class UpdateUsernameForm(FlaskForm):
    username = StringField('New Username', validators=[
        InputRequired(),
        Length(min=1, max=40)
    ])
    submit_username = SubmitField('Change Username')

    def validate_username(self, username):
        user = Educator.objects(username = username.data).first()
        if user:
            raise ValidationError('Username already exists. Try again')

# represents the form required for educators to upload profile pictures
class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'png'],), FileRequired()
    ])
    submit_picture = SubmitField('Update Picture')

# represents the form required for educators to update bio as needed
class UpdateBioForm(FlaskForm):
    bio = TextAreaField(
        'Update Bio', validators=[InputRequired(),Length(min=5, max=500)
    ])
    submit_bio = SubmitField('Update')

# represents the form required for educators to upload lesson plans. This will either be pdf or doc file
class UploadLessonPlanForm(FlaskForm):
    lesson_plan_course_name =  lesson_plan_name = StringField(
        "Course Name", validators=[InputRequired(), Length(min=5, max=100)])
    lesson_plan_number = StringField(
        "Course Number", validators=[InputRequired(), Length(min=2, max=10)])
    lesson_plan_topic = StringField(
        "Course Topic", validators=[InputRequired(), Length(min=2, max=100)])
    lesson_plan_school = StringField(
        "School", validators=[InputRequired(), Length(min=5, max=100)])
    lesson_plan = FileField('Lesson Plan', validators=[
        FileAllowed(['pdf','docx']) , FileRequired()
    ])

# represents the form required to review educators. This review will be based 
# on videos, lesson plans and how educators performed. This will most likely be # for students only, or perhaps educators too
class ReviewEducatorsForm(FlaskForm):
    review = TextAreaField(
        'Add a comment', validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit_review = SubmitField('Comment')
    
    