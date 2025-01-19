#     METHODE DE CREATION DES TABLES
#=======================================

from sqlite3 import connect, Error as sqlite3Error

def init_db(debug=True):
    try:
        conn = connect('flashcard.db')
        c = conn.cursor()
        
        c.execute("PRAGMA foreign_keys = ON;")
        c.execute('''CREATE TABLE IF NOT EXISTS cards(
                        id INTEGER PRIMARY KEY,
                        question TEXT,
                        reponse TEXT,
                        probabilite REAL,
                        id_theme INTEGER, 
                        FOREIGN KEY (id_theme) REFERENCES themes(id) ON DELETE RESTRICT
                    );
                ''') 
        
        c.execute('''CREATE TABLE IF NOT EXISTS themes(
                        id INTEGER PRIMARY KEY,
                        theme TEXT     
                    );
                ''')   
        
        c.execute('''CREATE TABLE IF NOT EXISTS stats(
                        id INTEGER PRIMARY KEY,
                        bonnes_reponses INTEGER,
                        mauvaises_reponses INTEGER,
                        date DATE
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