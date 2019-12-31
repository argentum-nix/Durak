import shutil
import pygame
import os


# borra los archivos pyc y __pycache__
def limpiar_dir():
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__':
                path = os.path.join(root, dir)
                print('Borrando {}'.format(os.path.abspath(path)))
                shutil.rmtree(path)
        for name in files:
            if name.endswith('.pyc'):
                path = os.path.join(root, name)
                print('Borrando {}'.format(os.path.abspath(path)))
                os.remove(path)


# retorna direccion actual
def current_dir():
    return os.getcwd()


def exists(file):
    return os.path.exists(file)


def write_txt(file, what):
    with open(file, 'w') as f:
        f.write(what)


def delete_txt(file):
    os.remove(file)


class Estados_Juego:
    def __init__(self):
        self.background_color = (60, 179, 113)
        self.white = (255, 255, 255)
        # IDEA: usar algo tipo map(lambda x: x/2, color) para generar la lista, pero es de a -30
        self.white_to_bg_fade = [self.white, (238, 255, 255), (238, 255, 255), (178, 255, 221),
                                 (149, 255, 193), (120, 236, 165), (91, 207, 139), (60, 179, 113)]

        self.menu_option_deselect = (50, 50, 50)
        self.menu_option_select = (255, 255, 255)

        self.keybinding = {
            'up': [pygame.K_UP, pygame.K_w],
            'down': [pygame.K_DOWN, pygame.K_s],
            'right': [pygame.K_RIGHT, pygame.K_d],
            'left': [pygame.K_LEFT, pygame.K_a],
            'select': pygame.K_RETURN,
            'pause': pygame.K_p,
            'back': pygame.K_ESCAPE
        }

        self.quit = False
        self.st_done = False
