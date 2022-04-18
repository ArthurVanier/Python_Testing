from locust import HttpUser, task

class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get('')
    
    @task
    def showSummary(self):
        self.client.post('showSummary', {"email": "john@simplylift.co"})
    
    @task
    def logout(self):
        self.client.get('logout')
    
    @task
    def purchase_places(self):
        self.client.post('purchasePlaces', {
        "places": "1",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
