from locust import HttpLocust, TaskSet, task

#
# locust -f loadtest/api.py --host=http://localhost:8080
#

class APIEndpoints(TaskSet):

    # Documentation pages

    @task(2)
    def docs(self):
        self.client.get("/api/")
    

    # Category models
    
    @task(2)
    def keywords(self):
        self.client.get("/api/keywords")
    
    @task(2)
    def naics(self):
        self.client.get("/api/naics")
        
    @task(2)
    def psc(self):
        self.client.get("/api/psc")
        
    @task(2)
    def setasides(self):
        self.client.get("/api/setasides")
        
    @task(2)
    def zones(self):
        self.client.get("/api/zones")
        
    @task(2)
    def vehicles(self):
        self.client.get("/api/vehicles")
        
    @task(2)
    def pools(self):
        self.client.get("/api/pools")
        
    
    # Vendor models

    @task(2)
    def memberships(self):
        self.client.get("/api/memberships")
        
    @task(2)
    def vendors(self):
        self.client.get("/api/vendors")


    # Contract models
    
    @task(2)
    def agencies(self):
        self.client.get("/api/agencies")
        
    @task(2)
    def places_of_performance(self):
        self.client.get("/api/placesofperformance")
        
    @task(2)
    def pricing(self):
        self.client.get("/api/pricing")
        
    @task(2)
    def statuses(self):
        self.client.get("/api/statuses")
        
    @task(2)
    def contracts(self):
        self.client.get("/api/contracts")

    
    # Misc API endpoints
    
    @task(2)
    def metadata(self):
        self.client.get("/api/metadata")


class WebsiteUser(HttpLocust):
    task_set = APIEndpoints
    min_wait = 5000
    max_wait = 9000
