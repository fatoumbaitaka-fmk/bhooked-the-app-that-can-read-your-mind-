
import streamlit as st
from projet_informatique_L1.pages import accueil, section1, section2

st.set_page_config(
    page_title="Gestion de Bibliothèque",
    layout="wide"
)

st.sidebar.title("Menu")

# --- 3. RÉGLAGES (BARRE LATÉRALE) - Déplacés ici pour être globaux ---
st.sidebar.subheader("Réglages Interface")
theme_choisi = st.sidebar.selectbox("Ambiance", ["Or (par défaut)", "Rose", "Bleu"], key="main_theme")

if theme_choisi == "Rose":
    bg_color, accent_bar = "#FFF0F5", "#FFB6C1"
elif theme_choisi == "Bleu":
    bg_color, accent_bar = "#F0F8FF", "#B0C4DE"
else:
    bg_color, accent_bar = "#F9F7F2", "#D4AF37"

# Store these in session_state for pages to access easily
st.session_state['bg_color'] = bg_color
st.session_state['accent_bar'] = accent_bar

pages = {
    "Accueil": accueil,
    "Profil Utilisateur": section1,
    "Chatbot": section2,
}

selection = st.sidebar.selectbox("Aller à", list(pages.keys()))

# Exécution de la page sélectionnée
pages[selection].app()
