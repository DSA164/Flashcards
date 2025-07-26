#=====================================================#
#        Eléments communs aux fonctions sqlite3       #
#=====================================================#


from sqlite3 import connect
from contextlib import contextmanager  # contextmanager pour: yield
from sqlite3 import Error as sqlite3Error
from typing import Tuple
from common_language import LANGUAGE, MESSAGE_TYPES # ('success', 'warning', 'error', 'info')

from streamlit import session_state as stss
if 'language' not in stss:
            stss.language = LANGUAGE[0]
language = stss.language

SQL_MESSAGE = {
    'and': {
            LANGUAGE[0]: 'et',
            LANGUAGE[1]: 'and',
        },
    'card': {
            LANGUAGE[0]: 'La carte',
            LANGUAGE[1]: 'The cards',
        },
    'theme': {
            LANGUAGE[0]: 'Le theme',
            LANGUAGE[1]: 'The theme',
        },  
    'user': {
            LANGUAGE[0]: "L'utilisateur",
            LANGUAGE[1]: 'The user',
        },
    'id': {
            LANGUAGE[0]: "L'ID",
            LANGUAGE[1]: 'The ID',
        },
    'at_id': {
            LANGUAGE[0]: "à l'ID",
            LANGUAGE[1]: 'at the ID',
        },
    'event': {
            LANGUAGE[0]: "L'événement",
            LANGUAGE[1]: 'The event',
        },
    'existing': {
            LANGUAGE[0]: 'existant',
            LANGUAGE[1]: 'current',
        },
    'existing_f': {
            LANGUAGE[0]: 'existante',
            LANGUAGE[1]: 'current',    
        },
    'get_all_cards_success': {
            LANGUAGE[0]: 'La carte',
            LANGUAGE[1]: 'The cards',
        },
    'card_created': {
            LANGUAGE[0]: "La carte a été ajoutée à la base de données à l'ID",
            LANGUAGE[1]: "The card has been added to the database at ID",
        },
    'user_created': {
            LANGUAGE[0]: "L'utilisateur a été ajouté à la base de données à l'ID",
            LANGUAGE[1]: "The user has been added to the database at ID",
        },
    'event_recorded': {
            LANGUAGE[0]: "L'événement a été enregistré dans la base de données à l'ID",
            LANGUAGE[1]: "The event has been recorded intto the database at ID",
        },
    'card_proba': {
            LANGUAGE[0]: "La probabilité d'apparition de la carte ID =",
            LANGUAGE[1]: "The appearance probability for the card ID =",
        },
    'for_user': {
            LANGUAGE[0]: "pour l'utilisateur ID =",
            LANGUAGE[1]: "for the user ID =",
        },
    'user_card_proba': {
            LANGUAGE[0]: "La 'user card proba' à l'ID",
            LANGUAGE[1]: "La 'user card proba' at the ID",
        },
    'created': {
            LANGUAGE[0]: "a été ajouté à la base de données à l'ID",
            LANGUAGE[1]: "has been added to the database at ID",
        },
    'created_f': {
            LANGUAGE[0]: "a été ajoutée à la base de données à l'ID",
            LANGUAGE[1]: "has been added to the database at ID",
        },
    'is_get_db': {
            LANGUAGE[0]: 'a été recupéré de la base de données',
            LANGUAGE[1]: 'has been retrieved from the database',
        },
    'is_get_db_f': {
            LANGUAGE[0]: 'a été recupérée de la base de données',
            LANGUAGE[1]: 'has been retrieved from the database',
        },
    'is_removed_db': {
            LANGUAGE[0]: 'a été supprimé de la base de données',
            LANGUAGE[1]: 'is removed from the database',
        },
    'is_removed_db_f': {
            LANGUAGE[0]: 'a été supprimée de la base de données',
            LANGUAGE[1]: 'is removed from the database',
        },
    'is_updated_db': {
            LANGUAGE[0]: 'a été mis à jour dans la base de données',
            LANGUAGE[1]: 'is updated in the database',
        },
    'is_updated_db_f': {
            LANGUAGE[0]: 'a été mise à jour dans la base de données',
            LANGUAGE[1]: 'is updated in the database',
        },
    'all_cards_get': {
            LANGUAGE[0]: 'La list des cartes a été récupérée de la base de données',
            LANGUAGE[1]: "The cards's list has been retrieved from the database",
        },
    'all_themes_get': {
            LANGUAGE[0]: 'La list des thèmes a été récupérée de la base de données',
            LANGUAGE[1]: "The themes's list has been retrieved from the database",
        },
    'all_users_get': {
            LANGUAGE[0]: 'La list des utilisateurs a été récupérée de la base de données',
            LANGUAGE[1]: "The users's list has been retrieved from the database",
        },
    'with_following_info': {
            LANGUAGE[0]: 'avec les informations suivantes',
            LANGUAGE[1]: 'with the following information',
        },
    'cards_list_with_themeID': {
            LANGUAGE[0]: 'La liste des cartes ayant le thème ID = ',
            LANGUAGE[1]: "The cards's list with the ID theme = ",
        },
    'list_cards_ID': {
            LANGUAGE[0]: "La liste des ID des cartes a été recupérée de la table 'cards'",
            LANGUAGE[1]: "The list of cards's ID has been retrieved from the 'cards' table.",
        },
    'list_themes_ID': {
            LANGUAGE[0]: "La liste des ID des thèmes a été recupérée de la table 'themes'",
            LANGUAGE[1]: "The list of themes's ID has been retrieved from the 'themes' table.",
        },
    'list_used_themes_ID': {
            LANGUAGE[0]: "La liste des ID des thèmes utilisée a été recupérée de la table 'cards'",
            LANGUAGE[1]: "The list of used themes's ID has been retrieved from the 'cards' table.",
        },
    'with_question': {
            LANGUAGE[0]: 'avec la question',
            LANGUAGE[1]: 'with the question',
        },
    'number_of': {
            LANGUAGE[0]: 'Le nombre de',
            LANGUAGE[1]: 'The number of',
        },
    'in_table': {
            LANGUAGE[0]: 'dans la table',
            LANGUAGE[1]: 'in the table',
        },
    'list_events_by_user': {
            LANGUAGE[0]: "La liste des évenements pour l'utilisateur",
            LANGUAGE[1]: 'The list of events for the user',
        },
    'list_events_by_user_id': {
            LANGUAGE[0]: "La liste des évenements pour l'utilisateur",
            LANGUAGE[1]: 'The list of events for the user',
        },
    'user_card_proba_id': {
            LANGUAGE[0]: "L'ID de la 'user card proba' (user_id, card_id) = ",
            LANGUAGE[1]: "The ID of the 'user card proba' (user_id, card_id) =  ",
        },

}



