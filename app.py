import streamlit as st
from cv_processor import CVProcessor
from mistral_api import MistralAPI
from jooble_api import JoobleAPI
from config import load_config
from utils import save_uploaded_file

# Charger les configurations
config = load_config()

# Initialiser les objets
cv_processor = CVProcessor()
mistral_api = MistralAPI(config['MISTRAL_API_KEY'])
jooble_api = JoobleAPI(config['JOOble_API_KEY'])

# Fonction principale de l'application
def main():
    st.set_page_config(page_title="CV Improvement Chatbot", page_icon="🤖", layout="wide")

    # CSS pour personnaliser l'apparence
    st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f9;
        color: #333;
        font-family: 'Arial', sans-serif;
    }
    .sidebar .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .chat-container {
        background-color: #fff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .user-message {
        background-color: #6d737a;
        color: #fff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        float: right;
        clear: both;
    }
    .bot-message {
        background-color: #37393b;
        color: #fff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        float: left;
        clear: both;
    }
    .chat-input {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-top: 10px;
    }
    .chat-button {
        width: 100%;
        padding: 10px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 5px;
        margin-top: 10px;
        cursor: pointer;
    }
    .chat-button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    st.sidebar.title("Chat")
    
    # Initialiser une clé dans session_state pour le premier message
    if 'first_message' not in st.session_state:
        st.session_state.first_message = True

    chat_input = st.sidebar.text_input("Vous:", key="chat_input", placeholder="Tapez votre message ici...")
    
    if st.sidebar.button("Envoyer", key="send_button"):
        if chat_input:
            st.sidebar.markdown(f'<div class="user-message">Vous: {chat_input}</div>', unsafe_allow_html=True)
            
            # Appel à Mistral pour obtenir la réponse du chatbot
            response = mistral_api.get_chatbot_response(chat_input)
            
            # Afficher la réponse du bot
            st.sidebar.markdown(f'<div class="bot-message">Chatbot: {response}</div>', unsafe_allow_html=True)
            
            # Marquer que le premier message a été affiché
            st.session_state.first_message = False

    # Si c'est le premier chargement, ne pas afficher le message par défaut
    # if st.session_state.first_message:
    #     st.sidebar.markdown(f'<div class="bot-message">Chatbot: Bienvenue! Comment puis-je vous aider aujourd\'hui?</div>', unsafe_allow_html=True)

    # Upload du CV
    st.header("Upload your CV")
    uploaded_file = st.file_uploader("Upload or drag and drop your CV (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])
    job_type = st.text_input("Enter the job title:")
    location = st.text_input("Enter the location:", "France")

    if uploaded_file is not None and job_type and location:
        # Sauvegarder le fichier temporairement
        temp_file_path = save_uploaded_file(uploaded_file)

        # Extraire le texte du CV
        extracted_text = cv_processor.extract_text(temp_file_path)

        if extracted_text:
            # Obtenir les descriptions de postes
            job_descriptions = jooble_api.get_job_descriptions(job_type, location)

            if job_descriptions:
                # Obtenir les recommandations pour améliorer le CV
                recommendations = mistral_api.get_recommendations(extracted_text, job_descriptions)
                st.subheader("CV Improvement Recommendations")
                st.write(recommendations)

                # Ajouter d'autres fonctionnalités
                st.subheader("Other Functionalities")
                if st.button("Get Interview Questions"):
                    interview_questions = mistral_api.get_interview_questions(extracted_text, job_descriptions)
                    st.write(interview_questions)

                if st.button("Get Job Recommendations"):
                    job_recommendations = mistral_api.get_job_recommendations(extracted_text, job_descriptions)
                    st.write(job_recommendations)

if __name__ == "__main__":
    main()
