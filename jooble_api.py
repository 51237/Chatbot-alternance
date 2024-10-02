import requests
import json
import time

class JoobleAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_job_descriptions(self, job_type, location="France"):
        start_time = time.time()
        try:
            url = f"https://fr.jooble.org/api/{self.api_key}"

            headers = {
                "Content-Type": "application/json"
            }

            body = json.dumps({
                "keywords": job_type,  # Mots-clés du poste
                "location": location,  # Localisation, par défaut "France"
                "radius": "50"
            })

            response = requests.post(url, headers=headers, data=body)

            # Afficher le code de statut et la réponse brute pour le débogage
            print(f"Request URL: {url}")
            print(f"Request Body: {body}")
            print(f"Response Status Code: {response.status_code}")

            if response.status_code == 200:
                job_descriptions = response.json().get('jobs', [])  # Renvoie une liste vide si 'jobs' n'est pas dans la réponse
            else:
                print(f"Error fetching job descriptions from Jooble: {response.status_code} - {response.text}")
                job_descriptions = []  # Renvoie une liste vide au lieu de None
        except Exception as e:
            print(f"Error fetching job descriptions from Jooble: {e}")
            job_descriptions = []
        end_time = time.time()
        print(f"Time taken to fetch job descriptions from Jooble: {end_time - start_time} seconds")
        return job_descriptions