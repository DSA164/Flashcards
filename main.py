#    PROGAMME PRINCIPAL
#==========================

# Librairie avec les fonctions personelles
from .init import init_db  # fichier sqlite3 pour générer les tables
from crud_cards import *
from crud_themes import *
from crud_stats import *

# Message de débugage:
debug = True   # mettre à False pour ne plus avoir les messages informatifs


# Creation des tables
if __name__ == '__main__':
    init_db(debug)