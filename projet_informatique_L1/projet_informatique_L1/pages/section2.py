%%writefile projet_informatique_L1/pages/section2.py
import streamlit as st
import google.generativeai as genai
import os # Import os for file operations
# Récupérez la clé API depuis les secrets de Colab
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def get_user_name_from_profile():
    """Reads the user's name from profil_utilisateur.txt if available."""
    profile_path = "profil_utilisateur.txt"
    if os.path.exists(profile_path):
        with open(profile_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("Nom:"):
                    return line.split(":", 1)[1].strip().capitalize() # Capitalize for better presentation
    return "utilisateur" # Default name if not found

def app():
    # Retrieve global settings from session_state
    bg_color = st.session_state.get('bg_color', '#F9F7F2')
    accent_bar = st.session_state.get('accent_bar', '#D4AF37')

    # --- 2. STYLE CSS (copied from accueil.py) ---
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Poppins:wght@300;400;600&display=swap');
        .stApp {{ background-color: {bg_color}; transition: 0.5s; }}
        .titre-royal {{ font-family: 'Playfair Display', serif; font-size: 100px !important; font-style: italic; color: #000 !important; text-align: center; margin: 0; }}
        .slogan {{ font-family: 'Poppins', sans-serif; text-align: center; letter-spacing: 5px; font-size: 14px; color: #333; margin-bottom: 20px; text-transform: uppercase; }}
        .book-card {{ background: white; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); height: 410px; }}
        .book-img {{ width: 100%; height: 230px; object-fit: cover; border-radius: 5px; }}
        .book-title {{ font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: 600; color: #000; margin-top: 10px; height: 35px; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
        .book-author {{ font-family: 'Poppins', sans-serif; font-size: 11px; color: #666; font-style: italic; margin-top: 5px; }}

        /* STYLE GENRE : Texte NOIR, barre de couleur épaisse */
        h3 {{
            font-family: 'Playfair Display', serif;
            color: #000 !important;
            border-bottom: 8px solid {accent_bar};
            display: inline-block;
            padding-bottom: 5px;
            margin-top: 40px !important;
            font-size: 1.8rem;
        }}

        .section-perso {{ background: rgba(255,255,255,0.7); padding: 30px; border-radius: 20px; border: 3px dashed {accent_bar}; margin-top: 50px; }}
        </style>
        """, unsafe_allow_html=True)

    st.header("Chatbot IA 🤖") # Changed header to reflect chatbot-only
    st.write("Discutez avec notre assistant virtuel propulsé par Gemini.") # Changed description

    # Get user name
    user_name = get_user_name_from_profile()

    # Initialisation du modèle Gemini
    if 'gemini_model' not in st.session_state:
        try:
            st.session_state.gemini_model = genai.GenerativeModel('gemini-3.1-flash-lite')
        except Exception as e:
            st.error(f"Erreur d'initialisation du modèle : {e}\nAssurez-vous que votre GOOGLE_API_KEY est correctement configurée dans les secrets de Colab.")
            st.stop()

    # No tabs, direct chatbot display as requested
    st.subheader("Parlez à l'IA")
    # Initialiser l'historique du chat
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Add an initial greeting message if the chat is new
        st.session_state.messages.append({"role": "assistant", "content": f"Bonjour {user_name}! Comment puis-je vous aider aujourd'hui ?"})


    # Afficher les messages de l'historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrée utilisateur
    if prompt := st.chat_input("Posez votre question ici..."):
        # Prepend user's name to the prompt for context, but only to the model, not to display in chat history
        prompt_with_context = f"L'utilisateur {user_name} demande: {prompt}"

        # Ajouter le message utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Générer la réponse
        with st.chat_message("assistant"):
            try:
                # Use the contextualized prompt for generation
                response = st.session_state.gemini_model.generate_content(prompt_with_context)
                assistant_response = response.text
                st.markdown(assistant_response)
                # Ajouter la réponse de l'assistant à l'historique
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
