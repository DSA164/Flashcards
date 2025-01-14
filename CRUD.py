#      Fonction CRUD pour les flashcards
#===========================================

from sqlite3 import connect, Error
from contextlib import contextmanager  # contextmanager pour: yield

#      Fonction de debuggage 
#--------------------------------

def open_db(debug: bool):
    if debug:
        print("Connection à la base réussie")
        
        
def close_db(debug: bool):
    if debug:
        print("La base de donnée à été fermée avec succès")
        
        
def log_message(message: str, debug: bool):
        if debug:
            print(message)


#      Manipulation de la base de donnée
#-------------------------------------------

@contextmanager
def database_connection(debug: bool = False):
    conn = None
    try:
        conn = connect('flashcard')
        open_db(debug)
        yield conn  # permet de retourner sans intérompre la fonction
    except Error as e:
        print(f"La connection à la base de donnée a échoué en raison de:\n{e}")
        raise # pour que l'erreur soit accessible depuis la fonction parente
    finally: # try: finally: pour s'assurer que la connection à la base de donnée soit toujours fermée même en cas d'erreur
        if conn is not None:
            conn.close()
            close_db(debug)
        
    
# Créer une carte
def create_card(question: str, reponse: str, probabilite: str, id_theme: int, debug: bool = False): 
    last_id = None
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute('''
                        INSERT INTO cards (question, reponse, probabilite, id_theme) 
                        VALUES (?, ?, ?, ?)
                    ''', (question, reponse, probabilite, id_theme)
                    )
            conn.commit()
            last_id = c.lastrowid
        except Error as e:
            print(f"Erreur lors de la création de la carte : \n{e}")
            return None  
    return get_card(last_id, debug) if last_id is not None else None
    
    
# Récupérer une carte    
def get_card(id: int, debug: bool = False):
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM cards WHERE id=?", (id, )) 
            card = c.fetchone()
        except Error as e:
            print(f"Erreur lors de la récupération de la carte : \n{e}")
            card = None
    return card
    

# Mettre à jour une carte avec des nouvelles données
def update_card(id: int, question: str, reponse: str, probabilite: str, id_theme: int, debug: bool = False):
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute('''UPDATE cards SET question=? , reponse=?, probabilite=?, id_theme=? WHERE id=?
                    ''',(question, reponse, probabilite, id_theme, id))
            conn.commit()
            card = get_card(id, debug)
            if card and debug:
                print(f"La carte {id} a été mise à jour avec les informtions suivantes: \n{card}")
        except Error as e:
            print(f"La carte {id} n'a pas pu être mise à jour en raison de: \n{e}")
    return card
    
    
# Supprimer une carte
def delete_card(id: int, debug: bool = False):
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            card = get_card(id, debug)
            c.execute("DELETE FROM cards WHERE id=?", (id, ))
            conn.commit()
            if c.rowcount > 0 and debug:
                print(f"La carte {id} a été supprimée avec succès!")
            elif debug:
                print(f"Aucune carte trouvée avec l'ID {id}.")
        except Error as e:
            print(f"La carte {id} n'a pas pu être supprimée en raison de: \n{e}")
    return card


# Récupérer toutes les cartes
def get_all_cards(debug: bool = False):
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM cards")
            cards = c.fetchall()
            if cards and debug:
                print("Voici les cartes présentes dans le jeu:")
                print("(id, question, reponse, probabilite, id_theme)")
                for card in cards:
                    print(card)
        except Error as e:
            print(f"La selection n'a pas pu être opérée:\n{e}")
    return cards
    
    
# Retourner le nombre total de cartes
def get_number_of_cards(debug: bool = False): 
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute("SELECT COUNT(id) FROM cards")
            count = c.fetchone()
        except Error as e:
            print(f"La demande n'a pas pu être réalisée en raison de: {e}")
    return count[0] if count in locals() else None
    
    
# Récupérer les cartes appartenant à un thème particulier
def get_cards_by_theme(id_theme: int, debug: bool = False):
    with database_connection(debug) as conn:    
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM cards WHERE id_theme=?", (id_theme,))
            cards = c.fetchall()
            if cards and debug:
                print(f"Liste des cartes avec le thèmeID = {id_theme}:\n")
                for card in cards:
                    print(card)
            elif debug:
                print(f"Il n'y a pas des cartes ayant le themeID = {id_theme}")
        except Error as e:
            print(f"La selection demandée n'a pas pu être faite en raison de:\n{e}")
    return cards if cards in locals() else None