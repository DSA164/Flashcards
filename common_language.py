#       Liste des langues:
#--------------------------------
LANGUAGE = ['FR', 'EN']

from streamlit import session_state as stss
if 'language' not in stss:
            stss.language = LANGUAGE[0]
language = stss.language



#      Variable communes:
#--------------------------------

MESSAGE_TYPES = ('success', 'warning', 'error', 'info')



GAME_STR = {
    'befor_to_play': {
            LANGUAGE[0]: 'Veuillez selectionner un ou  plusieurs thèmes pour jouer.',
            LANGUAGE[1]: 'Please chose one or several themes to play.',
        },
    'your_answer': {
            LANGUAGE[0]: 'Votre réponse',
            LANGUAGE[1]: 'Your answer',
        },  
    'correct_answer': {
            LANGUAGE[0]: 'Bonne réponse',
            LANGUAGE[1]: 'Correct answer',
        }, 
    'comparison': {
            LANGUAGE[0]: 'Comparaison',
            LANGUAGE[1]: 'Comparison',
        }, 
    'do_you_answer_correctly': {
            LANGUAGE[0]: 'Avez-vous répondu correctement à la question?',
            LANGUAGE[1]: 'Did you answer the question correctly?',
        }, 
    'bravo1': {
        LANGUAGE[0]: "Bravo, vous avez bien répondu!",
        LANGUAGE[1]: "Well done, you answered correctly!",
        }, 
    'bravo2': {
        LANGUAGE[0]: "Félicitations, c’est la bonne réponse!",
        LANGUAGE[1]: "Congratulations, you answered correctly!",
        }, 
    'bravo3': {
        LANGUAGE[0]: "C'est correcte, félicitations!",
        LANGUAGE[1]: "Congratulations, you answered correctly!",
        }, 
    'bravo4': {
        LANGUAGE[0]: "C’est exact, bravo!",
        LANGUAGE[1]: "That's correct, congratulations!",
        },
    'wrong1': {
        LANGUAGE[0]: "Dommage, ce n’est pas la bonne réponse.",
        LANGUAGE[1]: "Sorry, that’s not the correct answer.",
    },
    'wrong2': {
        LANGUAGE[0]: "Ce n’est pas la bonne réponse, essayez encore!",
        LANGUAGE[1]: "That’s not the right answer, try again!",
    },
    'wrong3': {
        LANGUAGE[0]: "Dommage, vous ferez mieux à la prochaine !",
        LANGUAGE[1]: "Too bad, you'll do better next time!",
    },
    'wrong4': {
        LANGUAGE[0]: "Ce n’est pas grave, vous y arriverez bientôt !",
        LANGUAGE[1]: "No worries, you'll get it soon!",
    },
    'theme_of_cards': {
            LANGUAGE[0]: 'Thème de la carte',
            LANGUAGE[1]: "Card's theme",
        }, 
    'personal_stats': {
            LANGUAGE[0]: 'Your stats',
            LANGUAGE[1]: "Personal stats",
        }, 
    'session_scores': {
            LANGUAGE[0]: 'Scores de la session',
            LANGUAGE[1]: "Session scores",
        }, 
    'daily_scores': {
            LANGUAGE[0]: 'Scores journaliers ',
            LANGUAGE[1]: "Daily scores",
        }, 
    'overall_scores': {
            LANGUAGE[0]: 'Scores globaux',
            LANGUAGE[1]: "Overall scores",
        }, 
    'wrong_answers': {
            LANGUAGE[0]: 'Mauvaises réponse',
            LANGUAGE[1]: "Wrong answers",
        }, 
    'correct_answers': {
            LANGUAGE[0]: 'Bonnes réponse',
            LANGUAGE[1]: "Correct answers",
        }, 
    'daily_score': {
            LANGUAGE[0]: 'Score du jour',
            LANGUAGE[1]: "Today score",
        }, 
    'best_score': {
            LANGUAGE[0]: 'Meilleur score',
            LANGUAGE[1]: "Best score",
        }, 
    'mean_score': {
            LANGUAGE[0]: 'Score moyen',
            LANGUAGE[1]: "Mean score",
        }, 
    'number_theme_played': {
            LANGUAGE[0]: 'Nombre thèmes joués',
            LANGUAGE[1]: "Number of themes played",
        }, 
}


