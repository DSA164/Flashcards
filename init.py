#     METHODE DE CREATION DES TABLES
#=======================================

from sqlite3 import connect, Error as sqlite3Error

def init_db(debug=True):
    try:
        conn = connect('flashcard.db')
        c = conn.cursor()
        
        c.execute("PRAGMA foreign_keys = ON;")
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        name TEXT,
                        user_password TEXT NOT NULL,
                        role TEXT DEFAULT 'user',
                        date_joined TEXT
                    );  
            ''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS themes(
                        id INTEGER PRIMARY KEY,
                        theme TEXT     
                    );
                ''') 
        
        c.execute('''CREATE TABLE IF NOT EXISTS cards(
                        id INTEGER PRIMARY KEY,
                        question TEXT,
                        reponse TEXT,
                        probabilite REAL,
                        id_theme INTEGER, 
                        FOREIGN KEY (id_theme) REFERENCES themes(id) ON DELETE RESTRICT
                    );
                ''') 
        
        c.execute('''CREATE TABLE IF NOT EXISTS user_card_probabilities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        card_id INTEGER,
                        probabilite REAL DEFAULT 0.5,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE,
                        UNIQUE (user_id, card_id)
                    );
 
                ''') 
          
        c.execute('''CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            card_id INTEGER,
            result TEXT CHECK (result IN ('success', 'failure')),
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE
        );      
            ''') 
                
        conn.commit()
        if debug:
            print('Initialisation des tables réussie')
    except sqlite3Error as e:
        print(f"Erreur lors de la création des tables: {e}")
    finally:
        conn.close()
        if debug:
            print('Connection à la base de donnée fermée')