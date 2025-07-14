#===================================================#
#        Fonctions CRUD pour les flashcards         #
#===================================================#

from sqlite3 import Error as sqlite3Error
from common_sqlite import MESSAGE_TYPES, database_connection
from typing import List, Tuple
from common_language import LANGUAGE, MESSAGE_TYPES # ('success', 'warning', 'error', 'info')
from common_sqlite import get_number_of_items, SQL_MESSAGE, SQL_WARNING, SQL_ERRORS
from datetime import datetime 
from streamlit_authenticator.utilities.hasher import Hasher

from streamlit import session_state as stss
if 'language' not in stss:
            stss.language = LANGUAGE[0]

      
# users (id, username, user_password, role, date_joined)   All TEXT except id INTEGER
#--------------------------------------------------------------------------------------   
    
#---------------------------------------------------# 
#                Créer un utilisateur               #
#---------------------------------------------------#
def create_user(username: str, name: str, user_password: str, role: str = 'user',  debug: bool = False) -> Tuple[Tuple[int, str, str, str, str, str] | None, str, str]:
    with database_connection(debug) as (conn, c):
        try:
            existing_user, existing_user_message, existing_user_message_type = get_user_by_username(username = username, debug = debug)
            
            if existing_user_message_type == MESSAGE_TYPES[2]:
                user = existing_user
                message = existing_user_message
                message_type = existing_user_message_type
                
            elif existing_user:
                user = existing_user
                message = f"{SQL_WARNING['user_exist'][stss.language]} {user[0]}!"
                message_type = existing_user_message_type
                
            else:     
                date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                hashed_password = Hasher.hash(user_password.strip())
                username = username.strip()
                name = name.strip()
                
                c.execute('''INSERT INTO users (username, name, user_password, role, date_joined) 
                            VALUES (?, ?, ?, ?, ?)
                        ''', (username, name, hashed_password, role, date_joined)
                        )
                conn.commit()
                last_id = c.lastrowid
                message = f"{SQL_MESSAGE['user_created'][stss.language]} {last_id}" 
                message_type = MESSAGE_TYPES[0]
                new_user, new_user_get_message, _ = get_user_by_ID(id = last_id, debug = debug)
                if new_user is None:
                    message =  f"{message} {SQL_MESSAGE['but_wrong_event'][stss.language]}: {new_user_get_message}"
                    message_type = MESSAGE_TYPES[1]
                else:
                    user = new_user
                    
        except sqlite3Error as e:
            user = None
            message = f"{SQL_ERRORS['error_user_create'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
      
    if debug:
        print(message)
            
    return user, message, message_type






#---------------------------------------------------# 
#       Obtenir l'utilisateur par son surnom        #
#---------------------------------------------------#
def get_user_by_username(username: str = '', debug: bool = False) -> Tuple[Tuple[int, str, str, str, str, str] | None, str, str]:    
    with database_connection(debug) as (_, c):
        try:
            c.execute("SELECT * FROM users WHERE username=? COLLATE NOCASE", (username, )) 
            user = c.fetchone()
            if user:
                message = f"{SQL_MESSAGE['user'][stss.language]} '{username}' {SQL_MESSAGE['is_get_db'][stss.language]}."
                message_type = MESSAGE_TYPES[0]
            else:
                message = f"{SQL_MESSAGE['user'][stss.language]} '{username}' {SQL_WARNING['not_in_db'][stss.language]}."
                message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            user = None
            message = f"{SQL_MESSAGE['error_missing_user'][stss.language]} '{username}': \n{e}"
            message_type = MESSAGE_TYPES[2]
            
    if debug:
        print(message)
        
    return user, message, message_type




#---------------------------------------------------# 
#         Obtenir l'utilisateur par son nom         #
#---------------------------------------------------#
def get_user_by_name(name: str = '', debug: bool = False) -> Tuple[Tuple[int, str, str, str, str, str] | None, str, str]:    
    with database_connection(debug) as (_, c):
        try:
            c.execute("SELECT * FROM users WHERE name=?", (name, )) 
            user = c.fetchone()
            if user:
                message = f"{SQL_MESSAGE['user'][stss.language]} '{name}' {SQL_MESSAGE['is_get_db'][stss.language]}."
                message_type = MESSAGE_TYPES[0]
            else:
                message = f"{SQL_MESSAGE['user'][stss.language]} '{name}' {SQL_WARNING['not_in_db'][stss.language]}."
                message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            user = None
            message = f"{SQL_MESSAGE['error_missing_user'][stss.language]} '{name}': \n{e}"
            message_type = MESSAGE_TYPES[2]
            
    if debug:
        print(message)
        
    return user, message, message_type




#---------------------------------------------------# 
#          Obtenir l'utilisateur par son ID         #
#---------------------------------------------------#
def get_user_by_ID(id: int, debug: bool = False) -> Tuple[Tuple[int, str, str, str, str, str] | None, str, str]:
    with database_connection(debug) as (_, c):
        try:
            c.execute("SELECT * FROM users WHERE id=?", (id, )) 
            user = c.fetchone()
            if user:
                message = f"{SQL_MESSAGE['user'][stss.language]} {id} {SQL_MESSAGE['is_get_db'][stss.language]}."
                message_type = MESSAGE_TYPES[0]
            else:
                message = f"{SQL_MESSAGE['user'][stss.language]} {id} {SQL_WARNING['not_in_db'][stss.language]}."
                message_type = MESSAGE_TYPES[1]
            
        except sqlite3Error as e:
            user = None
            message = f"{SQL_MESSAGE['error_missing_user'][stss.language]} '{id}': \n{e}"
            message_type = MESSAGE_TYPES[2]
            
    if debug:
        print(message)
        
    return user, message, message_type




#---------------------------------------------------# 
#           Obtenir tous les utilisateurs           #
#---------------------------------------------------#
def get_all_users(debug: bool = False) -> Tuple[List[Tuple[int, str, str, str, str, str]] | None, str, str]:
    with database_connection(debug) as (_, c):
        try:
            c.execute("SELECT * FROM users")
            users = c.fetchall()
            if users is not None:
                if users:
                    message = SQL_MESSAGE['all_users_get'][stss.language]
                    message_type = MESSAGE_TYPES[0]
                else:
                    message = SQL_WARNING['users_table_empty'][stss.language]
                    message_type = MESSAGE_TYPES[1]

        except sqlite3Error as e:
            users =  None
            message = f"{SQL_ERRORS['error_all_users_get'][stss.language]}: \n{e}"
            message_type = MESSAGE_TYPES[2]
    
    if debug:
        print(message)
        
    return users, message, message_type
    