SQL_WARNING = {
    'user_exist': {
            LANGUAGE[0]: "Ce nom d'utilisateur exite déjà dans la base de donnée à l'ID",
            LANGUAGE[1]: 'This user name already exists in the database at the ID',    
        },
    'not_in_db': {
            LANGUAGE[0]: "n'existe pas dans la base de données",
            LANGUAGE[1]: 'does not exist in the database',    
        },
    'cards_table_empty': {
            LANGUAGE[0]: "La table 'cards' est vide!",
            LANGUAGE[1]: "the 'cards' table is empty!",
        },
    'themes_table_empty': {
            LANGUAGE[0]: "La table 'themes' est vide!",
            LANGUAGE[1]: "The 'themes' table is empty!",
        },
    'users_table_empty': {
            LANGUAGE[0]: "La table 'users' est vide!",
            LANGUAGE[1]: "The 'users' table is empty!",
        },
    'cards_table_empty_id_theme': {
            LANGUAGE[0]: "La table 'cards' est vide ou bien les cartes présentes ne pointent vers aucun theme!",
            LANGUAGE[1]: "The 'cards' table is empty, or the existing cards are not associated with any theme!",
        },
    'but_wrong_event': {
            LANGUAGE[0]: "Mais, l'événement suivant c'est produit",
            LANGUAGE[1]: "However, the following event occurred",
        },
    'already_removed': {
            LANGUAGE[0]: "vous avez peut-être lancer la commande plusieurs fois ou un autre processus l'a supprimé pendant l'exécution!",
            LANGUAGE[1]: "You may have run the command multiple times, or another process deleted it during execution!",
        },
    'no_card_with_themeID': {
            LANGUAGE[0]: "Il n'y a pas de carte ayant le thème ID = ",
            LANGUAGE[1]: "There are no cards with ID theme = ",
        },
    'no_card_with_question': {
            LANGUAGE[0]: "Il n'existe aucune carte dans la base de données avec la question",
            LANGUAGE[1]: "There are no cards in the database with the question",
        },
    'wrong_card_probability': {
            LANGUAGE[0]: "La carte n'a pas été créée car la probabilité d'apparition n'est pas comprise entre",
            LANGUAGE[1]: "The card was not created because the appearance probability is not between",
        },
    'wrong_card_probability_update': {
            LANGUAGE[0]: "La carte n'a pas été mise à jour car la probabilité d'apparition n'est pas comprise entre",
            LANGUAGE[1]: "The card was not updated because the appearance probability is not between",
        },
    'already_existing_db': {
            LANGUAGE[0]: "est déjà présent dans la base de données",
            LANGUAGE[1]: "is already present in the database",
        },
    'could_not_be_modified': {
            LANGUAGE[0]: "n'a pus pu être modifiée en raison de:",
            LANGUAGE[1]: "could not be modified for the following reason:",
        },
    
}




