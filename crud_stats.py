#      Fonctions CRUD pour les statistiques
#===============================================

from sqlite3 import Error as sqlite3Error
from crud_cards import get_card,update_card
from crud_users import get_user_by_username
from datetime import datetime
import matplotlib.pyplot as plt
from common_language import LANGUAGE, MESSAGE_TYPES # ('success', 'warning', 'error', 'info')
from common_sqlite import database_connection, SQL_MESSAGE, SQL_WARNING, SQL_ERRORS
from typing import List, Tuple

from streamlit import session_state as stss
if 'language' not in stss:
            stss.language = LANGUAGE[0]
language = stss.language

#      Manipulation de la base de donnée
#-------------------------------------------

# stats (id, bonnes_reponses, mauvaises_reponses, date)

# user_card_probabilities (id, user_id, card_id, probabilite)
   
#----------------------------------------------------------------------------# 
#      Obtenir user_card_proba par le couple unique (user_id, card_id)       #
#----------------------------------------------------------------------------#   
def get_id_of_user_card_probability(user_id: int, card_id: int, debug: bool = False) -> Tuple[int | None, str, str]: 
    with database_connection(debug) as (_, c):
        try:
            c.execute(
                        '''SELECT * FROM user_card_probabilities
                            WHERE user_id=? AND card_id=?''',
                      (user_id, card_id)
                      )
            user_card_proba = c.fetchone()
            if user_card_proba:
                id = user_card_proba[0]
                message = f"{SQL_MESSAGE['user_card_proba_id'][stss.language]} ({user_id}, {card_id}) {SQL_MESSAGE['is_get_db'][stss.language]}."
                message_type = MESSAGE_TYPES[0]
            else:
                id = None
                message = f"{SQL_MESSAGE['user_card_proba_id'][stss.language]} ({user_id}, {card_id}) {SQL_WARNING['not_in_db'][stss.language]}."
                message_type = MESSAGE_TYPES[1]
                
        except sqlite3Error as e:
            user_card_proba = None
            message = f"{SQL_ERRORS['error_get_user_card_proba_id'][stss.language]} ({user_id}, {card_id}): \n{e}"
            message_type = MESSAGE_TYPES[2]
      
    if debug:
        print(message)
        
    return id, message, message_type




#---------------------------------------------------# 
#         Obtenir user_card_proba par son ID        #
#---------------------------------------------------# 
def get_user_card_probability_by_id(id: int, debug: bool = False) -> Tuple[Tuple[int, int, int, float] | None, str, str]: 
    with database_connection(debug) as (conn, c):
        try:
            c.execute(
                        '''SELECT * FROM user_card_probabilities
                            WHERE id=?''',
                      (id, )
                      )
            user_card_proba = c.fetchone()
            if user_card_proba:
                id = user_card_proba[0]
                message = f"{SQL_MESSAGE['user_card_proba'][stss.language]} {id} {SQL_MESSAGE['is_get_db'][stss.language]}."
                message_type = MESSAGE_TYPES[0]
            else:
                id = None
                message = f"{SQL_MESSAGE['user_card_proba'][stss.language]} {id} {SQL_WARNING['not_in_db'][stss.language]}."
                message_type = MESSAGE_TYPES[1]
                
        except sqlite3Error as e:
            user_card_proba = None
            message = f"{SQL_ERRORS['error_get_user_card_proba_by_id'][stss.language]} {id}: \n{e}"
            message_type = MESSAGE_TYPES[2]
      
    if debug:
        print(message)
        
    return user_card_proba, message, message_type




