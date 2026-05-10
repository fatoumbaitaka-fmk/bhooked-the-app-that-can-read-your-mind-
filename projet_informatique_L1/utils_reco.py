
import requests
import random
import re
from datetime import datetime
import statistics
import os # Import os for environment variables
import google.generativeai as genai

#LES FONCTIONS À UTILISER DANS LE CODE PRINCIPAL SONT LES TROIS FONCTIONS DE RECOMMENDATION
#----- RECOMMANDATIONS: AUTEURS, GENRES, ALÉATOIRES

#CE QU'IL MANQUE: Il faut implanter l'IA dans les fonctions genre_via_ia et traduire_titre. Il faut implémenter traduire_titre avant que les fonctions de recommandations retournent le résultats

# --- Google API Configuration ---
# Clé API de Google Books pour avoir des résultats de requêtes stables
GOOGLEBOOKS_API_KEY = os.environ.get('GOOGLE_BOOKS_API_KEY')

# GOOGLE_API_KEY for Gemini, also from Colab secrets
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

# --- Genre Lists ---
FICTION_GENRES = [
    "Fiction", "Literary Fiction", "Classic", "Classics", "Contemporary", "General Fiction"
]

SFF_GENRES = [
    "Science Fiction", "Sci-Fi", "Fantasy", "Epic Fantasy", "High Fantasy", "Urban Fantasy",
    "Dark Fantasy", "Sword and Sorcery", "Space Opera", "Dystopian", "Utopia",
    "Post-Apocalyptic", "Cyberpunk", "Steampunk", "Time Travel", "Alternate History"
]

CRIME_GENRES = [
    "Mystery", "Detective", "Crime", "Thriller", "Psychological Thriller", "Suspense",
    "Noir", "Police Procedural", "Legal Thriller", "Political Thriller", "Espionage", "Spy Fiction"
]

ROMANCE_GENRES = [
    "Romance", "Contemporary Romance", "Historical Romance", "Paranormal Romance",
    "Romantic Suspense", "Chick Lit", "Love Stories", "Dark Romance",
]

HORREUR_GENRES = [
    "Horror", "Gothic", "Supernatural", "Ghost Stories", "Occult", "Paranormal", "Dark Fiction"
]

AVENTURE_GENRES = [
    "Adventure", "Action", "War", "Military", "Survival", "Western", "Sea Stories", "Exploration"
]

HISTORIQUE_GENRES = [
    "Historical Fiction", "History", "Historical", "War Stories", "Ancient History",
    "Medieval", "Modern History"
]

PHILOSOPHIE_GENRES = [
    "Philosophy", "Ethics", "Metaphysics", "Logic", "Existentialism", "Political Philosophy",
    "Political Science"
]

NONFICTION_GENRES = [
    "Nonfiction", "Biography", "Autobiography", "Memoir", "Essays", "Essay", "Journalism", "True Crime"
]

SCIENCE_GENRES = [
    "Science", "Physics", "Biology", "Chemistry", "Astronomy", "Mathematics",
    "Computer Science", "Artificial Intelligence", "Technology", "Engineering"
]

SELF_GENRES = [
    "Self-Help", "Personal Development", "Psychology", "Motivation", "Productivity",
    "Mindfulness", "Well-being"
]

RELIGION_GENRES = [
    "Religion", "Spirituality", "Christianity", "Islam", "Buddhism", "Theology",
    "Mythology", "Folklore"
]

ART_GENRES = [
    "Art", "Music", "Cinema", "Photography", "Design", "Architecture", "Performing Arts"
]

EDU_GENRES = [
    "Education", "Language", "Linguistics", "Writing", "Grammar", "Study Aids"
]

JEUNESSE_GENRES = [
    "Children", "Juvenile Fiction", "Young Adult", "YA Fiction", "Teen", "Coming of Age"
]

COUNTRIES = [
    "French Drama", "French Comedy", "French Literature", "Russian Literature",
    "Spanish Literature", "Italian Literature", "Portuguese Literature",
    "German Literature", "English Literature", "Chinese Literature", "Japanese Literature",
    "Korean Literature", "Arabic Literature", "Greek Literature", "Hebrew Literature",
    "Afro-American Literature", "Carribean Literature", "Jamaican Literature",
    "European Literature", "African Literature", "American Literature", "Asian Literature",
    "Pacific Literature", "Nigerian Literature", "South African Literature",
    "Egyptian Literature", "Kenyan Literature", "Senegalese Literature",
    "Moroccan Literature", "Algerian Literature", "Ghanaian Literature",
    "Ethiopian Literature"

]

THEMES = [
    "Love", "Friendship", "Family", "Relationship", "Magic", "Fighting", "School",
    "University", "Office"

]

AUTRES_GENRES = [
    "Drama", "Comedy", "Tragedy", "Tragicomedy", "Humour", "Humor", "Literary Criticism",
    "Criticism", "Manga", "Poems", "Poesy", "Poetry", "Play", "Novel", "Romanticism",
    "Lyricism", "Epic", "Ode", "Novella", "Novellette", "Courte Nouvelle", "Short Story", "Satire",
    "Mythology", "Collections", "Documentary", "Sociology", "Economics"
]

GENRES_VALIDES = (
    FICTION_GENRES + SFF_GENRES + CRIME_GENRES + ROMANCE_GENRES + HORREUR_GENRES +
    AVENTURE_GENRES + HISTORIQUE_GENRES + PHILOSOPHIE_GENRES + NONFICTION_GENRES +
    SCIENCE_GENRES + SELF_GENRES + RELIGION_GENRES + ART_GENRES + EDU_GENRES +
    JEUNESSE_GENRES + COUNTRIES + THEMES + AUTRES_GENRES
)

