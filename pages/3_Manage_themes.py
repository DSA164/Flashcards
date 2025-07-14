#===================================================#
#         Gestion des thèmes dans streamlit         #
#===================================================#

import streamlit as st 
from streamlit import session_state as stss
from crud_cards import get_cards_by_theme, get_existing_card_ids
from crud_themes import create_theme, delete_theme, update_theme, get_theme, get_all_themes, get_theme_id, get_existing_theme_ids
import pandas as pd
from common_streamlit import THEMES_FUNCS, THEMES_FUNCS_NAMES, THEMES_COLUMNS, BUTTON_STR, PAGES_STR, ERRORS_STR
from common_streamlit import init_card_session, init_theme_session, show_session_state_variables, sidebar_common, show_card,message_type_format, get_cards_by_theme_selection
from common_language import LANGUAGE, MESSAGE_TYPES # ('success', 'warning', 'error', 'info')

st.set_page_config(page_title='Themes management', layout = 'wide')
sidebar_common()

# ---------------------------------------------------# 
#                     Fonctions                      #
# ---------------------------------------------------# 

def go_to_function_theme(function):
    for func in THEMES_FUNCS:
        stss[func] = True if func == function else False
    st.rerun()
    
    

def go_back_button_theme():
    if st.button(BUTTON_STR['goback'][stss.language]):
        init_theme_session(reset=True)
        init_card_session(reset = True)
        go_to_function_theme(THEMES_FUNCS[0])
    
        
        
        
def get_all_themes_list():
    themes, message, message_type = get_all_themes()
    all_themes_list = []
    if message_type != MESSAGE_TYPES[0]:
        message_type_format(message, message_type)
    elif themes:
        for card in themes:
            all_themes_list.append(card)
            
    all_themes = pd.DataFrame(all_themes_list, columns=THEMES_COLUMNS[stss.language])
    st.dataframe(all_themes, hide_index=True, )
    
        
        
        
def show_theme(theme_id, modify = False, debug=False):
    
    stss.current_theme, stss.current_theme_message, stss.current_theme_message_type = get_theme(theme_id, debug)
    stss.theme_modification = False
    
    if modify:
        stss.updated_theme = [None] * len(THEMES_COLUMNS[LANGUAGE[0]])
    
    with st.container(border=True):
        if stss.current_theme_message_type != MESSAGE_TYPES[0]:
            message_type_format(stss.current_theme_message, stss.current_theme_message_type)
        elif stss.current_theme:
            for i, info in enumerate(stss.current_theme):
                c1, c2 = st.columns((1,5))
                with c1.container(border=True):
                        st.write(THEMES_COLUMNS[stss.language][i])
                if i > 0 and modify:
                    with c1:                             
                        st.markdown(
                            f"<div style='text-align:right'>{PAGES_STR['modification'][stss.language]}</div>",
                            unsafe_allow_html=True
                        )
                                
                with c2.container(border=True): 
                        st.write(info)
                if i == 0 and modify:
                    stss.updated_theme[i] = stss.current_theme[i]
                elif i > 0 and modify:
                    with c2:
                        stss.updated_theme[i] = st.text_input(
                                        label = '', 
                                        key =  f"updated_{THEMES_COLUMNS[LANGUAGE[0]][i]}",
                                        label_visibility = "collapsed",
                                        placeholder = BUTTON_STR['fill_in_here'][stss.language],
                                        max_chars = 16,
                                        )
    
    # Pour mettre à jour un thème 
    if modify and stss.current_theme is not None:
        
        stss.current_theme = list(stss.current_theme)
        
        for i, (theme_info, update_theme_info) in enumerate(zip(stss.current_theme, stss.updated_theme)):
            if i == 0:
                injection_guard = update_theme_info != theme_info
                if injection_guard:
                    st.error(ERRORS_STR['mismatch_theme_ID'][stss.language])
                    stss.theme_modification = False
            
            elif (
                    update_theme_info is not None
                    and update_theme_info != '' # Si champ laisser vide on garder l'état de la carte
                    and update_theme_info != theme_info
                    and not injection_guard
                ):
                
                stss.current_theme[i] = update_theme_info
                
        stss.current_theme = tuple(stss.current_theme) 
                    
        if all(info is not None and info != '' for info in stss.current_theme):
            stss.theme_modification = True
        else:
            stss.theme_modification = False






         