#------------------------------------------------------# 
#         Créer ou mettre à jour user_card_proba       #
#------------------------------------------------------#    
def update_user_card_probability(user_id: int, card_id: int, increment: float = 0.00, debug: bool = False) -> Tuple[Tuple[int, int, int, float] | None, str, str]:
    with database_connection(debug) as (conn, c):
        try:
            c.execute(
                        '''SELECT * FROM user_card_probabilities
                            WHERE user_id=? AND card_id=?''',
                      (user_id, card_id)
                      )
            user_card_proba = c.fetchone()
            # On attribue la probalité par défaut de la carte si aucune probabilité pour la carte en question n'a pas encore été attribuée au joueur
            if user_card_proba:
                
                c.execute('''UPDATE user_card_probabilities 
                             SET probabilite = probabilite + ?
                             WHERE user_id=? AND card_id=? ''', (increment, user_id, card_id))
                conn.commit()
                last_id = user_card_proba[0]
                message = f"{SQL_MESSAGE['card_proba'][stss.language]} {card_id} {SQL_MESSAGE['for_user'][stss.language]} {user_id} {SQL_MESSAGE['created'][stss.language]} {SQL_MESSAGE['at_id'][stss.language]} {last_id}."
                message_type = MESSAGE_TYPES[0]
                
            else:
                card_get, card_get_message, card_get_message_type = get_card(id = card_id, debug = debug)
                if card_get:
                    proba = card_get[3]
                    c.execute('''INSERT INTO user_card_probabilities  (user_id, card_id, probabilite)
                                VALUES (?, ?, ?) ''', (user_id, card_id, proba))
                    conn.commit()
                    last_id = c.lastrowid
                    message = f"{SQL_MESSAGE['card_proba'][stss.language]} {card_id} {SQL_MESSAGE['for_user'][stss.language]} {user_id} {SQL_MESSAGE['created'][stss.language]}."
                    message_type = MESSAGE_TYPES[0]
                else:
                    message = f"{SQL_MESSAGE['card_proba'][stss.language]} {card_id} {SQL_MESSAGE['for_user'][stss.language]} {user_id} {SQL_WARNING['could_not_be_modified']} {card_get_message}"
                    message_type = card_get_message_type
                    
            user_card_proba_updated, user_card_proba_updated_message, _= get_user_card_probability_by_id(id = last_id, debug = debug)
            if not user_card_proba_updated:
                message = f"{message} {SQL_WARNING['but_wrong_event'][stss.language]}: {user_card_proba_updated_message}"
                message_type = MESSAGE_TYPES[1]
        
        except sqlite3Error as e:
            user_card_proba = None
            message = f"{SQL_ERRORS['error_user_create'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
      
    if debug:
        print(message)
        
    return user_card_proba_updated, message, message_type






# Mettre à jour la carte (vérifie si une entrée pour la mise à jour existe déjà)
def update_stats(is_correct: bool, debug: bool = False):
    today = datetime.now().strftime('%Y-%m-%d')   # mise au format SQL
    stat = None
    with database_connection(debug) as (conn, c):
        try:
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
        except sqlite3Error as e:
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
    except sqlite3Error as e :
        print(f"La probalité de la carte {card_id} n'a pas pu être mise à jour en raison de:\n{e}")
        return None
    return probabilite


# Récupérer les statistiques au cours du temps
def get_stats(debug: bool = False):
    with database_connection(debug) as (conn, c):
        try:
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
        except sqlite3Error as e:
            print(f"Les statistiques n'ont pas pu être lues en raison de:\n{e}")
            return None
    return stats



 #   events table (id, user_id, card_id, result, timestamp)
#---------------------------------------------------# 
#        Récupérer un événement par son ID          #
#---------------------------------------------------# 

def get_event_by_id(id: int, debug: bool = False) -> Tuple[Tuple[int, int, int, str, str] | None, str, str]:
    with database_connection(debug) as (_, c):
        try:       
            c.execute('''SELECT * FROM events WHERE id=? ''', (id,))
            event = c.fetchone()
            if event:
                message = f"{SQL_MESSAGE['event'][stss.language]} '{id}' {SQL_MESSAGE['is_get_db'][stss.language]}."
                message_type = MESSAGE_TYPES[0]
            else:
                message = f"{SQL_MESSAGE['event'][stss.language]} '{id}' {SQL_WARNING['not_in_db'][stss.language]}."
                message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            event = None
            message = f"{SQL_MESSAGE['error_missing_event'][stss.language]} '{id}': \n{e}"
            message_type = MESSAGE_TYPES[2]
            
    if debug:
        print(message)
        
    return event, message, message_type   
 



