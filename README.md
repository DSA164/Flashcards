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

## V1.5
- Création des fichiers de test: 
  - TEST1 pour tester la fonction init_db en créant 20 flashcards: 10 sur le thème "Python" et 10 sur le thème "SQL" 
  - TEST2 pour les fonctions CRUD de manipulation des tables Cards, Themes et Stats
- Ajout de `c.execute('PRAGMA foreign_keys = ON;')` pour activer les `FOREIGN KEY`
- Remplacement `Error` par `sqlite3Error` car nom réservé. (`from sqlite3 import Error as sqlite3Error`)
- Ajout de la fonction `get_theme_id()` dans `crud_themes.py` pour le scripts TEST1. Cette fonction n'est pas demandée dans les instructions et sert uniquement dans les scripts test des fonctions CRUD.
- Correction dans des fonctions `create_card()` et `create_theme()` avec une vérification de l'existence de l'instance dans la BD avant insertion.
- Correction de code mineures

## V1.6
- Amélioration de la gestion de la connexion à la base de données : `database_connection()` retourne désormais à la fois l'instance de connexion `conn` et le curseur `c` pour faciliter les opérations sur la base de données et éviter les répétitions.
- Amélioration du formatage de `README.md`