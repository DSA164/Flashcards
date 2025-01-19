#      Fonctions CRUD pour les thèmes
#=========================================

from sqlite3 import Error as sqlite3Error
from crud_cards import database_connection

# themes (id, theme) 

# Créer un thèmes
def create_theme(theme: str, debug: bool = False):
    last_id = None
    with database_connection(debug) as conn:
        try:
            if theme in [t for t in get_all_themes(False)]:
                print(f"Le theme '{theme}' existe déjà dans la base de données")
                return None
            else:
                c = conn.cursor()
                c.execute("INSERT INTO themes (theme) VALUES (?)", (theme,))
                conn.commit()
                last_id = c.lastrowid
        except sqlite3Error as e:
            print(f"Erreur lors de la création du thème : \n{e}")
            return None  
    return get_theme(last_id, debug) if last_id is not None else last_id
            

# Récupérer un thème   
def get_theme(id: int, debug: bool = False):
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM themes WHERE id=?", (id, )) 
            theme = c.fetchone()
        except sqlite3Error as e:
            print(f"Erreur lors de la récupération du thème : \n{e}")
            theme = None
    return theme


# Mettre à jour un thème avec des nouvelles données
def update_theme(id: int, theme:str, debug: bool = False):
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute("UPDATE themes SET theme=? WHERE id=?", (theme, id))
            conn.commit()
            updated_theme = get_theme(id, debug)
            if updated_theme and debug:
                print(f"La thème {id} a été mis à jour avec les informations suivantes: \n{updated_theme}")
        except sqlite3Error as e:
            print(f"Le thème {id} n'a pas pu être mis à jour en raison de: \n{e}")
    return updated_theme

    
# Supprimer un thème
def delete_theme(id: int, debug: bool = False):
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            deleted_theme = get_theme(id, debug)
            c.execute("DELETE FROM themes WHERE id=?", (id, ))
            conn.commit()
            if c.rowcount > 0 and debug:
                print(f"Le thème {id} a été supprimé avec succès!")
            elif debug:
                print(f"Aucun thème trouvé avec l'ID {id}.")
                return None
        except sqlite3Error as e:
            print(f"Le thème {id} n'a pas pu être supprimé en raison de: \n{e}")
    return deleted_theme


# Récupérer toutes les thèmes
def get_all_themes(debug: bool = False):
    themes = []
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM themes")
            themes = c.fetchall()
            if themes and debug:
                print("Voici les thèmes présents dans le jeu:")
                print("(id, theme)")
                for theme in themes:
                    print(theme)
        except sqlite3Error as e:
            print(f"La sélection n'a pas pu être opérée:\n{e}")
            return None
    return themes


# Récupérer l'id d'un thème
def get_theme_id(theme:str, debug: bool = False):
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute("SELECT id FROM themes WHERE theme=?", (theme,))
            id = c.fetchone()
            if id and debug:
                print(f"L'id {id} du thème '{theme}' a été récupérée")
            elif not id:
                print(f"Le thème '{theme}' n'existe pas dans la table themes")
                return None
        except sqlite3Error as e:
            print(f"La sélection n'a pas pu être opérée:\n{e}")
            return None
        return id[0]

