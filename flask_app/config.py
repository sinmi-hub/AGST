# This file serves as configuration file for AGST project

# Secret Key : Secret key is used to secure sessions and cookies. Good for protecting against cross-site request forgery (CSRF) attacks
# MongoDB_Host: Connects our project to our NoSQL database (MongoDB)
# API_URL: This is pretty much the base URL for the API explorer that we are using for this project. This is used in tandem with query to 

SECRET_KEY = b'N\xb7\xad\xf5eJ\xf3\xb3\xe9\xd6\xab\xddjuc\xb4'
MONGODB_HOST = 'mongodb+srv://mojeyomi:Bqr4WxhoghT8ANLe@agstbackend.s0t6liq.mongodb.net/?retryWrites=true&w=majority'
API_URL = "https://geodata.md.gov/imap/rest/services/Education/MD_EducationFacilities/FeatureServer/5/query" # TODO, DOUBE CHECK