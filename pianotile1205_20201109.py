import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize Pygame and create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piano Tile Game")
clock = pygame.time.Clock()

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound files
#hit_sound = pygame.mixer.Sound('hit_sound.wav')  
pygame.mixer.music.load('voice.mp3')  #background music

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()
        self.size = 50
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 3
        self.rect.y = HEIGHT - self.size
        self.speed = 10
        self.is_colliding = False  # New variable to track collision status

# Tile
class Tile(pygame.sprite.Sprite):
    def __init__(self, screen_width, color):
        super().__init__()
        self.size = 50
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(screen_width // 6, screen_width * 5 // 6 - self.size)
        self.rect.y = random.randint(-self.size * 2, -self.size)  # Adjusted initial y-coordinate
        self.speed = 5

    def update(self):
        self.rect.y += self.speed  # Move the tile downward

def main():
    pygame.mixer.music.set_volume(1.0)  # Set background music volume to 0

    # Create player
    player = Player(WIDTH)

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    tiles = pygame.sprite.Group()
    all_sprites.add(player)

    # Sequence of tiles (0 = Red, 1 = Green, 2 = Blue, 3 = Yellow)
    tile_sequence = [0, 1, 2, 3, 0, 1, 2, 3]  # Adjust the sequence as needed
    current_tile_index = 0
    tile_spawn_timer = 0
    tile_spawn_delay = 60  # Adjust the delay between tile spawns

    #sound_playing = False

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.rect.left > WIDTH // 6:
            player.rect.x -= player.speed
        if keys[pygame.K_RIGHT] and player.rect.right < WIDTH * 5 // 6:
            player.rect.x += player.speed

        # Update timer and spawn tiles based on the sequence
        tile_spawn_timer += 1
        if tile_spawn_timer >= tile_spawn_delay:
            color = [RED, GREEN, BLUE, YELLOW][tile_sequence[current_tile_index]]
            new_tile = Tile(WIDTH, color)
            tiles.add(new_tile)
            all_sprites.add(new_tile)
            current_tile_index = (current_tile_index + 1) % len(tile_sequence)
            tile_spawn_timer = 0

        # Update sprites
        all_sprites.update()
        tiles.update()
        
        # Remove tiles that are out of the screen
        tiles = pygame.sprite.Group([tile for tile in tiles if tile.rect.top < HEIGHT])


        # Check for collisions with the player
        collisions = pygame.sprite.spritecollide(player, tiles, True) #kill block when collide
        
        for tile in tiles:
            if pygame.sprite.collide_rect(player, tile):
                player.is_colliding = True
                pygame.mixer.music.set_volume(0.0)  # Set background music volume to 1
                
            else:
                player.is_colliding = False

        
        # Draw everything
        screen.fill(WHITE)
        all_sprites.draw(screen)
        tiles.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    pygame.mixer.music.stop()  # Stop the background music when the game ends
    main()