TRADUCTION_GENRES = {
    "Fiction": "Fiction", "Literary Fiction": "Fiction", "Classic": "Littérature Classique",
    "Classics": "Littérature Classique", "Contemporary": "Littérature Contemporaine",
    "General Fiction": "Fiction", "Science Fiction": "Science Fiction", "Sci-Fi": "Science Fiction",
    "Fantasy": "Fantasy", "Epic Fantasy": "Fantasy Épique", "High Fantasy": "Fantasy Épique",
    "Urban Fantasy": "Fantasy Urbaine", "Dark Fantasy": "Dark Fantasy", "Sword and Sorcery": "Épée et Sorcellerie",
    "Space Opera": "Space Opera", "Dystopian": "Dystopie", "Utopian": "Utopie",
    "Post-Apocalyptic": "Post Apocalyptique", "Cyberpunk": "Cyberpunk", "Steampunk": "Steampunk",
    "Time Travel": "Voyage dans le Temps", "Alternate History": "Uchronie", "Mystery": "Mystère",
    "Detective": "Enquête", "Crime": "Crime", "Thriller": "Thriller", "Psychological Thriller": "Thriller Psychologique",
    "Suspense": "Suspens", "Noir": "Roman Noir", "Police Procedural": "Procédure Policière",
    "Legal Thriller": "Thriller Juridique", "Espionage": "Espionnage", "Spy Fiction": "Espionnage",
    "Romance": "Romance", "Contemporary Romance": "Romance Contemporaine", "Historical Romance": "Romance Historique",
    "Paranormal Romance": "Romance Paranormale", "Romantic Suspense": "Romance Thriller",
    "Chick Lit": "Chick Lit", "Love Stories": "Romance", "Dark Romance": "Dark Romance",
    "Horror": "Horreur", "Gothic": "Roman Gothique", "Supernatural": "Surnaturel",
    "Ghost Stories": "Histoires de Fantômes", "Occult": "Occulte", "Paranormal": "Paranormal",
    "Dark Fiction": "Récit Sombre", "Adventure": "Aventure", "Action": "Action", "War": "Roman de Guerre",
    "Military": "Roman Militaire", "Survival": "Survie", "Western": "Western", "Sea Stories": "Fiction Maritime",
    "Exploration": "Exploration", "Historical Fiction": "Fiction Historique", "History": "Non-Fiction Historique",
    "Historical": "Non-Fiction Historique", "War Stories": "Récits de Guerre", "Ancient History": "Antiquité",
    "Medieval": "Récit Médiéval", "Modern History": "Récit d'Histoire Moderne", "Philosophy": "Philosophie",
    "Ethics": "Éthique", "Metaphysics": "Métaphysique", "Logic": "Logique", "Existentialism": "Existentialisme",
    "Political Philosophy": "Philosophie Politique", "Political Science": "Sciences Politiques",
    "Nonfiction": "Non-Fiction", "Biography": "Biographie", "Autobiography": "Autobiographie", "Memoir": "Mémoires",
    "Essays": "Essai", "Essay": "Essai", "Journalism": "Journalisme", "True Crime": "True Crime",
    "Science": "Sciences", "Physics": "Physique", "Biology": "Biologie", "Chemistry": "Chimie",
    "Astronomy": "Astronomie", "Mathematics": "Mathématiques", "Computer Science": "Informatique",
    "Artificial Intelligence": "Intelligence Artificielle", "Technology": "Technologie", "Engineering": "Ingénierie",
    "Self-Help": "Développement Personnel", "Personal Development": "Développement Personnel",
    "Psychology": "Psychologie", "Motivation": "Motivation", "Productivity": "Productivité",
    "Mindfulness": "Pleine Conscience", "Well-being": "Bien-être", "Religion": "Religion",
    "Spirituality": "Spiritualité", "Christianity": "Christianisme", "Islam": "Islam",
    "Judaism": "Judaïsme", "Buddhism": "Bouddhisme", "Theology": "Théologie", "Mythology": "Mythologie",
    "Folklore": "Folklore", "Art": "Art", "Music": "Musique", "Cinema": "Cinéma", "Photography": "Photographie",
    "Design": "Design", "Architecture": "Architecture", "Performing Arts": "Arts de la Scène",
    "Education": "Éducation", "Language": "Langues", "Linguistics": "Linguistique", "Writing": "Écriture",
    "Grammar": "Grammaire", "Study Aids": "Aides à l'Étude", "Children": "Jeunesse",
    "Juvenile Fiction": "Fiction Jeunesse", "Young Adult": "Young Adult", "YA Fiction": "Young Adult",
    "Teen": "Adolescent", "Coming of Age": "Roman d'Initiation", "French Drama": "Théâtre Français",
    "French Comedy": "Comédie Française", "French Literature": "Littérature Française",
    "Russian Literature": "Littérature Russe", "Spanish Literature": "Littérature Espagnole",
    "Italian Literature": "Littérature Italienne", "Portuguese Literature": "Littérature Portugaise",
    "German Literature": "Littérature Allemande", "English Literature": "Littérature Anglaise",
    "European Literature": "Littérature Européenne", "Arabic Literature": "Littérature Arabe",
    "Greek Literature": "Littérature Grecque", "Hebrew Literature": "Littérature Hébraïque",
    "Nigerian Literature": "Littérature Nigériane", "South African Literature": "Littérature Sud-Africaine",
    "Egyptian Literature": "Littérature Égyptienne", "Kenyan Literature": "Littérature Kenyane",
    "Senegalese Literature": "Littérature Sénégalaise", "Moroccan Literature": "Littérature Marocaine",
    "Algerian Literature": "Littérature Algérienne", "Ghanaian Literature": "Littérature Ghanéenne",
    "Ethiopian Literature": "Littérature Éthiopienne", "African Literature": "Littérature Africaine",
    "Lebanese Literature": "Littérature Libanaise", "Chinese Literature": "Littérature Chinoise",
    "Japanese Literature": "Littérature Japonaise", "Korean Literature": "Littérature Coréenne",
    "Asian Literature": "Littérature Asiatique", "American Literature": "Littérature Américaine",
    "Afro-American Literature": "Littérature Afro-Américaine", "Carribean Literature": "Littérature Caribéenne",
    "Jamaican Literature": "Littérature Jamaïcaine", "Pacific Literature": "Littérature du Pacifique",
    "Love": "Amour", "Friendship": "Amitié", "Family": "Famille", "Relationship": "Relations",
    "Magic": "Magie", "Fighting": "Combat", "School": "École", "University": "Université",
    "Office": "Bureau", "Drama": "Drame", "Comedy": "Comédie", "Tragedy": "Tragédie",
    "Tragicomedy": "Tragi-Comédie", "Humour": "Humour", "Humor": "Humour",
    "Literary Criticism": "Critique Littéraire", "Criticism": "Critique Littéraire",
    "Manga": "Manga", "Poems": "Poésie", "Poesy": "Poésie", "Poetry": "Poésie",
    "Play": "Pièce de Théâtre", "Novel": "Roman", "Romanticism": "Romantisme",
    "Lyricism": "Lyrisme", "Epic": "Épopée", "Ode": "Ode", "Novella": "Nouvelle Longue",
    "Novellette": "Courte Nouvelle", "Short Story": "Courte Histoire", "Satire": "Satire",
    "Collections": "Collections", "Documentary": "Documentaire", "Sociology": "Sociologie",
    "Economics": "Économie", "Cooking": "Cuisine", "Travel": "Voyage", "Food": "Gastronomie", "Political Thriller": "Thriller Politique",
}

