# Projet : Application de Flashcards

## 2.1 Introduction au projet
Le but de ce projet est de construire une application de flashcards. Ce type d’application permet à l’utilisateur de créer des cartes mentales, avec une information ou question par carte, et d’essayer de répondre à la question ou d’expliquer le concept. La subtilité est que l’apparition des cartes dépend de si vous arrivez à avoir la bonne réponse. Plus vous serez à l’aise avec un concept, moins la carte apparaîtra. En revanche, plus vous avez du mal avec un concept, plus la carte apparaîtra fréquemment.

L’objectif de cette partie est de développer la base de données et les fonctions de base pour interagir avec elle. Par la suite, nous développerons l’interface dans le chapitre de Streamlit pour aboutir à une application de flashcards utilisable.

## 2.2 Schéma de la Base de Données
Votre base de données pour l’application de Flashcards comprendra trois tables principales :

- **cards** : Contient les flashcards.
- **themes** : Contient les thèmes des flashcards.
- **stats** : Contient les statistiques des réponses des utilisateurs.

### Détail des Tables :

- **cards**
  - `id` : INTEGER, PRIMARY KEY
  - `question` : TEXT
  - `reponse` : TEXT
  - `probabilite` : REAL
  - `id_theme` : INTEGER, FOREIGN KEY REFERENCES themes(id) ON DELETE RESTRICT

- **themes**
  - `id` : INTEGER, PRIMARY KEY
  - `theme` : TEXT

- **stats**
  - `id` : INTEGER, PRIMARY KEY
  - `bonnes_reponses` : INTEGER
  - `mauvaises_reponses` : INTEGER
  - `date` : DATE

*Note :* Le champ *probabilite* est un réel compris entre 0.1 et 1.
Pour éviter de supprimer une flashcard utilisant un thème, la contrainte *ON DELETE RESTRICT* est ajoutée à la clé étrangère *id_theme*.

## 2.3 Fonctions à Implémenter

Votre tâche est de créer les fonctions Python suivantes pour interagir avec la base de données SQLite. Ces fonctions doivent respecter les spécifications fournies.

### 2.3.1 Initialisation de la Base de Données

**Fonction :** `init_db()`

**Description :**
- Initialise la base de données en créant les tables *cards*, *themes*, et *stats* si elles n’existent pas.
- Insère des thèmes prédéfinis dans la table *themes*.
- Utilise `sqlite3.connect()` pour établir une connexion.
- Valide les modifications avec `conn.commit()` et ferme la connexion.

### 2.3.2 Fonctions CRUD pour les Flashcards

**Fonctions :**
- `create_card(question, reponse, probabilite, id_theme)` : Crée une carte.
- `get_card(id)` : Récupère une carte.
- `update_card(id, question, reponse, probabilite, id_theme)` : Met à jour une carte.
- `delete_card(id)` : Supprime une carte.
- `get_all_cards()` : Récupère toutes les cartes.
- `get_number_of_cards()` : Obtient le nombre total de cartes.
- `get_cards_by_theme(id_theme)` : Récupère les cartes par thème.

### 2.3.3 Fonctions CRUD pour les Thèmes

**Fonctions :**
- `create_theme(theme)` : Crée un thème.
- `get_theme(id_theme)` : Récupère un thème.
- `update_theme(id_theme, theme)` : Met à jour un thème.
- `delete_theme(id_theme)` : Supprime un thème.
- `get_all_themes()` : Récupère tous les thèmes.

### 2.3.4 Fonctions pour les Statistiques

**Fonctions :**
- `update_stats(is_correct)` : Met à jour les statistiques.
- `update_card_probability(card_id, is_correct)` : Met à jour la probabilité d’apparition d’une carte.
- `get_stats()` : Récupère les statistiques au travers du temps.

**Indications pour l’implémentation :**
- **update_stats()** :
  - Vérifie l’existence d’une entrée pour la date du jour.
  - Met à jour ou crée une nouvelle entrée dans la table *stats*.

- **update_card_probability()** :
  - Multiplie la probabilité actuelle par 0.9 si la réponse est correcte, sinon par 1.1.
  - Restreint la probabilité entre 0.1 et 1.0.
  - Utilise des paramètres dans les requêtes SQL pour éviter les injections SQL.

*Note :* Ajoutez une gestion des erreurs avec des blocs `try...except` pour garantir la robustesse du code.

---

Ce fichier contient les instructions pour le projet et doit être placé dans le répertoire GitHub correspondant. Assurez-vous de suivre les spécifications pour chaque fonction afin d’assurer une bonne gestion de la base de données et des interactions utilisateur.

