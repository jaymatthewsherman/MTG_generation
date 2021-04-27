import streamlit as st
import pandas as pd
import numpy as np
import torch
import random
from sklearn.model_selection import train_test_split

# ============= Hyperparameters  ================

DEPENDENCY_GRAPH = {"rarity":[],
                    "color":[],
                    "type":["rarity", "color"],
                    "mana_cost":["type", "color"],
                    "power":["mana_cost", "type"],
                    "toughness":["mana_cost", "type"],
                    "loyalty":["mana_cost", "type"]}

# ============= Project-level Imports ===========

from site_utils import present_image, concatenate_values, generate_text, process_rules_text
from nontext_generation import generate_nontext

def load_data():
    data = pd.read_csv("cards.csv")
    random.seed(0)
    return train_test_split(data, test_size=0.2)
train_data, test_data = load_data()


# ========== Site Begin =============

st.title('Magic: The Gathering Card Generation')
st.text('Parker Griep & Jay Sherman')

st.header('Instructions')

# Color and Rarity Selection
st.markdown("To input a rarity, choose a value from the dropdown, or leave the value as 'Unspecified' to randomize"
            " the rarity value based on the probabilities of each rarity value in the training data.\n"
            "To input a color, type the letters representing the mana, with the representations show below. "
            "Only one- and two-colored cards can be generated. The letters do not need to be in any particular order. "
            "Leave the textbox blank to randomize the mana based on based on the probabilities of each color "
            "in the training data. A name can also be specified, but this will not affect features generation.\n")
st.write(pd.DataFrame({"Symbols":["B", "G", "R", "U", "W"],
                      "Color": ["Black", "Green", "Red", "Blue", "White"]}))

name_selection = st.text_input('Name')
rarity_selection = st.selectbox('Rarity', options=("Unspecified", "Common", "Uncommon", "Rare", "Mythic"))
color_selection = st.text_input("Color")

#when the button is clicked
specified_values = {}
if st.button("Generate"):
    if rarity_selection != 'Unspecified':
        specified_values["rarity"] = rarity_selection.lower()
    if color_selection != "":
        u_color_selection = color_selection.upper()
        u_color_selection = [char for char in u_color_selection]
        u_color_selection.sort()
        u_color_selection = "".join(u_color_selection)
        specified_values["color"] = u_color_selection

    try:
        card = generate_nontext(train_data, DEPENDENCY_GRAPH, specified_values)
        card["name"] = name_selection if name_selection != "" else "Name"
        card["text"] = generate_text(card)
        card["text"] = process_rules_text(card["text"], card["name"])
        present_image(st, card)
    except IndexError as e:
        st.markdown("**Such a card has never been seen before (absent in training set). "
                    "Specify new color and rarity. Refer to the table above if you believe this issue stems "
                    "from your color selection.**")