page= 275
vitesse= 225
PAGES_PER_MIN = vitesse / page

MOODS = {
    "Dans un autre monde ✨":["Fiction", "Utopie","Supernaturel", "Mythologie", "Jeunesse",
                             "Roman d'Initiation", "Amitié", "Manga", "Roman", "Épopée"],

    "Romance Addict 💖": ["Romance", "Romance Historique", "Romance Paranormal",
                          "Romance Thriller", "Chick Lit", "Dark Romance", "Roman Gothique",
                          "Amour", "Drame", "Roman"],

    "Détective🕵️": ["Mystère", "Enquête", "Crime", "Suspens", "Roman Noir",
                     "Procédure Policière", "Thriller Juridique", "True Crime",
                     "Roman"],

    "Chasseur de frissons 🔪": ["Mystère", "Crime", "Thriller", "Thriller Psychologique",
                                "Suspens", "Thriller Juridique", "Romance Paranormale",
                                "Romance Thriller", "Horreur", "Paranormal", "Survie", "True Crime",
                                "Roman"],

    "Explorateur 🌌": ["Science-Fiction", "Voyage dans le Temps", "Supernaturel",
                       "Aventure", "Exploration", "Astronomie", "Roman"],

    "Dans un autre monde 🧚": ["Fantasy", "Fantasy Épique", "Fantasy Urbaine",
                               "Supernaturel", "Roman"],

    "D'une autre époque 📚": ["Steampunk", "Voyage dans le Temps",
                              "Romance Historique", "Roman Gothique", "Roman de Guerre",
                              "Western", "Fiction Historique", "Non-Fiction Historique",
                              "Antiquité", "Récit Médiéval", "Comédie", "Tragédie",
                              "Théâtre", "Roman", "Littérature Romantique"],

    "Man VS🏔️": ["Roman de Guerre", "Survie", "Fiction Maritime", "Non-Fiction Historique",
               "Récit de l'Époque Moderne", "Sciences Politiques", "Non-Fiction"],

    "Nerd 🤓": ["Littérature Classique", "Fantasy Épique", "Dark Fantasy",
                "Épée et Sorcellerie", "Space Opera", "Cyberpunk", "Steampunk",
                "Roman Gothique", "Aventure", "Roman de Guerre", "Antiquité",
                "Récit Médiéval", "Récit de l'Époque Moderne", "Philosophie et Éthique",
                "Sciences", "Mythologie", "Folklore", "Théâtre Français",
                "Comédie Francaise", "Comédie", "Tragédie", "Drame", "Manga", "Poésie",
                "Théâtre", "Roman", "Littérature Romantique", "Épopée"],

    "Nerd Type 1 🤓": ["Littérature Classique", "Roman Gothique", "Antiquité",
                       "Récit Médiéval", "Récit de l'Époque Moderne", "Philosophie et Éthique",
                       "Mythologie", "Théâtre Français", "Comédie Francaise",
                       "Comédie", "Tragédie", "Poésie", "Théâtre", "Roman",
                       "Littérature Romantique", "Épopée"],

    "Nerd Type 2 🤓": ["Fantasy Épique", "Dark Fantasy", "Épée et Sorcellerie",
                       "Space Opera", "Cyberpunk", "Steampunk", "Aventure",
                       "Roman de Guerre", "Sciences", "Folklore", "Manga", "Roman",
                       "Épopée"],

    "Curieux 🌍": ["Antiquité", "Récit Médiéval", "Non-Fiction Historique",
                   "Philosophie et Éthique", "Essai Logique", "Sciences Politiques",
                   "Non-Fiction", "Essai", "Journalisme", "Sciences", "Physique",
                   "Biologie", "Chimie", "Astronomie", "Mathématiques", "Informatique",
                   "Technologie", "Psychologie", "Théologie", "Mythologie", "Folklore",
                   "Musique", "Cinéma", "Design", "Architecture", "Éducation", "Langues et Linguistique",
                   "Littérature Française", "Littérature Russe", "Littérature Espagnole",
                   "Littérature Anglaise", "Littérature Européenne", "Littérature Arabe",
                   "Littérature Grecque", "Littérature Hebraïque", "Littérature Nigériane",
                   "Littérature SudAfricaine", "Littérature Egyptienne", "Littérature Kenyane",
                   "Littérature Sénégalaise", "Littérature Marocaine", "Littérature Algériene",
                   "Littérature Ghanéenne", "Littérature Ethiopienne", "Littérature Africaine",
                   "Littérature Libanaise", "Littérature Chinoise", "Littérature Japonaise",
                   "Littérature Coréenne", "Littérature Asiatique", "Littérature Américaine",
                   "Littérature Afro-Américaine", "Littérature Caribéenne", "Littérature Jamaïcaine",
                   "Littérature du Pacifique", "Critique Littéraire", "Théâtre", "Épopée",
                   "Documentaire", "Sociology", "Économie"],

    "Étudiant en Sciences 🎓": ["Essai Logique", "Essai", "Sciences", "Physique",
                             "Biologie", "Chimie", "Astronomie", "Mathématiques",
                             "Informatique", "Technologie", "Sciences de l'Ingénieur"],

    "Étudiant en Lettres 🎓": ["Non-Fiction Historique", "Antiquité", "Récit Médiéval",
                            "Récit de l'Époque Moderne", "Philosophie et Éthique",
                            "Essai Logique", "Essai", "Psychologie", "Religion",
                            "Théologie","Art", "Langues et Linguistique", "Comédie",
                            "Tragédie", "Poésie", "Théâtre", "Sociology"],

    "Apprenti de la vie 💡": ["Développement Personnel", "Psychologie", "Religion",
                              "Spiritualité", "Éducation", "Cuisine", "Voyage","Cuisine"],

    "Baka 🥷🐺": ["Dark Fantasy", "Dystopie", "Crime", "Thriller Psychologique",
                   "Romance Thriller", "Dark Romance", "Récit Sombre", "Survie",
                   "True Crime", "Manga"],

    "Girls' Girl 💅🖤": ["Romance", "Romance Paranormale", "Romance Thriller",
                     "Chick Lit", "Crime", "Thriller", "Thriller Psychologique",
                     "Dark Romance", "Roman Gothique", "Supernaturel", "Paranormal",
                     "True Crime", "Mythologie", "Young Adult", "Manga", "Roman"],

    "Testosterone Lit 🦾🧭": ["Romance", "Action", "Roman de Guerre", "Survie", "Western",
                         "True Crime", "Mythologie", "Manga", "Roman"],

    "Univers Alternatifs 🌀": ["Dystopie", "Utopie", "Uchronie","Supernaturel"],

    "Futur Sombre 🌑": ["Dystopie", "Post Apocalyptique", "Cyberpunk", "Récit Sombre",
                        "Survie"],

    "Dans l'ombre 🕶️":["Espionnage", "Thriller", "Thriller Politique", "Action"],

    "Haute Tension 🧨": ["Espionnage", "Thriller", "Roman Noir",
                         "Thriller Politique", "Suspens", "Romance Thriller", "Aventure",
                         "Action", "Survie", "Roman de Guerre"],
    "Artiste 🖊️": ["Art", "Musique", "Cinéma", "Photographie", "Design", "Architecture",
                "Performance", "Théâtre Français", "Comédie Francaise", "Amour",
                "Drame", "Comédie", "Tragédie", "Tragi-Comédie", "Poésie", "Théâtre",
                "Roman", "Littérature Romantique", "Littérature Lyrique", "Épopée", "Ode"],
    "La Vraie Vie 📰": ["Non-Fiction", "Art", "Biographie", "Philosophie et Éthique",
                     "Autobiographie", "Mémoire", "Essai"],
    "Lecteur Classique 📜":["Fiction", "Jeunesse", "Adolescent", "Young Adult", "Roman d'Initiation",
                         "Théâtre Français", "Comédie Francaise", "Drame", "Comédie", "Tragédie",
                         "Critique Littéraire", "Poésie", "Théâtre", "Roman", "Épopée", "Ode",
                         "Novella", "Nouvelle", "Collections Littéraires"],
    "Littérature du Monde 🗺️": ["Littérature Française", "Littérature Russe", "Littérature Espagnole",
                             "Littérature Italienne", "Littérature Portugaise", "Littérature Allemande",
                             "Littérature Anglaise", "Littérature Européenne", "Littérature Arabe",
                             "Littérature Grecque", "Littérature Hebraïque", "Littérature Nigériane",
                             "Littérature SudAfricaine", "Littérature Egyptienne", "Littérature Kenyane",
                             "Littérature Sénégalaise", "Littérature Marocaine", "Littérature Algériene",
                             "Littérature Ghanéenne", "Littérature Ethiopienne", "Littérature Africaine",
                             "Littérature Libanaise", "Littérature Chinoise", "Littérature Japonaise",
                             "Littérature Coréenne", "Littérature Asiatique", "Littérature Américaine",
                             "Littérature Afro-Américaine", "Littérature Caribéenne", "Littérature Jamaïcaine",
                             "Littérature du Pacifique"]
}

