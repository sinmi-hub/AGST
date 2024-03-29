from flask_login import UserMixin # good for user authentication
from . import db, login_manager
from .utils import curr_datetime



# ------------------------------USER MANAGEMENT---------------------------------
# This function, decorated with @login_manager.user_loader, is used to load a user from the database. It uses the argument, educator_id to find the specific educator that might exist in the database, and returns the first occurrence of the educator with such username.
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class User(db.Document, UserMixin):
    # necessary, so MongoEngine can tell this class will be inherited. Found on stack overflow. This seems to be set to False by default
    meta = {'allow_inheritance': True}

    # Common field for all subclasses to be inherited. 
    firstname = db.StringField(required=True, min_length=2, max_length=40)
    lastname = db.StringField(required=True, min_length=2, max_length=40)
    username = db.StringField(required=True, unique=True, min_length=2, max_length=40)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=12) # length of 12
    profile_pic = db.ImageField()
    bio =  db.StringField()

    # returns the user's first name and last name using current states
    def fullname(self):
        return f"{self.firstname} {self.lastname}"
    
    # helps user to update bio in real time
    def set_bio(self, bio_msg):
        self.bio = bio_msg
        self.save() # saves to databse??
    
    def set_profile_pic(self, profile_pic):
        self.profile_pic = profile_pic
        self.save()

# This class describes the user model and what each user (Educator's) state and characteristics should have
class Educator(User):
    institution = db.StringField(required=True)
    role = db.StringField("Educator")
    
    # Get the corresponding place that they teach
    def get_institution(self):
       return self.institution
    
    def get_role(self):
        return self.role


# represents student class
class Student(User):
    college = db.StringField(required=True)
    role = db.StringField("Student")

    def get_institution(self):
        return self.college
    
    def get_role(self):
        return self.role

# Any other person who would love to add opinion, or teach, but does not necessarily have any academic experience
class InformalEducator(User):
    college = db.StringField("")
    role = db.StringField("Informal Educator")

    def get_role(self):
        return self.role


  
    
#-------------------------CONTENT MANAGEMENT------------------------------------
# stores lesson plan updated by educators or professor's
class LessonPlan(db.Document):
    course_name = db.StringField(required=True, min_length=5, max_length=100)
    course_number = db.StringField(required=True, min_length=2, max_length=10)
    topic = db.StringField(required=True, min_length=2, max_length=100)
    school = db.StringField(required=True, min_length=5, max_length=100)
    lesson_plan_file = db.FileField(required=True) 

    # keeps track who and when lesson plan was updated
    user_upload = db.ReferenceField(User, required=True)
    upload_date = db.DateTimeField(default=curr_datetime(), required=True)

# stores reviews for educators
class Review(db.Document):
    # reference to the user who wrote the review
    reviewer = db.ReferenceField(User, required=True)  
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.DateTimeField(default=curr_datetime(), required=True)
    
    educator_reviewed = db.ReferenceField(Educator, required=True)  
    lesson_plan_reviewed = db.ReferenceField(LessonPlan, required=True)
