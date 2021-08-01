"""
enemy templates

enemies will have the same template structure as the player

each enemy has four levels, you will choose your enemy by
ENEMY_TEMPLATES[enemy_name][level]
ENEMY_TEMPLATES["bear"][2]

the enemy name, ie: the key in the dictionary
 will also be the token name when drawing 
"""

ENEMY_TEMPLATES = {
    # Sample
    "bear": [
        {
            "NAME": "brown bear",
            "ATK": 2,
            "DEF": 3,
            "HP": 8,
            "MP": 0,
            "SPELLS": [],
            "COLOR": [(150,75,0), (0, 0, 0)],
        },{
            "NAME": "sea bear",
            "ATK": 5,
            "DEF": 8,
            "HP": 13,
            "MP": 0,
            "SPELLS": [],
            "COLOR": [(20, 150, 35), (0, 0, 0)],
        },{
            "NAME": "b ear",
            "ATK": 9,
            "DEF": 14,
            "HP": 25,
            "MP": 2,
            "SPELLS": ["slack"],
            "COLOR": [(128,191,255), (230, 0, 230)],
        },{
            "NAME": "death bear",
            "ATK": 15,
            "DEF": 19,
            "HP": 35,
            "MP": 4,
            "SPELLS": ["slack", "claw"],
            "COLOR": [(0, 0, 0), (255, 0, 0)],
        }
    ],
}
