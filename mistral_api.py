import os
import time
from mistralai import Mistral

class MistralAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Mistral(api_key=api_key)
        self.conversation_history = []

    def get_recommendations(self, cv_text, job_descriptions):
        start_time = time.time()
        try:
            prompt = f"""Analyze the following CV text and job descriptions to provide detailed recommendations in the language of the CV for for improving the CV:

            CV Text:
            {cv_text}

            Job Descriptions:
            {job_descriptions}

            Please provide the following information in text format:
            - Recommendations for improving the CV based on the job descriptions
            - Suggestions for enhancing the description of experiences
            - Advice on highlighting relevant skills and competencies
            - Tips for mentioning technical tools and software
            - Recommendations for emphasizing language proficiency
            - Suggestions for including relevant training and certifications
            - General improvements to make the CV more professional and attractive to HR and recruitment bots
            """

            messages = [{"role": "system", "content": "You are an assistant that provides detailed recommendations for improving CVs based on job descriptions."}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.stream(
                model="mistral-large-latest",
                messages=messages
            )

            recommendations = ""
            for chunk in response:
                recommendations += chunk.data.choices[0].delta.content

            self.conversation_history.append({"role": "assistant", "content": recommendations})
        except Exception as e:
            print(f"Error getting recommendations from Mistral: {e}")
            recommendations = None
        end_time = time.time()
        print(f"Time taken to get recommendations from Mistral: {end_time - start_time} seconds")
        return recommendations

    def get_interview_questions(self, cv_text, job_descriptions):
        start_time = time.time()
        try:
            prompt = f"""Analyze the following CV text and job descriptions to provide detailed and relevant interview questions in the language of the CV :

            CV Text:
            {cv_text}

            Job Descriptions:
            {job_descriptions}

            Please provide the following information in text format:
            - Potential interview questions based on the job descriptions
            - Questions related to the candidate's experiences and how they align with the job requirements
            - Questions about the candidate's technical skills and competencies
            - Questions about the candidate's use of technical tools and software
            - Questions about the candidate's soft skills and interpersonal abilities
            - Questions about the candidate's problem-solving and decision-making skills
            - Questions about the candidate's language proficiency
            - Questions about the candidate's training and certifications
            - Questions that are commonly asked in highly competitive and selective interviews
            - Questions that might be asked by an HR representative, a technical manager, and their supervisor
            - General questions to assess the candidate's fit for the role and the company culture
            """

            messages = [{"role": "system", "content": "You are an assistant that provides detailed and relevant interview questions based on job descriptions."}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.stream(
                model="mistral-large-latest",
                messages=messages
            )

            interview_questions = ""
            for chunk in response:
                interview_questions += chunk.data.choices[0].delta.content

            self.conversation_history.append({"role": "assistant", "content": interview_questions})
        except Exception as e:
            print(f"Error getting interview questions from Mistral: {e}")
            interview_questions = None
        end_time = time.time()
        print(f"Time taken to get interview questions from Mistral: {end_time - start_time} seconds")
        return interview_questions

    def get_job_recommendations(self, cv_text, job_descriptions):
        start_time = time.time()
        try:
            prompt = f"""Analyze the following CV text and job descriptions to provide detailed and relevant job recommendations in the language of the CV:

            CV Text:
            {cv_text}

            Job Descriptions:
            {job_descriptions}

            Please provide the following information in text format:
            - Job recommendations based on the CV and job descriptions
            - Suggestions for jobs that match the candidate's experiences
            - Recommendations for jobs that align with the candidate's skills and competencies
            - Suggestions for jobs that require the candidate's technical tools and software knowledge
            - Recommendations for jobs that value the candidate's soft skills and interpersonal abilities
            - Suggestions for jobs that recognize the candidate's problem-solving and decision-making skills
            - Recommendations for jobs that value the candidate's language proficiency
            - Suggestions for jobs that recognize the candidate's training and certifications
            - General recommendations for jobs that are a good fit for the candidate's career path and aspirations
            - Recommendations for jobs that the candidate might not have considered but are a good match based on their profile
            """

            messages = [{"role": "system", "content": "You are an assistant that provides detailed and relevant job recommendations based on CV and job descriptions."}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.stream(
                model="mistral-large-latest",
                messages=messages
            )

            job_recommendations = ""
            for chunk in response:
                job_recommendations += chunk.data.choices[0].delta.content

            self.conversation_history.append({"role": "assistant", "content": job_recommendations})
        except Exception as e:
            print(f"Error getting job recommendations from Mistral: {e}")
            job_recommendations = None
        end_time = time.time()
        print(f"Time taken to get job recommendations from Mistral: {end_time - start_time} seconds")
        return job_recommendations

    def get_chatbot_response(self, user_message):
        try:
            if "simulate interview" in user_message.lower():
                return self.simulate_interview()

            prompt = f"""Please provide a detailed and helpful response to the following user message following the language of the CV :

            User Message:
            {user_message}

            Please consider the following aspects in your response:
            - Provide clear and concise information
            - Address the user's specific concerns or questions
            - Offer practical advice or suggestions
            - Use a professional and friendly tone
            - Include relevant examples or explanations if necessary
            - Ensure the response is comprehensive and covers all aspects of the user's query
            """

            messages = [{"role": "system", "content": "You are a helpful and professional assistant."}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.stream(
                model="mistral-large-latest",
                messages=messages
            )

            bot_response = ""
            for chunk in response:
                bot_response += chunk.data.choices[0].delta.content

            self.conversation_history.append({"role": "assistant", "content": bot_response})
            return bot_response
        except Exception as e:
            print(f"Error getting chatbot response from Mistral: {e}")
            return "Désolé, une erreur s'est produite."

    def simulate_interview(self):
        try:
            cv_text = self.get_cv_text_from_history()
            job_descriptions = self.get_job_descriptions_from_history()

            if not cv_text or not job_descriptions:
                return "Désolé, je n'ai pas suffisamment d'informations pour simuler un entretien. Veuillez fournir votre CV et les descriptions de poste."

            interview_questions = self.get_interview_questions(cv_text, job_descriptions)
            if interview_questions:
                self.conversation_history.append({"role": "assistant", "content": interview_questions})
                return interview_questions
            else:
                return "Désolé, je n'ai pas pu générer de questions d'entretien."
        except Exception as e:
            print(f"Error simulating interview: {e}")
            return "Désolé, une erreur s'est produite."

    def get_cv_text_from_history(self):
        for message in reversed(self.conversation_history):
            if "cv text" in message["content"].lower():
                return message["content"].replace("cv text: ", "")
        return None

    def get_job_descriptions_from_history(self):
        for message in reversed(self.conversation_history):
            if "job descriptions" in message["content"].lower():
                return message["content"].replace("job descriptions: ", "")
        return None

# Exemple d'utilisation
if __name__ == "__main__":
    api_key = os.environ["MISTRAL_API_KEY"]
    mistral_api = MistralAPI(api_key)

    cv_text = "Votre texte de CV ici"
    job_descriptions = ["Description de poste 1", "Description de poste 2"]

    recommendations = mistral_api.get_recommendations(cv_text, job_descriptions)
    print("Recommendations:", recommendations)

    user_message = "Bonjour, comment puis-je améliorer mon CV ?"
    bot_response = mistral_api.get_chatbot_response(user_message)
    print("Chatbot Response:", bot_response)

    user_message = "Pouvez-vous simuler un entretien pour moi ?"
    bot_response = mistral_api.get_chatbot_response(user_message)
    print("Chatbot Response:", bot_response)