SQL_ERRORS = {
    'error_table': {
            LANGUAGE[0]: 'Table inconnue ou non autorisée',
            LANGUAGE[1]: 'Unknown or unauthorized table',
        },
    'error_access_db': {
            LANGUAGE[0]: 'Une erreur est survenue lors de la tentative de connection à la base de donnée',
            LANGUAGE[1]: 'An error occurred while attempting to connect to the database',
        },
    'error_missing_card': {
            LANGUAGE[0]: 'Une erreur est survenue lors de la tentative de récupération de la carte',
            LANGUAGE[1]: 'An error occurred while attempting to retrieve the card',
        },
    'error_missing_theme': {
            LANGUAGE[0]: 'Une erreur est survenue lors de la tentative de récupération du thème',
            LANGUAGE[1]: 'An error occurred while attempting to retrieve the theme',
        },
    'error_missing_user': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de récupération de l'utilisateur",
            LANGUAGE[1]: 'An error occurred while attempting to retrieve the user',
        },
    'error_missing_event': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de récupération de l'événement",
            LANGUAGE[1]: 'An error occurred while attempting to retrieve the event',
        },
    'error_all_cards_get': {
            LANGUAGE[0]: "La liste des cartes n'a pas pu être récupérée de la base de données, en raison de",
            LANGUAGE[1]: "The list of cards could not be retrieved from the database due to",
        },
    'error_all_themes_get': {
            LANGUAGE[0]: "La liste des thèmes n'a pas pu être récupérée de la base de données, en raison de",
            LANGUAGE[1]: "The list of themes could not be retrieved from the database due to",
        },
    'error_all_users_get': {
            LANGUAGE[0]: "La liste des utilisateurs n'a pas pu être récupérée de la base de données, en raison de",
            LANGUAGE[1]: "The list of users could not be retrieved from the database due to",
        },
    'error_card_create': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de création de la carte",
            LANGUAGE[1]: "An error occurred while attempting to create the card",
        },  
    'error_theme_create': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de création du theme",
            LANGUAGE[1]: "An error occurred while attempting to create the theme",
        },   
    'error_user_create': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de création de l'utilisateur",
            LANGUAGE[1]: "An error occurred while attempting to create the user",
        }, 
    'error_event_record': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de enregistrement de l'événement",
            LANGUAGE[1]: "An error occurred while attempting to record the event",
        }, 
    'error_card_update': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de mise à jour de la carte",
            LANGUAGE[1]: "An error occurred while attempting to update the card",
        },
    'error_get_theme_id': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de récupération de l'ID du theme",
            LANGUAGE[1]: "An error occurred while attempting to get the theme's ID",
        },
    'error_get_user_card_proba_id': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de récupération de l'ID de la 'user card proba' (user_id, card_id) =",
            LANGUAGE[1]: "An error occurred while attempting to get the 'user card proba' ID for (user_id, card_id) =",
        },
    'error_get_user_card_proba_by_id': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de récupération de la 'user card proba' à l'ID",
            LANGUAGE[1]: "An error occurred while attempting to get the 'user card proba' at the ID",
        },
    'error_theme_update': {
            LANGUAGE[0]: "Une erreur est survenue lors de la tentative de mise à jour de la carte",
            LANGUAGE[1]: "An error occurred while attempting to update the card",
        },
    'error_is_removed_db': {
            LANGUAGE[0]: "n'a pas pu être supprimé de la base de donnée en raison de",
            LANGUAGE[1]: "could not be removed from the database due to",
        },
    'error_is_removed_db_f': {
            LANGUAGE[0]: "n'a pas pu être supprimée de la base de donnée en raison de",
            LANGUAGE[1]: "could not be removed from the database due to",
        },
    'error_list_cards_ID': {
            LANGUAGE[0]: "La liste des ID des cartes n'a pu être recupérée de la table 'cards' en raison de",
            LANGUAGE[1]: "The list of cards's ID could not be retrieved from the 'cards' table due to",
        },
    'error_list_themes_ID': {
            LANGUAGE[0]: "La liste des ID des thèmes n'a pu être recupérée de la table 'themes' en raison de",
            LANGUAGE[1]: "The list of themes's ID could not be retrieved from the 'themes' table due to",
        },
    'error_list_themes_ID_from_cards': {
            LANGUAGE[0]: "La liste des ID des thèmes n'a pu être recupérée de la table 'cards' en raison de",
            LANGUAGE[1]: "The list of themes's ID could not be retrieved from the 'cards' table due to",
        },
    'error_card_with_question': {
            LANGUAGE[0]: "La vérification de la présence de la carte dans la base de données n'a pas pu être exécutée en raison de",
            LANGUAGE[1]: "The check for the presence of the card in the database could not be performed due to",
        },
    'error_number_of': {
            LANGUAGE[0]: 'Une erreur est survenue lors de la tentative de récupération du nombre de',
            LANGUAGE[1]: 'An error occurred while attempting to the number of',
        },
    
     
        
}


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

