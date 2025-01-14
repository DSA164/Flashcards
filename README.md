# Flashcards
Programme de flashcards en python pour des fiches d'apprentissage par renforcement

# Changelog

## v1.0
- Ajout des instructions pour réaliser ce projet: Intructions.md
- Creation du script d'initialisation de la base de donnée: init.py 
- Creation du script de manipulation CRUD de la table 'cards': CRUD.py
- Création du script main.py 

## v1.1
- emplacement de 'comment' par 'debug' pour plus de clarté (init.py, CRUD.py, main.py)
- utilisation des " " pour les simples lignes
- toutes les fonctions retournent une variable pour être employée dans le programme principal
- utilisation de la valeur int du tuple count
- import des erreurs depuis sqlite3 pour une avoir des messages d'erreur spécifique a sqlite3
- trop de répétions pour les messages d'erreur (if + print)... => creation de fonction de log
réutilisation de la fonction get_card() dans les autres fonctions, en relisant le code ce midi je me suis rendu compte que je répétais les mêmes codes



