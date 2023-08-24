import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
	def __init__(self) -> None:
		super().__init__()

		player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
		player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
		self.player_walk = [player_walk_1, player_walk_2]
		self.player_index = 0
		self.player_jumb = pygame.image.load("graphics/Player/jump.png").convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(bottomleft = (100, 500))
		self.gravity = 0

	def get_rect(self):
		return self.rect

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
			self.gravity = -22

	def player_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 500: self.rect.bottom = 500

	def player_animation(self):
		if self.rect.bottom < 500: self.image = self.player_jumb
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk): self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.player_gravity()
		self.player_animation()

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
obstacle_rect_list = []

# Snail
snail_frame_1 = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/Snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_index = 0
snail_surface = snail_frames[snail_index]
snail_speed = 4

# Fly
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png")
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png")
fly_frames = [fly_frame_1, fly_frame_2]
fly_index = 0
fly_surface = fly_frames[fly_index]
fly_speed = 5

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

# Timer
obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_event, 1500)

# Snail Timer
snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)

# Fly Timer
fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 300)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_state == "over":
				game_state = "playing"
				game_time = int(pygame.time.get_ticks() / 1000)

		if game_state == "playing":
			if event.type == obstacle_event:
				if randint(0, 1):
					obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(1000, 1200), 500)))
				else:
					obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(1000, 1200), 250)))

			if event.type == snail_timer:
				if snail_index == 0: snail_index = 1
				else: snail_index = 0
				snail_surface = snail_frames[snail_index]

			if event.type == fly_timer:
				if fly_index == 0: fly_index = 1
				else: fly_index = 0
				fly_surface = fly_frames[fly_index]

	if game_state == "playing":
		screen.blit(sky_surface, (0, 0))
		screen.blit(ground_surface, (0, 500))
		# Score
		score = update_score()
		# Obstacles
		obstacle_rect_list = obstacle_movement(obstacle_rect_list)

		# Player
		player.draw(screen)
		player.update()

		# Game over
		# game_state = collisions(player.get_rect(), obstacle_rect_list)

	elif game_state == "over":
		obstacle_rect_list.clear()
		screen.fill("Black")

		game_over_text_surface = text_surface.render("Game Over!", False, "White")
		game_over_text_surface_rect = game_over_text_surface.get_rect(center = (500, 300))
		screen.blit(game_over_text_surface, game_over_text_surface_rect)

	pygame.display.update()
	clock.tick(60)