#---------------------------------------------------# 
#        Récupérer les événements par joeur         #
#---------------------------------------------------# 

def get_events_by_user_id(user_id: int, debug: bool = False) -> Tuple[Tuple[int, int, int, str, str] | None, str, str]:
    with database_connection(debug) as (_, c):
        try:       
            c.execute('''SELECT * FROM events WHERE user_id=? ''', (user_id,))
            event = c.fetchone()
            if event:
                message = f"{SQL_MESSAGE['event'][stss.language]} '{id}' {SQL_MESSAGE['is_get_db'][stss.language]}."
                message_type = MESSAGE_TYPES[0]
            else:
                message = f"{SQL_MESSAGE['event'][stss.language]} '{id}' {SQL_WARNING['not_in_db'][stss.language]}."
                message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            event = None
            message = f"{SQL_MESSAGE['error_missing_event'][stss.language]} '{id}': \n{e}"
            message_type = MESSAGE_TYPES[2]
            
    if debug:
        print(message)
        
    return event, message, message_type 
 
 
 
 
#---------------------------------------------------# 
#        Ajouter un évenement par user name         #
#---------------------------------------------------# 

def record_event_by_username(username: str, card_id: int, result: str, debug: bool = False) -> Tuple[Tuple[int, int, int, str, str] | None, str, str]:
    with database_connection(debug) as (conn, c):
        try:
            user, user_id_message, user_id_message_type = get_user_by_username(username = username, debug = debug)
            if not user:
                message = user_id_message
                message_type = user_id_message_type
            else:
                user_id = user[0]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute('''INSERT INTO events (user_id, card_id, result, timestamp)
                            VALUES (?, ?, ?, ?)''', (user_id, card_id, result, timestamp))
                conn.commit()
                last_id = c.lastrowid
                message = f"{SQL_MESSAGE['event_recorded'][stss.language]} {last_id}" 
                message_type = MESSAGE_TYPES[0]
                new_event, new_event_get_message, _ = get_event_by_id(id = last_id, debug = debug)
                if new_event is None:
                    message =  f"{message} {SQL_MESSAGE['but_wrong_event'][stss.language]}: {new_event_get_message}"
                    message_type = MESSAGE_TYPES[1]
                else:
                    event = new_event
                    
        except sqlite3Error as e:
            event = None
            message = f"{SQL_ERRORS['error_event_record'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
                
    return event, message, message_type



#---------------------------------------------------# 
#         Ajouter un évenement par user ID          #
#---------------------------------------------------# 

def record_event_by_user_id(user_id: str, card_id: int, result: str, debug: bool = False) -> Tuple[Tuple[int, int, int, str, str] | None, str, str]:
    with database_connection(debug) as (conn, c):
        try:

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute('''INSERT INTO events (user_id, card_id, result, timestamp)
                        VALUES (?, ?, ?, ?)''', (user_id, card_id, result, timestamp))
            conn.commit()
            last_id = c.lastrowid
            message = f"{SQL_MESSAGE['event_recorded'][stss.language]} {last_id}" 
            message_type = MESSAGE_TYPES[0]
            new_event, new_event_get_message, _ = get_event_by_id(id = last_id, debug = debug)
            if new_event is None:
                message =  f"{message} {SQL_MESSAGE['but_wrong_event'][stss.language]}: {new_event_get_message}"
                message_type = MESSAGE_TYPES[1]
            else:
                event = new_event
                    
        except sqlite3Error as e:
            event = None
            message = f"{SQL_ERRORS['error_event_record'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
                
    return event, message, message_type                