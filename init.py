#     METHODE DE CREATION DES TABLES
#=======================================

from sqlite3 import connect, Error

def init_db(comment=True):
    try:
        conn = connect('flashcard.db')
        c = conn.cursor()
        c.execute('''
                    CREATE TABLE IF NOT EXISTS cards(
                        id INTEGER PRIMARY KEY,
                        question TEXT,
                        reponse TEXT,
                        probabilite REAL,
                        id_theme INTEGER 
                        FOREIGN (id_theme) KEY REFERENCES themes(id) ON DELETE RESTRICT
                    );
                ''') 
        
        c.execute(''' 
                    CREATE TABLE IF NOT EXISTS themes(
                        id INTEGER PRIMARY KEY,
                        theme TEXT     
                    );
                ''')   
        
        c.execute('''
                    CREATE TABLE IF NOT EXISTS stats(
                        id INTEGER PRIMARY KEY,
                        bonnes_reponses INTEGER,
                        mauvaises_reponses INTEGER,
                        date DATE
                    );
                ''')   
        
        conn.commit()
        if comment:
            print('Initialisation des tables réussie')
    except Error as e:
        print(f"Erreur lors de la création des tables: {e}")
    finally:
        conn.close()
        if comment:
            print('Connection à la base de donnée fermée')