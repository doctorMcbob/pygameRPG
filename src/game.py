"""
Okay here we go

This is where i should really flush out the ideas of the game

it will have grid tile based movement
encounter based combat old school JRPG style

lets keep the system simple
ATK DEF HP MP
and spells

enemies will have levels, 1 through 4
each level will have a different name and color scheme (ie dragon quest)

i'll make the enemy templates now. sounds fun. src/templates/enmies.py

The world will be a dict
TILES = {
    "water" : Set(), <--- set of positions
    "grass" : Set(),
    "mountains": Set(),
    ...
}

TANGIBLE = Set("wall", "person", "tree" ... )

if you want to step left up right or down you check if the
 new player position would be in any of the tangible tilesets
 or if they dont have the boat, if theyre in water.
 if they arent then they can step there and the player is moved down




"""
from src.config.game import *

from src.templates.player import PLAYER_TEMPLATE
from src.levels import LEVELS

def new_game():
    return {
        "PLAYER" : PLAYER_TEMPLATE.copy(),
        "LEVEL"  : STARTING_LEVEL,
    }

def run_game():
    """
    todo here, save file logic
    """
    game_state = new_game()