# --- Utility Functions (from TnUY1ns3NY25) ---
GENRES_optim = [g for g in GENRES_VALIDES if len(g.split()) <= 2]

def normaliser_texte(texte):
    """Normalise le texte en le mettant en minuscules et en supprimant les caractères non alphanumériques."""
    if not texte: return ""
    texte = texte.lower()
    texte = re.sub(r"[^a-z0-9àâéèêëîïôûùç]+", " ", texte)
    return texte.strip()

def matching_partiel_genre(gnr):
    """Trouve une correspondance partielle pour gnr dans GENRES-VALIDES"""
    if gnr == "Inconnu":
        return "Inconnu"
    genre=normaliser_texte(gnr)
    bestmatch= None
    bestscore=0

    for g in GENRES_VALIDES:
        valide_nor = normaliser_texte(g)

        if genre in valide_nor or valide_nor in genre:
            score = min(len(genre), len(valide_nor))

            if score > bestscore:
                bestscore = score
                bestmatch = g

    if bestmatch == None:
        return gnr
    return bestmatch

def traduction_genre(genre):
    """Traduis les genres avec le dictionnaire TRADUCTION GENRE"""
    if genre == "Inconnu":
        return "Inconnu"
    return TRADUCTION_GENRES.get(genre, genre)

def traiter_genre(genres):
    """Traitement des genres pour avoir des informations plus homogènes"""
    genres_traites = []
    for g in genres:
        g = matching_partiel_genre(g)
        g = traduction_genre(g)
        genres_traites.append(g)
    return genres_traites

def traduire_titre(titre):
    """Traduction du livre en français en utilisant Gemini API."""
    if not titre: return "Titre inconnu"
    prompt = f"Donne uniquement le titre officiel en français du livre suivant : '{titre}'. Si le titre est déjà en français ou n'a pas de traduction officielle, renvoie exactement '{titre}'."
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return titre # Return original title on error

#Extractions des Informations du Fichier

