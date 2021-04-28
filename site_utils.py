import requests
import streamlit as st
from gpt_generator import GPTGenerator

gpt_generator = GPTGenerator("gpt2-epochs3")

def generate_text(card):
    if card['type'] == 'Creature':
        return gpt_generator.generate(card['rarity'], card['color'], card['type'], card['mana_cost'], power=card['power'], toughness=card['toughness'])
    elif card['type'] == 'Planeswalker':
        return gpt_generator.generate(card['rarity'], card['color'], card['type'], card['mana_cost'], loyalty=card['loyalty'])
    return gpt_generator.generate(card['rarity'], card['color'], card['type'], card['mana_cost'])

def process_color(color_string):
    n_colorless = len([char for char in color_string if color_string == "M"])
    color_elements = [n_colorless] if n_colorless != 0 else []
    color_elements = color_elements + [char.lower() for char in color_string if color_string != "M"]
    new_color_string = "".join([f"%7B{ce.lower()}%7D" for ce in color_elements])
    return new_color_string

def process_rules_text(text, name):
    replace_dict = {"\"<card>": "",
                    "</card>\"": "",
                    "<line>": "",
                    "</line>": "\n",
                    "T": "{t}",
                    "<precolon>": "",
                    "</precolon>": ":",
                    "<symbol>": "",
                    "</symbol>": "",
                    "<color>": "",
                    "</color>": "",
                    "<reminder>": "",
                    "</reminder>": "",
                    "<bullet>": "•",
                    "</bullet>": "",
                    "<sentence>": "",
                    " </sentence>": ".",
                    "<CARD_NAME>": name,
                    }
    if "\"<card>" in text:
        text = text[text.index("\"<card>"):]
    for key in list(replace_dict.keys()):
        text = text.replace(key, replace_dict[key])
    text = text.strip()
    return text

def present_image(st, card):
    st.markdown("**Name: **{}".format(card["name"]))
    st.markdown("**Type: **{}".format(card["type"]))
    st.markdown("**Color: **{}".format(card["color"]))
    st.markdown("**Mana Cost: **{}".format(card["mana_cost"]))
    if card["type"] == "Creature":
        st.markdown("**Power: **{}".format(card["power"]))
        st.markdown("**Toughness: **{}".format(card["toughness"]))
    elif card["type"] == "Planeswalker":
        st.markdown("**Loyalty: **{}".format(card["loyalty"]))
    st.markdown("**Rules Text: **{}".format(card["text"]))

def concatenate_values(card):
    attributes = [ card['rarity'], card['color'], card['type'], card['mana_cost'] ]
    if card['type'] == "Creature":
        attributes.extend([card['power'], card['toughness']])
    elif card['type'] == "Planeswalker":
        attributes.append(card['loyalty'])
    return " ".join(attributes)