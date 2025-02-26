from operator import itemgetter
from collections import defaultdict

#TODO: Should differentiate types that are 4x - 2x - 1x - 0.5x - 0.25x - 0x on the format super_duper_effective - super_effective - normal - not_very_effective - super_not_very_effective - no_effect
def calculate_type_effectiveness(type1, type2):
    if(type2 is None):    
        return get_type_effectiveness_for_type(type1)

    type1_effectiveness = get_type_effectiveness_for_type(type1)
    type2_effectiveness = get_type_effectiveness_for_type(type2)

    combined_effectiveness = defaultdict(set)
    
    # Combine super_effective, normal, not_very_effective, and no_effect sets
    for category in ["super_effective", "normal", "not_very_effective", "no_effect"]:
        combined_effectiveness[category] = set(type1_effectiveness[category]) | set(type2_effectiveness[category])

    # Adjust effectiveness based on type interactions
    for t in type1_effectiveness["super_effective"]:
        if t in type2_effectiveness["not_very_effective"]:
            combined_effectiveness["super_effective"].discard(t)
            combined_effectiveness["normal"].add(t)
    
    for t in type1_effectiveness["not_very_effective"]:
        if t in type2_effectiveness["super_effective"]:
            combined_effectiveness["not_very_effective"].discard(t)
            combined_effectiveness["normal"].add(t)
    
    for t in type2_effectiveness["super_effective"]:
        if t in type1_effectiveness["not_very_effective"]:
            combined_effectiveness["super_effective"].discard(t)
            combined_effectiveness["normal"].add(t)
    
    for t in type2_effectiveness["not_very_effective"]:
        if t in type1_effectiveness["super_effective"]:
            combined_effectiveness["not_very_effective"].discard(t)
            combined_effectiveness["normal"].add(t)

    for category in ["super_effective", "not_very_effective"]:
        for t in list(combined_effectiveness[category]):
            if t in combined_effectiveness["normal"]:
                combined_effectiveness["normal"].discard(t)

    # Any type that exists in super_effective, normal, or not_very_effective but also exists in no_effect should be moved to no_effect
    for category in ["super_effective", "normal", "not_very_effective"]:
        for t in list(combined_effectiveness[category]):
            if t in combined_effectiveness["no_effect"]:
                combined_effectiveness[category].discard(t)
    
    return {k: list(v) for k, v in combined_effectiveness.items()}


    # Extract super_effective, normal, not_very_effect and no_effect from both variables using the itemgetter
    # Any type that exist in either super_effective, normal or no_very_effective for type1 and also exists in the no_effect set of type2 should be placed in type2
    # Compare the super_effective types of type1 to the not_very_effectives of type2. If a type from the super_effective set exists in the not_very_effective set, then that type should be replaced into the normal effectiveness set
    # If a type on type1 is not_very_effective, but has normal effectiveness on type2, then the type should be moved to normal
    # if a not_very_effective type on type1 has normal effectiveness or super effectiveness on type2, it should be moved to normal

def get_type_effectiveness_for_type(type):
    return type_effectiveness_for_attacking_dict[type]