# Accéder à la base de donnée
@contextmanager
def database_connection(debug: bool = False):
    conn = None
    try:
        conn = connect('flashcard.db')
        open_db(debug)
        c = conn.cursor()
        yield conn, c   # permet de retourner sans intérompre la fonction
    except sqlite3Error as e:
        print(f"{SQL_ERRORS['error_access_db'][language]}:\n{e}")
        raise # pour que l'erreur soit accessible depuis la fonction parente
    finally: # try: finally: pour s'assurer que la connection à la base de donnée soit toujours fermée même en cas d'erreur
        if conn is not None:
            conn.close()
            close_db(debug)
            

#--------------------------------------------------------------------------------------# 
#         Retourner le nombre total d'élement d'une table de la base de données        #
#--------------------------------------------------------------------------------------#
def get_number_of_items(table_name: str, item_name: str, debug: bool = False) -> Tuple[int | None, str, str]:
    with database_connection(debug) as (_, c):
        try:
            # Récupérer dynamiquement la liste des tables existantes
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = {row[0] for row in c.fetchall()}
            
            # Evite le risque d'injection SQL
            if table_name not in tables:
                raise ValueError(f"{SQL_ERRORS['error_table'][language]}: {table_name}")

            c.execute(f"SELECT COUNT(id) FROM {table_name}")
            count = c.fetchone()[0]
            message = f"{SQL_MESSAGE['number_of'][language]} {item_name} {SQL_MESSAGE['in_table'][language]} '{table_name}' {SQL_MESSAGE['is_get_db'][language]}."
            message_type = MESSAGE_TYPES[0]

        except sqlite3Error as e:
            count = None
            message = f"{SQL_ERRORS['error_number_of'][language]} {item_name} {SQL_MESSAGE['in_table'][language]} '{table_name}': {e}"
            message_type = MESSAGE_TYPES[2]
        except ValueError as e:
            count = None
            message = str(e)
            message_type = MESSAGE_TYPES[1]

    if debug:
        print(message)

    return count, message, message_type
