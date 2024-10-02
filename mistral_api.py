import requests
import json
import time

class MistralAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.conversation_history = []

    def get_recommendations(self, cv_text, job_descriptions):
        start_time = time.time()
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            prompt = f"""Analyze the following CV text and job descriptions to provide recommendations for improving the CV:

            CV Text:
            {cv_text}

            Job Descriptions:
            {json.dumps(job_descriptions, indent=2)}

            Please provide the following information in JSON format:
            - Recommendations for improving the CV based on the job descriptions
            """

            data = {
                "model": "mistral-tiny",
                "messages": [{"role": "system", "content": "You are an assistant that provides recommendations for improving CVs based on job descriptions."}]
            }

            data["messages"].extend(self.conversation_history)
            data["messages"].append({"role": "user", "content": prompt})

            response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)

            if response.status_code == 200:
                recommendations = response.json()['choices'][0]['message']['content']
                self.conversation_history.append({"role": "assistant", "content": recommendations})
            else:
                recommendations = None
        except Exception as e:
            print(f"Error getting recommendations from Mistral: {e}")
            recommendations = None
        end_time = time.time()
        print(f"Time taken to get recommendations from Mistral: {end_time - start_time} seconds")
        return recommendations

    def get_interview_questions(self, cv_text, job_descriptions):
        start_time = time.time()
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            prompt = f"""Analyze the following CV text and job descriptions to provide potential interview questions:

            CV Text:
            {cv_text}

            Job Descriptions:
            {json.dumps(job_descriptions, indent=2)}

            Please provide the following information in JSON format:
            - Potential interview questions based on the job descriptions
            """

            data = {
                "model": "mistral-tiny",
                "messages": [{"role": "system", "content": "You are an assistant that provides potential interview questions based on job descriptions."}]
            }

            data["messages"].extend(self.conversation_history)
            data["messages"].append({"role": "user", "content": prompt})

            response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)

            if response.status_code == 200:
                interview_questions = response.json()['choices'][0]['message']['content']
                self.conversation_history.append({"role": "assistant", "content": interview_questions})
            else:
                interview_questions = None
        except Exception as e:
            print(f"Error getting interview questions from Mistral: {e}")
            interview_questions = None
        end_time = time.time()
        print(f"Time taken to get interview questions from Mistral: {end_time - start_time} seconds")
        return interview_questions

    def get_job_recommendations(self, cv_text, job_descriptions):
        start_time = time.time()
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            prompt = f"""Analyze the following CV text and job descriptions to provide job recommendations:

            CV Text:
            {cv_text}

            Job Descriptions:
            {json.dumps(job_descriptions, indent=2)}

            Please provide the following information in JSON format:
            - Job recommendations based on the CV and job descriptions
            """

            data = {
                "model": "mistral-tiny",
                "messages": [{"role": "system", "content": "You are an assistant that provides job recommendations based on CV and job descriptions."}]
            }

            data["messages"].extend(self.conversation_history)
            data["messages"].append({"role": "user", "content": prompt})

            response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)

            if response.status_code == 200:
                job_recommendations = response.json()['choices'][0]['message']['content']
                self.conversation_history.append({"role": "assistant", "content": job_recommendations})
            else:
                job_recommendations = None
        except Exception as e:
            print(f"Error getting job recommendations from Mistral: {e}")
            job_recommendations = None
        end_time = time.time()
        print(f"Time taken to get job recommendations from Mistral: {end_time - start_time} seconds")
        return job_recommendations