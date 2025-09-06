import pygame
from sys import exit

from pygame.time import Clock

pygame.init()
pantalla = pygame.display.set_mode((1500,920))
pygame.display.set_caption("easter egg")
reloj = pygame.time.Clock()

fondo= pygame.image.load("fotos/game_background_3. 2.png").convert()
piso = pygame.Surface((1500, 200))  # width=1500, height=200
piso.fill('black')  # brown color for ground

enemigo_1= pygame.image.load('fotos/Wraith_01_Moving Forward_000.png')


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

    pantalla.blit(fondo,(0,-0))
    pantalla.blit(piso, (0, 820))
    pantalla.blit(enemigo_1, (0, 520))
    #se dubuja todos los elemntos y se hace
    pygame.display.update()
    reloj.tick(60)