BUTTON_STR = {
    'new_player': {
            LANGUAGE[0]: 'NOUVEAU JOUEUR',
            LANGUAGE[1]: 'NEW PLAYER',
        },   
    'chose_player': {
            LANGUAGE[0]: 'CHOISIR JOUEUR',
            LANGUAGE[1]: 'CHOSE PLAYER',
        }, 
    'yes': {
            LANGUAGE[0]: 'Oui',
            LANGUAGE[1]: 'Yes',
        },
    'no': {
            LANGUAGE[0]: 'Non',
            LANGUAGE[1]: 'No',
        },
    'confirm': {
            LANGUAGE[0]: 'Valider',
            LANGUAGE[1]: 'Confirm',
        },
    'play': {
            LANGUAGE[0]: 'JOUER',
            LANGUAGE[1]: 'PLAY',
        },
    'stop': {
            LANGUAGE[0]: 'STOP',
            LANGUAGE[1]: 'STOP',
        },
    'try_again': {
            LANGUAGE[0]: 'Réessayer',
            LANGUAGE[1]: 'Try again',
        },   
    'goback':  {
            LANGUAGE[0]: 'Retour',
            LANGUAGE[1]: 'Go back',
        },
    'confirm': {
            LANGUAGE[0]: 'Confirmer',
            LANGUAGE[1]: 'Confirm',
        },
    'create_confirm': {
            LANGUAGE[0]: 'Confirmer la creation',
            LANGUAGE[1]: 'Confirm creation',
        },
    'update_confirm': {
            LANGUAGE[0]: 'Confirmer la mise à jour',
            LANGUAGE[1]: 'Confirm update',
        },
    'delete_confirm': {
            LANGUAGE[0]: 'Confirmer la suppression',
            LANGUAGE[1]: 'Confirm deletion',
        },
    'delete': {
            LANGUAGE[0]: 'Supprimer',
            LANGUAGE[1]: 'Delete',
        },  
    'create_card': {
            LANGUAGE[0]: 'Créer une nouvelle carte',
            LANGUAGE[1]: 'Create a new card',
        },  
    'create_theme': {
            LANGUAGE[0]: 'Créer un nouveau thème',
            LANGUAGE[1]: 'Create new theme',
        },  
    'update_card': {
            LANGUAGE[0]: 'Mettre à jour une autre carte',
            LANGUAGE[1]: 'Update another card',
        },  
    'update_theme': {
            LANGUAGE[0]: 'Mettre à jour un autre thème',
            LANGUAGE[1]: 'Update another theme',
        },
    'delete_card': {
            LANGUAGE[0]: 'Supprimer une autre carte',
            LANGUAGE[1]: 'Delete another card',
        },  
    'delete_theme': {
            LANGUAGE[0]: 'Supprimer un autre thème',
            LANGUAGE[1]: 'Delete another theme',
        },
    'new_theme': {
            LANGUAGE[0]: 'Nouveau thème',
            LANGUAGE[1]: 'New theme',
        },
    'all_theme': {
            LANGUAGE[0]: 'Tous les thèmes',
            LANGUAGE[1]: 'All the themes',
        },
    'no_theme': {
            LANGUAGE[0]: 'Aucun thème',
            LANGUAGE[1]: 'No theme',
        },
    'fill_in_here': {
            LANGUAGE[0]: 'Compléter ici',
            LANGUAGE[1]: 'Fill in here',
        },
    'select_a_theme': {
            LANGUAGE[0]: 'Selectionner un thème',
            LANGUAGE[1]: 'Please select a theme',
        },
    'select_themes': {
            LANGUAGE[0]: 'Selectionner un ou plusieurs thèmes',
            LANGUAGE[1]: 'Please select one or several themes',
        },
    'refresh_variable': {
            LANGUAGE[0]: 'Rafraîchir variables',
            LANGUAGE[1]: 'Refresh variable',
        },

}
        
