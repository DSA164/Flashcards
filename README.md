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
- toutes les fonctions retournent une variable pour être employée dans le programme principa
- utilisation de la valeur int du tuple count
- import des erreurs depuis sqlite3 pour une avoir des messages d'erreur spécifique a sqlite3
- trop de répétions pour les messages d'erreur (if + print)... => creation de fonction de log
réutilisation de la fonction get_card() dans les autres fonctions, en relisant le code ce midi je me suis rendu compte que je répétais les mêmes codes

## v1.2
- Utilisation de la gestion de contexte et création d'une méthode de connexion à la base de données pour éviter d'avoir à l'ouvrir et la fermer dans chaque fonction.
- Vérification que les variables sont initialisées avant de les retourner par les méthodes :
  - soit en les initialisant à "None" au début de la méthode,
  - soit en vérifiant qu'elles sont présentes dans les variables locales avec locals().
- Définition des types des arguments des méthodes pour éviter les erreurs lors des appels

## v1.3
- CRUD.py à été renommé par crud_cards.py
- Creation du script CRUD pour les thèmes: crud_themes.py
- Correction mineur pour les variables non initialisée
- probabilite fix at float instead of str

## v1.4
- Creation du script CRUD pour les statistiques: crud_stats.py
- Vérification que probabilite soit bien comprise entre 0.1 et 1 dans create_cards() et update_card()
- Correction mineur dans crud_cards, crud_themes et main.py
- Correction des paragraphe dans Instructions.md

## V1.5
- Création des fichiers de test: 
  - TEST1 pour tester la fonction init_db en créant 20 flashcards: 10 sur le thème 'Python' et 10 sur le thème 'SQL' 
  - TEST2 pour les fonctions de manipulation des tables Cards, Themes et Stats
- Ajout de "c.execute('PRAGMA foreign_keys = ON;')" pour activer les FOREIGN KEY
- Remplecement 'Error' par 'sqlite3Error' car nom réservé. ('from sqlite3 import Error as sqlite3Error')
- Ajout d'une fonction get_theme_id() dans crud_themes.py pour le scripts TEST1
- Correction dans des fonctions create_card() et create_theme() avec un vérication d'existance d'existance de l'instance dans la BD avant insertion
- Correction de code mineures