%%writefile projet_informatique_L1/pages/section1.py
import streamlit as st
import os
from projet_informatique_L1 import utils_reco # Import utils_reco

def nettoyer(texte):
    """Retire les espaces superflus et met en minuscules."""
    return " ".join(texte.split()).lower()

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

    st.header("Profil Utilisateur 👤")
    st.write("Gérez vos informations et votre collection de livres.")

    # Initialisation de la liste des livres
    if 'liste_livres' not in st.session_state:
        st.session_state['liste_livres'] = []

    # Champs de saisie
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom complet")
        age = st.number_input("Âge", min_value=0, max_value=120, step=1)
    with col2:
        genres_disponibles = ["Romance", "Thriller/Policier", "Jeunesse", "Manga", "Science-Fiction", "Fantastique", "Littérature Classique", "Littérature Afro"]
        genres_preferes = st.multiselect("Genres littéraires préférés (au moins 1)",
                                           genres_disponibles)

    st.divider()

    # Gestion de la liste de livres
    st.subheader("Ma Liste de Lectures (Min. 5 livres)")
    col_titre, col_auteur = st.columns([0.7, 0.3])
    with col_titre:
        nouveau_livre_titre = st.text_input("Titre du livre à ajouter")
    with col_auteur:
        nouveau_livre_auteur = st.text_input("Auteur")

    if st.button("Ajouter à ma liste"):
        if nouveau_livre_titre and nouveau_livre_auteur:
            titre_propre = nettoyer(nouveau_livre_titre)
            auteur_propre = nettoyer(nouveau_livre_auteur)
            livre_complet = {"titre": titre_propre, "auteur": auteur_propre}

            # Check if book (title+author) is already in the list
            if livre_complet not in st.session_state['liste_livres']:
                st.session_state['liste_livres'].append(livre_complet)
                st.success(f"Livre ajouté : {titre_propre} de {auteur_propre}")
            else:
                st.warning("Ce livre est déjà dans votre liste.")
        else:
            st.error("Veuillez entrer un titre ET un auteur valides.")

    # Affichage de la liste
    if st.session_state['liste_livres']:
        st.info(f"Livres ajoutés : {len(st.session_state['liste_livres'])}")
        for index, livre in enumerate(st.session_state['liste_livres']):
            st.text(f"{index + 1}. {livre['titre']} - {livre['auteur']}")

    st.divider()

    # Enregistrement
    if len(st.session_state['liste_livres']) < 5 or not genres_preferes:
        warning_msg = "⚠️ Vous devez ajouter au moins 5 livres"
        if not genres_preferes:
            warning_msg += " et sélectionner au moins un genre littéraire"
        warning_msg += " pour pouvoir enregistrer votre profil."
        st.warning(warning_msg)
    else:
        if st.button("Enregistrer le Profil"):
            try:
                nom_nettoye = nettoyer(nom)
                with open("profil_utilisateur.txt", "w", encoding="utf-8") as f:
                    f.write("#PROFIL#\n")
                    f.write(f"Nom: {nom_nettoye}\n")
                    f.write(f"Age: {age}\n")
                    f.write("#GENRES_LITTERAIRES#\n")
                    f.write(", ".join(genres_preferes) + "\n") # Store genres as comma-separated string
                    f.write("#LIVRES#\n")
                    # Write books as 'title - author'
                    for livre in st.session_state['liste_livres']:
                        f.write(f"{livre['titre']} - {livre['auteur']}\n")

                st.success("Profil enregistré avec succès dans 'profil_utilisateur.txt' !")
            except Exception as e:
                st.error(f"Erreur lors de l'enregistrement : {e}")

    st.divider()

    # --- Nouveau : Section Récapitulatif de Lecture ---
    st.markdown("<h3>📊 Votre Récapitulatif de Lecture</h3>", unsafe_allow_html=True)
    profile_path = "profil_utilisateur.txt"

    if os.path.exists(profile_path):
        try:
            st.markdown("<div class='section-perso'>", unsafe_allow_html=True)
            _, _, _, livres_from_file = utils_reco.extraire_profil_data(profile_path)

            if livres_from_file and len(livres_from_file) >= 1:
                # Auteur préféré
                p1_auteur, p2_auteurs = utils_reco.wrapped_auteur(profile_path, n=3)
                st.subheader("Vos Auteurs Préférés")
                st.write(p1_auteur)
                if p2_auteurs:
                    for key, value in p2_auteurs.items():
                        if key != 'top_1': # Already displayed by p1_auteur
                            st.write(value)

                # Genre préféré
                p3_genre, p4_genres = utils_reco.wrapped_genre(profile_path, n=3)
                st.subheader("Vos Genres Préférés")
                st.write(p3_genre)
                if p4_genres:
                    for key, value in p4_genres.items():
                        if key != 'top_1':
                            st.write(value)

                # Construire la base pour les fonctions dépendantes
                base_pour_recap = utils_reco.construire_base(livres_from_file)

                if base_pour_recap:
                    # Temps de lecture et ancienneté
                    p6_age, p7_anciens, p8_recents, p9_temps, p10_top_temps = utils_reco.wrapped_temps(base_pour_recap, n=3)
                    st.subheader("Votre Temps de Lecture")
                    st.write(p6_age)
                    st.write(p9_temps)
                    if p10_top_temps:
                        st.markdown(f"**Livres qui vous ont pris le plus de temps :** {p10_top_temps}")

                    st.subheader("Vos Lectures les plus Anciennes et Récentes")
                    st.markdown("**Vos 3 lectures les plus anciennes :**")
                    for key, value in p7_anciens.items():
                        st.write(value)
                    st.markdown("**Vos 3 lectures les plus récentes :**")
                    for key, value in p8_recents.items():
                        st.write(value)

                    # Score de Diversité
                    st.subheader("Votre Diversité de Lecture")
                    diversite = utils_reco.wrapped_diversite(profile_path)
                    st.write(diversite)

                    # Mood du lecteur
                    st.subheader("Votre Mood de Lecteur")
                    p11_mood, p12_mood_complement = utils_reco.wrapped_mood(profile_path)
                    st.write(p11_mood)
                    if p12_mood_complement:
                        st.write(p12_mood_complement)
                else:
                    st.info("Impossible de générer toutes les statistiques de lecture. Assurez-vous que les titres et auteurs de vos livres sont reconnaissables.")

            else:
                st.info("Ajoutez au moins un livre à votre profil pour voir votre récapitulatif de lecture.")
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erreur lors de la génération du récapitulatif : {e}")
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("Enregistrez votre profil (avec au moins 5 livres et un genre) pour accéder à votre récapitulatif de lecture.")
