import pygame
from sys import exit
from random import randint

def update_score() -> int:
	current_time = int(pygame.time.get_ticks() / 1000) - game_time
	score_surface = text_surface.render(f"Score: {current_time}", False, "#5A5A5A")
	score_rect = score_surface.get_rect(center = (500, 100))
	screen.blit(score_surface, score_rect)

	return current_time

def obstacle_movement(obstacle_rect_list) -> list:
	if obstacle_rect_list:
		for obstacle_rect in obstacle_rect_list:
			if obstacle_rect.bottom == 500:
				obstacle_rect.x -= snail_speed
				screen.blit(snail_surface, obstacle_rect)
			else:
				obstacle_rect.x -= fly_speed
				screen.blit(fly_surface, obstacle_rect)

		obstacle_rect_list = [obstacle_rect for obstacle_rect in obstacle_rect_list if obstacle_rect.x > -100]
		return obstacle_rect_list
	else: return []

def collisions(player, obstacles) -> str:
	if obstacles:
		for obstacle in obstacles:
			if player.colliderect(obstacle): return "over"
	return "playing"

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Hello pygame")
clock = pygame.time.Clock()
text_surface = pygame.font.Font("font/Pixeltype.ttf", 50)
msg_text_surface = pygame.font.Font("font/Pixeltype.ttf", 30)
game_state = "playing"
game_time = 0
score = 0

# Sky
sky_surface = pygame.image.load("graphics/Sky.png").convert()
sky_surface = pygame.transform.scale(sky_surface, (1000, 600))

# Ground
ground_surface = pygame.image.load("graphics/Ground.png").convert()
ground_surface = pygame.transform.scale(ground_surface, (1000, 100))

# Obstacles
snail_surface = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
fly_surface = pygame.image.load("graphics/Fly/Fly1.png")
snail_speed = 4
fly_speed = 5

obstacle_rect_list = []

# Player
player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(bottomleft = (100, 500))
player_gravity = 0
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (500, 300))

# Timer
obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_event, 1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_state == "playing" and player_rect.bottom >= 500:
				player_gravity = -22
			elif event.key == pygame.K_SPACE and game_state == "over":
				game_state = "playing"
				game_time = int(pygame.time.get_ticks() / 1000)

		if event.type == obstacle_event:
			if randint(0, 1):
				obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(1000, 1200), 500)))
			else:
				obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(1000, 1200), 250)))

	if game_state == "playing":
		screen.blit(sky_surface, (0, 0))
		screen.blit(ground_surface, (0, 500))
		# Score
		score = update_score()
		# Obstacles
		obstacle_rect_list = obstacle_movement(obstacle_rect_list)

		# Player
		player_gravity += 1
		player_rect.y += player_gravity
		if player_rect.bottom >= 500: player_rect.bottom = 500
		screen.blit(player_surface, player_rect)

		# Game over
		game_state = collisions(player_rect, obstacle_rect_list)

	elif game_state == "over":
		obstacle_rect_list.clear()
		player_rect.bottomleft = (100, 500)
		player_gravity = 0

		screen.fill((94, 129, 162))
		screen.blit(player_stand, player_stand_rect)

		game_over_text_surface = text_surface.render("PyGame", False, "White")
		game_over_text_surface_rect = game_over_text_surface.get_rect(center = (500, 100))
		# Message
		game_msg = msg_text_surface.render("Press Space to start", False, "White")
		game_msg_rect = game_msg.get_rect(center = (500, 135))
		# Score
		game_score = msg_text_surface.render(f"Your Score: {score}", False, "White")
		game_score_rect = game_score.get_rect(center = (500, 135))

		screen.blit(game_over_text_surface, game_over_text_surface_rect)
		if score: screen.blit(game_score, game_score_rect)
		else: screen.blit(game_msg, game_msg_rect)

	pygame.display.update()
	clock.tick(60)