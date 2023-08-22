import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Hello pygame")
clock = pygame.time.Clock()
landing_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surface = pygame.image.load("graphics/Sky.png").convert()
sky_surface = pygame.transform.scale(sky_surface, (1000, 600))

ground_surface = pygame.image.load("graphics/Ground.png").convert()
ground_surface = pygame.transform.scale(ground_surface, (1000, 100))

landing_text = landing_font.render("My Game", True, "Black")

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (1100, 500))
snail_speed = 4

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	screen.blit(sky_surface, (0, 0))
	screen.blit(ground_surface, (0, 500))
	screen.blit(landing_text, (450, 100))

	if snail_rect.right < 0:
		snail_rect.left = 1100
	else:
		snail_rect.left -= snail_speed
	screen.blit(snail_surface, snail_rect)

	pygame.display.update()
	clock.tick(60)