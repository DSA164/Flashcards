#===================================================#
#           Fonctions CRUD pour les thèmes          #
#===================================================#

from sqlite3 import Error as sqlite3Error
from common_language import LANGUAGE, MESSAGE_TYPES # ('success', 'warning', 'error', 'info')
from common_sqlite import database_connection, get_number_of_items, SQL_MESSAGE, SQL_WARNING, SQL_ERRORS
from typing import List, Tuple

from streamlit import session_state as stss
if 'language' not in stss:
            stss.language = LANGUAGE[0]


#---------------------------------------------------# 
#                  Créer un thème                   #
#---------------------------------------------------# 
def create_theme(theme_name: str, debug: bool = False) -> Tuple[Tuple[int, str] | None, str, str]:
    last_id = None
    theme_name = str(theme_name)
    with database_connection(debug) as (conn, c):
        try:
            themes, message_get, message_get_type = get_all_themes(debug)    
            if message_get_type == MESSAGE_TYPES[2]:
                message = f"{SQL_ERRORS['error_theme_create'][stss.language]}: \n{message_get} "
                message_type = message_get_type
                
            elif theme_name.lower() not in [t[1].lower() for t in themes]:
                c.execute("INSERT INTO themes (theme) VALUES (?)", (theme_name,))
                conn.commit()
                last_id = c.lastrowid
                
                if last_id:
                    message = f"{SQL_MESSAGE['theme'][stss.language]} '{theme_name}' {SQL_MESSAGE['created'][stss.language]} {last_id}."
                    message_type = MESSAGE_TYPES[0]

                    theme, message_get, message_get_type = get_theme(last_id, debug)
                    if theme is None:
                        message = f"{message} {SQL_MESSAGE['but_wrong_event'][stss.language]}: \n{message_get}"
                        message_type = MESSAGE_TYPES[1]
            
            else:
                id, _, _ = get_theme_id(theme_name, debug)
                theme, _, _ = get_theme(id, debug)
                message = f"{SQL_MESSAGE['theme'][stss.language]} '{theme_name}' {SQL_WARNING['already_existing_db'][stss.language]}!"
                message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            theme = None
            message = f"{SQL_ERRORS['error_theme_create'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]  
            
        if debug:
            print(message)

    return theme, message, message_type
            



#---------------------------------------------------# 
#                Récupérer un thème                 #
#---------------------------------------------------#   
def get_theme(id: int, debug: bool = False) -> Tuple[Tuple[int, str] | None, str, str]:
    with database_connection(debug) as (_, c):
        try:
            c.execute("SELECT * FROM themes WHERE id=?", (id, ))
            theme = c.fetchone()
            if theme is not None:
                message = f"{SQL_MESSAGE['theme'][stss.language]} {id} {SQL_MESSAGE['is_get_db'][stss.language]}."
                message_type = MESSAGE_TYPES[0]
            else:
                message = f"{SQL_MESSAGE['theme'][stss.language]} {id} {SQL_WARNING['not_in_db'][stss.language]}."
                message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            theme = None
            message = f"{SQL_MESSAGE['error_missing_theme'][stss.language]} {id}: \n{e}"
            message_type = MESSAGE_TYPES[2]
            
        if debug:
            print(message)
            
    return theme, message, message_type




#---------------------------------------------------# 
#              Mettre à jour un thème               #
#---------------------------------------------------# 
def update_theme(id: int, theme_name:str, debug: bool = False) -> Tuple[Tuple[int, str] | None, str, str]:
    with database_connection(debug) as (conn, c):
        try:
            c.execute("UPDATE themes SET theme=? WHERE id=?", (theme_name, id))
            conn.commit()
            message = f"{SQL_MESSAGE['theme'][stss.language]} {id} {SQL_MESSAGE['is_updated_db'][stss.language]} {SQL_MESSAGE['with_following_info'][stss.language]}: \n{theme_name}"
            message_type = MESSAGE_TYPES[0]
            updated_theme, message_get, _ = get_theme(id, debug)
            
            if updated_theme is None:
                message = f"{message} {SQL_MESSAGE['but_wrong_event'][stss.language]}: {message_get}"
                message_type = MESSAGE_TYPES[1]
          
        except sqlite3Error as e:
            message = f"{SQL_ERRORS['error_theme_update'][stss.language]} {id}: \n{e}"
            updated_theme = None
            message_type = MESSAGE_TYPES[2]
            
        if debug:
            print(message)
            
    return updated_theme, message, message_type

    
    
    