def get_a_theme_streamlit(modify: bool = False, debug: bool = False):
    
    if 'theme_id' not in st.session_state or stss.theme_id is None:
        stss.theme_id = min(stss.exist_thm_ids)
        
    stss.theme_available = False
        
    c1_4, _ = st.columns((1,5))
    
    stss.theme_id = c1_4.number_input(
        f'{PAGES_STR['chose_number_from_1_to'][stss.language]} {max(stss.exist_thm_ids)}', 
        min_value = min(stss.exist_thm_ids), 
        max_value = max(stss.exist_thm_ids), 
        value = 1,
        )
    
    if stss.exist_thm_ids is None:
        st.error()
    if stss.theme_id in stss.exist_thm_ids:
        show_theme(theme_id = stss.theme_id, modify = modify)
        stss.theme_available = True
    else:
        st.warning(f"{PAGES_STR['theme'][stss.language]} {stss.theme_id} {PAGES_STR['is_no_more_db'][stss.language]}")
        stss.list_card_by_theme, stss.list_card_by_theme_message, stss.list_card_by_theme_message = get_cards_by_theme(id_theme = stss.theme_id)  
        if stss.list_card_by_theme is None:
            st.error(f"{ERRORS_STR['error_get_card_by_theme'][stss.language]}: {stss.list_card_by_theme_message}")            
        elif stss.list_card_by_theme != []:   
            st.error(f"{ERRORS_STR['error_card_use_deleted_theme'][stss.language]}") 
        
             
            

# ---------------------------------------------------# 
#           Session variables initialisation         #
# ---------------------------------------------------#   
if THEMES_FUNCS[0] not in stss:
    stss[THEMES_FUNCS[0]] = True
for func in THEMES_FUNCS[1:]:
    if func not in stss:
        stss[func] = False
               
     
list_of_sess_var = [stss[THEMES_FUNCS[i]] for i in range(len(THEMES_FUNCS))]

   
        
        
# ---------------------------------------------------# 
#                 Common page header                 #
# ---------------------------------------------------# 
head_1, head_2 = st.columns((5,1))
head_1.markdown(f'# {PAGES_STR['manage_themes'][stss.language]}')
with head_2:
    if any(list_of_sess_var[1:]):
        go_back_button_theme()
    else:
        if st.button(BUTTON_STR['play'][stss.language]):
            init_theme_session(reset=True)
            init_card_session(reset=True)
            go_to_function_theme(THEMES_FUNCS[0])
            
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
if stss[THEMES_FUNCS[0]]:
    
    if 'debug' in stss and stss.debug:
        st.sidebar.subheader(PAGES_STR['session_variables'][stss.language])
        st.sidebar.write(stss)
    
    c1, _ , c2 = st.columns((4,1,4))

    with c1.container(border=True):
        st.subheader(PAGES_STR['visualization'][stss.language])
        for func, name in zip(THEMES_FUNCS[1:4], THEMES_FUNCS_NAMES[stss.language][1:4]):
            if st.button(name, use_container_width=True):
              go_to_function_theme(func)  
            

    with c2.container(border=True):
        st.subheader(PAGES_STR['modification'][stss.language])
        for func, name in zip(THEMES_FUNCS[4:], THEMES_FUNCS_NAMES[stss.language][4:]):
            if st.button(name, use_container_width=True):
              go_to_function_theme(func)
              
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
#              Get a theme page section             #
#---------------------------------------------------# 
elif stss[THEMES_FUNCS[1]]:
    st.subheader(THEMES_FUNCS_NAMES[stss.language][1])
    
    init_theme_session()
        
    get_a_theme_streamlit(debug = stss.debug)
            

#---------------------------------------------------# 
#             Get all theme page section            #
#---------------------------------------------------# 
elif stss[THEMES_FUNCS[2]]:
    st.subheader(THEMES_FUNCS_NAMES[stss.language][2])
    get_all_themes_list()




#---------------------------------------------------# 
#          Get cards by theme page section          #
#---------------------------------------------------#  


elif stss[THEMES_FUNCS[3]]:
    st.subheader(THEMES_FUNCS_NAMES[stss.language][3])
    
    card_sess_var_list, card_sess_var_list_with_msg = init_card_session()
    get_cards_by_theme_selection(stss.debug)
    
    
    
        
