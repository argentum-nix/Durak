import pygame
from sys_tools import current_dir

# Definición de camino al font y los tamaños.
path = current_dir() + "/data/fonts/font.ttf"
pygame.font.init()
font_T = pygame.font.Font(path, 15)
font_S = pygame.font.Font(path, 20)
font_M = pygame.font.Font(path, 60)
font_B = pygame.font.Font(path, 80)
font_L = pygame.font.Font(path, 100)

'''
render_text(size, text, color)
|   Dependiente de tamaño de texto que se
|   requiere, la funcion genera el texto renderizado
|   y lo retorna.
'''


def render_text(size, text, color):
    if size == "T":
        font = font_T.render(text, True, color)
    elif size == "S":
        font = font_S.render(text, True, color)
    elif size == "M":
        font = font_M.render(text, True, color)
    elif size == "B":
        font = font_B.render(text, True, color)
    elif size == "L":
        font = font_L.render(text, True, color)
    return font
