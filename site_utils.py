import requests
from bs4 import BeautifulSoup


def generate_text(prepend):
    return f"{prepend} <card> <line> <precolon> <color> B </color> </precolon>" \
           f" <s> regenerate <CARD_NAME> the next time this creature would be" \
           f" destroyed this turn, it isnt instead tap it, remove all " \
           f"damage from it, and remove it from combat " \
           f"</s> </line> <card>"

def process_color(color_string):
    n_colorless = len([char for char in color_string if color_string == "M"])
    color_elements = [n_colorless] if n_colorless != 0 else []
    color_elements = color_elements + [char.lower() for char in color_string if color_string != "M"]
    new_color_string = "".join([f"%7B{ce.lower()}%7D" for ce in color_elements])
    #return "%7B1%7D"
    return new_color_string

def process_rules_text(text, name):
    replace_dict = {"<card>": "",
                    "</card>": "",
                    "<s>": "",
                    "</s>": ".",
                    "<CARD_NAME>": name,
                    "<line>": "\n",
                    "</line>": "",
                    " T ": " {t} ",
                    "<precolon>": "",
                    "</precolon>": ":",
                    "<symbol>": "",
                    "</symbol>": "",
                    "<color>": "",
                    "</color>": "",
                    "<reminder>": "",
                    "</reminder>": "",
                    "<bullet>": "•",
                    "</bullet>": ""
                    }
    for key in list(replace_dict.keys()):
        text = text.replace(key, replace_dict[key])
    text = text.strip()
    return text

def present_image_planeswalker(st, card):
    url = "https://mtgcardsmith.com/src/actions/planes.php"

    name = card["name"]
    color_string = process_color(card["color"])
    rarity = card["rarity"]
    text = card["text"]
    loyalty = card["loyalty"]

    payload = f'name=%2B{name}&' \
              f'custom_mana={color_string}&' \
              f'special_card_color=&' \
              f'subtype=&' \
              f'rarity={rarity}n&' \
              f'set_icon=mtgcs1&' \
              f'ability1cost=0&' \
              f'ability1={process_rules_text(text, name)}&' \
              f'ability2cost=0&' \
              f'ability2=placeholder&' \
              f'ability3cost=0&' \
              f'ability3=placeholder&' \
              f'loyalty={loyalty}&' \
              f'artist=&' \
              f'category=&' \
              f'creator=&' \
              f'customCount=1&' \
              f'image_path=pw_upload_pic%2Fart_1619543222170119.jpg'
    headers = {
        'authority': 'mtgcardsmith.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://mtgcardsmith.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://mtgcardsmith.com/planeswalker/edit.php',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__cfduid=d32ef51e583c2af3caa3e691efda968081619398014; mtgcardsmith=aE9mu9n9pbMLlvUL8oUwRfakBImPqgM5vil8jcdnKiHj2liL; __stripe_mid=a87aecaa-cf3a-4a5b-a55d-5d33681f06e33e05f3; __stripe_sid=7e239458-aba8-4073-8709-f6fdae6d58e4293252; __cfduid=d0a9d296b23abdfe20647192d591ec7cb1619537895; mtgcardsmith=sFMAl0EmiWVLFOW2dF-NlXr-zrD-rXNnZr66R7j-zgWSpu0k'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def present_image_general(st, card):

    name = card["name"]
    color_string = process_color(card["color"])
    type = card["type"]
    rarity = card["rarity"]
    text = card["text"]
    power = card["power"] if card["type"] == "creature" else ""
    toughness = card["toughness"] if card["type"] == "creature" else ""

    url = "https://mtgcardsmith.com/src/actions/m15card"

    payload = f'slug=&create_date=&name={name}&' \
              f'custom_mana={color_string}&' \
              f'watermark=&special_card_color=&' \
              f'type={type.capitalize()}&' \
              f'custom_type=&' \
              f'subtype=&' \
              f'rarity={rarity}&' \
              f'set_icon=mtgcs1&' \
              f'text_size=large&' \
              f'description={process_rules_text(text, name)}&' \
              f'power={power}&' \
              f'toughness={toughness}&' \
              f'artist=&' \
              f'category=&' \
              f'creator=&' \
              f'image_path=%2Fupload_pic%2F1619537644879157'
    headers = {
        'authority': 'mtgcardsmith.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://mtgcardsmith.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://mtgcardsmith.com/mtg-card-maker/edit',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__cfduid=d32ef51e583c2af3caa3e691efda968081619398014; mtgcardsmith=aE9mu9n9pbMLlvUL8oUwRfakBImPqgM5vil8jcdnKiHj2liL; __stripe_mid=a87aecaa-cf3a-4a5b-a55d-5d33681f06e33e05f3; __stripe_sid=7e239458-aba8-4073-8709-f6fdae6d58e4293252; __cfduid=d0a9d296b23abdfe20647192d591ec7cb1619537895; mtgcardsmith=sFMAl0EmiWVLFOW2dF-NlXr-zrD-rXNnZr66R7j-zgWSpu0k'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def present_image(st, card):

    st.write(card)

    """response = None
    if card["type"] == "Planeswalker":
        response = present_image_planeswalker(st, card)
    else:
        response = present_image_general(st, card)

    new_response = requests.get("https://mtgcardsmith.com/preview?img=1619543862503775&t=182949")

    soup = BeautifulSoup(new_response.text, 'html.parser')
    card = soup.find('img', class_="card-large")

    st.write(new_response.__dict__)
    st.write(new_response.text)"""


def concatenate_values(card):
    if card["type"] == "Creature":
        return f"{card['type']} {card['color']} {card['rarity']} {card['mana_cost']} {card['power']} {card['toughness']}"
    elif card["type"] == "Planeswalker":
        return f"{card['type']} {card['color']} {card['rarity']} {card['mana_cost']} {card['loyalty']}"
    else:
        return f"{card['type']} {card['color']} {card['rarity']} {card['mana_cost']}"
