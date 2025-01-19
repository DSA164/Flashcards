from init import init_db  # mes fonctions de creations de la base de donnéecond
from crud_cards import create_card # mes fonctions d'intéraction avec la table themes
from crud_themes import create_theme, get_theme_id, get_all_themes # mes fonctions d'intéraction avec les tables themes 
# *** get_theme_id *** n'existe pas dans l'énoncé de base !
import random

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
        ]
    }
    
    for theme in questions.keys():
        if theme not in [item[1] for item in get_all_themes(debug)]:
            create_theme(theme, debug)

    for theme, cards in questions.items():
       
        theme_id = get_theme_id(theme)
        for question, reponse, probabilite in cards:
            create_card(question, reponse, probabilite, theme_id)

if __name__ == "__main__":
    print("===================================================")
    print("===============       TEST 2       ================")
    print("===================================================")
    debug = True
    init_db(debug)
    inject_flashcards(debug)

