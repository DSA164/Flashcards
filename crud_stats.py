#      Fonctions CRUD pour les statistiques
#===============================================

from sqlite3 import Error
from crud_cards import database_connection, get_card,update_card
from datetime import datetime
from matplotlib.pyplot import plot as plt

#      Manipulation de la base de donnée
#-------------------------------------------

# stats (id, bonnes_reponses, mauvaises_reponses, date)

# Mettre à jour la carte (vérifie si une entrée pour la mise à jour existe déjà)
def update_stats(is_correct: bool, debug: bool = False):
    today = datetime.now().strftime('%Y-%m-%d')   # mise au format SQL
    stat = None
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute("SELECT bonnes_reponses, mauvaises_reponses FROM stats WHERE date=?", (today,))
            reponses = c.fetchone()
            # Creer un nouvelle entrée si non existant
            if reponses is None:  
                bonnes_reponses = 1 if is_correct else 0
                mauvaises_reponses = 0 if is_correct else 1
                c.execute('''INSERT INTO stats (bonnes_reponses, mauvaises_reponses, date) 
                          VALUES (?, ?, ?)''', (bonnes_reponses, mauvaises_reponses, today) )
            # Mise à jour de l'existant
            else:
                bonnes_reponses, mauvaises_reponses = reponses
                bonnes_reponses += 1 if is_correct else 0
                mauvaises_reponses += 0 if is_correct else 1
                c.execute("UPDATE stats SET bonnes_reponses=?, mauvaises_reponses=? WHERE date=?", (bonnes_reponses, mauvaises_reponses, today))
            conn.commit()
            c.execute("SELECT * FROM stats WHERE date=?", (today,))
            stat = c.fetchone()  
        except Error as e:
            print(f"La statistique n'a pas pu être mise à jour en raison de:\n{e}")
    return stat


# cards (id, question, reponse, probabilite, id_theme) 

# Mettre à jour la probabilité d'apparition d'un carte
def update_card_probability(card_id: int, is_correct: bool, debug: bool = False):
    probabilite = None
    try:
        card = get_card(card_id, debug)
        if card is None:
            print(f"La carte {card_id} n'existe pas!")
            return None
        probabilite = card[3]
        probabilite *= 0.9 if is_correct else 1.1
        probabilite = max(0.1, min(probabilite, 1.0))
        update_card(card[0], card[1], card[2], probabilite, card[4]) 
    except Error as e :
        print(f"La probalité de la carte {card_id} n'a pas pu être mise à jour en raison de:\n{e}")
        return None
    return probabilite


# Récupérer les statistiques au cours du temps
def get_stats(debug: bool = False):
    with database_connection(debug) as conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM stats")
            stats = c.fetchall()
            if not stats:
                print("Aucune statistique n'est présente dans la base de donnée!")
                return None
            elif debug:
                bonnes_reponses = [raw[1] for raw in stats]
                mauvaises_reponses =  [raw[2] for raw in stats]
                periode =  [raw[3] for raw in stats]
                plt.figure(figsize = (8, 6))
                plt.scatter(periode, bonnes_reponses, label='Bonnes', color='blue', marker='o')
                plt.scatter(periode, mauvaises_reponses, label='Mauvaises',color='red', marker='x')
                plt.title('Evolution des réponses apportées au cours du temps')
                plt.xlabel('Période')
                plt.ylabel('Nombre de réponses')
                plt.legend()
                plt.show()
        except Error as e:
            print(f"Les statistiques n'ont pas pu être lues en raison de:\n{e}")
            return None
    return stats