#---------------------------------------------------#       
#             Create theme page section             #
#---------------------------------------------------#
elif stss[THEMES_FUNCS[4]]:
    st.subheader(THEMES_FUNCS_NAMES[stss.language][4])
    
    init_theme_session()
    
    if 'debug' in stss and stss.debug:
        if st.sidebar.button(f"🔄 {BUTTON_STR['refresh_variable'][stss.language]}"):
            st.rerun()
        show_session_state_variables([
                                'new_theme',
                                'new_theme_created', 
                                'created_theme' , 
                                'created_theme_message', 
                                'created_theme_message_type'
                            ])
        
    
    if not stss.new_theme_created:  
        
        if stss.new_theme is None:
            stss.new_theme = []
            for col in THEMES_COLUMNS[stss.language]:
                stss.new_theme.append(None)
   
        with st.container(border=True):
            height = 71
            for i, info in enumerate(THEMES_COLUMNS[stss.language]):
                c1, c2 = st.columns((1,5))
                if i == 1:
                    with c1.container(border=True, height=height):
                        st.write(THEMES_COLUMNS[stss.language][i])
                        
                    with c2.container(border=True, height=height): 
                        stss.new_theme[i] = st.text_input(
                            label = '', 
                            key = f"theme_info_{i-1}",
                            label_visibility = "collapsed",
                            max_chars = 16,
                            )
                        
                # Not in use, be ready in case of new theme properties    
                elif i > 1:
                    with c1.container(border=True, height=height):
                        st.write(THEMES_COLUMNS[stss.language][i])
                        
                    with c2.container(border=True, height=height): 
                        stss.new_theme[i] = st.text_input(
                            label = '', 
                            key = f"theme_info_{i-1}",
                            label_visibility = "collapsed"
                            )
                            
        if st.button(BUTTON_STR['create_confirm'][stss.language]):
            check_theme = []
            for i, info in enumerate(stss.new_theme):
                if i != 0 and (info == '' or info is None):
                    check_theme.append(i)
            
            if check_theme:   
                st.warning(f"{PAGES_STR['theme'][stss.language]} {PAGES_STR['not_created'][stss.language]}: {' '.join(THEMES_COLUMNS[stss.language][i] for i in check_theme)}")
            
            else:
                stss.created_theme, stss.created_theme_message, stss.created_theme_message_type  = create_theme(theme_name = stss.new_theme[1], debug = stss.debug)   
                stss.new_theme_created = True
                st.rerun()
            
    else:
        message_type_format(stss.created_theme_message, stss.created_theme_message_type)
        st.markdown(f'#### {PAGES_STR['theme_detail'][stss.language]}:')
        show_theme(stss.created_theme[0])
        st.markdown(f'#### {PAGES_STR['themes_list'][stss.language]}:')
        get_all_themes_list()
        st.divider()
        if st.button(BUTTON_STR['create_theme'][stss.language]):
            init_theme_session(reset=True)
            st.rerun()
    
    
    
    
#---------------------------------------------------# 
#            Delete theme page section              #
#---------------------------------------------------# 
elif stss[THEMES_FUNCS[5]]:
    st.subheader(THEMES_FUNCS_NAMES[stss.language][5])
    
    init_theme_session()
    
    if 'debug' in stss and stss.debug:
        show_session_state_variables(
                             [
                                'theme_id', 
                                'current_theme',
                                'theme_del_confirm', 
                                'theme_confirmation', 
                                'deleted_theme', 
                                'deleted_theme_message', 
                                'deleted_theme_message_type',
                                'exist_thm_ids',
                                'free_theme',
                                'list_card_by_theme',
                            ]
                        )

    get_a_theme_streamlit(debug = stss.debug)
    stss.list_card_by_theme, stss.list_card_by_theme_message, stss.list_card_by_theme_message = get_cards_by_theme(id_theme = stss.theme_id)
    
    if stss.list_card_by_theme is None:
        st.error(f"{ERRORS_STR['error_get_card_by_theme'][stss.language]: {stss.list_card_by_theme_message}}")
        stss.free_theme = False
    elif stss.list_card_by_theme == []:
        stss.free_theme = True
    
    if not stss.theme_confirmation:
        if not stss.theme_del_confirm:
            if st.button(
                    label = BUTTON_STR['delete'][stss.language], 
                    disabled = not stss.free_theme    
                ):
                stss.theme_del_confirm = True
                st.rerun()
            elif not stss.free_theme:
                st.warning(f"{PAGES_STR['not_delete_card'][stss.language]} {len(stss.list_card_by_theme)} {PAGES_STR['cards'][stss.language]}!")
            
        else: 
            stss.theme_confirmation = st.segmented_control(
                f"{PAGES_STR['deletion_confirm'][stss.language]} {PAGES_STR['theme'][stss.language].lower()} {stss.theme_id}?",
                [ 
                    BUTTON_STR['yes'][stss.language], 
                    BUTTON_STR['no'][stss.language]
                ]
                )
        #st.rerun()

    # 'Oui' 
    elif stss.theme_confirmation == BUTTON_STR['yes'][stss.language]:  
        stss.deleted_theme, stss.deleted_theme_message, stss.deleted_theme_message_type = delete_theme(stss.theme_id)
        st.info(f'{PAGES_STR['theme'][stss.language]} {stss.theme_id} {PAGES_STR['is_removed_db'][stss.language]}')
        if st.button(BUTTON_STR['delete_theme'][stss.language]):
            init_theme_session(reset=True)
            st.rerun()
            
    # 'Non'         
    elif stss.theme_confirmation == BUTTON_STR['no'][stss.language]:  
        st.info(f'{PAGES_STR['theme'][stss.language]} {stss.theme_id} {PAGES_STR['not_removed_db'][stss.language]}')
        
        if st.button(BUTTON_STR['delete_theme'][stss.language]):
            init_theme_session(reset=True)
            st.rerun()
    
  
  