def extraire_profil_data(file_path):
    """Extracts user profile data from the given file path."""
    nom = ""
    age = 0
    genres_preferes = []
    liste_livres = []

    if not os.path.exists(file_path):
        return nom, age, genres_preferes, liste_livres

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Use regex to extract data blocks
    nom_match = re.search(r"#PROFIL#\nNom: (.*?)\n", content)
    if nom_match: nom = nom_match.group(1).strip()

    age_match = re.search(r"Age: (\d+)\n", content)
    if age_match: age = int(age_match.group(1))

    genres_match = re.search(r"#GENRES_LITTERAIRES#\n(.*?)\n", content, re.DOTALL)
    if genres_match: genres_preferes = [g.strip() for g in genres_match.group(1).split(',')] if genres_match.group(1).strip() else []

    livres_match = re.search(r"#LIVRES#\n(.*?)(?:\n#|$)", content, re.DOTALL)
    if livres_match:
        for line in livres_match.group(1).strip().split('\n'):
            if ' - ' in line:
                titre, auteur = line.split(' - ', 1)
                liste_livres.append({'titre': titre.strip(), 'auteur': auteur.strip()})

    return nom, age, genres_preferes, liste_livres

def extraire_livres(file_path):
  """Extraction des livres du fichier texte"""
  if not os.path.exists(file_path):
        return []

  livres = []
  with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
  livres_match = re.search(r"#LIVRES#\n(.*?)(?:\n#|$)", content, re.DOTALL)
  if livres_match:
        for line in livres_match.group(1).strip().split('\n'):
            if ' - ' in line:
                titre, auteur = line.split(' - ', 1)
                livres.append({'titre': titre.strip(), 'auteur': auteur.strip()})
  return livres

def extraire_auteurs(file_path):
  """Extraction des auteurs du fichier texte"""
  livres = extraire_livres(file_path)
  return [livre['auteur'] for livre in livres]

def extraire_genres(file_path):
  """Extraction des genres du fichier texte"""
  if not os.path.exists(file_path):
        return []

  with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

  genres = []
  genres_match = re.search(r"#GENRES_LITTERAIRES#\n(.*?)\n", content, re.DOTALL)
  if genres_match: genres = [g.strip() for g in genres_match.group(1).split(',')] if genres_match.group(1).strip() else []

  return genres

def recuperer_genres(livres):
    """
    Récupère les genres des livres à l'aide de Google Books API, avec OpenLibrary et l'intelligence artificielle comme solutions de repli.
    """
    genres = []

    def genre_openlibrary(titre, auteur):
        """Fallback Open Library: recherche de genre"""
        url = "https://openlibrary.org/search.json"
        params = {
            "title": titre,
            "author": auteur,
            "limit": 5
        }

        try:
            res = requests.get(url, params=params)
            data = res.json()
        except:
            return "Inconnu"

        if "docs" in data:
            for doc in data["docs"]:
                sujets = doc.get("subject", [])
                if sujets:
                    return sujets[0]

        return "Inconnu"

    def genre_via_ia(titre, auteur):
        """Fallback IA: recherche de genre"""
        try:
            prompt = f"Donne un seul genre littéraire (ex: Science Fiction, Romance) pour le livre '{titre}' de {auteur}. Réponds par un seul mot ou groupe de mots."
            response = gemini_model.generate_content(prompt)
            return response.text.strip()
        except:
            return "Fiction"

    for livre in livres:
        titre = livre["titre"]
        auteur = livre.get("auteur", "")

        genre = "Inconnu"
        tour  = 0
        maxtours= 3

      #Recherche du genre dans Google Books API, 3 fois
        while tour < maxtours:
            url = "https://www.googleapis.com/books/v1/volumes"
            params = {"q": f'intitle:"{titre}" inauthor:"{auteur}"',
                      "key": GOOGLEBOOKS_API_KEY
            }

            try:
                res = requests.get(url, params=params)
                data = res.json()

                if "items" in data:
                    info = data["items"][0]["volumeInfo"]
                    genre = info.get("categories", ["Inconnu"])[0]
                if genre != "Inconnu":
                    break
            except:
                genre = "Inconnu"
            tour += 1

      #Fallback OpenLibrary puis IA
        if genre == "Inconnu":
          genre = genre_openlibrary(titre, auteur)
        if genre == "Inconnu":
          genre = genre_via_ia(titre, auteur)

        genres.append(genre)
      #Traitement des genres pour avoir des résultats plus homogènes
    genres = traiter_genre(genres)

    return genres


def compter_livres(livres):
    """Compte le nombre de livres"""
    return len(livres)

def compter_genre(genres, genre_recherche):
    """Compte les occurrences d'un genre dans une liste."""
    compteur = 0
    for genre in genres:
        if genre == genre_recherche:
            compteur += 1
    return compteur

def auteur_principal(livres):
    """Trouve l'auteur le plus fréquent dans une liste"""
    compteur = {}
    for livre in livres:
        auteur = livre["auteur"]
        if auteur in compteur:
            compteur[auteur] += 1
        else:
            compteur[auteur] = 1
    if not compteur:
        return "Aucun auteur", 0
    auteur_max = max(compteur, key=compteur.get)
    return auteur_max, compteur[auteur_max]

def genre_favori(genres_list):
    """Trouve le genre le plus fréquent dans une liste de genres"""
    compteur = {}
    for g in genres_list:
        if g == "Inconnu":
            continue
        if g in compteur:
            compteur[g] += 1
        else:
            compteur[g] = 1
    if not compteur:
        return "Inconnu"
    return max(compteur, key=compteur.get)

# --- Logique de recommendations ---
def recommander_par_auteur(auteur_name, num_results=3):
    """Logique de recommandation par auteur utilisant Google Books API et OpenLibrary API"""
    recommandations = []
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": f"inauthor:{auteur_name}", "maxResults": num_results + 2, "key": GOOGLEBOOKS_API_KEY}

    try:
        res = requests.get(url, params=params)
        items = res.json().get("items", [])
        for item in items:
            info = item.get("volumeInfo", {})
            t = info.get("title")
            # Traduction systématique du titre pour l'utilisateur
            titre_fr = traduire_titre(t)
            img = info.get("imageLinks", {}).get("thumbnail", "https://via.placeholder.com/128x192")
            recommandations.append({"titre": titre_fr, "auteur": auteur_name, "img": img})
            if len(recommandations) >= num_results: break
    except:
        pass
    return recommandations

