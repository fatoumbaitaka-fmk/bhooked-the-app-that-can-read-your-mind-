
import streamlit as st
import os
# removed requests import as it's no longer needed for static library
import utils_reco
# removed GOOGLEBOOKS_API_KEY import as it's no longer needed
import random

def app():
    # Retrieve global settings from session_state
    bg_color = st.session_state.get('bg_color', '#F9F7F2')
    accent_bar = st.session_state.get('accent_bar', '#D4AF37')
    # est_connecte is no longer directly used for displaying the personalized section
    age_lecteur = st.session_state.get('age_lecteur', 20)

    # Dark mode warning with custom styling for better visibility
    st.markdown("""
        <div style="background-color: #FFF3CD; color: #664D03; padding: 10px; border-radius: 5px; border: 1px solid #FFECB5; text-align: center;">
            ⚠️ Ce site n'est pas optimisé pour le mode sombre. Veuillez adapter vos paramètres pour une meilleure expérience de lecture.
        </div>
        """, unsafe_allow_html=True)

    # --- 1. BASE DE DONNÉES (L'ACCUEIL AVEC VRAIS LIVRES) ---
    # Hardcoded library of books for each genre
    bibliotheque_complete = {
        "Romance 💖": [
        {"titre": "Orgueil et Préjugés", "auteur": "Jane Austen", "img": "https://m.media-amazon.com/images/I/71E+DX8sc5L._SL1491_.jpg"},
        {"titre": "Jamais plus", "auteur": "Colleen Hoover", "img":"https://m.media-amazon.com/images/I/81tFVqLBpRL._SL1500_.jpg"},
        {"titre": "Captive", "auteur": "Sarah Rivens", "img": "https://www.bruna.nl/images/active/carrousel/fullsize/9789464103533_front.jpg"},
        {"titre": "After", "auteur": "Anna Todd", "img": "https://m.media-amazon.com/images/I/61f098chyyL._SL1500_.jpg"},
        {"titre": "Valentina", "auteur": "Arza Reed", "img": "https://m.media-amazon.com/images/I/81WUwFpzGrL._SL1500_.jpg"}
    ],
    "Policier 🕵️‍♂️": [
        {"titre": "Dix petits nègres", "auteur": "Agatha Christie", "img": "https://i.ebayimg.com/images/g/RN0AAOSwxxZhXc1Z/s-l1600.webp"},
        {"titre": "Sherlock Holmes", "auteur": "A. Conan Doyle", "img": "https://m.media-amazon.com/images/I/51-cIrKicXL._SY445_SX342_ML2_.jpg"},
        {"titre": "Code 93", "auteur": "Olivier Norek", "img": "https://m.media-amazon.com/images/I/71C4AKJ5VsL._SY342_.jpg"},
        {"titre": "Glacé", "auteur": "Bernard Minier", "img": "https://images2.medimops.eu/product/6bcc53/M02845635028-880px.webp"},
        {"titre": "Harry Quebert", "auteur": "Joël Dicker", "img": "https://m.media-amazon.com/images/I/41x7MkVv3lL._SY445_SX342_ML2_.jpg"}
    ],
    "Humour 😂": [
        {"titre": "Bridget Jones", "auteur": "Helen Fielding", "img": "https://m.media-amazon.com/images/I/61aHGvFh8+L._SY342_.jpg"},
        {"titre": "Demain j'arrête !", "auteur": "G. Legardinier", "img": "https://m.media-amazon.com/images/I/41KRiV01sHL._SY445_SX342_ML2_.jpg"},
        {"titre": "Complètement cramé", "auteur": "G. Legardinier", "img": "https://m.media-amazon.com/images/I/512jrn60ixL._SY342_.jpg"},
        {"titre": "H2G2", "auteur": "Douglas Adams", "img": "https://m.media-amazon.com/images/I/515ogfBPO5L._SY445_SX342_ML2_.jpg"},
        {"titre": "Le Vieux qui ne voulait pas", "auteur": "J. Jonasson", "img": "https://m.media-amazon.com/images/I/51zX6qfg8qL._SY445_SX342_ML2_.jpg"}
    ],
    "Jeunesse 🧸": [
        {"titre": "Harry Potter", "auteur": "J.K. Rowling", "img": "https://m.media-amazon.com/images/I/71N6SgkNlcL._SY342_.jpg"},
        {"titre": "Le Petit Prince", "auteur": "St-Exupéry", "img": "https://m.media-amazon.com/images/I/710wth0vXZL._SY342_.jpg"},
        {"titre": "Journal dégonflé", "auteur": "Jeff Kinney", "img": "https://m.media-amazon.com/images/I/819MvXA8zlL._SL1500_.jpg"},
        {"titre": "Percy Jackson", "auteur": "Rick Riordan", "img": "https://m.media-amazon.com/images/I/816xbkCic4L._SL1500_.jpg"},
        {"titre": "Narnia", "auteur": "C.S. Lewis", "img": "https://m.media-amazon.com/images/I/510R5kj659L._SY445_SX342_ML2_.jpg"}
    ],
    "Science-fiction 🚀": [
        {"titre": "Dune", "auteur": "Frank Herbert", "img": "https://m.media-amazon.com/images/I/61pHGBNl9NL._SY342_.jpg"},
        {"titre": "1984", "auteur": "George Orwell", "img": "https://m.media-amazon.com/images/I/71Y9X7FYkcL._SY342_.jpg"},
        {"titre": "Fondation", "auteur": "Isaac Asimov", "img": "https://m.media-amazon.com/images/I/71hHEeSi48L._SY342_.jpg"},
        {"titre": "Fahrenheit 451", "auteur": "Ray Bradbury", "img": "https://m.media-amazon.com/images/I/71b674P2aKL._SY342_.jpg"},
        {"titre": "Le Meilleur des mondes", "auteur": "Aldous Huxley", "img": "https://img4.labirint.ru/rc/8c54fa2d75e88769d631db4300c135c1/363x561q80/books100/992262/cover.jpg?1712125584"}
    ],
    "Fantastique 🪄": [
        {"titre": "Le Seigneur des Anneaux", "auteur": "Tolkien", "img": "https://m.media-amazon.com/images/I/81BR5SaDYZL._SY342_.jpg"},
        {"titre": "Le Sorceleur", "auteur": "A. Sapkowski", "img": "https://m.media-amazon.com/images/I/71lMrQva2yL._SY342_.jpg"},
        {"titre": "Twilight", "auteur": "Stephenie Meyer", "img": "https://m.media-amazon.com/images/I/91VSuOjN3RL._SY342_.jpg"},
        {"titre": "Eragon", "auteur": "C. Paolini", "img": "https://m.media-amazon.com/images/I/810YXT+S6sL._SY342_.jpg"},
        {"titre": "À la croisée des mondes", "auteur": "Philip Pullman", "img": "https://media.senscritique.com/media/000011264444/source_big/A_la_croisee_des_mondes_L_integrale.jpg"}
    ],
    "Littérature Classique 📜": [
        {"titre": "Les Misérables", "auteur": "Victor Hugo", "img": "https://m.media-amazon.com/images/I/61Jx5wL-LHL._SY342_.jpg"},
        {"titre": "L'Étranger", "auteur": "Albert Camus", "img": "https://media.senscritique.com/media/000007143411/source_big/L_Etranger.jpg"},
        {"titre": "Madame Bovary", "auteur": "G. Flaubert", "img": "https://m.media-amazon.com/images/I/81Yw4c0iILL._SY342_.jpg"},
        {"titre": "Le Rouge et le Noir", "auteur": "Stendhal", "img": "https://upload.wikimedia.org/wikipedia/commons/7/71/Le_rouge_et_le_noir_1831.JPG"},
        {"titre": "Bel-Ami", "auteur": "Maupassant", "img": "https://m.media-amazon.com/images/I/71Zm+3tnhOL._SL1500_.jpg"}
    ],
        "Littérature Afro 🇦": [
            {"titre": "Une vie de boy", "auteur": "Ferdinand Oyono", "img": "https://m.media-amazon.com/images/I/713sM2EMGsL._SL1311_.jpg"},
            {"titre": "Le ketala", "auteur": "Fatou Diom", "img": "https://m.media-amazon.com/images/I/61e0X9DN30L._SL1051_.jpg"},
            {"titre": "Les impatientes", "auteur": "Djaïli Amadou Amal", "img": "https://static.fnac-static.com/multimedia/PE/Images/FR/NR/48/5e/d1/13721160/1540-1/tsp20250910084300/Les-impatientes.jpg"},
            {"titre": "Une si longue lettre", "auteur": "Mariama Ba", "img": "https://m.media-amazon.com/images/G/01/apparel/rcxgs/tile._CB483369110_.gif"},
            {"titre": "Névralgies", "auteur": "Léon Gontran Damas", "img": "https://m.media-amazon.com/images/I/51hM6S5kWcL.jpg"}
        ],
        "Éducation 💡": [
        {"titre": "Père riche Père pauvre", "auteur": "Robert Kiyosaki", "img": "https://m.media-amazon.com/images/I/616inIm4FZL._SY342_.jpg"},
        {"titre": "Sapiens", "auteur": "Yuval Noah Harari", "img": "https://m.media-amazon.com/images/I/717sO7vkyUL._SY342_.jpg"},
        {"titre": "Un rien peut tout changer", "auteur": "James Clear", "img": "https://i0.wp.com/deenshop.be/wp-content/uploads/2022/09/Un-rien-peut-tout-changer-scaled.jpeg?fit=1597%2C2560&ssl=1"},
        {"titre": "Devenez riche", "auteur": "Ramit Sethi", "img": "https://media.s-bol.com/r0jRjqjlwk6W/541x840.jpg"},
        {"titre": "Les 4 accords Toltèques", "auteur": "Don Miguel Ruiz", "img": "https://m.media-amazon.com/images/I/71-p+XR1q0L._SY342_.jpg"}
    ]
    }

    # --- 2. STYLE CSS ---
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

    # --- 3. ENTÊTE ---
    st.markdown("<p style='text-align:center; font-size:40px; margin-bottom:0;'>👑</p>", unsafe_allow_html=True)
    st.markdown('<p class="titre-royal">bhooked</p>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">L\'application qui lit dans tes pensées ✨</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:30px; margin-top:10px;'>🌿</p>", unsafe_allow_html=True)

    # --- 4. SECTION RECOMMANDATIONS DYNAMIQUES (basées sur le profil) ---
    profile_path = "profil_utilisateur.txt"
    if os.path.exists(profile_path):
          nom_profil, age_profil, genres_profil, livres_profil = utils_reco.extraire_profil_data(profile_path)

          st.markdown("<div class='section-perso'>", unsafe_allow_html=True)
          st.markdown(f"✨ Spécialement pour vous {nom_profil}")

          # --- Recommandations par Auteur Préféré ---
          st.markdown("#### 📚 D'autres livres de vos auteurs favoris")
          if livres_profil and len(livres_profil) >= 5:
              auteur_prefere, _ = utils_reco.auteur_principal(livres_profil)
              if auteur_prefere != "Aucun auteur":
                  st.write(f"Puisque vous aimez {auteur_prefere}, voici d'autres titres :")
                  recos_auteur = utils_reco.recommandations_auteurs(profile_path, num_results=3)
                  if recos_auteur:
                      cols = st.columns(3)
                      for i, reco in enumerate(recos_auteur):
                          with cols[i]:
                              st.markdown(f"""
                              <div class="book-card">
                                  <img src="{reco['img']}" class="book-img">
                                  <div class="book-title">{reco['titre']}</div>
                                  <div class="book-author">{reco['auteur']}</div>
                              </div>
                              """, unsafe_allow_html=True)
                  else:
                      st.info(f"Aucune recommandation trouvée pour l\'auteur {auteur_prefere}.")
              else:
                  st.info("Ajoutez au moins 5 livres à votre profil pour identifier vos auteurs favoris et recevoir des recommandations.")
          else:
              st.info("Veuillez ajouter au moins 5 livres à votre profil pour identifier vos auteurs favoris et recevoir des recommandations.")

          # --- Recommandations par Genres Préférés ---
          st.markdown("#### ✨ Suggestions basées sur vos genres")
          if genres_profil:
              genre_favori_user = utils_reco.genre_favori(genres_profil)
              st.write(f"Vous aimez le genre '{genre_favori_user}' ! Voici quelques pépites :"
              )
              recos_genre = utils_reco.recommander_par_genre(genre_favori_user, num_results=3)
              if recos_genre:
                  cols = st.columns(3)
                  for i, reco in enumerate(recos_genre):
                      with cols[i]:
                          st.markdown(f"""
                          <div class="book-card">
                              <img src="{reco['img']}" class="book-img">
                              <div class="book-title">{reco['titre']}</div>
                              <div class="book-author">{reco['auteur']}</div>
                          </div>
                          """, unsafe_allow_html=True)
              else:
                  st.info(f"Aucune recommandation trouvée pour le genre {genre_favori_user}.")
          else:
              st.info("Sélectionnez vos genres littéraires préférés dans votre profil pour recevoir des recommandations.")

          # --- Recommandations Aléatoires (pour la découverte) ---
          st.markdown("#### 💡 Pour la découverte")
          st.write("Envie d'explorer de nouveaux horizons ?")
          recos_aleatoires = utils_reco.recommandations_aleatoires(num_results=2)
          if recos_aleatoires:
              cols = st.columns(2)
              for i, reco in enumerate(recos_aleatoires):
                  with cols[i]:
                      st.markdown(f"""
                      <div class="book-card">
                          <img src="{reco['img']}" class="book-img">
                          <div class="book-title">{reco['titre']}</div>
                          <div class="book-author">{reco['auteur']}</div>
                      </div>
                      """, unsafe_allow_html=True)
          else:
              st.info("Impossible de générer des recommandations aléatoires pour le moment.")

          st.markdown("</div>", unsafe_allow_html=True)
    else:
          st.markdown("<div class='section-perso'>", unsafe_allow_html=True)
          st.markdown("<h3>✨ Créez votre profil pour des recommandations personnalisées !</h3>", unsafe_allow_html=True)
          st.markdown("</div>", unsafe_allow_html=True)

    # --- 5. AFFICHAGE DE LA BIBLIOTHÈQUE PAR DÉFAUT ---
    # Filtrage par âge : si - de 13 ans, on ne montre que 3 genres
    if age_lecteur < 13:
          genres_a_afficher = ["Jeunesse 🧸", "Humour 😂", "Éducation 💡"]
    else:
          genres_a_afficher = list(bibliotheque_complete.keys())

    for genre in genres_a_afficher:
          st.markdown(f"### {genre}")
          livres = bibliotheque_complete[genre]
          cols = st.columns(5)
          for i in range(min(len(livres), 5)): # Corrected loop range
              with cols[i]:
                  st.markdown(f"""
                  <div class="book-card">
                      <img src="{livres[i]['img']}" class="book-img">
                      <div class="book-title">{livres[i]['titre']}</div>
                      <div class="book-author">{livres[i]['auteur']}</div>
                  </div>
                  """, unsafe_allow_html=True)

    st.markdown("<br><br><p style='text-align:center;'>🌿 🌸 🌿</p>", unsafe_allow_html=True)
