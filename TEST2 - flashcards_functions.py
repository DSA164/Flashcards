from crud_cards import create_card, get_card, update_card, delete_card, get_all_cards
from crud_themes import create_theme, get_all_themes, delete_theme
from crud_stats import update_stats, get_stats

# ------------------------------------------------------#
#        Attention si TEST 2 à déjà été lancer:         #
#           - supprimer la base de donnée               #
#           - relancer TEST 1                           #
#           - puis lancer TEST 2                        #
# ------------------------------------------------------#

# cards (id, question, reponse, probabilite, id_theme) 
# themes (id, theme)
# stats (id, bonnes_reponses, mauvaises_reponses, date)

def test_functions(debug):
    # Tester la création de thème
    print("Testing themes...")
    new_theme = create_theme("Test Theme", debug)
    theme_id = new_theme[0]
    assert new_theme is not None
    themes = get_all_themes(debug)
    assert any(theme[0] == theme_id for theme in themes)

    # Tester la création de carte
    print("Testing cards...")
    card = create_card("Test Question", "Test Answer", 0.5, theme_id, debug)
    card_id = card[0]
    assert card_id is not None
    card = get_card(card_id, debug)
    assert card[1] == "Test Question"

    # Tester la récupération de toutes les cartes
    print("Testing get_all_cards...")
    all_cards = get_all_cards(debug)
    assert any(c[0] == card_id for c in all_cards)

    # Tester la mise à jour de carte
    print("Testing card update...")
    update_card(card_id, "Updated Question", "Updated Answer", 0.7, theme_id, debug)
    card = get_card(card_id, debug)
    assert card[1] == "Updated Question"
 
    # Tester la suppression de carte
    print("Testing card deletion...")
    delete_card(card_id, debug)
    assert get_card(card_id, debug) is None

    # Tester la mise à jour des stats
    print("Testing stats...")
    update_stats(True)
    stats = get_stats(debug)
    assert stats is not None

    # Nettoyer après le test
    delete_theme(theme_id, debug)
    print("All tests passed.")

if __name__ == "__main__":
    print("===================================================")
    print("===============       TEST 2       ================")
    print("===================================================")
    test_functions(True)
