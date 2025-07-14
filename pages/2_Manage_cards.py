#===================================================#
#         Gestion des cartes dans streamlit         #
#===================================================#


import streamlit as st 
from streamlit import session_state as stss
from crud_cards import create_card, delete_card, update_card, get_card, get_all_cards, get_number_of_cards, get_existing_card_ids, get_cards_by_theme
from crud_cards import PROB_MIN, PROB_MAX
from crud_themes import create_theme, get_theme, get_all_themes, get_theme_id, get_existing_theme_ids
import pandas as pd 
from common_streamlit import CARDS_FUNCS, CARDS_FUNCS_NAMES, CARDS_COLUMNS, BUTTON_STR, PAGES_STR, ERRORS_STR
from common_streamlit import init_card_session, show_session_state_variables, sidebar_common, message_type_format, show_card ,get_cards_by_theme_selection
from common_language import LANGUAGE, MESSAGE_TYPES # ('success', 'warning', 'error', 'info')
from typing import List


st.set_page_config(page_title='Cards management', layout = 'wide')
sidebar_common()

#---------------------------------------------------# 
#             Fonctions and constants               #
#---------------------------------------------------# 

CARD_INPUT_HEIGHT = 71

def go_to_function(function):
    for func in CARDS_FUNCS:
        stss[func] = True if func == function else False
    st.rerun()
    
    
    
def go_back_button():
    if st.button(BUTTON_STR['goback'][stss.language]):
        init_card_session(reset = True)
        go_to_function(CARDS_FUNCS[0])
        
           
        
            
def get_a_card_streamlit(modify: bool = False, debug: bool = False):

    stss.card_available = False
    c1_f1, _ = st.columns((1,5)) # pour fine tuner la largeur de l'input box
    stss.card_id = c1_f1.number_input(
        f'{PAGES_STR['chose_number_from_1_to'][stss.language]} {max(stss.exist_card_ids)}', 
        min_value = 1, 
        max_value = max(stss.exist_card_ids), 
        value = 1,
        )
    
    if stss.exist_card_ids is None:
        st.error(ERRORS_STR['error_bd_cards'][stss.language])
        
    elif not stss.exist_card_ids:
        st.warning(PAGES_STR['cards_table_empty'][stss.language])
        
    elif stss.card_id in stss.exist_card_ids:
        show_card(id = stss.card_id, modify = modify, debug = debug)
        stss.card_available = True
    
    else:
        st.warning(f"{PAGES_STR['card'][stss.language]} {stss.card_id} {PAGES_STR['is_no_more_db'][stss.language]}")
                             
                  
                  
                  
def show_card_list(id_theme):
    list_card = get_cards_by_theme(id_theme)
    
    

  
  
#---------------------------------------------------# 
#          Session variables initialisation         #
#---------------------------------------------------#   
if CARDS_FUNCS[0] not in stss:
    stss[CARDS_FUNCS[0]] = True
for func in CARDS_FUNCS[1:]:
    if func not in stss:
        stss[func] = False
        
                
list_of_sess_var = [stss[CARDS_FUNCS[i]] for i in range(len(CARDS_FUNCS))]
        
        
        
        
#---------------------------------------------------# 
#                 Common page header                #
#---------------------------------------------------# 
if 'language' not in stss:
    stss.language = LANGUAGE[0]
head_1, head_2 = st.columns((5,1))
head_1.markdown(f'# {PAGES_STR['manage_cards'][stss.language]}')
with head_2:
    if any(list_of_sess_var[1:]):
        go_back_button()
    else:

        if st.button(BUTTON_STR['play'][stss.language]): 
            init_card_session(reset=True)
            
            home_url = "/"  # adapte selon ton app
            st.markdown(
                f"""
                <meta http-equiv="refresh" content="0; url={home_url}">
                """,
                unsafe_allow_html=True
            )
     


# Ajouter un espace vide dans head_1 pour équilibrer la hauteur avec head_2
with head_1:
    st.empty()  # un conteneur vide, mais qui garantit un alignement correct
st.divider()
st.write('')

stss.exist_card_ids, stss.exist_card_ids_message, stss.exist_card_ids_message_type  = get_existing_card_ids(stss.debug)
stss.exist_thm_ids, stss.exist_thm_ids_message, stss.exist_thm_ids_message_type  = get_existing_theme_ids(stss.debug)




