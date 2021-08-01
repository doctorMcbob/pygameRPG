import pygame
from pygame.locals import *
from pygame import Surface, Rect

from pathlib import Path
import os

tokenpath = Path(os.path.dirname(os.path.abspath(__file__))) / "bin"
keyboardpath = tokenpath / "keyboard"

TOKENS = {}
KEYBOARD = {}
KEYBOARD_MAP = {
    K_a: "a", K_b: "b", K_c: "c", K_d: "d", K_e: "e",
    K_f: "f", K_g: "g", K_h: "h", K_i: "i", K_j: "j",
    K_k: "k", K_l: "l", K_m: "m", K_n: "n", K_o: "o",
    K_p: "p", K_q: "q", K_r: "r", K_s: "s", K_t: "t",
    K_u: "u", K_v: "v", K_w: "w", K_x: "x", K_y: "y",
    K_z: "z", 
    K_0: "0", K_1: "1", K_2: "2", K_3: "3", K_4: "4",
    K_5: "5", K_6: "6", K_7: "7", K_8: "8", K_9: "9",
    K_PLUS: "+", K_MINUS: "-", K_COLON: ":",
    K_SPACE: " ", K_AT: "@", K_EXCLAIM: "!",
    K_AMPERSAND: "&", K_QUOTE: "'",
    K_QUOTEDBL: '"', K_HASH: "#", K_DOLLAR: "$",
    K_LEFTPAREN: "(", K_RIGHTPAREN: ")",
    K_ASTERISK: "*", K_COMMA: ",", K_PERIOD: ".",
    K_SLASH: "/", K_SEMICOLON: ";", K_LESS: "<",
    K_GREATER: ">",  K_EQUALS: "=", K_QUESTION: "?",
    K_LEFTBRACKET: "[", K_RIGHTBRACKET: "]",
    K_BACKSLASH: "\\",
}
CHARACTER_MAP = {
    "+": "plus",          "-": "minus",          ":":"colon",
    " ": "base",          "@": "at",             "!": "exclamation",
    "&": "ampersand",     "#": "hash",           "$": "dollar",
    "(": "openparenth",   ")": "closeparenth",   "*": "star",
    ",": "comma",         ".": "period",         "/": "slash",
    ";": "semicolon",     "<": "lessthan",       ">": "greaterthan",
    "=": "equals",        "?": "question",       "[": "openbracket",
    "]": "closebracket",  "{": "openbrace",      "}": "closebrace",
    "\\":"backslash",     "%": "percent",        "`": "tick",
    "~": "tilda",         "^": "carrot",         "_": "underscore",
    "|": "pipe",          "'": "singlequote",    '"': "doublequote",
}

for token in os.listdir(tokenpath):
    try:
        with open(tokenpath/token, "r") as f:
            TOKENS[token] = eval(f.read())
    except:
        continue

for token in os.listdir(keyboardpath):
    try:
        with open(keyboardpath/token, "r") as f:
            KEYBOARD[token] = eval(f.read())
    except:
        continue

def draw_token(dest, name, pos, colorkey=(1, 255, 1), col1=(0, 0, 0), col2=(255, 255, 255), PW=1):
    tokenpool = TOKENS
    if name in KEYBOARD:
        tokenpool = KEYBOARD
    for i, t in enumerate(tokenpool[name]):
        x, y = i % 16, i // 16
        if t != 0:
            pygame.draw.rect(dest,
                             [colorkey, col1, col2][t],
                             Rect((pos[0] + x*PW, pos[1] + y*PW),
                                  (PW, PW)))


def draw_sentance(dest, string, pos, colorkey=(1, 255, 1), col1=(0, 0, 0), col2=(255, 255, 255), PW=1):
    for i, s in enumerate(string):
        if s in CHARACTER_MAP:
            s = CHARACTER_MAP[s]
        POS = (pos[0] + (i*PW*16), pos[1])
        draw_token(dest, s, POS, colorkey, col1, col2, PW)
            
    
if __name__ == """__main__""":
    pygame.init()
    PW = 2
    SCREEN = pygame.display.set_mode((PW*16*16, PW*16*16))
    pygame.display.set_caption("text demo")
    
    COLORS = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 0), (0, 255, 255)]
    c1, c2 = 0, 1
    
    text = ""
    
    while True:
        SCREEN.fill((0, 0, 0))
        draw_sentance(SCREEN, text, (0, 0), col1=COLORS[c1], col2=COLORS[c2], PW=2)


        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE: quit()

                if e.key in KEYBOARD_MAP:
                    text = text + KEYBOARD_MAP[e.key]

                if e.key == K_BACKSPACE: text = text[:-1]
                
                if e.key == K_LEFT: c1 = (c1 - 1) % len(COLORS)
                if e.key == K_RIGHT: c1 = (c1 + 1) % len(COLORS)
                if e.key == K_UP: c2 = (c2 - 1) % len(COLORS)
                if e.key == K_DOWN: c2 = (c2 + 1) % len(COLORS)