#---------------------------------------------------# 
#              Update theme page section            #
#---------------------------------------------------#     
 
elif stss[THEMES_FUNCS[6]]:
    st.subheader(THEMES_FUNCS_NAMES[stss.language][6]) 
    
    init_theme_session()
        
    if 'debug' in stss and stss.debug:
        if st.sidebar.button(f"🔄 {BUTTON_STR['refresh_variable'][stss.language]}"):
            st.rerun()
        show_session_state_variables([
                                'current_theme',
                                'theme_available',
                                'updated_theme',
                                'theme_modification',
                                'theme_modification_to_be_confirmed',
                                'modified_theme',
                            ])
    
    if stss.theme_confirmation is None:  
        
        get_a_theme_streamlit(modify = True, debug = stss.debug)
    
        if stss.theme_available:
                        
                if not stss.theme_modification_to_be_confirmed:    
                    if st.button(
                            label = BUTTON_STR['update_confirm'][stss.language],
                            disabled = not stss.theme_modification
                        ):
                            stss.theme_modification_to_be_confirmed = True
                            st.rerun()
                else: 
                    stss.theme_confirmation = st.segmented_control(
                            f"{PAGES_STR['modification_confirm'][stss.language]} {PAGES_STR['theme'][stss.language].lower()} {stss.theme_id}?", 
                            [ 
                                BUTTON_STR['yes'][stss.language], 
                                BUTTON_STR['no'][stss.language]
                            ]
                            )
        else:
            st.warning(f"{PAGES_STR['theme'][stss.language]} {stss.theme_id} {PAGES_STR['is_no_more_db'][stss.language]}")


    # 'OUI'            
    elif stss.theme_confirmation == BUTTON_STR['yes'][stss.language] and stss.modified_theme is None:
        check_card = []
        for i, info in enumerate(stss.current_theme):
            if i != 0 and (info == '' or info is None):
                check_card.append(i)
                
        if check_card:   
            st.warning(f"{PAGES_STR['card'][stss.language]} {PAGES_STR['not_created_f'][stss.language]}: {' '.join(CARDS_COLUMNS[stss.language][i] for i in check_card)}")
       
        else:
            stss.modified_theme, stss.modified_theme_message, stss.modified_theme_message_type = update_theme(
                                                                                                        id = stss.current_theme[0],
                                                                                                        theme_name = stss.current_theme[1], 
                                                                                                        debug = stss.debug
                                                                                                    )
            st.rerun()
                        
    # 'NON'        
    elif stss.theme_confirmation == BUTTON_STR['no'][stss.language] and stss.modified_card is None:  
        st.info(f'{PAGES_STR['theme'][stss.language]} {stss.theme_id} {PAGES_STR['not_updated_db'][stss.language]}')

        if st.button(BUTTON_STR['update_theme'][stss.language]):
            init_theme_session(reset=True)
            st.rerun()

    else: 
        message_type_format(stss.modified_theme_message, stss.modified_theme_message_type)
        st.markdown(f'#### {PAGES_STR['theme_detail'][stss.language]}:')
        show_theme(theme_id = stss.current_theme[0], modify = False, debug = stss.debug)
        st.divider()
        if st.button(BUTTON_STR['update_theme'][stss.language]):
            init_theme_session(reset=True)
            st.rerun()

   