def recommander_par_genre(genre_name, num_results=3):
    recommandations = []
    unique_titles = set()

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": f"subject:{genre_name}",
              "maxResults": 40, # Fetch more to pick random ones
              "key": GOOGLEBOOKS_API_KEY
    }
    try:
        res = requests.get(url, params=params)
        data = res.json()
        items = data.get("items", [])
        random.shuffle(items) # Shuffle to get varied results

        for item in items:
            info = item.get("volumeInfo", {})
            title = info.get("title")
            authors = info.get("authors", ["Inconnu"])
            image_links = info.get("imageLinks", {})
            thumbnail = image_links.get("thumbnail") or image_links.get("smallThumbnail", "https://via.placeholder.com/128x192?text=Livre")

            if title and title not in unique_titles:
                recommandations.append({"titre": title, "auteur": authors[0], "img": thumbnail})
                unique_titles.add(title)
                if len(recommandations) >= num_results:
                    return recommandations
    except Exception as e:
        print(f"Error fetching from Google Books for genre {genre_name}: {e}")

    return recommandations

def choisir_genres(genres_list):
    if not genres_list:
        return ["Fiction", "Aventure", "Mystère"] # Valeurs par défaut

    if len(genres_list) >= num:
        return random.sample(genres_list, num)
    return genres_list

def livre_aleatoire():
    mot = random.choice(GENRES_optim)

    url = "https://www.googleapis.com/books/v1/volumes"

    try:
        params = {
            "q": f"subject:{mot}",
            "maxResults": 1,
            "key": GOOGLEBOOKS_API_KEY
        }

        res = requests.get(url, params=params)
        data = res.json()
        total = data.get("totalItems", 0)

        if total == 0:
            return {"titre": "Inconnu", "auteur": "Inconnu", "img": "https://via.placeholder.com/128x192?text=Livre"}

        start_index = random.randint(0, min(total - 1, 40)) # Limit max startIndex to avoid too many requests

        params = {
            "q": f"subject:{mot}",
            "maxResults": 20, # Fetch a batch to pick a random one
            "startIndex": start_index,
            "key": GOOGLEBOOKS_API_KEY
            }

        res = requests.get(url, params=params)
        data = res.json()

        if "items" in data and len(data["items"]) > 0:
            livre_item = random.choice(data["items"])
            info = livre_item.get("volumeInfo", {})

            titre = info.get("title", "Inconnu")
            auteurs = info.get("authors", ["Inconnu"])
            image_links = info.get("imageLinks", {})
            thumbnail = image_links.get("thumbnail") or image_links.get("smallThumbnail", "https://via.placeholder.com/128x192?text=Livre")

            return {
                "titre": titre,
                "auteur": auteurs[0],
                "img": thumbnail
            }
    except Exception as e:
        print(f"Error fetching random book for subject {mot}: {e}")

    return {"titre": "Inconnu", "auteur": "Inconnu", "img": "https://via.placeholder.com/128x192?text=Livre"}

# Fonction de Recommandation (Celle à utiliser dans le code principal.)
def recommandations_auteurs(file_path, num_results=3):
    auteurs = extraire_auteurs(file_path)
    if not auteurs: return []

    # Get the most frequent author if available, otherwise just use one of the extracted authors
    principal_auteur, _ = auteur_principal(extraire_livres(file_path))
    if principal_auteur != "Aucun auteur":
        return recommander_par_auteur(principal_auteur, num_results=num_results)
    elif auteurs: # If no principal, try with any available author
        return recommander_par_auteur(auteurs[0], num_results=num_results)
    return []

def recommandations_genres(file_path, num_results=3):
    genres_profil = extraire_genres(file_path)
    if not genres_profil: return []

    genre_prefere = genre_favori(genres_profil)
    if genre_prefere != "Inconnu":
        return recommander_par_genre(genre_prefere, num_results=num_results)

    return []

def recommandations_aleatoires(num_results=2):
    reco_alea = []
    for i in range(num_results):
        reco_alea.append(livre_aleatoire())
    return reco_alea


#––––––––––––––––––RÉCAP/WRAPPED DE LECTURE–––––––––––––––

def extraire_annee(date_str):
    try:
        return int(date_str[:4])
    except:
        return None

def convertir_heures(heures):
    h = int(heures)
    minutes = int(round((heures - h) * 60))

    return f"{h}h{minutes:02d}"

def format_liste_fr(elements):
    if not elements:
        return ""

    if len(elements) == 1:
        return elements[0]

    if len(elements) == 2:
        return f"{elements[0]} et {elements[1]}"

    return ", ".join(elements[:-1]) + " et " + elements[-1]

def analyser_livre(titre, auteur):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f'intitle:"{titre}" inauthor:"{auteur}"',
        "maxResults": 15,
        "key": GOOGLEBOOKS_API_KEY
    }

    res = requests.get(url, params=params)
    data = res.json()

    items = data.get("items", [])

    pages = []
    annees = []
    ratings = []

    for item in items:
        info = item.get("volumeInfo", {})
        pc = info.get("pageCount")
        if isinstance(pc, int):
            pages.append(pc)

        date = info.get("publishedDate")
        if date:
            annee = extraire_annee(date)
            if annee:
                annees.append(annee)

        rc = info.get("ratingsCount")
        ar = info.get("averageRating")
        if isinstance(rc, int) and isinstance(ar, (int, float)):
            ratings.append((rc, ar))

    median_pages = statistics.median(pages) if pages else -1

    oldest_year = min(annees) if annees else -1

    if ratings:
        best = max(ratings, key=lambda x: x[0])
        best_ratings_count = best[0]
        best_average_rating = best[1]
    else:
        best_ratings_count = -1
        best_average_rating = -1

    return titre, auteur, median_pages, oldest_year, best_ratings_count, best_average_rating

def construire_base(livres):
    base = []

    for livre in livres:
        titre = livre["titre"]
        auteur = livre.get("auteur", "")

        try:
            data = analyser_livre(titre, auteur)
        except:
            continue

        base.append(data)

    return base

def top_auteurs(livres, n):
    compteur = {}

    for livre in livres:
        auteur = livre.get("auteur", "Inconnu")

        if auteur == "Inconnu":
            continue

        if auteur in compteur:
            compteur[auteur] += 1
        else:
            compteur[auteur] = 1

    classement = sorted(compteur.items(), key=lambda x: x[1], reverse=True)

    return classement[:n]

