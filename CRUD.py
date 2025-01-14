#      Fonction CRUD pour les flashcards
#===========================================

from sqlite3 import connect

# Créer une carte
def create_card(question, reponse, probabilite, id_theme): 
    conn = connect('flashcard')
    c = conn.cursor()
    c.execute('''
              INSERT INTO cards (question, reponse, probabilite, id_theme) 
              VALUES (?, ?, ?, ?)
              ''', (question, reponse, probabilite, id_theme)
              )
    conn.commit()
    conn.close()
    
    
# Récupérer une carte    
def get_card(id):
    conn = connect('flashcard')
    # try: finally: pour s'assurer que la connection à la base de donnée soit toujours fermée même en cas d'erreur
    try:
        c = conn.cursor()
        c.execute('''SELECT * FROM cards WHERE id = (?)
                ''', (id, )) 
        card = c.fetchone()
    except Exception as e:
        print(f"Erreur lors de la récupération de la carte : \n{e}")
        card = None
    finally:
        conn.close()
    return card
    

# Mettre à jour une carte avec des nouvelles données
def update_card(id, question, reponse, probabilite, id_theme):
    conn = connect('flashcard')
    try:
        c = conn.cursor()
        c.execute('''UPDATE cards SET question=? , reponse=?, probabilite=?, id_theme=? WHERE id=?
                ''',(question, reponse, probabilite, id_theme, id))
        conn.commit()
        c.execute('''SELECT * FROM cards WHERE id=?
                ''', (id, ))
        update = c.fetchone()
        if update:
            print(f"La carte {id} a été mise à jour avec les informtions suivantes: \n{update}")
    except Exception as e:
        print(f"La carte {id} n'a pas pu être mise à jour en raison de: \n{e}")
    finally:
        conn.close()
        
    
# Supprimer une carte
def delete_card(id):
    conn = connect('flashcard')
    c = conn.cursor()
    try:
        c.execute('''DELETE FROM cards WHERE id=?
                ''', (id, ))
        conn.commit()
        if c.rowcount > 0:
            print(f"La carte {id} a été supprimée avec succès!")
        else:
            print(f"Aucune carte trouvée avec l'ID {id}.")
    except Exception as e:
        print(f"La carte {id} n'a pas pu être supprimée en raison de: \n{e}")
    finally:
        conn.close()
    

# Récupérer toutes les cartes
def get_all_cards():
    conn = connect('flashcard')
    try:
        c = conn.cursor()
        c.execute('''SELECT * FROM cards
                ''')
        cartes = c.fetchall()
        if cartes:
            print("Voici les cartes présentes dans le jeu:")
            print("(id, question, reponse, probabilite, id_theme)")
            for carte in cartes:
                print(carte)
    except Exception as e:
        print(f"La selection n'a pas pu être opérée:\n{e}")
    finally:
        conn.close()
    
    
# Retourner le nombre total de cartes
def get_number_of_cards(): 
    conn = connect('flashcard')
    try:
        c = conn.cursor()
        c.execute('''SELECT COUNT(id) FROM cards
                ''')
        count = c.fetchone()
    except Exception as e:
        print(f"La demande n'a pas pu être réalisée en raison de: {e}")
    finally:
        conn.close()
    return count
    
# Récupérer les cartes appartenant à un thème particulier
def get_cards_by_theme(id_theme):
    conn = connect('flashcard')
    try:
        c = conn.cursor()
        c.execute('''SELECT * FROM cards WHERE id_theme=?
                ''', (id_theme,))
        cartes = c.fetchall()
        if cartes:
            print(f"Liste des cartes avec le thèmeID = {id_theme}:\n")
            for carte in cartes:
                print(carte)
        else:
            print(f"Il n'y a pas des cartes ayant le themeID = {id_theme}")
    except Exception as e:
        print("La selection demandée n'a pas pu être faite en raison de:\n{e}")
    finally:
        conn.close()
    return cartes