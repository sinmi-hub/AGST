import requests
from .config import BASE_MAPS_URL, API_URL, END_URL, END_MAPS_URL

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
    
    # This function helps to generate a sort of static map for each school 
    # that is generated from our api call to API_URL.
    def generate_map(self):
        address = f"{self.street}, {self.city}, {self.state}, {self.zip}"
        address = address.replace(" ", "+")
        api_call = f"{BASE_MAPS_URL}{address}{END_MAPS_URL}"

        print(api_call)
        return api_call
    



    
class SchoolClient(object):
    def __init__(self):
        self.sess = requests.Session()
        self.base_url = API_URL
        self.schools = self.fetch_all_schools() 

    # fetches all the schools in maryland, once for each session and then stores this result locally
    def fetch_all_schools(self):

        #====== API CALL============
        query = f"{self.base_url}{END_URL}"
        response = self.sess.get(query)

        #======= HANDLING CASES OF FAILURE IN API CALL=============
        # This is based on Maryland's API explorer. It uses features and 
        # attributes as keys, and values in the json format.
        if response.status_code == 200:
            schools_json = response.json()['features']
            return [School(school['attributes']) for school in schools_json]
        
        else:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized" + f"Error: {response.status_code}"
            )
            # TODO. Make it try again or except

    # helps to search value returned by the API call for a specific school
    def search_by_name(self, name):
        return [school for school in self.schools if name.lower() in school.name.lower()]
    
    # printing out the schools in a clear format
    def display_schools(self, schls):
        for schl in schls:
            print("-Located in {schl.city}")
    
#==========================EXAMPLE USAGE TO TEST=============================
if __name__ == "__main__":
    client = SchoolClient()

    # search for a school by name
    search_results = client.search_by_name("Marriotts Ridge")
    client.display_schools(search_results)

