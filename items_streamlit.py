import streamlit as st 
from streamlit import session_state as stss
from pyfiglet import Figlet  




####################################################################
# Génère l'ASCII-art (5 lignes) puis colore chaque caractère
####################################################################


# ------------------------- 1) Génère l'ASCII-art ------------------------- #
fig      = Figlet(font="big") 
asciiart = fig.renderText("WELCOME TO FLASHCARD")

                 # 5 lignes de haut, sans \b ou tabulations

# ------------------------- 2) Fonction arc-en-ciel ----------------------- #
COLORS = ["#ff5555", "#ff9e55", "#f1fa8c",
          "#50fa7b", "#57c7ff", "#bd93f9", "#ff79c6"]

def welcome(html_text: str) -> str:
    """Renvoie l'ASCII-art coloré caractère par caractère."""
    result, idx = [], 0
    for ch in html_text:
        if ch == "\n":                    # nouvelle ligne → balise HTML <br>
            result.append("<br>")
        else:
            color = COLORS[idx % len(COLORS)]
            # &nbsp; pour préserver les espaces, sinon le dessin s'écrase
            ch_html = "&nbsp;" if ch == " " else ch
            result.append(f"<span style='color:{color}'>{ch_html}</span>")
            idx += 1
    return "".join(result)

WELCOME = f"""
<div style="font-family: monospace; line-height: 1; white-space: pre;">
  {welcome(asciiart)}
</div>
"""


def etat_selection(selection, text):

    # Bouton visuel "allumé" ou "éteint" selon l'état
    button_color = "#5686C4" if selection else "#CCCCCC"

    st.markdown(
        f"""
        <div style="
            display:inline-block;
            padding:16px 32px;
            border-radius:8px;
            background:{button_color};
            color:#222;
            font-weight:bold;
            border:3px solid #888;
            box-shadow: 2px 2px 8px #aaa;
            text-align:center;
            width:220px;        /* largeur fixe */
            height:56;        /* hauteur fixe */
            line-height:56;  /* centre verticalement le texte si une seule ligne */
            margin-top: 32px;     /* ou la valeur que tu veux */
            argin-bottom: 32px;
            ">
            {text}
        </div>
        """, 
        unsafe_allow_html=True
    )