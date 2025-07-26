import streamlit as st 
from streamlit import session_state as stss
from crud_themes import get_all_themes, get_theme, get_used_theme_ids
from crud_users import get_user_by_username 
from crud_stats import update_user_card_probability, record_event_by_user_id
from common_authentificator import sign_in_form
from common_language import PAGES_STR, BUTTON_STR, GAME_STR, MESSAGE_TYPES # ('success', 'warning', 'error', 'info')
from common_sqlite import SQL_MESSAGE, SQL_WARNING, SQL_ERRORS
from common_streamlit import init_session_variable, sidebar_common, init_play_session, show_session_state_variables, message_type_format, get_cards_by_theme
from common_streamlit import PLAY_FUNCS, PLAY_FUNCS_NAMES,  CARDS_COLUMNS
from items_streamlit import WELCOME, etat_selection
from common_game import go_to_function_play, chose_a_card
from common_authentificator import init_authentificator, AUTH_MESSAGE, AUTH_WARNING, AUTH_ERRORS
import random


st.set_page_config(page_title='Flashcards', layout = 'wide', page_icon = ':black_joker:')

# Vérifie si on doit forcer un rerun complet
if st.session_state.get("_force_rerun", False):
    st.session_state["_force_rerun"] = False
    st.rerun()
    
#if stss.get("authentication_status") is None:
#    init_play_session(reset=True)
#    go_to_function_play(PLAY_FUNCS[0])


init_play_session()
play_pl_hold, stop_pl_hold = sidebar_common()





# ---------------------------------------------------# 
#           Session variables initialisation         #
# ---------------------------------------------------#   
if PLAY_FUNCS[0] not in stss:
    stss[PLAY_FUNCS[0]] = True
for func in PLAY_FUNCS[1:]:
    if func not in stss:
        stss[func] = False



#---------------------------------------------------# 
#          Starting section (page d'intro)          #
#---------------------------------------------------# 
if stss[PLAY_FUNCS[0]] or (stss.get("authentication_status") is None and stss[PLAY_FUNCS[3]]):
    if not stss[PLAY_FUNCS[0]]: # pour reinitialiser l'app à la page d'acceuil depuis le deconnection en mode "jeux"
        go_to_function_play(PLAY_FUNCS[0])
        init_play_session(reset = True)
        
    if 'debug' in stss and stss.debug:
        st.sidebar.subheader(PAGES_STR['session_variables'][stss.language])
        st.sidebar.write(stss)
    
    st.markdown("#")
    st.markdown("###")
    _, c0, _ = st.columns((2,5,2))
    with c0.container(border=True):
        st.markdown(WELCOME, unsafe_allow_html=True)
    _, c1 = st.columns((16,11))
    c1.markdown("###### By Banana Brain Company Inc. :banana:")
    st.markdown("###")
    _, c2a, _, c2b, _ = st.columns((3,2,1,2,3))

    if c2a.button(BUTTON_STR['new_player'][stss.language], use_container_width = True):
        go_to_function_play(PLAY_FUNCS[1])

    if c2b.button(BUTTON_STR['chose_player'][stss.language], use_container_width = True):
        go_to_function_play(PLAY_FUNCS[2])
        
    



#---------------------------------------------------# 
#                   Partie commune                  #
#---------------------------------------------------# 
else:
    head_1, head_2 = st.columns((5,1))
  
    with head_2:
        if st.button('INTRO'):
            go_to_function_play(PLAY_FUNCS[0])
            init_play_session(reset = True)
      


#---------------------------------------------------# 
#                   Créer un joueur                 #
#---------------------------------------------------# 
if stss[PLAY_FUNCS[1]]:
    #st.subheader(PLAY_FUNCS_NAMES[stss.language][1])
    
    st.markdown("# ") 
    sign_in_form()

       
 
    
