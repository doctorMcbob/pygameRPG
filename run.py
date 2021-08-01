"""
Welcome friends. On this beautiful day I decided to make a game

this is the first code i am writing at 11:30 :)

i gave it some thought and decided it would be nice to clean up my level editors,
 so im making the editor right off the bat.
 it should be launched with the boot script just like the game.

This is going to be an RPG because I've never made one.

Using token builder from my LURD2 game, I've used it in other projects too at this point,
I might make the tiles bigger... undecided.

Anyways, the next file im going to will be src/game.py and src/editor.py
"""
import sys

from src.game import run_game
from src.editor import run_editor

if '-e' in sys.argv:
    run_editor(sys.argv[-1])

else: run_game()