type_effectiveness_for_attacking_dict=  {
    "normal": {
        "super_effective": ["fighting"],
        "normal": ["normal", "flying", "poison", "ground", "rock", "bug", "steel", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark"],
        "not_very_effective": [],
        "no_effect": ["ghost"]
    },
    "fighting": {
        "super_effective": ["flying", "psychic"],
        "normal": ["normal", "fighting", "poison", "ground", "ghost", "steel", "fire", "water", "grass", "electric", "ice", "dragon"],
        "not_very_effective": ["rock", "bug", "dark"],
        "no_effect": []
    },
    "flying": {
        "super_effective": ["rock", "electric", "ice"],
        "normal": ["normal", "flying", "poison", "ghost", "steel", "fire", "water", "psychic", "dragon", "dark"],
        "not_very_effective": ["fighting", "bug", "grass"],
        "no_effect": ["ground"]
    },
    "poison": {
        "super_effective": ["ground", "psychic"],
        "normal": ["normal", "flying", "rock", "ghost", "steel", "fire", "water", "electric", "ice", "dragon", "dark"],
        "not_very_effective": ["fighting", "poison", "bug", "grass"],
        "no_effect": []
    },
    "ground": {
        "super_effective": ["water", "grass", "ice"],
        "normal": ["normal", "fighting", "flying", "ground", "bug", "ghost", "steel", "fire", "psychic", "dragon", "dark"],
        "not_very_effective": ["poison", "rock"],
        "no_effect": ["electric"]
    },
    "rock": {
        "super_effective": ["fighting", "ground", "steel", "water", "grass"],
        "normal": ["rock", "bug", "ghost", "electric", "psychic", "ice", "dragon", "dark"],
        "not_very_effective": ["normal", "flying", "poison", "fire"],
        "no_effect": []
    },
    "bug": {
        "super_effective": ["flying", "rock", "fire"],
        "normal": ["normal", "poison", "bug", "ghost", "steel", "water", "electric", "psychic", "ice", "dragon", "dark"],
        "not_very_effective": ["fighting", "ground", "grass"],
        "no_effect": []
    },
    "ghost": {
        "super_effective": ["ghost", "dark"],
        "normal": ["flying", "ground", "rock", "steel", "fire", "water", "grass", "electric", "psychic", "ice", "dragon"],
        "not_very_effective": ["poison", "bug"],
        "no_effect": ["normal", "fighting"]
    },
    "steel": {
        "super_effective": ["fighting", "ground", "fire"],
        "normal": ["ghost", "water", "electric", "dark"],
        "not_very_effective": ["normal", "flying", "rock", "bug", "steel", "grass", "psychic", "ice", "dragon"],
        "no_effect": ["poison"]
    },
    "fire": {
        "super_effective": ["ground", "rock", "water"],
        "normal": ["normal", "fighting", "flying", "poison", "ghost", "electric", "psychic", "dragon", "dark"],
        "not_very_effective": ["bug", "steel", "fire", "grass", "ice"],
        "no_effect": []
    },
    "water": {
        "super_effective": ["grass", "electric"],
        "normal": ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "psychic", "dragon", "dark"],
        "not_very_effective": ["steel", "fire", "water", "ice"],
        "no_effect": []
    },
    "grass": {
        "super_effective": ["flying", "poison", "bug", "fire", "ice"],
        "normal": ["normal", "fighting", "rock", "ghost", "steel", "psychic", "dragon", "dark"],
        "not_very_effective": ["ground", "water", "grass", "electric"],
        "no_effect": []
    },
    "electric": {
        "super_effective": ["ground"],
        "normal": ["normal", "electric", "poison", "rock", "bug", "ghost", "fire", "water", "grass", "psychic", "ice", "dragon", "dark"],
        "not_very_effective": ["flying", "steel", "electric"],
        "no_effect": []
    },
    "psychic": {
        "super_effective": ["bug", "ghost", "dark"],
        "normal": ["normal", "flying", "poison", "ground", "rock", "steel", "fire", "water", "grass", "electric", "ice", "dragon"],
        "not_very_effective": ["fighting", "psychic"],
        "no_effect": []
    },
    "ice": {
        "super_effective": ["fighting", "rock", "steel", "fire"],
        "normal": ["normal", "flying", "poison", "ground", "bug", "ghost", "water", "grass", "electric", "psychic", "dragon", "dark"],
        "not_very_effective": ["ice"],
        "no_effect": []
    },
    "dragon": {
        "super_effective": ["ice", "dragon"],
        "normal": ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel", "psychic", "dark"],
        "not_very_effective": ["fire", "water", "grass", "electric"],
        "no_effect": []
    },
    "dark": {
        "super_effective": ["fighting", "bug"],
        "normal": ["normal", "flying", "poison", "ground", "rock", "steel", "fire", "water", "grass", "electric", "ice", "dragon"],
        "not_very_effective": ["ghost", "dark"],
        "no_effect": ["psychic"]
    }
}
"""
    This dict contains values of each type's effectiveness against other types. The types are listed in a way which "expects" that the type is the defending type.

    E.g: If the OCR extracts the pokemon Bulbasaur (a poison / grass type), then your returned value should be: 
    ```
        "poison": {
            "super_effective": ["ground", "psychic"],
            "normal": ["normal", "flying", "rock", "ghost", "steel", "fire", "water", "electric", "ice", "dragon", "dark"],
            "not_very_effective": ["fighting", "poison", "bug", "grass"],
            "no_effect": []
        }
    ```

    as well as
    ```
        "grass": {
            "super_effective": ["flying", "poison", "bug", "fire", "ice"],
            "normal": ["normal", "fighting", "rock", "ghost", "steel", "psychic", "dragon", "dark"],
            "not_very_effective": ["ground", "water", "grass", "electric"],
            "no_effect": []
        }
    ```

    This means that using a ``ground`` or ``psychic`` type attack against a poison type pokemon should be "super effective"
"""