PAGES_STR = {
    'themes_select': {
            LANGUAGE[0]: 'Selectioner un ou plusieurs thèmes',
            LANGUAGE[1]: 'Select one or several themes',
        },
    'cards': {
            LANGUAGE[0]: 'cartes',
            LANGUAGE[1]: 'cards',
        },
    'stats': {
            LANGUAGE[0]: 'Statistiques',
            LANGUAGE[1]: 'Statistics',
        },
    'manage_cards': {
            LANGUAGE[0]: 'Gestion des cartes',
            LANGUAGE[1]: 'Cards management',
        },
    'manage_themes': {
            LANGUAGE[0]: 'Gestion des thèmes',
            LANGUAGE[1]: 'Themes management',
        },
    'modification': {
            LANGUAGE[0]: 'Modification',
            LANGUAGE[1]: 'Modification',
        },
    'modif_to_be_applied': {
            LANGUAGE[0]: 'Laisser vide pour conserver la valeur actuelle ',
            LANGUAGE[1]: 'Let empty to conserve the current value',
        }, 
    'visualization': {
            LANGUAGE[0]: 'Visualisation',
            LANGUAGE[1]: 'Visualization',
        },
    'number_of_cards': {
            LANGUAGE[0]: 'Nombre de cartes',
            LANGUAGE[1]: 'Number of cards',
        },
    'number_of_themes': {
            LANGUAGE[0]: 'Nombre de thèmes',
            LANGUAGE[1]: 'Number of themes',
        },
    'session_variables': {
            LANGUAGE[0]: 'Variables dans la session',
            LANGUAGE[1]: 'Variables in session',
        },
    'used_session_variables': {
            LANGUAGE[0]: 'Variables de session utilisées',
            LANGUAGE[1]: 'Used variables in session',
        },
    'card_detail': {
            LANGUAGE[0]: 'Détail de la carte',
            LANGUAGE[1]: "Card's detail",
        },
    'theme_detail': {
            LANGUAGE[0]: 'Theme',
            LANGUAGE[1]: 'Thème',
        },
    'cards_list': {
            LANGUAGE[0]: 'Liste des cartes',
            LANGUAGE[1]: 'Cards list',
        },
    'themes_list': {
            LANGUAGE[0]: 'Liste des thèmes',
            LANGUAGE[1]: 'Themes list',
        },
    'chose_number_from_1_to': {
            LANGUAGE[0]: 'Choisissez un nombre entre 1 et ',
            LANGUAGE[1]: 'Chose a number between 1 and ',
        },
    'card': {
            LANGUAGE[0]: 'La carte',
            LANGUAGE[1]: 'The cards',
        },
    'theme': {
            LANGUAGE[0]: 'Le theme',
            LANGUAGE[1]: 'The theme',
        },  
    'to_be_updated': {
            LANGUAGE[0]: 'à mettre à jour',
            LANGUAGE[1]: 'to be updated',
        },
    'to_be_created': {
            LANGUAGE[0]: 'à créer',
            LANGUAGE[1]: 'to be created',
        },
    'existing': {
            LANGUAGE[0]: 'existant',
            LANGUAGE[1]: 'current',
        },
    'existing_f': {
            LANGUAGE[0]: 'existante',
            LANGUAGE[1]: 'current',
        },
    'is_no_more_db': {
            LANGUAGE[0]: "n'est plus dans la base de données",
            LANGUAGE[1]: 'is no more available in the database',
        },
    'is_removed_db': {
            LANGUAGE[0]: 'a été supprimé de la base de données',
            LANGUAGE[1]: 'is removed from the database',
        },
    'is_removed_db_f': {
            LANGUAGE[0]: 'a été supprimée de la base de données',
            LANGUAGE[1]: 'is removed from the database',
        },
    'not_removed_db': {
            LANGUAGE[0]: 'a été conservé dans la base de données',
            LANGUAGE[1]: 'has been kept in the database',
        },
    'not_removed_db_f': {
            LANGUAGE[0]: 'a été conservée dans la base de données',
            LANGUAGE[1]: 'has been kept in the database',
        },
    
    'is_updated_db': {
            LANGUAGE[0]: 'a été mis à jour dans la base de données',
            LANGUAGE[1]: 'is updated in the database',
        },
    'is_updated_db_f': {
            LANGUAGE[0]: 'a été mise à jour dans la base de données',
            LANGUAGE[1]: 'is updated in the database',
        },
    'not_updated_db': {
            LANGUAGE[0]: 'a été laissé inchangé dans la base de données',
            LANGUAGE[1]: 'has been kept unchanged in the database',
        },
    'not_updated_db_f': {
            LANGUAGE[0]: 'a été laissé inchangée dans la base de données',
            LANGUAGE[1]: 'has been kept unchanged in the database',
        },
    'deletion_confirm': {
            LANGUAGE[0]: 'Etes-vous certain de vouloir supprimer',
            LANGUAGE[1]: 'Are you sure you want to delete',
        }, 
    'modification_confirm': {
            LANGUAGE[0]: 'Etes-vous certain de vouloir mettre à jour',
            LANGUAGE[1]: 'Are you sure you want to modify',
        },
    'not_created': {
            LANGUAGE[0]: "n'as été créé car les informations suivantes sont manquantes",
            LANGUAGE[1]: 'has not been created because following information are missing',
        },
    'not_created_f': {
            LANGUAGE[0]: "n'as été créée car les informations suivantes sont manquantes",
            LANGUAGE[1]: 'has not been created because following information are missing',
        },
     
    'existing_theme_selection': {
            LANGUAGE[0]: "Ce thème existe déjà. Veuillez choisir un autre nom ou le sélectionner dans la liste.",
            LANGUAGE[1]: 'This theme already exists. Please choose a different name or select it from the list.',
        },
    'session_state_empty': {
            LANGUAGE[0]: 'Session state est vide',
            LANGUAGE[1]: 'session state is empty',
        },
    'cards_table_empty': {
            LANGUAGE[0]: "La table 'Cards' est vide",
            LANGUAGE[1]: "the 'Cards' table is empty",
        },
    'not_delete_card': {
            LANGUAGE[0]: "Le thème ne pas être supprimé car il est utilisé par",
            LANGUAGE[1]: "The thème can not be removed because it is used by",
        },
    

}

