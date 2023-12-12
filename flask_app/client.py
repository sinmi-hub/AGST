import requests
from .config import API_URL

class School(object):
    def __init__(self, school_json):
        self.county = school_json['County']
        self.psc_number = school_json['PSC_NUMBER']
        self.name = school_json['SCHOOL_NAME']
        self.street = school_json['STREET']
        self.city = school_json['CITY']
        self.state = school_json['STATE']
        self.zip = school_json['ZIP']
        self.grades = school_json['Grades']
        self.school_type = school_json['School_Type']

    def __repr__(self):
        return f"{self.name} - {self.city}, {self.state}"
    
    def __str__(self):
        return f"{self.name} - Located in {self.city}, {self.state}"

class SchoolClient(object):
    def __init__(self):
        self.sess = requests.Session()
        self.base_url = API_URL
        self.schools = self._fetch_all_schools() # Store values of the API call locally each session

    # function that does an API CALL
    def _fetch_all_schools(self):
        #====== API CALL============
        query = f"{self.base_url}?where=School_Type%20%3D%20'HIGH'%20OR%20Grades%20%3D%20'9-12'&outFields=*&outSR=4326&f=json"
        response = self.sess.get(query)

        #======= HANDLING CASES OF FAILURE IN API CALL=============
        # This is based on Maryland's API explorer. It uses features and 
        # attributes as keys, and values in the json format.
        if response.status_code == 200:
            schools_json = response.json()['features']
            return [School(school['attributes']) for school in schools_json]
        
        else:
            return f"Error: {response.status_code}" # TODO. Make it try again or except

    # helps to search value returned by the API call for a specific school
    def search_by_name(self, name):
        return [school for school in self.schools if name.lower() in school.name.lower()]
    
    # printing out the schools in a clear format
    def display_schools(self, schls):
        for schl in schls:
            print(schl)
    
#==========================EXAMPLE USAGE TO TEST=============================
if __name__ == "__main__":
    client = SchoolClient()

    # search for a school by name
    search_results = client.search_by_name("Marriotts Ridge")
    client.display_schools(search_results)

