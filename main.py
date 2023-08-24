import pygame
from sys import exit
from random import randint, choice

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

	def get_rect(self) -> pygame.Rect:
		return self.rect

	def player_input(self) -> None:
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 500: self.gravity = -22

	def player_gravity(self) -> None:
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 500: self.rect.bottom = 500

	def player_animation(self) -> None:
		if self.rect.bottom < 500: self.image = self.player_jumb
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk): self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self) -> None:
		self.player_input()
		self.player_gravity()
		self.player_animation()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type: str) -> None:
		super().__init__()

		if type == "snail":
			snail_frame_1 = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
			snail_frame_2 = pygame.image.load("graphics/Snail/snail2.png").convert_alpha()
			self.frames = [snail_frame_1, snail_frame_2]
			y_pos = 500
			self.speed = 5
		else:
			fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png")
			fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png")
			self.frames = [fly_frame_1, fly_frame_2]
			y_pos = 400
			self.speed = 6

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(1000, 1100), y_pos))

	def obstacle_animation(self) -> None:
		self.animation_index += 0.1
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def obstacle_movement(self) -> None:
		self.rect.x -= self.speed

	def update(self) -> None:
		self.obstacle_animation()
		self.obstacle_movement()
		self.destroy()

	def destroy(self) -> None:
		if self.rect.x < -100: self.kill()

def update_score() -> int:
	current_time = int(pygame.time.get_ticks() / 1000) - game_time
	score_surface = text_surface.render(f"Score: {current_time}", False, "#5A5A5A")
	score_rect = score_surface.get_rect(center = (500, 100))
	screen.blit(score_surface, score_rect)

	return current_time

def collision_sprite() -> str:
	if pygame.sprite.spritecollide(player.sprite, obstacles, False):
		obstacles.empty()
		return "over"
	else: return "playing"

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

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()

# Timer
obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_event, 1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_state == "over":
				game_state = "playing"
				game_time = int(pygame.time.get_ticks() / 1000)

		if event.type == obstacle_event and game_state == "playing":
			obstacles.add(Obstacle(choice(["fly", "snail", "snail"])))

	if game_state == "playing":
		screen.blit(sky_surface, (0, 0))
		screen.blit(ground_surface, (0, 500))
		# Score
		score = update_score()

		# Player
		player.draw(screen)
		player.update()

		# Obstacles
		obstacles.draw(screen)
		obstacles.update()

		# Game over
		game_state = collision_sprite()

	elif game_state == "over":
		screen.fill("Black")

		game_over_text_surface = text_surface.render("Game Over!", False, "White")
		game_over_text_surface_rect = game_over_text_surface.get_rect(center = (500, 300))
		screen.blit(game_over_text_surface, game_over_text_surface_rect)

	pygame.display.update()
	clock.tick(60)