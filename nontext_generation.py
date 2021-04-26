import random

def generate_feature(cards, feature, dependencies):
    keys = list(dependencies.keys())
    cards_copy = cards.copy()

    for key in keys:
        cards_copy = cards_copy[(cards_copy[key] == dependencies[key])]
    try:
        return random.choice(list(cards_copy[feature]))
    except IndexError as e:
        print(feature, dependencies)
        raise (e)


def generate_nontext(cards, dependency_graph, prespecified_values = {}):
    """Note: keys in the dependency graph point to a list of that node's parents in the 
    dependency graph. This code assumes that the dependency_graphs keys are in order such that a node
    comes before all the node's children."""
    new_card = prespecified_values
    keys = [key for key in list(dependency_graph.keys()) if key not in list(new_card.keys())]
    for feature in keys:
        dependencies = {parent: new_card[parent] for parent in dependency_graph[feature]}
        new_card[feature] = generate_feature(cards, feature, dependencies)
    return new_card
