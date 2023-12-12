# AGST Final Project

## Description
 This a Flask-based web application. The purpose of this *web-based platform* is to centralize and showcase educational content, specifically videos and lesson plans, posted by agricultural educators from various schools across the state of Maryland. We want to encourage the sharing of educational materials among educators and serve as a real time tool for teaching agricultural concepts to students through visually rich content. Especially in areas where lesson plans can be compared, and restructured in such a way that explanation of various difficult concepts can be easier to understand. For now, the scope of this project is limited to AG educators and agricultural department, but this can be modified later on.

## Installation
- Install Python: Ensure that Python 3.10 or newer is installed on your system.
- Set up a virtual environment (optional but recommended):
    - Run python -m venv venv to create a virtual environment in the directory where you want virtual env to be created.

## Installation & Setup Part 1
For this project, we will be using a virtual environment. This is like like having a personalized workspace for each of your projects, keeping everything neat and organized, and ensuring that changes in one project don't mess up the others. A virtual environment allows you to set up these specific requirements for your project without interfering with what's needed for other projects. For this project, we will be using a specific virtual environment called 'venv'. In order for this to function, venv must be downloaded in the same directory that this AGST project is in.

Typically venv comes installed with python. You can simply create a new virtual environment using
- Create a new virtual environment: `python3 -m venv /pathofvirtualenvironment`
- Activate a virtual environment: `source /pathofvirtualenvironment/activate`
- Deactivate: `deactivate`


## Installation & Setup Part 2
Activate your virtual environment and use pip3 install -r requirements.txt

## Project structure

### Root Directory
- run.py: This is the main entry point to run the Flask application.
- .flaskenv: Contains environment variables for Flask.
- requirements.txt: Lists all Python dependencies for the project.
- READme.md: The file you are currently reading, which provides a guide to this project.
- images/: A directory to store images used in the project.
- tests/: Contains tests for the application.

### Flask App
- flask_app/: The main directory for the Flask application.
    - __init__.py: Initializes the Flask application and its configurations.
    - client.py: Handles client-side logic.
    - config.py: Contains configuration settings for the app. (Not here for securitu reasons)
    - forms.py: Defines forms used in the app.
    - models.py: Contains the database models.
    - utils.py: Utility functions for the app.

### Static
- flask_app/static/: Contains static files like CSS.
        `custom.css: Custom CSS styles.`
- flask_app/templates/: Contains HTML templates.
    - 404.html: Custom 404 error page.
    - account.html: Educator's account page template.
    - content_view.html: Template for content viewing.
    - header.html: Common header for all pages.
    - index.html: Homepage template.
    - layout.html: Base layout for the app.
    - login.html: Login page template.
    - register.html: Educator registration page template.
    - user_detail.html: Educator detail page template.

### Educator Module
- flask_app/educator/: A sub-module for educator's -related routes and logic.
    - __init__.py: Initializes the educator module.
    -  routes.py: Defines routes for educator operations.

## Running the Project
To run this project, stay in the `AGST_Project/` directory, or whatever you decide to name the directory, for this project  and use the `flask run` command. The file that is run is `run.py`. It simply imports the `app` object from the `flask_app/` package. The reason for this is to
avoid too much imports in Python projects.

In `__init__.py`, apps will be created by calling the `create_app()` function.

## Usage

Once the application is running, navigate to http://localhost:5000 in your web browser to view the application. VScode will show this when you run the project in the terminal

## Testing
To run tests, navigate to the tests/ directory and execute the test scripts.

## Contribution
Contributions to the project are welcome. Please follow the existing file structure and coding conventions.

## Support
For support or to report issues, please file an issue in the project's issue tracker.