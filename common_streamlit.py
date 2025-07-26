#=====================================================#
#         Eléments communs aux pages streamlit        #
#=====================================================#

import streamlit as st 
from typing import List
from common_language import LANGUAGE, MESSAGE_TYPES # ('success', 'warning', 'error', 'info')
from crud_themes import get_theme, get_all_themes, get_theme_id
from crud_cards import get_card, get_cards_by_theme, PROB_MIN, PROB_MAX
import pandas as pd
from common_authentificator import AUTH_MESSAGE
from common_language import BUTTON_STR, PAGES_STR, ERRORS_STR

from streamlit import session_state as stss
language = stss.language

#---------------------------------------------------# 
#             Management lists and dicts            #
#---------------------------------------------------# 
  
# Session state bolean variable for corresponding page sections 
PLAY_FUNCS = ('intro_play', 'create_player','chose_player', 'play')

PLAY_FUNCS_NAMES = {
    LANGUAGE[0]: ('welcome', 'Créer un jouer', 'Choisir un joueur', 'Jouer'),
    LANGUAGE[1]: ('welcome', 'Create player', 'Chose a player', 'Play'),
}


# Session state bolean variable for corresponding page sections 
CARDS_FUNCS = ('intro_cards', 'create_card', 'delete_card', 'update_card', 'get_card', 'get_all_cards', 'get_cards_by_theme')

# Names of the page sections 
CARDS_FUNCS_NAMES = {
    LANGUAGE[0]: ('intro cards', 'Voir carte par ID', 'Voir toutes les cartes', 'Voir les cartes par thèmes', 'Créer une carte', 'Supprimer une carte', 'Mettre à jour une carte'),
    LANGUAGE[1]: ('intro cards', 'Get card by ID', 'Get all the cards', 'Get cards by theme', 'Create card', 'Delete card', 'Update card'),
}


# showing name for card columns
CARDS_COLUMNS = {
    LANGUAGE[0]: ('ID carte', 'Question', 'Réponse', 'Probabilité', 'Thème'),
    LANGUAGE[1]: ('Card ID', 'Question', 'Response', 'Probability', 'Theme'),
}

# Session state bolean variable for corresponding page sections 
THEMES_FUNCS = ('intro_themes', 'get_theme', 'get_all_themes', 'get_cards_by_theme', 'create_theme', 'delete_theme', 'update_theme')

# Names of the page sections 
THEMES_FUNCS_NAMES = {
    LANGUAGE[0]: ('intro themes', 'Voir un thème', 'Voir tous les thèmes', 'Voir les cartes par thèmes', 'Créer un thème', 'Supprimer un thème', 'Mettre à jour un thème'),
    LANGUAGE[1]: ('intro themes', 'Get theme by ID', 'Get all the themes', 'Get cards by theme', 'Create theme', 'Delete theme', 'Update theme')
}


# showing name for card columns
THEMES_COLUMNS = {
    LANGUAGE[0]: ('ID thème', 'Thème'),
    LANGUAGE[1]: ('Theme ID', 'Theme'),
}







#---------------------------------------------------# 
#                     Functions                     #
#---------------------------------------------------# 
# fonction pour initialiser les variables de sessions si elle existe pas, et l'option de forcer un reset, pour changement page par exemple
def init_session_variable(sess_var_list: List[str] = None, sess_var_list_with_msg: List[str] = None, reset: bool = False):
    if sess_var_list:
        for sess_var in sess_var_list:
            if sess_var not in stss or reset:
                stss[sess_var] = None
    if sess_var_list_with_msg:
        for sess_var in sess_var_list_with_msg:
            if sess_var not in stss or reset:
                stss[sess_var] = None
            if f'{sess_var}_message' not in stss or reset:
                stss[f'{sess_var}_message'] = None
            if f'{sess_var}_message_type' not in stss or reset:
                stss[f'{sess_var}_message_type'] = None
                
                