#---------------------------------------------------# 
#                Supprimer un thème                 #
#---------------------------------------------------# 
def delete_theme(id: int, debug: bool = False) -> Tuple[Tuple[int, str] | None, str, str]:
    with database_connection(debug) as (conn, c):
        try:
            deleted_theme, message_get, message_get_type = get_theme(id, debug)
            if deleted_theme is None:
                message = message_get
                message_type = message_get_type
                
            else:
                c.execute("DELETE FROM themes WHERE id=?", (id, ))
                conn.commit()
                if c.rowcount > 0:
                    message = f"{SQL_MESSAGE['theme'][stss.language]} {id} {SQL_MESSAGE['is_removed_db'][stss.language]}."
                    message_type = MESSAGE_TYPES[0]
                else:
                    deleted_theme = None
                    message = f"{SQL_MESSAGE['theme'][stss.language]} {id} {SQL_WARNING['not_in_db'][stss.language]}, {SQL_WARNING['already_removed'][stss.language]}"
                    message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            deleted_theme = None
            message = f"{SQL_MESSAGE['theme'][stss.language]} {id} {SQL_ERRORS['error_is_removed_db_'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
            
        if debug:
            print(message)
            
    return deleted_theme, message, message_type




#---------------------------------------------------# 
#            Récupérer toutes les thèmes            #
#---------------------------------------------------# 
def get_all_themes(debug: bool = False) -> Tuple[List[Tuple[int, str]] | None, str, str]:
    with database_connection(debug) as (_, c):
        try:
            c.execute("SELECT * FROM themes")
            themes = c.fetchall()
            if themes is not None:
                if themes:
                    message = SQL_MESSAGE['all_themes_get'][stss.language]
                    message_type = MESSAGE_TYPES[0]
                else:
                    message = SQL_WARNING['themes_table_empty'][stss.language]
                    message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            themes =  None
            message = f"{SQL_ERRORS['error_all_themes_get'][stss.language]} \n{e}"
            message_type = MESSAGE_TYPES[2]
        
        if debug:
            print(message)

    return themes, message, message_type






#----------------------------------------------------# 
#         Retourner le nombre total de cartes        #
#----------------------------------------------------#
def get_number_of_theme(debug: bool = False) -> Tuple[int | None, str, str]: 
    count, message, message_type = get_number_of_items('themes', 'thèmes', debug = debug)
        
    return count,message, message_type
   
   
   
   
#---------------------------------------------------# 
#             Récupérer l'id d'un thème             #
#---------------------------------------------------# 
def get_theme_id(theme:str, debug: bool = False) -> Tuple[int | None, str, str]:
    with database_connection(debug) as (_, c):
        try:
            c.execute("SELECT id FROM themes WHERE theme=? COLLATE NOCASE", (theme,))
            id = c.fetchone() # None or (int,)
            if id is not None:
                id = id[0]
                message = f"{SQL_MESSAGE['theme'][stss.language]} {id} {SQL_MESSAGE['theme'][stss.language]} '{theme}' {SQL_MESSAGE['is_get_db'][stss.language]}."
                message_type = MESSAGE_TYPES[0]
                
            else:
                message = f"{SQL_MESSAGE['theme'][stss.language]} '{theme}' {SQL_WARNING['not_in_db'][stss.language]}!"
                message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            id = None
            message = f"{SQL_ERRORS['error_get_theme_id'][stss.language]}:\n{e}"
            message_type = MESSAGE_TYPES[2]
        
        if debug:
            print(message)
            
        return id, message, message_type
    


#--------------------------------------------------------------------------------------------------# 
#          Retourner la liste de theme ids exitants sans ceux qui aurait pu être supprimés         #
#--------------------------------------------------------------------------------------------------# 
def get_existing_theme_ids(debug: bool = False) -> Tuple[List[int] | None, str, str]:
    with database_connection() as (_, c):
        try:
            c.execute("SELECT id FROM themes ORDER BY id")
            exiting_theme_ids = [row[0] for row in c.fetchall()]
            if exiting_theme_ids:
                message = SQL_MESSAGE['list_themes_ID'][stss.language]
                message_type = MESSAGE_TYPES[0]
            else:
                message = SQL_WARNING['themes_table_empty'][stss.language] 
                message_type = MESSAGE_TYPES[1]
                
        except sqlite3Error as e:
            exiting_theme_ids = None
            message = f"{SQL_ERRORS['error_list_theme_ID'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
            
        if debug:
            print(message)
            
    return exiting_theme_ids, message, message_type 


#-------------------------------------------------------------------------------------------# 
#                 Retourner la liste de theme ids utilisé par les cartes                    #
#-------------------------------------------------------------------------------------------# 
def get_used_theme_ids(debug: bool  =False) -> Tuple[List[int] | None, str, str]:
    with database_connection() as (_, c):
        try:
            c.execute("SELECT DISTINCT id_theme FROM cards")
            used_theme_ids = [row[0] for row in c.fetchall()]
            if used_theme_ids:
                message = SQL_MESSAGE['list_used_themes_ID'][stss.language]
                message_type = MESSAGE_TYPES[0]
            else:
                message = SQL_WARNING['cards_table_empty_id_theme'][stss.language] 
                message_type = MESSAGE_TYPES[1]
        
        
        except sqlite3Error as e:
            used_theme_ids = None
            message = f"{SQL_ERRORS['error_list_themes_ID_from_cards'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
            
        if debug:
            print(message)
            print(f"used_theme_ids: {used_theme_ids}")
            
    return used_theme_ids, message, message_type

