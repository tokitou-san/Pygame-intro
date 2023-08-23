import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Hello pygame")
clock = pygame.time.Clock()
text_surface = pygame.font.Font("font/Pixeltype.ttf", 50)
game_state = "playing"
game_time = 0

# Sky
sky_surface = pygame.image.load("graphics/Sky.png").convert()
sky_surface = pygame.transform.scale(sky_surface, (1000, 600))

# Ground
ground_surface = pygame.image.load("graphics/Ground.png").convert()
ground_surface = pygame.transform.scale(ground_surface, (1000, 100))

# Snail
snail_surface = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (1100, 500))
snail_speed = 4

# Player
player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(bottomleft = (100, 500))
player_gravity = 0

def update_score():
	current_time = int(pygame.time.get_ticks() / 1000) - game_time
	score_surface = text_surface.render(f"Score: {current_time}", False, "#5A5A5A")
	score_rect = score_surface.get_rect(center = (500, 100))
	screen.blit(score_surface, score_rect)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_state == "playing" and player_rect.bottom >= 500:
				player_gravity = -20
			elif event.key == pygame.K_SPACE and game_state == "over":
				game_state = "playing"
				snail_rect.left = 1000
				game_time = int(pygame.time.get_ticks() / 1000)

	if game_state == "playing":
		screen.blit(sky_surface, (0, 0))
		screen.blit(ground_surface, (0, 500))
		# Score
		update_score()

		# Snail
		snail_rect.x -= snail_speed
		if snail_rect.right < 0: snail_rect.left = 1100
		screen.blit(snail_surface, snail_rect)

		# Player
		player_gravity += 1
		player_rect.y += player_gravity
		if player_rect.bottom >= 500: player_rect.bottom = 500
		screen.blit(player_surface, player_rect)

		if player_rect.colliderect(snail_rect):
			game_state = "over"

	elif game_state == "over":
		screen.fill("Black")

		game_over_text_surface = text_surface.render("Game Over!", False, "White")
		game_over_text_surface_rect = game_over_text_surface.get_rect(center = (500, 300))
		screen.blit(game_over_text_surface, game_over_text_surface_rect)

	pygame.display.update()
	clock.tick(60)