#---------------------------------------------------# 
#          Starting section (page d'intro)          #
#---------------------------------------------------# 
if stss[CARDS_FUNCS[0]]:
    
    if 'debug' in stss and stss.debug:
        st.sidebar.subheader(PAGES_STR['session_variables'][stss.language])
        st.sidebar.write(stss)
    
    c1, _ , c2 = st.columns((4,1,4))

    with c1.container(border=True):
        st.subheader(PAGES_STR['visualization'][stss.language])
        for func, name in zip(CARDS_FUNCS[1:4], CARDS_FUNCS_NAMES[stss.language][1:4]):
            if st.button(name, use_container_width=True):
              go_to_function(func)  
            

    with c2.container(border=True):
        st.subheader(PAGES_STR['modification'][stss.language])
        for func, name in zip(CARDS_FUNCS[4:], CARDS_FUNCS_NAMES[stss.language][4:]):
            if st.button(name, use_container_width=True):
              go_to_function(func)
              
    st.divider()
    st.write('')
    
    with st.container(border=True):
        if stss.exist_card_ids or stss.exist_card_ids == 0:
            st.write(f'{PAGES_STR['number_of_cards'][stss.language]}: {len(stss.exist_card_ids)}')
        else:
            message_type_format(stss.exist_card_ids_message, stss.exist_card_ids_message_type)
            
        if stss.exist_thm_ids or stss.exist_thm_ids == 0:    
            st.write(f'{PAGES_STR['number_of_themes'][stss.language]}: {len(stss.exist_thm_ids)}')
        else: 
            message_type_format(stss.exist_card_ids_message, stss.exist_card_ids_message_type)
     
     


#---------------------------------------------------# 
#              Get card page section                #
#---------------------------------------------------# 
elif stss[CARDS_FUNCS[1]]:
    st.subheader(CARDS_FUNCS_NAMES[stss.language][1])
        
    init_card_session()
    
    if 'debug' in stss and stss.debug:
        show_session_state_variables(['card_id'])
    
    get_a_card_streamlit(debug = stss.debug)




#---------------------------------------------------# 
#             Get all cards page section            #
#---------------------------------------------------# 
elif stss[CARDS_FUNCS[2]]:
    st.subheader(CARDS_FUNCS_NAMES[stss.language][2])
    
    all_cards_list = []
    all_themes, all_themes_message, all_themes_message_type = get_all_themes(debug = stss.debug)
    all_cards, all_cards_message, all_card_message_type = get_all_cards(debug = stss.debug)
    if all_themes is None:
        message_type_format(all_themes_message, all_themes_message_type)
    elif all_cards is None:
        message_type_format(all_cards_message, all_card_message_type)
    else:
        # On crée un dictionnaire des thèmes pour mapper le nom avec le numero de theme dans les cartes
        # C'est plus rapide qu'appeler get_theme pour chaque carte surtout si la liste de carte est longue
        themes = {theme[0]: theme[1] for theme in all_themes}
        def get_theme_name_fast(id_theme):
            return themes.get(id_theme)
        
        for card in all_cards:
            all_cards_list.append(card)
        
        all_cards_list = pd.DataFrame(all_cards_list, columns=CARDS_COLUMNS[stss.language])
        all_cards_list[CARDS_COLUMNS[stss.language][-1]] = all_cards_list[CARDS_COLUMNS[stss.language][-1]].map(get_theme_name_fast)
    
        st.dataframe(all_cards_list, hide_index=True)
    
    
    

#---------------------------------------------------# 
#          Get cards by theme page section          #
#---------------------------------------------------#  
elif stss[CARDS_FUNCS[3]]:
    st.subheader(CARDS_FUNCS_NAMES[stss.language][3])

    card_sess_var_list, card_sess_var_list_with_msg = init_card_session()
    get_cards_by_theme_selection(debug = stss.debug)

   


