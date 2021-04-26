def present_image(st, card):
    st.write(card)

def concatenate_values(card):
    if card["type"] == "Creature":
        return f"{card['type']} {card['color']} {card['rarity']} {card['mana_cost']} {card['power']} {card['toughness']}"
    elif card["type"] == "Planeswalker":
        return f"{card['type']} {card['color']} {card['rarity']} {card['mana_cost']} {card['loyalty']}"
    else:
        return f"{card['type']} {card['color']} {card['rarity']} {card['mana_cost']}"


