import pygame
import math

pygame.init()
clock = pygame.time.Clock()
fps = 60
width = 1270
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Endless Scroll")
background = pygame.image.load("images/background.png").convert()
background_width = background.get_width()
background_rect = background.get_rect()
scroll = 0
tiles = math.ceil(width  / background_width) + 1

run = True
while run:
  clock.tick(fps)
  for i in range(0, tiles):
    screen.blit(background, (i * background_width + scroll, 0))
    background_rect.x = i * background_width + scroll
    pygame.draw.rect(screen, 		(0,0,0), background_rect, 1)
  scroll -= 5
  if abs(scroll) > background_width:
    scroll = 0
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  pygame.display.update()

pygame.quit()