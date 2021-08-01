"""
loads all the levels into memory
"""

from pathlib import Path
import os

levelpath = Path(os.path.dirname(os.path.abspath(__file__))) / "bin"

LEVELS = {}

for level in os.listdir(levelpath):
    try:
        with open(levelpath/level, "r") as f:
            LEVELS[level] = eval(f.read())
    except:
        continue