def top_genres(genres, n):
    compteur = {}

    for genre in genres:
        if genre == "Inconnu":
            continue
        if genre in compteur:
            compteur[genre] += 1
        else:
            compteur[genre] = 1

    if not compteur:
        return []

    classement = sorted(compteur.items(), key=lambda x: x[1], reverse=True)

    return classement[:n]

def top_popularite(base, n):
    scores = []

    for titre, auteur, _, _, count, rating in base:

        if count == "Inconnu" or rating == "Inconnu":
            continue

        score = count * rating
        scores.append((titre, score))

    if not scores:
        return "Erreur"

    classement = sorted(scores, key=lambda x: x[1], reverse=True)

    return classement[:n]

def annee_openlibrary(titre, auteur):
      url = "https://openlibrary.org/search.json"
      params = {"title": titre, "author": auteur, "limit":1 }
      try:
          res = requests.get(url, params=params)
          data = res.json()
      except:
          return None
      docs = data.get("docs")
      if not docs:
          return None
      return docs[0].get("first_publish_year")

def top_age(base, n, croissant=True):
    resultats = []

    for titre, auteur, _, oldest_year, _, _ in base:

        if oldest_year == -1:
            annee = annee_openlibrary(titre, auteur)
            if annee:
                continue # Continue if year cannot be found from OpenLibrary either
            oldest_year = annee

        resultats.append((titre, oldest_year))

    if not resultats:
        return []

    classement = sorted(resultats, key=lambda x: x[1], reverse=not croissant)

    return classement[:n]

def age_lecture(base):
    annees = []

    for titre, auteur, _, oldest_year, _, _ in base:

        if oldest_year != -1:
            annees.append(oldest_year)
        else:
            annee = annee_openlibrary(titre, auteur)
            if annee:
                annees.append(annee)

    if not annees:
        return -1

    moyenne = sum(annees) / len(annees)
    annee_actuelle = datetime.now().year

    return round(annee_actuelle - moyenne, 1)

def analyse_temps_lecture(base, n):
    total_minutes = 0
    resultats = []

    for titre, auteur, median_pages, _, _, _ in base:

        if median_pages == -1:
            continue

        minutes = median_pages / PAGES_PER_MIN

        total_minutes += minutes
        resultats.append((titre, round(minutes, 2)))

    if total_minutes == 0 or not resultats:
        return "Erreur"

    classement = sorted(resultats, key=lambda x: x[1], reverse=True)
    top_n = classement[:n]

    heures = round(total_minutes / 60, 2)

    return round(total_minutes), heures, top_n


def buildtop_stats(classement, total=None, mode="count"):
    stats = []

    if mode == "score":
        total_score = sum(val for _, val in classement)
    else:
        total_score = total

    for i, (nom, valeur) in enumerate(classement):
        if mode == "score":
            pourcentage = round((valeur / total_score) * 100, 1) if total_score > 0 else 0
        else:
            pourcentage = round((valeur / total) * 100, 1) if total > 0 else 0

        stats.append({
            "nom": nom,
            "rang": i + 1,
            "count": valeur,
            "pourcentage": pourcentage
        })

    return stats

def author_loyalty(livres, auteurs):
    if not auteurs:
        return None

    if len(auteurs) > 4:
        selection = random.sample(auteurs, 4)
    else:
        selection = auteurs

    resultats = []

    total_livres = compter_livres(livres)

    for auteur in selection:
        count = 0

        for livre in livres:
            if livre.get("auteur") == auteur:
                count += 1

        pourcentage = round((count / total_livres) * 100, 1)

        resultats.append({
            "auteur": auteur,
            "count": count,
            "pourcentage": pourcentage
        })

    return resultats

def diversity_score(genres):
    genresv = [g for g in genres if g != "Inconnu"]

    if not genresv:
        return -1

    uniques = set(genresv)

    score = len(uniques) / len(genresv) *100

    return round(score, 2)

def mood_reader(genres_utilisateur):
    scores = {}

    for mood, genres_mood in MOODS.items():
        matches = sum(
            1 for g in genres_utilisateur
            if g != "Inconnu" and g in genres_mood
        )

        score = round(matches / len(genres_mood), 2) if genres_mood else 0
        scores[mood] = score

    classement = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    classement = [c for c in classement if c[1] > 0]

    if not classement:
        return []

    return classement[:2]

#FONCTION PRINCIPAL POUR CONSTRUIRE LE WRAPPED/RÉCAP

# base=construire_base(extraire_livres(fichier)) # This line caused the NameError, removed it from global scope

def wrapped_auteur(fichier, n):
    livres = extraire_livres(fichier)

    top = top_auteurs(livres, n)
    stats = buildtop_stats(top, total=len(livres), mode="count")

    if not stats:
        return "Erreur", "Erreur"

    top1 = stats[0]
    p1 = f"Ton auteur préféré est {top1['nom']}, avec {top1['count']} livres ({top1['pourcentage']}%)."

    p2 = {}
    for s in stats:
        p2[f"top_{s['rang']}"] = (
            f"Top {s['rang']} : {s['nom']} avec {s['count']} livres "
            f"({s['pourcentage']}%)."
        )

    return p1, p2

def wrapped_genre(fichier, n):
    livres = extraire_livres(fichier)
    genres = recuperer_genres(livres)

    top = top_genres(genres, n)
    if top == "Erreur" or not top:
        return {"Erreur": "Aucune donnée de popularité disponible."}

    stats = buildtop_stats(top, total=len(genres), mode="count")

    if not stats:
        return {"Erreur": "Aucune donnée de popularité disponible."}

    top1 = stats[0]
    p3 = f"Ton genre préféré est {top1['nom']} avec {top1['count']} lectures ({top1['pourcentage']}%)."

    p4 = {}
    for s in stats:
        p4[f"top_{s['rang']}"] = (
            f"Top {s['rang']} : {s['nom']} avec {s['count']} lectures "
            f"({s['pourcentage']}%)."
        )

    return p3, p4