ERRORS_STR = {
    'mismatch_card_ID': {
            LANGUAGE[0]: "Il y a une incohérence d’ID entre la carte à mettre jour et celle existante",
            LANGUAGE[1]: 'There is an ID mismatch between the card to be updated and the current one',
        },
    'mismatch_theme_ID': {
            LANGUAGE[0]: "Il y a une incohérence d’ID entre le thème à mettre jour et celui existant",
            LANGUAGE[1]: 'There is an ID mismatch between the theme to be updated and the current one',
        },
    'mandatory_new_theme': {
            LANGUAGE[0]: f"La liste des thèmes est vide, veuillez cocher '{BUTTON_STR['new_theme'][LANGUAGE[0]]}'",
            LANGUAGE[1]: f"The theme list is empty, please check '{BUTTON_STR['new_theme'][LANGUAGE[1]]}'",
        },
    'existing_f': {
            LANGUAGE[0]: 'existante',
            LANGUAGE[1]: 'current',
        },
    'existing_f': {
            LANGUAGE[0]: 'existante',
            LANGUAGE[1]: 'current',
        },
    'not_a_str': {
            LANGUAGE[0]: "n'est pas une string!",
            LANGUAGE[1]: 'is not a string!',
        },
    'not_in_session': {
            LANGUAGE[0]: "n'est pas dans la session!",
            LANGUAGE[1]: 'is not in session!',
        },
    'error_bd_cards': {
            LANGUAGE[0]: "La table 'cards' n'a pas pu être chargée de la base de donnée!",
            LANGUAGE[1]: "The 'cards' table could not be loaded from th database!",
        },
    'error_get_card_by_theme' : {
            LANGUAGE[0]: "La suppression a été interrompue, car la vérification des liens entre le thème et les cartes n’a pas pu être réalisée en raison de ",
            LANGUAGE[1]: "Deletion was interrupted because the verification of links between the theme and the cards could not be completed due to",
    },
    'error_card_use_deleted_theme' : {
            LANGUAGE[0]: "Erreur dans la base de donnée: des cartes utilisent toujours ce thème qui a été supprimé!",
            LANGUAGE[1]: "Database error: Some cards are still using this theme, which has already been deleted!",
    },
}


