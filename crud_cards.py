#===================================================#
#        Fonctions CRUD pour les flashcards         #
#===================================================#

from sqlite3 import Error as sqlite3Error
from common_sqlite import MESSAGE_TYPES, database_connection
from typing import List, Tuple
from common_language import LANGUAGE, MESSAGE_TYPES # ('success', 'warning', 'error', 'info')
from common_sqlite import get_number_of_items, SQL_MESSAGE, SQL_WARNING, SQL_ERRORS

from streamlit import session_state as stss
if 'language' not in stss:
            stss.language = LANGUAGE[0]



# Fixer l'intervale de valeur d'apparition d'une carte 
PROB_MIN = 0.1
PROB_MAX = 0.9
        
        
# cards (id, question, reponse, probabilite, id_theme) 
#------------------------------------------------------   
    
#---------------------------------------------------# 
#                  Créer une carte                  #
#---------------------------------------------------#
def create_card(question: str, reponse: str, probabilite: float, id_theme: int, debug: bool = False) -> Tuple[Tuple[int, str, str, float, int] | None, str, str]: 
    with database_connection(debug) as (conn, c):
        try:
            existing_card, existing_card_message, existing_card_message_type = get_card_by_question(question = question, debug = debug)
            
            if existing_card_message_type == MESSAGE_TYPES[2]:
                card = existing_card
                message = existing_card_message
                message_type = existing_card_message_type
                
            elif existing_card_message_type == MESSAGE_TYPES[0]:
                card = existing_card
                message = existing_card_message
                message_type = existing_card_message_type
                
            else:
                if probabilite < PROB_MIN or probabilite > PROB_MAX:
                    card = None
                    message = f"{SQL_WARNING['wrong_card_probability'][stss.language]} {PROB_MIN} {SQL_MESSAGE['and'][stss.language]} {PROB_MAX}!"
                    message_type = MESSAGE_TYPES[1]
                
                else:
                    c.execute('''INSERT INTO cards (question, reponse, probabilite, id_theme) 
                                VALUES (?, ?, ?, ?)
                            ''', (question, reponse, probabilite, id_theme)
                            )
                    conn.commit()
                    last_id = c.lastrowid
                    message = f"{SQL_MESSAGE['card_created'][stss.language]} {last_id}" 
                    message_type = MESSAGE_TYPES[0]
                    card, card_message, _ = get_card(id = last_id, debug = debug)
                    if card is None:
                        message =  f"{message} {SQL_MESSAGE['but_wrong_event'][stss.language]}: {card_message}"
                        message_type = MESSAGE_TYPES[1]
                    
        except sqlite3Error as e:
            card = None
            message = f"{SQL_ERRORS['error_card_create'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
      
    if debug:
        print(message)
            
    return card, message, message_type
    
    
    

#---------------------------------------------------# 
#                 Récupérer une carte               #
#---------------------------------------------------#
def get_card(id: int, debug: bool = False) -> Tuple[Tuple[int, str, str, float, int] | None, str, str]:
    with database_connection(debug) as (_, c):
        try:
            c.execute("SELECT * FROM cards WHERE id=?", (id, )) 
            card = c.fetchone()
            if card:
                message = f"{SQL_MESSAGE['card'][stss.language]} {id} {SQL_MESSAGE['is_get_db_f'][stss.language]}."
                message_type = MESSAGE_TYPES[0]
            else:
                message = f"{SQL_MESSAGE['card'][stss.language]} {id} {SQL_WARNING['not_in_db'][stss.language]}."
                message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            card = None
            message = f"{SQL_MESSAGE['error_missing_card'][stss.language]} {id}: \n{e}"
            message_type = MESSAGE_TYPES[2]
            
    if debug:
        print(message)
        
    return card, message, message_type
    



#--------------------------------------------------------------# 
#      Mettre à jour une carte avec des nouvelles données      #
#--------------------------------------------------------------#
def update_card(id: int, question: str, reponse: str, probabilite: float, id_theme: int, debug: bool = False) -> Tuple[Tuple[int, str, str, float, int] | None, str, str]:
    if probabilite < PROB_MIN or probabilite > PROB_MAX:
        updated_card = None
        message = f"{SQL_WARNING['wrong_card_probability_update'][stss.language]} {PROB_MIN} {SQL_MESSAGE['and'][stss.language]} {PROB_MAX}!"
        message_type = MESSAGE_TYPES[1]
        
    else:
        with database_connection(debug) as (conn, c):
            try:
                c.execute('''UPDATE cards SET question=? , reponse=?, probabilite=?, id_theme=? WHERE id=?
                        ''',(question, reponse, probabilite, id_theme, id))
                conn.commit()
                message = f"{SQL_MESSAGE['card'][stss.language]} {id} {SQL_MESSAGE['is_updated_db_f'][stss.language]} {SQL_MESSAGE['with_following_info'][stss.language]}." 
                message_type = MESSAGE_TYPES[0]
                updated_card, message_get, _ = get_card(id = id, debug = debug)

                if updated_card is None:
                    message = f"{message} {SQL_MESSAGE['but_wrong_event'][stss.language]}: {message_get}"
                    message_type = MESSAGE_TYPES[1]
                        
            except sqlite3Error as e:
                updated_card = None
                message = f"{SQL_ERRORS['error_theme_update'][stss.language]} {id}: \n{e}"
                message_type = MESSAGE_TYPES[2]
            
    if debug:
        print(message)
        
    return updated_card, message, message_type
    
    but_wrong_event
    