# fonction pour initialiser les variables de sessions si elle existe pas, et l'option de forcer un reset, pour changement page par exemple
def init_session_variable_dict(sess_var_list: List[dict] = None, sess_var_list_with_msg: List[dict] = None, reset: bool = False):
    if sess_var_list:
        for sess_var, value in sess_var_list.items():
            if sess_var not in stss or reset:
                stss[sess_var] = value
    if sess_var_list_with_msg:
        for sess_var, value in sess_var_list_with_msg.items():
            if sess_var not in stss or reset:
                stss[sess_var] = value
            if f'{sess_var}_message' not in stss or reset:
                stss[f'{sess_var}_message'] = ''
            if f'{sess_var}_message_type' not in stss or reset:
                stss[f'{sess_var}_message_type'] = ''
   
   
   
   
def init_play_session(reset: bool = False):
    play_sess_var_list = {
        'game_ongoing': False,
        'user_id': None,
        'logout': True,
        'all_themes_get': [],
        'options_themes': [],
        'selection_themes': [],
        'play_themes': [],
        'themes_selection_fixed': False,
        'next_round':  False,
        'card_is_chosen': False ,
        'chosen_theme_key': [],
        'chosen_card': [None, None, None, None, None],
        'card_available': False ,
        'cards_list': [],
        'submitted': False ,
        'user_response': '',
        'correct_response': '',
        'session_scores': 0.0,
        'correct_answers': 0,
        'wrong_answers': 0,
        'number_theme_played': [],
            }
   
    play_sess_var_list_with_msg = {
        'current_card': None, 
        'all_themes': [], 
        'theme': None, 
        'theme_id': None, 
        'exist_card_ids': [],
        'exist_thm_ids': [],
    }
   
    init_session_variable_dict(
        sess_var_list = play_sess_var_list,
        sess_var_list_with_msg = play_sess_var_list_with_msg,
        reset = reset 
    )
    
    return play_sess_var_list, play_sess_var_list_with_msg             
                
                
                
                
def init_card_session(reset: bool = False):
    card_sess_var_list = [
        'card_id', 
        'card_modification', 
        'new_theme', 
        'options_themes',
        'updated_card', 
        'new_card_id', 
        'new_card_created', 
        'selection_theme',
        'card_delete_to_be_confirmed', 
        'card_confirmation', 
        'card_modification_to_be_confirmed',
        'card_available',
    ]
   
    card_sess_var_list_with_msg = [
        'current_card', 
        'all_themes', 
        'theme', 
        'theme_id', 
        'new_card', 
        'created_theme', 
        'deleted_card',
        'modified_card',
        'exist_card_ids',
        'exist_thm_ids',
    ]
   
    init_session_variable(
        sess_var_list = card_sess_var_list,
        sess_var_list_with_msg = card_sess_var_list_with_msg,
        reset = reset 
    )
    
    return card_sess_var_list, card_sess_var_list_with_msg




def init_theme_session(reset: bool = False, exclusion: List = []):
    theme_sess_var_list = [
        'new_theme',
        'new_theme_created',
        'theme_id',
        'theme_confirmation',
        'theme_del_confirm',
        'free_theme',
        'theme_available',
        'updated_theme',
        'theme_modification',
        'theme_modification_to_be_confirmed',
    ]
   
    theme_sess_var_list_with_msg = [
        'created_theme',
        'list_card_by_theme', 
        'current_theme',
        'modified_theme',
    
    ]
    
    if exclusion:
        theme_sess_var_list_updated = [var for var in theme_sess_var_list if var not in exclusion]
        theme_sess_var_list_with_msg_updated = [var for var in theme_sess_var_list_with_msg if var not in exclusion]
    else:
        theme_sess_var_list_updated = theme_sess_var_list 
        theme_sess_var_list_with_msg_updated = theme_sess_var_list_with_msg 
        

    init_session_variable(
        sess_var_list = theme_sess_var_list_updated,
        sess_var_list_with_msg = theme_sess_var_list_with_msg_updated,
        reset = reset 
    )
    
    return theme_sess_var_list, theme_sess_var_list_with_msg



