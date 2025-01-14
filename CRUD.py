#      Fonction CRUD pour les flashcards
#===========================================

from sqlite3 import connect, Error

#      Fonction de debuggage 
#--------------------------------

def open_db(debug):
    if debug:
        print("Connection à la base réussie")
        
        
def close_db(debug):
    if debug:
        print("La base de donnée à été fermée avec succès")
        
        
def log_message(message, debug):
        if debug:
            print(message)


#      Manipulation de la base de donnée
#-------------------------------------------

# Créer une carte
def create_card(question, reponse, probabilite, id_theme, debug=False): 
    conn = connect('flashcard')
    c = conn.cursor()
    open_db(debug)
    try:
        c.execute('''
                INSERT INTO cards (question, reponse, probabilite, id_theme) 
                VALUES (?, ?, ?, ?)
                ''', (question, reponse, probabilite, id_theme)
                )
        conn.commit()
    except Error as e:
        print(f"Erreur lors de la création de la carte : \n{e}")
        return None  
    finally:
        conn.close()
        close_db(debug)
    return get_card(c.lastrowid, debug)
    
    
# Récupérer une carte    
def get_card(id, debug=False):
    conn = connect('flashcard')
    open_db(debug)
    # try: finally: pour s'assurer que la connection à la base de donnée soit toujours fermée même en cas d'erreur
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM cards WHERE id=?", (id, )) 
        card = c.fetchone()
    except Error as e:
        print(f"Erreur lors de la récupération de la carte : \n{e}")
        card = None
    finally:
        conn.close()
        close_db(debug)
    return card
    

# Mettre à jour une carte avec des nouvelles données
def update_card(id, question, reponse, probabilite, id_theme, debug=False):
    conn = connect('flashcard')
    open_db(debug)
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
    finally:
        conn.close()
        close_db(debug)
    return card
    
    
# Supprimer une carte
def delete_card(id, debug=False):
    conn = connect('flashcard')
    open_db(debug)
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
    finally:
        conn.close()
        close_db(debug)
    return card


# Récupérer toutes les cartes
def get_all_cards(debug=False):
    conn = connect('flashcard')
    open_db(debug)
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
    finally:
        conn.close()
        close_db(debug)
    return cards
    
    
# Retourner le nombre total de cartes
def get_number_of_cards(debug=False): 
    conn = connect('flashcard')
    open_db(debug)
    try:
        c = conn.cursor()
        c.execute("SELECT COUNT(id) FROM cards")
        count = c.fetchone()
    except Error as e:
        print(f"La demande n'a pas pu être réalisée en raison de: {e}")
    finally:
        conn.close()
        close_db(debug)
    return count[0]
    
    
# Récupérer les cartes appartenant à un thème particulier
def get_cards_by_theme(id_theme, debug=False):
    conn = connect('flashcard')
    open_db(debug)
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
    finally:
        conn.close()
        close_db(debug)
    return cards