#---------------------------------------------------# 
#                Supprimer une carte                #
#---------------------------------------------------#
def delete_card(id: int, debug: bool = False) -> Tuple[Tuple[int, str, str, float, int] | None, str, str]:
    with database_connection(debug) as (conn, c):
        try:
            deleted_card, card_message, card_message_type = get_card(id = id, debug = debug)
            if deleted_card is None:
                message = card_message
                message_type = card_message_type
            else:
                c.execute("DELETE FROM cards WHERE id=?", (id, ))
                conn.commit()
                if c.rowcount > 0:
                    message = f"{SQL_MESSAGE['card'][stss.language]} {id} {SQL_MESSAGE['is_removed_db_f'][stss.language]}."
                    message_type = MESSAGE_TYPES[0]
                        
                else:
                    deleted_card = None
                    message = f"{SQL_MESSAGE['card'][stss.language]} {id} {SQL_WARNING['not_in_db'][stss.language]}, {SQL_WARNING['already_removed'][stss.language]}"
                    message_type = MESSAGE_TYPES[1]

                      
        except sqlite3Error as e:
            deleted_card = None
            message = f"{SQL_MESSAGE['card'][stss.language]} {id} {SQL_ERRORS['error_is_removed_db_f'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
            
    if debug:
        print(message)
        
    return deleted_card, message, message_type




#---------------------------------------------------# 
#            Récupérer toutes les cartes            #
#---------------------------------------------------#
def get_all_cards(debug: bool = False) -> Tuple[List[Tuple[int, str, str, float, int]] | None, str, str]:
    with database_connection(debug) as (_, c):
        try:
            c.execute("SELECT * FROM cards")
            cards = c.fetchall()
            if cards is not None:
                if cards:
                    message = SQL_MESSAGE['all_cards_get'][stss.language]
                    message_type = MESSAGE_TYPES[0]
                else:
                    message = SQL_WARNING['cards_table_empty'][stss.language]
                    message_type = MESSAGE_TYPES[1]

        except sqlite3Error as e:
            cards =  None
            message = f"{SQL_ERRORS['error_all_cards_get'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
    
    if debug:
        print(message)
        
    return cards, message, message_type


 
 

#----------------------------------------------------# 
#         Retourner le nombre total de cartes        #
#----------------------------------------------------#
def get_number_of_cards(debug: bool = False) -> Tuple[int | None, str, str]: 
    count, message, message_type = get_number_of_items('cards', 'cartes', debug = debug)
        
    return count, message, message_type


    

#--------------------------------------------------------------------# 
#      Récupérer les cartes appartenant à un thème particulier       #
#--------------------------------------------------------------------#
def get_cards_by_theme(id_theme: int, debug: bool = False) -> Tuple[List[Tuple[int, str, str, float, int]] | None, str, str]:
    with database_connection(debug) as (_, c):    
        try:
            c.execute("SELECT * FROM cards WHERE id_theme=?", (id_theme,))
            cards = c.fetchall()
            if cards is not None:
                message = f"{SQL_MESSAGE['cards_list_with_themeID'][stss.language]} {id_theme} {SQL_MESSAGE['is_get_db_f'][stss.language]}:\n"
                message_type = MESSAGE_TYPES[0]
            else:
                message = f"{SQL_WARNING['no_card_with_themeID'][stss.language]} {id_theme}"
                message_type = MESSAGE_TYPES[1]
                
        except sqlite3Error as e:
            cards = None
            message = f"{SQL_ERRORS['error_all_cards_get'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
                 
        if debug:
            print(message)
            
    return cards, message, message_type




#--------------------------------------------------------------------------------------------# 
#          Retourner la liste de ids exitants sans ceux qui aurait pu être supprimés         #
#--------------------------------------------------------------------------------------------#
def get_existing_card_ids(debug: bool = False):
    with database_connection() as (_, c):
        try:
            c.execute("SELECT id FROM cards ORDER BY id")
            exiting_cards_ids = [row[0] for row in c.fetchall()]
            if exiting_cards_ids:
                message = SQL_MESSAGE['list_cards_ID'][stss.language]
                message_type = MESSAGE_TYPES[0]
            else:
                message = SQL_WARNING['cards_table_empty'][stss.language] 
                message_type = MESSAGE_TYPES[1]
                
        except sqlite3Error as e:
            exiting_cards_ids = None
            message = f"{SQL_ERRORS['error_list_cards_ID'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
            
        if debug:
            print(message)
            
    return exiting_cards_ids, message, message_type 




#------------------------------------------------------------------------# 
#      Retourner une carte si elle existe avec une question donnée       #
#------------------------------------------------------------------------#
def get_card_by_question(question, debug: bool = False) -> Tuple[Tuple[int, str, str, float, int] | None, str, str]:
    with database_connection() as (_, c):
        try:
            c.execute("SELECT * FROM cards WHERE question=? COLLATE NOCASE", (question,))
            card = c.fetchone()
            if card is not None:
                message = f"{SQL_MESSAGE['card'][stss.language]} {card[0]} {SQL_MESSAGE['is_get_db_f'][stss.language]} {SQL_MESSAGE['with_question']}: \"{question}\"" 
                message_type = MESSAGE_TYPES[0]
            else:
                message = f"{SQL_WARNING['no_card_with_question'][stss.language]}: \"{question}\"" 
                message_type = MESSAGE_TYPES[1]
                
        except sqlite3Error as e:
            card = None
            message = f"{SQL_ERRORS['error_card_with_question'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
            
        if debug:
            print(message)
            
    return card, message, message_type 
