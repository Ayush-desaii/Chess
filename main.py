import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption(("chess"))
icon = pygame.image.load(("chess.png"))
pygame.display.set_icon(icon)

running = True
while running:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False