"""
def init_theme_session(reset: bool = False):
    theme_sess_var_list = [
        'new_theme',
        'new_theme_created',
        'theme_id',
        'theme_confirmation',
        'theme_del_confirm',
        'free_theme',
        'theme_available',
        'updated_theme',
        'theme_modification',
        'theme_modification_to_be_confirmed',
    ]
   
    theme_sess_var_list_with_msg = [
        'created_theme',
        'list_card_by_theme', 
        'current_theme',
        'modified_theme',
    
    ]
    
    init_session_variable(
        sess_var_list = theme_sess_var_list,
        sess_var_list_with_msg = theme_sess_var_list_with_msg,
        reset = reset 
    )
    
    return theme_sess_var_list, theme_sess_var_list_with_msg
"""

# Fonction qui permet de conserver l'état de la variable de session du widget select language qu'on on change de page
def sidebar_common():
    with st.sidebar:
        if 'language' not in stss:
            stss.language = LANGUAGE[0]

        selected_language = st.radio(
            label='Language',
            options=LANGUAGE,
            #index=LANGUAGE.index(stss.language),  # montrer la langue courante
            label_visibility='collapsed',
            key='language',  
            horizontal=True,
            on_change=lambda: st.rerun(),
        )

        # Mise à jour explicite de la variable language
        #stss.language = selected_language

        # Toggle Debug
        stss['debug'] = st.toggle(label='Debug')
        
        if 'authentication_status' in stss and stss.authentication_status:
            st.sidebar.success(f"{AUTH_MESSAGE['welcome'][stss.language]} *{stss.name}* :grinning:")
            if stss.authenticator.logout(AUTH_MESSAGE['logout'][stss.language], "sidebar"):
                init_play_session(reset = True)
                for func in PLAY_FUNCS:
                    stss[func] = True if func == 'intro_play' else False
                #st.rerun()
                st.session_state["_force_rerun"] = True  # Flag pour forcer un rerun complet
            
        stop_pl_hold = st.empty()
        play_pl_hold = st.empty()
        
        if stss['debug']:
            for func in PLAY_FUNCS:
                st.write(f'{func}: {stss[func]}')
            
    return play_pl_hold, stop_pl_hold




def show_session_state_variables(var_list: List[str] = []):
    with st.sidebar:
        st.subheader(PAGES_STR['used_session_variables'][stss.language])
        if var_list:
    
            for var in var_list:
                if not isinstance(var, str):
                    st.error(f"{var} {ERRORS_STR['not_a_str'][stss.language]}")
                elif var not in stss:
                    st.error(f"{var} {ERRORS_STR['not_in_session'][stss.language]}")
                else:
                    st.write(f'{var}: {stss[var]}')
    
        # si il n'a pas de variable dans la liste on affiche toute la session
        else:
            if stss:
                st.write(PAGES_STR['session_variables'][stss.language])
                for key, value in stss.items():
                    st.write(f'{key}: {value}')
            else:
                st.info(PAGES_STR['session_state_empty'][stss.language])
                
            
def message_type_format(message, message_type):
        if message_type == MESSAGE_TYPES[0]:
            st.success(message)
        elif message_type == MESSAGE_TYPES[1]:
            st.warning(message)
        elif message_type == MESSAGE_TYPES[2]:
            st.error(message)
        elif message_type == MESSAGE_TYPES[3]:
            st.info(message)
        else:
            st.write(message)


             
             
