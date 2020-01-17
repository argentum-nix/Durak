import shutil
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
        self.white_to_bg_fade = [self.white, (238, 255, 255),
                                 (238, 255, 255), (178, 255, 221),
                                 (149, 255, 193), (120, 236, 165),
                                 (91, 207, 139), (60, 179, 113)]

        self.quit = False
        self.st_done = False
        self.durak = -1
