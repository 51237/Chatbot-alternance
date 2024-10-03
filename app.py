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
        }
        .chat-input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-top: 10px;
        }
        .chat-button {
            width: 48%;
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
        .clear-button {
            width: 48%;
            padding: 10px;
            background-color: #dc3545;
            color: #fff;
            border: none;
            border-radius: 5px;
            margin-top: 10px;
            cursor: pointer;
        }
        .clear-button:hover {
            background-color: #c82333;
        }
        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background-color: #f0f2f5;
            color: #333;
            border-radius: 0 0 10px 10px;
        }
        .footer a {
            color: #333;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        /* Modal styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgb(0,0,0);
            background-color: rgba(0,0,0,0.4);
        }
        .modal-content {
            background-color: #fefefe;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            max-width: 600px;
            border-radius: 10px;
        }
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }
        .close:hover,
        .close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("Chat")

    # Initialiser une clé dans session_state pour le premier message
    if 'first_message' not in st.session_state:
        st.session_state.first_message = True

    # Initialiser l'historique des conversations
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    chat_input = st.sidebar.text_input("Vous:", key="chat_input", placeholder="Tapez votre message ici...")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Envoyer", key="send_button"):
            if chat_input:
                st.sidebar.markdown(f'<div class="user-message">Vous: {chat_input}</div>', unsafe_allow_html=True)

                # Ajouter le message de l'utilisateur à l'historique des conversations
                st.session_state.conversation_history.append({"role": "user", "content": chat_input})

                # Appel à Mistral pour obtenir la réponse du chatbot
                response = mistral_api.get_chatbot_response(chat_input)

                # Afficher la réponse du bot
                st.sidebar.markdown(f'<div class="bot-message">Chatbot: {response}</div>', unsafe_allow_html=True)

                # Ajouter la réponse du bot à l'historique des conversations
                st.session_state.conversation_history.append({"role": "assistant", "content": response})

                # Marquer que le premier message a été affiché
                st.session_state.first_message = False

    with col2:
        if st.button("Clear Chat"):
            # Supprimer visuellement les messages du chat
            st.session_state.chat_history_display = []

    # Afficher l'historique des conversations
    if 'chat_history_display' not in st.session_state:
        st.session_state.chat_history_display = []

    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.session_state.chat_history_display.append(f'<div class="user-message">Vous: {message["content"]}</div>')
        else:
            st.session_state.chat_history_display.append(f'<div class="bot-message">Chatbot: {message["content"]}</div>')

    for message in st.session_state.chat_history_display:
        st.sidebar.markdown(message, unsafe_allow_html=True)

    # Bouton pour lancer la simulation d'entretien
    if st.sidebar.button("Simuler un entretien"):
        response = mistral_api.simulate_interview()
        st.sidebar.markdown(f'<div class="bot-message">Chatbot: {response}</div>', unsafe_allow_html=True)
        st.session_state.conversation_history.append({"role": "assistant", "content": response})

    # Button to expand chat to the center of the app
    if st.sidebar.button("Agrandir le chat"):
        st.markdown(
            """
            <div id="myModal" class="modal">
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <h2>Chat</h2>
                    <div id="modal-chat-content"></div>
                    <input type="text" id="modal-chat-input" placeholder="Tapez votre message ici...">
                    <button onclick="sendModalChatMessage()">Envoyer</button>
                </div>
            </div>
            <script>
            // Get the modal
            var modal = document.getElementById("myModal");

            // Get the <span> element that closes the modal
            var span = document.getElementsByClassName("close")[0];

            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = "none";
            }

            // When the user clicks anywhere outside of the modal, close it
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }

            function sendModalChatMessage() {
                var input = document.getElementById("modal-chat-input");
                var message = input.value;
                if (message) {
                    // Send message to the server
                    // Simulate server response
                    var response = "This is a simulated response.";
                    var chatContent = document.getElementById("modal-chat-content");
                    chatContent.innerHTML += "<div>Vous: " + message + "</div>";
                    chatContent.innerHTML += "<div>Chatbot: " + response + "</div>";
                    input.value = "";
                }
            }

            // Show the modal
            modal.style.display = "block";
            </script>
            """,
            unsafe_allow_html=True
        )

    # Upload du CV
    st.header("Upload your CV")
    uploaded_file = st.file_uploader("Upload or drag and drop your CV (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Sauvegarder le fichier temporairement
        temp_file_path = save_uploaded_file(uploaded_file)

        # Extraire le texte du CV
        extracted_text = cv_processor.extract_text(temp_file_path)

        if extracted_text:
            # Afficher les éléments de sélection du titre de poste et de la localisation
            job_type_options = ["Data Scientist", "Software Engineer", "Designer", "Manager", "Other"]
            job_type = st.selectbox("Select job title:", job_type_options)

            if job_type == "Other":
                job_type = st.text_input("Enter custom job title")

            location_options = ["France", "USA", "Canada", "UK", "Germany", "Other"]
            location = st.selectbox("Location:", location_options)

            if location == "Other":
                location = st.text_input("Enter custom location")

            if job_type and location:
                # Obtenir les descriptions de postes
                job_descriptions = jooble_api.get_job_descriptions(job_type, location)

                if job_descriptions:
                    # Ajouter le texte du CV et les descriptions de poste à l'historique des conversations
                    #st.session_state.conversation_history.append({"role": "user", "content": f"cv text: {extracted_text}"})
                    #st.session_state.conversation_history.append({"role": "user", "content": f"job descriptions: {job_descriptions}"})

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

    # Footer
    st.markdown("<div class='footer'><a href='#'>À propos</a><a href='#'>Conditions d'utilisation</a><a href='#'>Politique de confidentialité</a><span>Version 1.0</span></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()