def show_card(id: int = None, modify = False, create = False, debug: bool = False):
    
    height = 58 if not create else 71
    height_with_check_box = 90 
    
    if not create:
        stss.current_card, stss.current_card_message, stss.current_card_message_type = get_card(id = id)
    elif create:
        modify = True
        stss.current_card = [None] * (len(CARDS_COLUMNS[stss.language]))
        stss.current_card_message, stss.current_card_message_type = PAGES_STR['to_be_created'][stss.language], MESSAGE_TYPES[3]
        stss.selection_theme = True
        stss.card_modification = True
    else:
        stss.card_modification = False
        stss.selection_theme = False
        
    if modify and not create:
        stss.selection_theme = True
        stss.card_modification = True
            
    enumeration_card = stss.current_card if stss.current_card is not None else [None] * len(CARDS_COLUMNS[stss.language])
            
    
            
    if stss.selection_theme:
        stss.all_themes, stss.all_themes_message, stss.all_themes_message_type = get_all_themes(debug = debug)
        if stss.all_themes is not None:
            stss.options_themes = [theme[1] for theme in stss.all_themes]
        else:
            stss.card_modification = False
            
    updated_card = [None] * len(enumeration_card)
                
    with st.container(border=True):

        for i, info in enumerate(enumeration_card):
            c1, c2 = st.columns((1,5))
            # 1ERE COLONNE
            # =============================================
            if not(i == 0 and create):
                if i != 4 or not create:
                    with c1.container(border=True, height = height):
                        st.write(CARDS_COLUMNS[stss.language][i])  
                else:
                    with c1.container(border=True, height = height_with_check_box):
                        st.write(CARDS_COLUMNS[stss.language][i])  
                        stss.new_theme = st.checkbox(BUTTON_STR['new_theme'][stss.language])
                        
                if modify and not create:
                    with c1.container():
                        if i != 0 and i < 4:
                            
                            #st.write(PAGES_STR['modification'][stss.language], )
                            st.markdown(
                                f"<div style='text-align:right'>{PAGES_STR['modification'][stss.language]}</div>",
                                unsafe_allow_html=True
                            )
                            
                        if i==4:
                            stss.new_theme = st.checkbox(BUTTON_STR['new_theme'][stss.language])
            
            # 2EME COLONNE
            # =============================================
            
            # ID, Question, Réponse
            # ---------------------
            if i < 3 and not(i == 0 and create):   # Card ID                      
                with c2.container(border=True, height = height): 
                        
                    #if info != card[-1]:
                    if info is not None and not create:
                        st.write(info)
                        updated_card[i] = stss.current_card[i]
                    elif not create:
                        message_type_format(stss.current_card_message, stss.current_card_message_type)
                        stss.card_modification = False
                    elif i != 0: # cas on l'on crée une nouvelle carte
                        updated_card[i] = st.text_input(
                                label = '', 
                                key =  f"updated_{CARDS_COLUMNS[LANGUAGE[0]][i]}",
                                label_visibility = "collapsed",
                                placeholder = BUTTON_STR['fill_in_here'][stss.language],
                                )
                 
                if modify and i > 0 and not create:
                    with c2: # cas où l'on update une carte existante
                        updated_card[i] = st.text_input(
                                label = '', 
                                key =  f"updated_{CARDS_COLUMNS[LANGUAGE[0]][i]}",
                                label_visibility = "collapsed",
                                placeholder = PAGES_STR['modif_to_be_applied'][stss.language],
                                )
              
            # Probabilité
            # ------------
            if i == 3:
                with c2.container(border=True, height = height): 
                    if info is not None and not create:
                        st.write(info)
                    elif not create:
                        message_type_format(stss.current_card_message, stss.current_card_message_type)
                        stss.card_modification = False
                    else:  # cas on l'on crée une nouvelle carte
                        updated_card[i]  = st.slider(
                            label = '', 
                            min_value = PROB_MIN,
                            max_value = PROB_MAX, 
                            value = 0.5,
                            step = 0.05,
                            key = f"updated_{CARDS_COLUMNS[LANGUAGE[0]][i]}", 
                            label_visibility="collapsed"
                            )
                if modify and not create:  # cas où l'on update une carte existante
                    with c2:
                        updated_card[i]  = st.slider(
                            label = '', 
                            min_value = PROB_MIN,
                            max_value = PROB_MAX, 
                            value = info,
                            step = 0.05,
                            key = f"updated_{CARDS_COLUMNS[LANGUAGE[0]][i]}", 
                            label_visibility="collapsed"
                            )                    
                    
            # Thème
            # ---------------------
            if i == 4:
                if not create:
                    stss.theme, stss.theme_message, stss.theme_message_type = get_theme(id = info, debug = debug)
                
                with c2.container(border=True, height = height if not create else height_with_check_box): 
                    # cas update et show (partie commune)
                    if stss.theme is not None and not create:
                        st.write(stss.theme[1])
                        
                    # cas update et show avec un probleme pour récupérer le thème
                    elif not create:
                        message_type_format(stss.theme_message, stss.theme_message_type)
                        stss.card_modification = False
                        
                    # cas create
                    elif create:                  
                        if stss.all_themes is None and not stss.new_theme:
                            message_type_format(stss.all_themes_message, stss.all_themes_message_type)
                            stss.card_modification = False
                        else: 
                            if stss.new_theme:
                                updated_card[i] = st.text_input(
                                    label = '', 
                                    key = f"updated_{CARDS_COLUMNS[LANGUAGE[0]][i]}",
                                    label_visibility = "collapsed",
                                    placeholder = BUTTON_STR['fill_in_here'][stss.language],
                                    max_chars = 16,
                                )
                                if updated_card[i] in [theme[1] for theme in stss.all_themes]:
                                    c2.warning(PAGES_STR['existing_theme_selection'][stss.language])
                            
                            else: 
                                updated_card[i]  = st.selectbox(
                                    label = '',
                                    label_visibility= "collapsed",
                                    options = stss.options_themes,
                                    key = f"updated_{CARDS_COLUMNS[LANGUAGE[0]][i]}",
                                    index = None,  # Aucune option sélectionnée par défaut
                                    placeholder=BUTTON_STR['select_a_theme'][stss.language],  # Texte affiché par défaut
                                )
                           
                # cas update (même partie que create mais sans bordure en dessous de la zone commune avec bordure)           
                if modify and not create: 
                    with c2:
                        if stss.all_themes is None and not stss.new_theme:
                            message_type_format(stss.all_themes_message, stss.all_themes_message_type)
                            stss.card_modification = False
                        else: 
                            if stss.new_theme:
                                updated_card[i]  = st.text_input(
                                    label = '', 
                                    key = f"updated_{CARDS_COLUMNS[LANGUAGE[0]][i]}_not_create",
                                    label_visibility = "collapsed",
                                    placeholder = BUTTON_STR['fill_in_here'][stss.language],
                                    max_chars = 16,
                                )
                                if updated_card[i] in [theme[1] for theme in stss.all_themes]:
                                    st.warning(PAGES_STR['existing_theme_selection'][stss.language])
                                
                            else: 
                                updated_card[i]  = st.selectbox(
                                    label = '',
                                    label_visibility= "collapsed",
                                    options = stss.options_themes,
                                    key = f"updated_{CARDS_COLUMNS[LANGUAGE[0]][i]}_not_create",
                                    index = None,  # Aucune option sélectionnée par défaut
                                    placeholder= BUTTON_STR['select_a_theme'][stss.language],  # Texte affiché par défaut
                                )
        
    # UPDATE DE 'stss.current_card'
    # =============================================
    stss.updated_card = updated_card
    
    if modify and stss.all_themes == [] and not stss.new_theme:
        st.error(ERRORS_STR['mandatory_new_theme'][stss.language])
        stss.card_modification = False
        
    # Pour creer une carte        
    elif create and stss.current_card is not None:
        stss.current_card = list(stss.current_card)   
        
        for i, (card_info, update_card_info) in enumerate(zip(stss.current_card, stss.updated_card)):
            if i != 0 and update_card_info is not None:
                stss.current_card[i] = update_card_info
                
        stss.current_card = tuple(stss.current_card) 
        
        if all(info is not None and info != '' for info in stss.current_card[1:]):
            stss.card_modification = True
        else:
            stss.card_modification = False
          
            
    # Pour mettre à jour une carte 
    elif modify and stss.current_card is not None:
        stss.current_card = list(stss.current_card)
        
        for i, (card_info, update_card_info) in enumerate(zip(stss.current_card, stss.updated_card)):
            if i == 0:
                injection_guard = update_card_info != card_info
                if injection_guard:
                    st.error(ERRORS_STR['mismatch_card_ID'][stss.language])
                    stss.card_modification = False
            
            elif (  i != 4
                    and update_card_info is not None
                    and update_card_info != '' # Si champ laisser vide on garder l'état de la carte
                    and update_card_info != card_info
                    and not injection_guard
            ):
                stss.current_card[i] = update_card_info
            elif (
                i == 4 
                and update_card_info in ('', None)
 
            ):
                current_theme, _, _ = get_theme(id = stss.current_card[i], debug = debug)
                stss.current_card[i] = current_theme[1]
                
        stss.current_card = tuple(stss.current_card) 
                
        if all(info is not None and info != '' for info in stss.current_card):
            stss.card_modification = True
        else:
            stss.card_modification = False
                 
    # Pour lire une carte
    else:
        stss.card_modification = False
                
                   
             

