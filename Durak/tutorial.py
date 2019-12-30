import pygame
import sys_tools as st 


class Tutorial:
    def __init__(self):
        self.bg = pygame.image.load(
            st.current_dir() + "/data/other/example_game").convert_alpha()


    def get_event(self, event, keys):
        if event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()

    def render(self, clock, screen, p):
        screen.fill(self.bg)
        