import streamlit as st
from streamlit import session_state as stss
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
from crud_users import get_all_users, get_user_by_username, create_user
import secrets
from common_language import BUTTON_STR, AUTH_MESSAGE, AUTH_WARNING, AUTH_ERRORS, MESSAGE_TYPES # ('success', 'warning', 'error', 'info')
from common_game import go_to_function_play, PLAY_FUNCS



# --- Configuration des utilisateurs (crendentials structure) ---
#   credentials = {
#       "usernames": {
#           "alice": {
#               "name": "Alice Dupont",
#               # mot de passe hashé avec stauth.Hasher
#               "password": hashed_password[0]  # valeur = password1
#           },
#           "bob": {
#               "name": "Bob Martin",
#               "password": "$2b$12$eI7gVl3uYjR/9IYzrG8Q1uZBzLoXl1QEZ5cD2A6XYkf29a9Q8C.W7"  # valeur = password2
#           }
#       }
#   }



# NOUVELLE METHODO POUR CRYPTER LES MOTS DES PASSES AVEC 
#   1. Utiliser Hasher.hash() pour hacher un mot de passe individuel :
#      La méthode Hasher.hash(password) prend une chaîne de caractères et retourne son hachage bcrypt.
#   2. Utiliser Hasher.hash_passwords(credentials) pour hacher plusieurs mots de passe:
#      Cette méthode prend un dictionnaire credentials
#            credentials = {
#                'usernames': {
#                    'username1': {'password': 'password1', ...},
#                    'username2': {'password': 'password2', ...}
#                  }
#             }

        



#------------------------------------------------------------#
#     Charger les utilisateurs depuis la base de données     #
#------------------------------------------------------------#
def load_credentials(debug: bool = False) -> dict:
    users, message, message_type = get_all_users(debug=debug)
    credentials = {"usernames": {}}
    
    if users and message_type == MESSAGE_TYPES[0]:
        for user in users:
            user_id, username, name, user_password, role, date_joined = user
            credentials["usernames"][username] = {
                "name": name,
                "password": user_password  # Mot de passe déjà haché
            }
    else: 
        message = f"{AUTH_ERRORS['error_load_credentials'][stss.language]}: {message}"
        
    if debug:
        print(message)
        
    return credentials, message, message_type


#------------------------------------------------------------#
#            Configuration de l'authentification             #
#------------------------------------------------------------#
def config_authentification():
    cookie_name = "flashcard_login"
    cookie_key = secrets.token_hex(16)  # Clé sécurisée aléatoire
    cookie_expiry_days = 1
    return cookie_name, cookie_key, cookie_expiry_days




#------------------------------------------------------------#
#            Configuration de l'authentification             #
#------------------------------------------------------------#

def init_authentificator():
    # Charger les credentials depuis la base de données
    credentials, message, message_type = load_credentials(debug=True)  
    cookie_name, cookie_key, cookie_expiry_days = config_authentification()
    
    with st.container():
        _, auth_c1, _ = st.columns((1,2,1))
        with auth_c1:
            authenticator = stauth.Authenticate(
                credentials=credentials,
                cookie_name=cookie_name,
                cookie_key=cookie_key,
                cookie_expiry_days=cookie_expiry_days,
                
            )
    return authenticator, message, message_type




#------------------------------------------------------------#
#          Formulaire d'inscription (nouveau joueur)         #
#------------------------------------------------------------#    
def sign_in_form():
    _, form_c1, _ = st.columns((1,1.5,1))
    with form_c1:
        with st.form("Sign in", border=True):
            # Ligne 1 : Nom
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(
                    f"<div style='display: flex; height: 38px; align-items: center; font-size: 17px; font-weight: bold;'>{AUTH_MESSAGE['name'][stss.language]}</div>",
                    unsafe_allow_html=True
                )
            with col2:
                name = st.text_input(
                    'name_input',
                    max_chars=32,
                    label_visibility='collapsed',
                    placeholder=AUTH_MESSAGE['fill_name'][stss.language]
                )

            # Ligne 2 : Username
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(
                    f"<div style='display: flex; align-items: center; height: 38px; font-size: 17px; font-weight: bold;'>{AUTH_MESSAGE['username'][stss.language]}</div>",
                    unsafe_allow_html=True
                )
            with col2:
                username = st.text_input(
                    'username_input',
                    max_chars=16,
                    label_visibility='collapsed',
                    placeholder=AUTH_MESSAGE['fill_username'][stss.language]
                )

            # Ligne 3 : Password
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(
                    f"<div style='display: flex; align-items: center; height: 38px; font-size: 17px; font-weight: bold;'>{AUTH_MESSAGE['password'][stss.language]}</div>",
                    unsafe_allow_html=True
                )
            with col2:
                password = st.text_input(
                    'password_input',
                    max_chars=16,
                    type='password',
                    label_visibility='collapsed',
                    placeholder=AUTH_MESSAGE['fill_passwords'][stss.language]
                )

            col1.markdown('###### ')
            col2.markdown('###### ')
            
            _, form_c1b, _ = st.columns((1,1,1))

            if form_c1b.form_submit_button(BUTTON_STR['confirm'][stss.language], use_container_width = True):
                 
                user, _, _ = get_user_by_username()
                if user:
                    st.warning(AUTH_WARNING['already_existing_username'][stss.language])
                else:
                    create_user(username = username, name = name, user_password = password, debug = stss.debug)
                    go_to_function_play(PLAY_FUNCS[0])
                    st.rerun()
    


