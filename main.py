import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Hello pygame")
clock = pygame.time.Clock()

sky_surface = pygame.image.load("graphics/Sky.png").convert()
sky_surface = pygame.transform.scale(sky_surface, (1000, 600))

ground_surface = pygame.image.load("graphics/Ground.png").convert()
ground_surface = pygame.transform.scale(ground_surface, (1000, 100))

snail_surface = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (1100, 500))
snail_speed = 4

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(bottomleft = (100, 500))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if player_rect.collidepoint(event.pos): print ("Collide")

	screen.blit(sky_surface, (0, 0))
	screen.blit(ground_surface, (0, 500))

	snail_rect.x -= snail_speed
	if snail_rect.right < 0:
		snail_rect.left = 1100

	screen.blit(snail_surface, snail_rect)
	screen.blit(player_surface, player_rect)

	pygame.display.update()
	clock.tick(60)