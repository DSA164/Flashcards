from init import init_db  # mes fonctions de creations de la base de donnéecond
from crud_cards import create_card, get_card_by_question # mes fonctions d'intéraction avec la table themes
from crud_themes import create_theme, get_theme_id, get_all_themes # mes fonctions d'intéraction avec les tables themes 
# *** get_theme_id *** n'existe pas dans l'énoncé de base !
from common_sqlite import MESSAGE_TYPES

# cards (id, question, reponse, probabilite, id_theme) 
# themes (id, theme)
# stats (id, bonnes_reponses, mauvaises_reponses, date)


def inject_flashcards(debug):

    """themes = {"Python": None, "SQL": None}
    for theme_name in themes.keys():
        for theme in all_themes:
            if theme["theme"] == theme_name:
                themes[theme_name] = theme["id"]
                break
        if themes[theme_name] is None:
            themes[theme_name] = create_theme(theme_name)
    """
    questions = {
        "Python": [
                ("Qu'est-ce qu'une liste en Python ?", "Une collection ordonnée modifiable.", 0.5),
                ("Comment déclarer une variable ?", "variable = valeur", 0.5),
                ("À quoi sert la bibliothèque os ?", "Interagir avec le système d'exploitation.", 0.5),
                ("Quelle est la syntaxe pour une boucle for ?", "for x in iterable:", 0.5),
                ("Comment gérer les exceptions ?", "try...except", 0.5),
                ("Quelle est la différence entre une liste et un tuple ?", "Les tuples sont immuables.", 0.5),
                ("Comment définir une fonction ?", "Avec le mot-clé def.", 0.5),
                ("Qu'est-ce qu'un dictionnaire en Python ?", "Une collection non ordonnée d'éléments clé-valeur.", 0.5),
                ("Comment importer un module ?", "Avec import nom_du_module.", 0.5),
                ("Comment lire un fichier en Python ?", "Avec open(nom_fichier).", 0.5)
            ],
        
        "SQL": [
                ("Qu'est-ce qu'une base de données relationnelle ?", "Une base qui organise les données en tables liées.", 0.5),
                ("Quelle commande permet de créer une table ?", "CREATE TABLE nom_table (...).", 0.5),
                ("Comment insérer des données dans une table ?", "Avec INSERT INTO nom_table VALUES (...).", 0.5),
                ("Comment récupérer toutes les lignes d'une table ?", "Avec SELECT * FROM nom_table.", 0.5),
                ("Quelle commande permet de mettre à jour une ligne ?", "UPDATE nom_table SET colonne = valeur WHERE condition.", 0.5),
                ("Comment supprimer une ligne ?", "Avec DELETE FROM nom_table WHERE condition.", 0.5),
                ("Qu'est-ce qu'une clé primaire ?", "Un identifiant unique pour chaque ligne d'une table.", 0.5),
                ("Qu'est-ce qu'une jointure en SQL ?", "Une opération qui combine des lignes de plusieurs tables.", 0.5),
                ("Quelle commande permet d'ajouter une colonne ?", "ALTER TABLE nom_table ADD colonne TYPE.", 0.5),
                ("Comment compter le nombre de lignes ?", "Avec SELECT COUNT(*) FROM nom_table.", 0.5)
            ],
        
        "Algèbre linéaire": [
                ("Qu'est-ce qu'un vecteur ?", "Un objet mathématique avec magnitude et direction.", 0.5),
                ("Comment calculer le déterminant d'une matrice 2x2 ?", "ad - bc pour \n[a b] [c d].", 0.5),
                ("Qu'est-ce qu'une matrice inversible ?", "Une matrice dont le déterminant est non nul.", 0.5),
                ("Comment prendre la transpose d'une matrice ?", "Échanger lignes et colonnes.", 0.5),
                ("Qu'est-ce qu'une combinaison linéaire ?", "Somme scalaire de vecteurs.", 0.5),
                ("Qu'est-ce qu'un espace vectoriel ?", "Un ensemble de vecteurs avec addition/scalar multiplication.", 0.5),
                ("Comment déterminer le rang d'une matrice ?", "Nombre maximal de colonnes linéairement indépendantes.", 0.5),
                ("Qu'est-ce qu'un vecteur propre ?", "Vecteur non nul tel que A*v = λ*v.", 0.5),
                ("Qu'est-ce qu'une valeur propre ?", "Le scalaire λ tel que A*v = λ*v.", 0.5),
                ("Comment orthogonaliser des vecteurs ?", "Procédé de Gram-Schmidt.", 0.5)
            ],
        
    "Statistiques": [
            ("Qu'est-ce que la moyenne ?", "La somme des valeurs divisée par leur nombre.", 0.5),
            ("Qu'est-ce que la médiane ?", "La valeur qui sépare la distribution en deux.", 0.5),
            ("Qu'est-ce que l'écart-type ?", "Mesure de dispersion des données.", 0.5),
            ("Comment calculer la variance ?", "Moyenne des carrés des écarts à la moyenne.", 0.5),
            ("Qu'est-ce que la distribution normale ?", "Une courbe en cloche symétrique.", 0.5),
            ("Qu'est-ce que l'hypothèse nulle ?", "Hypothèse de base qu’on cherche à tester.", 0.5),
            ("Comment calculer un intervalle de confiance ?", "Estimation de l’intervalle probable pour un paramètre.", 0.5),
            ("Qu'est-ce que la corrélation ?", "Mesure de la relation entre deux variables.", 0.5),
            ("Qu'est-ce que la régression linéaire ?", "Modèle pour prédire y à partir de x.", 0.5),
            ("Qu'est-ce que le test t ?", "Test statistique pour comparer deux moyennes.", 0.5)
        ],
    
    "Streamlit": [
            ("Qu'est-ce que Streamlit ?", "Framework Python pour créer des applications web data.", 0.5),
            ("Comment installer Streamlit ?", "pip install streamlit", 0.5),
            ("Comment lancer une app Streamlit ?", "streamlit run app.py", 0.5),
            ("Comment afficher un titre ?", "st.title('Titre')", 0.5),
            ("Comment afficher un dataframe ?", "st.dataframe(df)", 0.5),
            ("Comment ajouter un slider ?", "st.slider('label', min, max)", 0.5),
            ("Comment ajouter un bouton ?", "st.button('Cliquer')", 0.5),
            ("Comment afficher une carte ?", "st.map(data)", 0.5),
            ("Comment utiliser sidebar ?", "st.sidebar.selectbox(...)", 0.5),
            ("Comment afficher un graphique ?", "st.line_chart(data)", 0.5)
        ],
    
    "Scikit-learn": [
            ("Qu'est-ce que Scikit-learn ?", "Bibliothèque Python pour machine learning.", 0.5),
            ("Comment importer un modèle ?", "from sklearn.linear_model import LinearRegression", 0.5),
            ("Comment entraîner un modèle ?", "model.fit(X, y)", 0.5),
            ("Comment faire une prédiction ?", "model.predict(X_new)", 0.5),
            ("Comment évaluer un modèle ?", "metrics.accuracy_score(y, y_pred)", 0.5),
            ("Comment diviser les données ?", "train_test_split(X, y)", 0.5),
            ("Qu'est-ce que la normalisation ?", "Transformer données pour moyenne=0 et variance=1.", 0.5),
            ("Qu'est-ce que le surapprentissage ?", "Modèle qui performe trop sur données entraînées.", 0.5),
            ("Qu'est-ce que la validation croisée ?", "Evaluation sur plusieurs splits.", 0.5),
            ("Comment exporter un modèle ?", "joblib.dump(model, 'model.pkl')", 0.5)
        ],
    
    "Terminal": [
            ("Comment lister les fichiers ?", "ls", 0.5),
            ("Comment changer de répertoire ?", "cd dossier", 0.5),
            ("Comment copier un fichier ?", "cp source dest", 0.5),
            ("Comment déplacer un fichier ?", "mv source dest", 0.5),
            ("Comment supprimer un fichier ?", "rm fichier", 0.5),
            ("Comment créer un répertoire ?", "mkdir nom", 0.5),
            ("Comment afficher le contenu ?", "cat fichier", 0.5),
            ("Comment chercher dans un fichier ?", "grep 'mot' fichier", 0.5),
            ("Comment afficher l'espace disque ?", "df -h", 0.5),
            ("Comment afficher les processus ?", "ps aux", 0.5)
        ],
    
    "GitHub": [
            ("Comment initialiser un repo ?", "git init", 0.5),
            ("Comment cloner un repo ?", "git clone url", 0.5),
            ("Comment vérifier le statut ?", "git status", 0.5),
            ("Comment ajouter des fichiers ?", "git add .", 0.5),
            ("Comment committer ?", "git commit -m 'msg'", 0.5),
            ("Comment pousser ?", "git push origin main", 0.5),
            ("Comment créer une branche ?", "git branch nom", 0.5),
            ("Comment changer de branche ?", "git checkout nom", 0.5),
            ("Comment fusionner ?", "git merge branche", 0.5),
            ("Comment voir les logs ?", "git log", 0.5)
        ]
    }
    
    # Récupérer tous les thèmes existants
    themes_list, themes_list_message, themes_list_message_type = get_all_themes(debug)
    if debug:
        print(f"{themes_list_message_type}: {themes_list_message}")
    if themes_list is None:
        return
    existing_themes_names = [] if themes_list == [] else [t[1] for t in themes_list]

    # Créer ou récupérer l'ID pour chaque thème
    theme_ids: dict[str, int] = {}
    
    for theme_name in questions.keys():
        if theme_name not in existing_themes_names:
            theme, theme_message, theme_message_type = create_theme(theme_name, debug)
            if debug:
                print(f"{theme_message_type}: {theme_message}")
            if theme is not None:
                theme_ids[theme_name] = theme[0]
                
        else:
            theme_id, theme_id_message, theme_id_message_type = get_theme_id(theme_name, debug)
            if debug:
                print(f"{theme_id_message_type}: {theme_id_message}")
            if theme_id is not None:
                theme_ids[theme_name] = theme_id

    # Insérer les cartes pour chaque thème, sans duplicata
    for theme_name, cards in questions.items():
        theme_id = theme_ids.get(theme_name)
        if theme_id is None:
            continue
        for q_text, q_reponse, q_prob in cards:
            # Vérifier si la carte existe déjà
            card, card_message, card_message_type = get_card_by_question(question=q_text, debug=debug)
            if debug and card_message_type != MESSAGE_TYPES[2]:
                print(f"{card_message_type}: {card_message}")
                
            if card is not None and card_message_type == MESSAGE_TYPES[0]:  # success
                continue
            
            # Créer la carte
            new_card, new_card_message, new_card_message_type = create_card(q_text, q_reponse, q_prob, theme_id, debug)
            if debug:
                print(f"{new_card_message_type}: {new_card_message}")
                
                
if __name__ == "__main__":
    print("===================================================")
    print("===============       TEST 1       ================")
    print("===================================================")
    debug = True
    init_db(debug)
    inject_flashcards(debug)