#---------------------------------------------------#       
#             Create card page section              #
#---------------------------------------------------#
elif stss[CARDS_FUNCS[4]]:
    st.subheader(CARDS_FUNCS_NAMES[stss.language][4])
 
    card_sess_var_list, card_sess_var_list_with_msg = init_card_session()
    
    
    if 'debug' in stss and stss.debug:
        # Bouton de rafraîchissement manuel
        if st.sidebar.button(f"🔄 {BUTTON_STR['refresh_variable'][stss.language]}"):
            st.rerun()

        show_session_state_variables(
            [var for var in card_sess_var_list + card_sess_var_list_with_msg if var not in [
                                                                                        'card_delete_to_be_confirmed', 
                                                                                        'card_confirmation', 
                                                                                        'deleted_card',
                                                                                        'options_themes',
                                                                                        'modified_card'
                                                                                        ]
            ]
        )
        
    if not stss.new_card_created:  
        show_card(create = True, debug = stss.debug)
                            
        if st.button(BUTTON_STR['create_confirm'][stss.language], disabled = not stss.card_modification):
            check_card = []
            for i, info in enumerate(stss.current_card):
                if i != 0 and (info == '' or info is None):
                    check_card.append(i)
            if check_card:   
                st.warning(f"{PAGES_STR['card'][stss.language]} {PAGES_STR['not_created_f'][stss.language]}: {' '.join(CARDS_COLUMNS[stss.language][i] for i in check_card)}")
            else:
                if stss.new_theme:
                    stss.created_theme, stss.created_theme_message, stss.created_theme_message_type = create_theme(theme_name = stss.current_card[4], debug = stss.debug)
                    
                    if stss.created_theme_message_type != MESSAGE_TYPES[0]:
                        message_type_format(stss.created_theme_message, stss.created_theme_message_type)
                    
                stss.theme_id, stss.theme_id_message, stss.theme_id_message_type = get_theme_id(theme = stss.current_card[4], debug = stss.debug)
                if stss.theme_id_message_type != MESSAGE_TYPES[0]:
                    message_type_format(stss.theme_id_message, stss.theme_id_message_type)
               
                if stss.theme_id is not None:
     
                    card, card_message, card_message_type  = create_card(
                                                                            question = stss.current_card[1], 
                                                                            reponse = stss.current_card[2], 
                                                                            probabilite = stss.current_card[3], 
                                                                            id_theme = stss.theme_id,
                                                                            debug = stss.debug
                                                                        )
                    
                stss.new_card_id, *stss.new_card_info = card if card is not None else [None]*len(CARDS_COLUMNS[stss.language])
                stss.new_card_message = card_message
                stss.new_card_message_type = card_message_type
                stss.new_card_created = True
                st.rerun()
            
    else:
        if stss.created_theme:
            message_type_format(stss.created_theme_message, stss.created_theme_message_type)
        message_type_format(stss.new_card_message, stss.new_card_message_type)
        st.markdown(f'#### {PAGES_STR['card_detail'][stss.language]}:')
        show_card(id = stss.new_card_id, modify = False, debug = stss.debug)
        st.divider()
        if st.button(BUTTON_STR['create_card'][stss.language]):
            init_card_session(reset = True)
            st.rerun()
    


#---------------------------------------------------# 
#             Delete card page section              #
#---------------------------------------------------# 
elif stss[CARDS_FUNCS[5]]:
    st.subheader(CARDS_FUNCS_NAMES[stss.language][5])

    init_card_session()
    
    if 'debug' in stss and stss.debug:
        show_session_state_variables(['card_id', 'card_delete_to_be_confirmed', 'card_confirmation', 'deleted_card'])
    
    if stss.card_confirmation is None:   
        
        get_a_card_streamlit()
        
        if stss.card_available:
            if not stss.card_delete_to_be_confirmed:
                if st.button(BUTTON_STR['delete'][stss.language]):
                    stss.card_delete_to_be_confirmed = True
                    st.rerun()
            else: 
                stss.card_confirmation = st.segmented_control(
                        f"{PAGES_STR['deletion_confirm'][stss.language]} {PAGES_STR['card'][stss.language].lower()} {stss.card_id}?", 
                        [ 
                            BUTTON_STR['yes'][stss.language], 
                            BUTTON_STR['no'][stss.language]
                        ]
                        )
                #st.rerun()

        else:
            st.warning(f"{PAGES_STR['card'][stss.language]} {stss.card_id} {PAGES_STR['is_no_more_db'][stss.language]}")
    
    # 'OUI'            
    elif stss.card_confirmation == BUTTON_STR['yes'][stss.language]:  
        stss.deleted_card, stss.deleted_card_message, stss.deleted_card_message_type = delete_card(id = stss.card_id)
        message_type_format(stss.deleted_card_message, stss.deleted_card_message_type)
        if st.button(BUTTON_STR['delete_card'][stss.language]):
            init_card_session(reset=True)
            st.rerun()
        
    # 'NON'        
    elif stss.card_confirmation == BUTTON_STR['no'][stss.language]:  
        st.info(f'{PAGES_STR['card'][stss.language]} {stss.card_id} {PAGES_STR['not_removed_db_f'][stss.language]}')

        if st.button(BUTTON_STR['delete_card'][stss.language]):
            init_card_session(reset=True)
            st.rerun()
            
            
            
            
