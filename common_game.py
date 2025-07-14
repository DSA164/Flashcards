#=======================================================#
#        Fonctions pour la partie principale, game      #
#=======================================================#

import streamlit as st 
from streamlit import session_state as stss
import random
from common_streamlit import PLAY_FUNCS
from typing import List
from crud_cards import get_cards_by_theme


# ---------------------------------------------------# 
#                     Fonctions                      #
# ---------------------------------------------------# 
def go_to_function_play(function):
    for func in PLAY_FUNCS:
        stss[func] = True if func == function else False
    st.rerun()
    
    
    
def one_select_activation(item_to_activate: str, items: List[str]) -> List[bool]:
    for item in items:
        stss[item] = True if item == item_to_activate else False
    st.rerun()
    
    
    
def chose_a_card(debug: bool = False):
    stss.cards_list = {}
    stss.card_is_chosen = False
    if stss.play_themes:
        for theme in stss.play_themes:
            cards_by_theme, _, _ = get_cards_by_theme(id_theme = theme[0], debug = debug)
            stss.cards_list[theme[1]] = cards_by_theme
        
        stss.chosen_theme_key = random.choice(list(stss.cards_list.keys()))
        stss.chosen_card = random.choice(stss.cards_list[stss.chosen_theme_key])
        if stss.chosen_card:
            stss.card_is_chosen = True