#---------------------------------------------------# 
#                  Chosir un joueur                 #
#---------------------------------------------------# 
elif stss[PLAY_FUNCS[2]]:
    st.subheader(PLAY_FUNCS_NAMES[stss.language][2])
    
    
    st.markdown("#")
    
    if stss.debug:
        auth_sess_var = [
                            #"email"
                            #"init",
                            "FormSubmitter:Login-Login",
                            "roles",
                            "set",
                            "logout",
                            "name",
                            "username",
                            "authentication_status",
                    ]
        with st.sidebar:
            show_session_state_variables(auth_sess_var)

    # Initialisation de l'authentificateur
    _,  login_c1 , _  = st.columns((1, 2, 1))
    with login_c1:
        if stss.logout == True:
            stss.authenticator, authenticator_message, authenticator_message_type = init_authentificator()
        else:
            st.warning(AUTH_WARNING['already_logged'][stss.language])
            

    # --- Affichage du formulaire de connexion ---
    # ATTENTION depuis la version 0.4 authenticator ne retourne plus de variable mais écrit directement dans la session state
    stss.authenticator.login(location="main")
    
    # --- Gestion des états d'authentification ---
    if stss.authentication_status:
        #st.sidebar.success(f"{AUTH_MESSAGE['welcome'][stss.language]} *{stss.name}* :grinning:")
        #authenticator.logout(AUTH_MESSAGE['logout'][stss.language], "sidebar")
        #stss.authenticator = authenticator
        print(f"{AUTH_MESSAGE['connected'][stss.language]}.")
        user_get, _, _ = get_user_by_username(stss.name)
        stss.user_id = user_get[0]
        go_to_function_play(PLAY_FUNCS[3])
    elif stss.authentication_status is False:
        st.error(AUTH_ERRORS['incorrect_credentials'][stss.language])
    elif stss.authentication_status is None:
        st.info(AUTH_MESSAGE['give_credentials'][stss.language])
      



