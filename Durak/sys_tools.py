import os

'''
current_dir()
|   Función que ocupa os.getcwd
|   para retonar la direccion actual.
'''


def current_dir():
    return os.getcwd()


'''
exists(file)
|   Retorna si el archivo existe o no en la carpeta actual.
'''


def exists(file):
    return os.path.exists(file)


'''
write_txt(file, what)
|   Escribe una línea al archivo file, de contenido what.
'''


def write_txt(file, what):
    with open(file, 'w') as f:
        f.write(what)


'''
delete_txt(file)
|   Función, que ocupa os.remove, para borrar un archivo txt.
'''


def delete_txt(file):
    os.remove(file)


'''
class Estados_Juego
|   Clase con algunas variables globales para toda clase.
'''


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