def wrapped_popularite(base, n):
    top = top_popularite(base, n)
    if top == "Erreur" or not top:
        return {"Erreur": "Aucune donnée de popularité disponible."}

    stats = buildtop_stats(top, mode="score")

    if not stats:
        return {"Erreur": "Impossible de calculer la popularité."}

    p5 = {}
    for s in stats:
        p5[f"top_{s['rang']}"] = (
            f"{s['nom']} est parmi tes livres les plus populaires "
            f"({s['pourcentage']}% du total)."
        )

    return p5


def wrapped_temps(base, n):
    age = age_lecture(base)
    p6 = f"Ton âge de lecture est de {age} ans."

    anciens = top_age(base, n, croissant=True)
    p7 = {}

    for i, (titre, annee) in enumerate(anciens, 1):
        p7[f"ancien_{i}"] = f"{titre} ({annee})"

    recents = top_age(base, n, croissant=False)
    p8 = {}

    for i, (titre, annee) in enumerate(recents, 1):
        p8[f"recent_{i}"] = f"{titre} ({annee})"

    resultat = analyse_temps_lecture(base, n)

    if resultat == "Erreur":
        return p6, p7, p8, "Temps de lecture indisponible.", ""

    total_minutes, heures, top_livres = resultat

    temps_str = convertir_heures(heures)

    p9 = f"Tu as passé environ {total_minutes} minutes à lire. Cela représente {temps_str}."

    titres = [f"{t} ({m} min)" for t, m in top_livres]
    liste = format_liste_fr(titres)

    if liste:
        p10 = f"Avec {liste}."
    else:
        p10 = ""

    return p6, p7, p8, p9, p10

def wrapped_loyaute(fichier):
    livres = extraire_livres(fichier)
    auteurs_claimed = extraire_auteurs(fichier)

    if not auteurs_claimed:
        return {"loyaute": "Aucun auteur favori déclaré."}

    sample = random.sample(auteurs_claimed, min(4, len(auteurs_claimed)))

    total = len(livres)
    resultats = {}

    for i, auteur in enumerate(sample, 1):

        count = sum(1 for l in livres if l["auteur"] == auteur)
        pourcentage = round((count / total) * 100, 1) if total > 0 else 0

        if pourcentage == 0:
            commentaire = "Tu dis l'aimer… mais tu ne le lis jamais 💀"
        elif pourcentage < 20:
            commentaire = "Pas très fidèle 😅"
        elif pourcentage < 50:
            commentaire = "Tu le lis de temps en temps 🙂"
        elif pourcentage < 80:
            commentaire = "Très fidèle 💪"
        else:
            commentaire = "Fan absolu 🔥"

        resultats[f"auteur_{i}"] = (
            f"{auteur} : {pourcentage}% — {commentaire}"
        )

    return resultats

def wrapped_diversite(fichier):
    livres = extraire_livres(fichier)
    genres = [g for g in recuperer_genres(livres) if g != "Inconnu"]

    total = len(genres)
    uniques = len(set(genres))

    if total == 0:
        return "Erreur"

    score = round((uniques / total) * 100, 1)

    return f"Tu as un score de diversité de {score}%. Tu explores plus de {uniques} genres différents!"

def wrapped_mood(fichier):
    DESCRIPTIONS_MOODS = {
        "Dans un autre monde ✨": "Tu es simpliste. Un bon livre te transporte facilement",
        "Romance Addict 💖": "Tu vis pour les histoires d’amour.",
        "Détective 🕵️": "Tu adores résoudre des mystères et suivre des enquêtes.",
        "Chasseur de frissons 🔪": "Tu cherches l’adrénaline et les sensations fortes.",
        "Explorateur 🌌": "Tu aimes voyager dans des univers inconnus et ouvrir ton esprit aux possibilités.",
        "Dans un autre monde 🧚": "Tu plonges dans des mondes fantastiques.",
        "D'une autre époque 📚": "Tu aimes les livres qui te font voyager dans le temps",
        "Man VS 🏔️": "Tu aimes voir l'Homme se confronter à lui-même ou la Nature",
        "Nerd 🤓": "Tu es passionné par les univers riches et complexes, ainsi que les mythes et vers complexes.",
        "Nerd Type 1 🤓": "Tu vis dans les mythes et les vers oubliés" ,
        "Nerd Type 2 🤓": "Tu adores les univers riches et complexe.",
        "Curieux 🌍": "Tu lis de tout et tu explores sans limites.",
        "Étudiant en Sciences 🎓": "Chef lâche les bouquins et profite de la vie.",
        "Étudiant en Lettres 🎓": "Chef lâche les bouquins et profite de la vie.",
        "Apprenti de la vie 💡": "Tu lis pour grandir et comprendre le monde.",
        "Baka 🥷🐺": "Tu aimes les univers sombres et intenses.",
        "Girls' Girl 💅🖤": "Tu mixes émotions, drame et intrigue avec style.",
        "Testosterone Lit 🦾🧭": "Tu préfères l’action, la survie et l’intensité.",
        "Univers Alternatifs 🌀": "Tu explores les réalités parallèles.",
        "Futur Sombre 🌑": "Tu es attiré.e par les futurs dystopiques.",
        "Dans l'ombre 🕶️": "Tu aimes les intrigues secrètes et les complots.",
        "Haute Tension 🧨": "Tu vis pour le suspense et l’action.",
        "Artiste 🖊️": "Tu apprécies la beauté et l’expression artistique.",
        "La Vraie Vie 📰": "Tu t’intéresses au réel et aux histoires vraies.",
        "Lecteur Classique 📜": "Tu apprécies les grands classiques intemporels.",
        "Globetrotter 🗺️": "Tu apprécies la littérature du Monde"
    }

    livres = extraire_livres(fichier)
    genres = recuperer_genres(livres)

    moods = mood_reader(genres)

    if moods == "Inconnu" or not moods:
        return "Impossible de déterminer ton mood lecteur."

    mood1, score1 = moods[0]

    description = DESCRIPTIONS_MOODS.get(
        mood1,
        "Tu as un style de lecture unique."
    )

    p11 = f"Ton mood de lecteur est : {mood1}. {description}"

    if len(moods) > 1:
        mood2, score2 = moods[1]

        p12 = f"Tu as aussi des vibes de {mood2.lower()} 😉"
    else:
        p12 = ""

    return p11, p12