#---------------------------------------------------# 
#                        Jouer                      #
#---------------------------------------------------# 
elif stss[PLAY_FUNCS[3]]:
    st.markdown('###')
    
        
    # Recupération et selection du/des thèmes
    # -----------------------------------------
    
    # limiter les acces à la basse de donnée dans la boucle de jeux
    if not stss.all_themes_get:
        stss.all_themes, stss.all_themes_message, stss.all_themes_message_type = get_all_themes(debug = stss.debug)
        
        if stss.all_themes_message_type != MESSAGE_TYPES[0]:
            with st.sidebar:  
                st.subheader(PAGES_STR['themes_select'][stss.language])   
                c1_thm, c2_thm = st.columns((1, 1))
                message_type_format(stss.all_themes_message, stss.all_themes_message_type)
                stss.options_themes = stss.all_themes
                
        else:

            if not stss.options_themes:
                stss.used_themes_id, _, _ = get_used_theme_ids()
                stss.options_themes = [theme[1] for theme in stss.all_themes if theme[0] in stss.used_themes_id]
            else:
                stss.all_themes_get = True
        
    if stss.all_themes:

        with st.sidebar:  
            st.subheader(PAGES_STR['themes_select'][stss.language])   
            c1_thm, c2_thm = st.columns((1, 1))
            with c1_thm:
                if st.button(BUTTON_STR['all_theme'][stss.language], disabled = stss.selection_themes == stss.options_themes or stss.next_round == True or stss.game_ongoing == True):
                    stss.selection_themes = stss.options_themes
                    st.rerun()
        
            with c2_thm:    
                if st.button(BUTTON_STR['no_theme'][stss.language], disabled = not stss.selection_themes or stss.next_round == True or stss.game_ongoing == True):
                    stss.selection_themes = []  
                    st.rerun()
                        
           
            current_selection = stss.selection_themes
            
            selection_themes = st.multiselect(
                label = BUTTON_STR['select_themes'][stss.language], 
                options = stss.options_themes, 
                #default = stss.selection_themes, # default = stss.selection_themes
                key = "selection_themes", # (on ne met rien ce qui permet que le multiselect soit dynamique)
                label_visibility = "hidden",
                placeholder = BUTTON_STR['select_themes'][stss.language],
                disabled = stss.next_round == True or stss.game_ongoing == True
                )
            
            #if selection_themes != stss.selection_themes:
             #   st.rerun()
        
            # ATTENTION: bug de streamlit qui a toujours un état de retard sur le modification des widget:
            # SOLUTION TROUVÉE: calculer dynamiquement la variable, au lieu d'utiliser la variable de session
            #selection_themes = stss.selection_themes
            
            play_themes = [theme for theme in stss.all_themes if theme[1] in selection_themes]
            
            if stss.play_themes != play_themes:
                stss.play_themes = play_themes

                
            if not stss.game_ongoing:    
                if play_pl_hold.button(
                        label = BUTTON_STR['play'][stss.language],
                        use_container_width = True, 
                        disabled = stss.next_round == True or stss.game_ongoing == True or selection_themes == []
                    ):
                        stss.next_round = True
                        st.rerun()
            else:
                if stop_pl_hold.button(
                    label = BUTTON_STR['stop'][stss.language],
                    use_container_width = True, 
                    disabled = stss.game_ongoing == False
                ):
                    stss.game_ongoing = False
                    stss.next_round = False  
                    stss.card_is_chosen = False
                    stss.submitted = False
                    stss.correct_response = False

                    st.rerun()
            
                
            if stss.debug:
                st.write(f"Dyn. var. 'play_themes' = {play_themes}")
                show_session_state_variables(['selection_themes', 'themes', 'options_themes', 'play_themes', 'next_round', 'card_is_chosen'])
        
    
    
    # Recupération de la carte
    # -----------------------------------------
    
    if stss.next_round and stss.selection_themes:
        chose_a_card()
        stss.next_round = False
        stss.game_ongoing = True
          

    correct_response = False

    game_c1, game_c2 = st.columns((5,3))
    
    
    # Fenêtre principale de jeu
    # --------------------------
    
    with game_c1.container(border=True, height = 520):
        if not stss.card_is_chosen or not play_themes: #and not stss.themes_selection_fixed:
            for i in range(2):
                st.markdown(f'#') 
            _, c1_2, _ = st.columns((1,4,1))
            with c1_2.container(border = True, height = 150, ):
                    st.markdown(
                        f"""
                        <div style="
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            height: 120px;
                            width: 100%;
                            text-align: center;
                            background: #282828;  /* gris clair, change au besoin */
                            border-radius: 2.5em; /* coins arrondis optionnels */
                        ">
                            <h2 style="margin: 0; font-size: calc(1rem + 1vw);">{GAME_STR['befor_to_play'][stss.language]}</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            stss.next_round = False       
                
        else:
            
            st.markdown(f'## {CARDS_COLUMNS[stss.language][2]}')
            st.info(stss.chosen_card[1])
            
            if not stss.submitted:
                stss.user_response = st.text_area(GAME_STR['your_answer'][stss.language], height=100, key='question' )
                
                if st.button('Valider', disabled = not stss.user_response):
                    stss.submitted = True
                    st.rerun()
                    
            #-------------------------------------------#
            #              Reponse correcte.            #
            #-------------------------------------------#
            elif stss.correct_response == 'yes':
                bravo_keys = [key for key in GAME_STR if key.startswith("bravo")]
                bravo_random = random.choice(bravo_keys)
                st.success(f'## {GAME_STR[bravo_random][stss.language]}', icon=":material/thumb_up:")
                if st.button(BUTTON_STR['try_again'][stss.language]):
                    stss.number_theme_played.append(stss.chosen_card[4])
                    stss.user_response = ''
                    stss.submitted = False
                    stss.correct_response = False
                    stss.next_round = True
                    st.rerun()
                
            #-------------------------------------------#
            #               Reponse fausse.             #
            #-------------------------------------------#
            elif stss.correct_response == 'no':
                wrong_keys = [key for key in GAME_STR if key.startswith("wrong")]
                wrong_random = random.choice(wrong_keys)
                st.error    (f'## {GAME_STR[wrong_random][stss.language]}', icon=":material/thumb_down:")
                if st.button(BUTTON_STR['try_again'][stss.language]):
                    stss.number_theme_played.append(stss.chosen_card[4])
                    stss.user_response = ''
                    stss.submitted = False
                    stss.correct_response = False
                    stss.next_round = True
                    st.rerun()
                    
            else:
                st.header(GAME_STR['comparison'][stss.language])
                c1, c2 = st.columns((1,1))
                c1.text(GAME_STR['your_answer'][stss.language])
                c1.warning(stss.user_response)
                c2.text(GAME_STR['correct_answer'][stss.language])
                c2.success(stss.chosen_card[2])
                
                st.divider()
                
                #-------------------------------------------#
                #          Validation de la réponse         #
                #-------------------------------------------#
                increment = 0.05
                st.write(GAME_STR['do_you_answer_correctly'][stss.language])
                c1b, c2b = st.columns((1,1))
                if c1b.button(BUTTON_STR['yes'][stss.language]):
                    stss.correct_response = 'yes'
                    stss.correct_answers += 1
                    _, _, _ = record_event_by_user_id(user_id = stss.user_id, card_id = stss.chosen_card[0], result='success', debug = stss.debug)
                    _, _, _ = update_user_card_probability(user_id = stss.user_id, card_id = stss.chosen_card[0], increment = -increment, debug = stss.debug)

                if c2b.button(BUTTON_STR['no'][stss.language]):
                    stss.correct_response = 'no'
                    stss.wrong_answers += 1
                    _, _, _ = record_event_by_user_id(user_id = stss.user_id, card_id = stss.chosen_card[0], result='failure', debug = stss.debug)
                    _, _, _ = update_user_card_probability(user_id = stss.user_id, card_id = stss.chosen_card[0], increment = increment, debug = stss.debug)


    # Liste des themes choisis et Highlight du thème en cours
    # -------------------------------------------------------- 
                
    with game_c2.container(border=True, height = 520):    
        st.markdown(f'### {GAME_STR['theme_of_cards'][stss.language]}')
        
        #selection_themes = stss.selection_themes
        
        if stss.all_themes and stss.selection_themes and 'chosen_card' in stss:
            
            played_themes = [theme for theme in stss.all_themes if theme[1] in stss.selection_themes]

            current_theme = [theme for theme in stss.play_themes if stss.chosen_card[4] == theme[0]]
            #current_theme = current_theme[0] # pour récupérer le tupple et non une liste avec 1 tupple
            
            if stss.debug:
                st.write(f"played_themes: {played_themes}")
                st.write(f"current_theme: {current_theme}")
                
            game_c2_c1, game_c2_c2 = st.columns((1,1))
            for i, theme in enumerate(played_themes):
                activation = bool(current_theme and theme == current_theme[0])
                #if theme == current_theme[0]:
                #    activation = True
                #else: 
                #    activation = False
                    
                if i % 2 == 0:
                    with game_c2_c1:
                        etat_selection(activation, theme[1])
                        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
                    #game_c2_c1.button(theme[1], use_container_width = True, disabled = not activation ) 
                else:
                    with game_c2_c2:
                        etat_selection(activation, theme[1])
                        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
                        
                    #game_c2_c2.button(theme[1], use_container_width = True, disabled = not activation )
                    
                if stss.debug:
                    st.write(f"iteration: {i}, theme: {theme}, activation: {activation}")
    

        if stss.debug:
            st.write(stss)
        if stss.debug and 'chosen_card' in stss:
            st.write(f"stss.chosen_card[4]: {stss.chosen_card[4]}")
            st.write(f"get_theme(stss.chosen_card[4]): {get_theme(id = stss.chosen_card[4], debug = stss.debug)}")


    # Bandeau statistique
    # -------------------------------------------------------- 
       
    game_c1b, game_c2b, game_c3b = st.columns((1,1,1))   
    
    temp = 0
    
    total = stss.correct_answers + stss.wrong_answers
    ratio = 0.0 if total == 0 else stss.correct_answers / total
    if stss.number_theme_played:
        differents_themes_played = len(tuple(stss.number_theme_played))
    else:
        differents_themes_played = 0
    
    with game_c1b.container(border=True): 
        st.markdown(f'### {GAME_STR['session_scores'][stss.language]}')
        st.write(f"{GAME_STR['correct_answers'][stss.language]} : {stss.correct_answers}") 
        st.write(f"{GAME_STR['wrong_answers'][stss.language]} : {stss.wrong_answers}")
        st.write(f"{GAME_STR['session_scores'][stss.language]} : **{ratio:.0%}**")
        st.write(f"{GAME_STR['number_theme_played'][stss.language]} : **{differents_themes_played}**")

        
    with game_c2b.container(border=True): 
        st.markdown(f'### {GAME_STR['daily_scores'][stss.language]}')
        st.write(f"{GAME_STR['correct_answers'][stss.language]} : **{temp}**") 
        st.write(f"{GAME_STR['wrong_answers'][stss.language]} : **{temp}**")
        st.write(f"{GAME_STR['mean_score'][stss.language]} : **{temp}**")
        st.write(f"{GAME_STR['best_score'][stss.language]} : **{temp}**")
        
    with game_c3b.container(border=True): 
        st.markdown(f'### {GAME_STR['overall_scores'][stss.language]}')
        st.write(f"{GAME_STR['correct_answers'][stss.language]} : **{temp}**") 
        st.write(f"{GAME_STR['wrong_answers'][stss.language]} : **{temp}**")
        st.write(f"{GAME_STR['mean_score'][stss.language]} : **{temp}**")
        st.write(f"{GAME_STR['best_score'][stss.language]} : **{temp}**")
    