AUTH_MESSAGE = {
    'welcome': {
            LANGUAGE[0]: 'Bienvenue',
            LANGUAGE[1]: 'Welcome',
        },
    'name': {
            LANGUAGE[0]: 'Prénom Nom ',
            LANGUAGE[1]: 'Surname Name',
        },
    'username': {
            LANGUAGE[0]: "Nom d'utilisateur",
            LANGUAGE[1]: 'Username',
        },
    'password': {
            LANGUAGE[0]: 'Mot de passe',
            LANGUAGE[1]: 'Password',
        },            
    'login': {
            LANGUAGE[0]: 'Se connecter',
            LANGUAGE[1]: 'Login',
        },
    'logout': {
            LANGUAGE[0]: 'Se déconnecter',
            LANGUAGE[1]: 'Logout',
        },
    'connected': {
            LANGUAGE[0]: 'Vous êtes connecté',
            LANGUAGE[1]: 'Your are loged in',
        },
    'give_credentials': {
            LANGUAGE[0]: 'Veuillez saisir vos identifiants',
            LANGUAGE[1]: 'Please enter your credentials',
        },    
    'fill_username': {
            LANGUAGE[0]: "Choisissez un identifiant (ex. ylecun75)",
            LANGUAGE[1]: "Choose a username (e.g. andrewng01)",
    },
    'fill_name': {
            LANGUAGE[0]: "Votre nom complet (ex. Yann LeCun)",
            LANGUAGE[1]: "Your full name (e.g. Andrew Ng)",
    },
    'fill_passwords': {
            LANGUAGE[0]: "Créez un mot de passe sécurisé",
            LANGUAGE[1]: "Create a secure password",
    },
    '': {
            LANGUAGE[0]: '',
            LANGUAGE[1]: '',
        },      
}


AUTH_WARNING = {
    'already_existing_username': {
            LANGUAGE[0]: "Ce nom d'utilisateur est déjà pris, veuillez en choisir un autre.",
            LANGUAGE[1]: 'This username is already taken, please choose another one.',
        },
    'already_logged': {
            LANGUAGE[0]: 'Vous êtes déjà connecté avec un compte utilisateur. Veuillez vous déconnecter avant de vous connecter avec un autre compte.',
            LANGUAGE[1]: 'You are already logged in with a user account. Please log out before signing in with another account.',
        },
    '': {
            LANGUAGE[0]: '',
            LANGUAGE[1]: '',
        }, 
}


AUTH_ERRORS = {
    'error_load_credentials': {
            LANGUAGE[0]: 'Erreur lors du chargement des credentials',
            LANGUAGE[1]: 'Error while attempting to load credentials',
        },
    'incorrect_credentials': {
            LANGUAGE[0]: 'Nom d’utilisateur ou mot de passe incorrect',
            LANGUAGE[1]: 'Username or password is incorrect',
        },
    '': {
            LANGUAGE[0]: '',
            LANGUAGE[1]: '',
        }, 
}