def get_cards_by_theme_selection(debug: bool = False) -> None:
    init_card_session()
    
    if 'debug' in stss and stss.debug:
        show_session_state_variables(['selection_theme', 'themes', 'options_themes'])
    
    stss.themes, stss.options_message, stss.options_message_type = get_all_themes(debug = stss.debug)
    if stss.selection_theme is None:
        stss.selection_theme = []

    if stss.options_message_type != MESSAGE_TYPES[0]:
        message_type_format(stss.options_message, stss.options_message_type)
    if stss.themes is not None:
        stss.options_themes = [theme[1] for theme in stss.themes]
    else:
        stss.options_themes = None
        
    if stss.options_themes is not None:
        c1_6, c2_6, _ = st.columns((1, 1, 4))
        with c1_6:
            if st.button(BUTTON_STR['all_theme'][stss.language], disabled = stss.selection_theme == stss.options_themes):
                stss.selection_theme = stss.options_themes
                st.rerun()
    
        with c2_6:    
            if st.button(BUTTON_STR['no_theme'][stss.language], disabled = not stss.selection_theme):
                stss.selection_theme = []
        
        st.multiselect(
            label = BUTTON_STR['select_themes'][stss.language], 
            options = stss.options_themes, 
            default = None, # default = stss.selection_theme
            key = "selection_theme", # (on ne met rien ce qui permet que le multiselect soit dynamique)
            label_visibility = "hidden",
            placeholder = BUTTON_STR['select_themes'][stss.language],
            )
    
        for theme in stss.selection_theme:
            st.divider()
            
            theme_id, theme_id_message, theme_id_message_type = get_theme_id(theme, stss.debug)
            if theme_id_message_type != MESSAGE_TYPES[0]:
                message_type_format(theme_id_message, theme_id_message_type)
            all_cards, all_cards_message, all_cards_message_type = get_cards_by_theme(theme_id, stss.debug)
            
            if all_cards_message_type != MESSAGE_TYPES[0]:
                message_type_format(all_cards_message, all_cards_message_type)
                
            if theme_id is not None:
                st.markdown(f'#### Theme: {theme}, theme ID = {theme_id}')            
                theme_cards_list = []
                for card in all_cards:
                    theme_cards_list.append(card)
                theme_cards_list = pd.DataFrame(theme_cards_list, columns=CARDS_COLUMNS[stss.language])
                theme_cards_list.drop(CARDS_COLUMNS[stss.language][-1], axis=1, inplace=True)
                st.dataframe(theme_cards_list, hide_index=True)
    
