# Flashcards
Programme de flashcards en python pour des fiches d'apprentissage par renforcement

# Changelog

## v1.0
- Ajout des instructions pour réaliser ce projet: `Instructions.md`
- Création du script d'initialisation de la base de données: `init.py` 
- Création du script de manipulation CRUD de la table 'cards': `CRUD.py`
- Création du script `main.py` 

## v1.1
- Remplacement de `comment` par `debug` pour plus de clarté dans `init.py`, `CRUD.py` et `main.py`
- Utilisation des `" "` pour les requêtes SQL d'une ligne
- Toutes les fonctions retournent une variable pour être employées dans le programme principal
- Utilisation de la valeur int du tuple count
- Import des erreurs depuis sqlite3 pour une avoir des messages d'erreur spécifiques à sqlite3
- Trop de répétitions pour les messages d'erreur (if + print)... => creation d'une fonction de log
- Suppression de la redondance de code en réutilisant la fonction `get_card()` dans les autres fonctions.

## v1.2
- Utilisation de la gestion de contexte et création d'une méthode de connexion à la base de données pour éviter d'avoir à l'ouvrir et la fermer dans chaque fonction.
- Vérification de l'initialisation variables avant de les retourner par les méthodes :
  - soit en les initialisant à `None` au début de la méthode,
  - soit en vérifiant qu'elles sont présentes dans les variables locales avec `locals()`.
- Ajout d'annotations de types explicites pour les arguments des méthodes, afin de renforcer la lisibilité du code et de prévenir les erreurs lors des appels.  

## v1.3
- `CRUD.py` a été renommé par `crud_cards.py`
- Création du script CRUD pour les thèmes: `crud_themes.py`
- Corrections mineures pour les variables non initialisées
- Le type de `probabilite` est fixé à `float` au lieu de `str`

## v1.4
- Création du script CRUD pour les statistiques: `crud_stats.py`
- Vérification que probabilite soit bien comprise entre 0.1 et 1 dans `create_cards()` et `update_card()`
- Corrections mineures dans `crud_cards.py`, `crud_themes.py` et `main.py`
- Correction des paragraphes dans `Instructions.md`

## v1.5
- Création des fichiers de test: 
  - TEST1 pour tester la fonction init_db en créant 20 flashcards: 10 sur le thème "Python" et 10 sur le thème "SQL" 
  - TEST2 pour les fonctions CRUD de manipulation des tables Cards, Themes et Stats
- Ajout de `c.execute('PRAGMA foreign_keys = ON;')` pour activer les `FOREIGN KEY`
- Remplacement `Error` par `sqlite3Error` car nom réservé. (`from sqlite3 import Error as sqlite3Error`)
- Ajout de la fonction `get_theme_id()` dans `crud_themes.py` pour le scripts TEST1. Cette fonction n'est pas demandée dans les instructions et sert uniquement dans les scripts test des fonctions CRUD.
- Correction dans des fonctions `create_card()` et `create_theme()` avec une vérification de l'existence de l'instance dans la BD avant insertion.
- Correction de code mineures

## v1.6
- Amélioration de la gestion de la connexion à la base de données : `database_connection()` retourne désormais à la fois l'instance de connexion `conn` et le curseur `c` pour faciliter les opérations sur la base de données et éviter les répétitions.
- Amélioration du formatage de `README.md`

## v1.7
- Enrichissement des fonctions SQLite avec typage, gestion des messages et support multilingue
  - Typage de retour explicite (ie: Tuple[Optional[Row], str, str])
  - Ajout de messages contextuels (succès, introuvable, erreur)
  - Classification des messages via message_type (info/warning/error)
  - Affichage conditionnel en mode debug
  - Simplification de la gestion de connexion (connexion ignorée avec ‘_’)
  - Introduction de dictionnaires multilingues pour les messages SQL `common_language.py`
  - Regroupement de fonctions et variables communes aux fonctions sqlite dans le scrypt `common_sqlite.py`git

## v1.8
- Ajout de 5 nouveaux thèmes et mise à jour pour des fonctions avec "message management" de la V1.7 dans le script: `TEST1 - inject_python_flashcards.py`  
  - Ajout
- Enrichissement de la base de données avec des nouvelles tables pour les gestions des utilisateurs et de leur statistiques: `init.py`
  - Ajout de la table **users** (gestion des comptes : id, username (unique), name, password, role, date_joined)  
  - Ajout de la table **user_card_probabilities** (liaison user–card, probabilité par défaut 0.5, FK ON DELETE CASCADE, contrainte UNIQUE)  
  - Ajout de la table **events** (historique des réponses : success/failure, timestamp, FK ON DELETE CASCADE)  
  - Passage à `ON DELETE CASCADE` pour les nouvelles relations pour éviter les éléments vide dans la DB
- Ajout de .gitignore avec la ligne __pycache__

## v2.0
- Création d'une application Streamlit avec des pages pour la gestion du jeu et des fonctionnalités principales
  - Pages principale de jeu `Flashcards.py`
  - Ajout de pages interactives (dossier `/pages`) pour la gestion des cartes `Manage_cards.py` et des thèmes `Manage_themes.py`, 
  - Ajout d'une pages pour la visualisation des statistiques `Stats.py` dans le dossier pages
  - Implémentation de fonctionnalités Streamlit communes dans `common_streamlit.py`
  - Implémentation des fonctionnalités du jeu dans `common_streamlit.py`
  - Implémentation de fonctions d'affichages avec intégration d'html: `items_streamlit.py`
  - Implémentation de fonctions pour la gestion des log et creation d'utilisateurs avec le module Streamlit-Authentificator 0.4.2: `common_authentificator.py`

## v2.1

- Préparation du packaging pour le déploiement sur Streamlit Cloud  
  - Definition de la version de python à utiliser: `.python-version` 
  - Definition du projet avec poetry: `pyproject.toml`
  - Ajout des dépendances: `poetry.lock` et `requirements.txt`

## v2.2
- Ajout de fonctions de gestion des tables **user_card_probabilities** et **events** dans `dans crud_stats.py`
- Correction de bug de connection, déconnection et de sortie du mode jeu