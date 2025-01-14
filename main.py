#    PROGAMME PRINCIPAL
#==========================

# Librairie avec les fonctions personelles
from .init import init_db  # fichier sqlite3 pour générer les tables
from CRUD import *

# Message de débugage:
debug = True   # mettre à False pour ne plus avoir les messages informatifs


# Creation des tables
if __name__ == '__main__':
    init_db(comment)