#---------------------------------------------------# 
#             Update card page section              #
#---------------------------------------------------# 
elif stss[CARDS_FUNCS[6]]:
    st.subheader(CARDS_FUNCS_NAMES[stss.language][6])
    
    
    card_sess_var_list, card_sess_var_list_with_msg = init_card_session()

    
    if 'debug' in stss and stss.debug:
            show_session_state_variables(
            [var for var in card_sess_var_list + card_sess_var_list_with_msg if var not in [
                                                                                        'new_card_message',
                                                                                        'new_card_message_type',
                                                                                        'new_theme_id',
                                                                                        'new_card_id',
                                                                                        'new_card_created',
                                                                                        'new_card_info',
                                                                                        'card_delete_to_be_confirmed', 
                                                                                        'deleted_card',
                                                                                        ]
            ]
        )
        
    if stss.card_confirmation is None and stss.modified_card is None:   
        
        get_a_card_streamlit(modify = True, debug = stss.debug)
        
        if stss.card_available:
                    
            if not stss.card_modification_to_be_confirmed:    
                if st.button(
                        label = BUTTON_STR['update_confirm'][stss.language],
                        disabled = not stss.card_modification
                    ):
                        stss.card_modification_to_be_confirmed = True
                        st.rerun()
            else: 
                stss.card_confirmation = st.segmented_control(
                        f"{PAGES_STR['modification_confirm'][stss.language]} {PAGES_STR['card'][stss.language].lower()} {stss.card_id}?", 
                        [ 
                            BUTTON_STR['yes'][stss.language], 
                            BUTTON_STR['no'][stss.language]
                        ]
                        )

        else:
            st.warning(f"{PAGES_STR['card'][stss.language]} {stss.card_id} {PAGES_STR['is_no_more_db'][stss.language]}")

    # 'OUI'            
    elif stss.card_confirmation == BUTTON_STR['yes'][stss.language] and stss.modified_card is None:
        check_card = []
        for i, info in enumerate(stss.current_card):
            if i != 0 and (info == '' or info is None):
                check_card.append(i)
        if check_card:   
            st.warning(f"{PAGES_STR['card'][stss.language]} {PAGES_STR['not_created_f'][stss.language]}: {' '.join(CARDS_COLUMNS[stss.language][i] for i in check_card)}")
        else:
            if stss.new_theme:
                stss.created_theme, stss.created_theme_message, stss.created_theme_message_type = create_theme(theme_name = stss.current_card[4], debug = stss.debug)
                
                if stss.created_theme_message_type != MESSAGE_TYPES[0]:
                    message_type_format(stss.created_theme_message, stss.created_theme_message_type)
                
            stss.theme_id, stss.theme_id_message, stss.theme_id_message_type = get_theme_id(theme = stss.current_card[4], debug = stss.debug)
            if stss.theme_id_message_type != MESSAGE_TYPES[0]:
                message_type_format(stss.theme_id_message, stss.theme_id_message_type)
            
            if stss.theme_id is not None:
        
                stss.modified_card, stss.modified_card_message, stss.modified_card_message_type = update_card(
                                                                                                    id = stss.current_card[0],
                                                                                                    question = stss.current_card[1],
                                                                                                    reponse = stss.current_card[2],
                                                                                                    probabilite = stss.current_card[3],
                                                                                                    id_theme = stss.theme_id,
                                                                                                )
                
                st.rerun()
                        
    # 'NON'        
    elif stss.card_confirmation == BUTTON_STR['no'][stss.language] and stss.modified_card is None:  
        st.info(f'{PAGES_STR['card'][stss.language]} {stss.card_id} {PAGES_STR['not_updated_db_f'][stss.language]}')

        if st.button(BUTTON_STR['update_card'][stss.language]):
            init_card_session(reset=True)
            st.rerun()

    else: 
        if stss.created_theme:
            message_type_format(stss.created_theme_message, stss.created_theme_message_type)
        message_type_format(stss.modified_card_message, stss.modified_card_message_type)
        st.markdown(f'#### {PAGES_STR['card_detail'][stss.language]}:')
        show_card(id = stss.modified_card[0], modify = False, debug = stss.debug)
        st.divider()
        if st.button(BUTTON_STR['update_card'][stss.language]):
            init_card_session(reset=True)
            st.rerun()
