import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60

# Initialize Pygame and create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piano Tile Game")
clock = pygame.time.Clock()

# Load background image
background_image = pygame.image.load("bgimg2.png")  # Replace with the path to your background image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load player image
player_image = pygame.image.load("anastasia1.png")  # Replace with the path to your player image
player_image = pygame.transform.scale(player_image, (50, 70))  # Resize the player image if needed

# Load tile images
tile_images = [
    pygame.image.load("tile1.png"),    # Replace with the path to your red tile image
    pygame.image.load("tile2.png"),  # Replace with the path to your green tile image
    pygame.image.load("tile3.png"),   # Replace with the path to your blue tile image
    pygame.image.load("tile5.png"), # Replace with the path to your yellow tile image
]

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()
        self.image = player_image  # Use the loaded player image
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 3
        self.rect.y = HEIGHT - self.rect.height  # Adjust the y-coordinate based on the image size
        self.speed = 10
        self.is_colliding = False

# Tile
class Tile(pygame.sprite.Sprite):
    def __init__(self, screen_width, image, voice,initial_x, initial_y):
        super().__init__()
        self.image = pygame.transform.scale(image, (50, 150))  # Resize the tile image if needed
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y
        self.speed = 2.0
        self.voice = voice  # Reference to the additional music

    def get_scaling_factor(self, player):
        # Calculate the scaling factor based on the overlap of player and tile
        overlap = max(0, min(player.rect.bottom, self.rect.bottom) - max(player.rect.top, self.rect.top))
        scaling_factor = overlap / self.rect.height
        return scaling_factor

    def update(self):
        self.rect.y += self.speed  # Move the tile downward

def starting_page():
    start_image1 = pygame.image.load("Fimg1.png")  # Replace with the path to your starting image 1
    start_image1 = pygame.transform.scale(start_image1, (WIDTH, HEIGHT))

    start_image2 = pygame.image.load("Fimg2.png")  # Replace with the path to your starting image 2
    start_image2 = pygame.transform.scale(start_image2, (WIDTH, HEIGHT))

    nkl_image = pygame.image.load("NKL.png")  # Replace with the path to your NKL image
    nkl_image = pygame.transform.scale(nkl_image, (93, 100))  # Adjust the size as needed

    nkl_rect = nkl_image.get_rect()
    nkl_rect.topleft = (10, HEIGHT - 110)

    screen.blit(start_image1, (0, 0))  # Draw the starting image 1
    screen.blit(nkl_image, nkl_rect.topleft)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

        # Check if NKL is in the middle of the screen
        if WIDTH // 3 < nkl_rect.centerx < 2 * WIDTH // 3:
            screen.blit(start_image2, (0, 0))  # Draw the starting image 2
        else:
            screen.blit(start_image1, (0, 0))  # Draw the starting image 1

        screen.blit(nkl_image, nkl_rect.topleft)
        pygame.display.flip()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
            if nkl_rect.collidepoint(mouse_x, mouse_y):
                nkl_rect.x = mouse_x - nkl_rect.width // 2
                nkl_rect.y = mouse_y - nkl_rect.height // 2

    return nkl_rect

    
def main():
    pygame.init()
    # Show starting page and get NKL rect
    nkl_rect = starting_page()
    
    # Create player
    player = Player(WIDTH)

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    tiles = pygame.sprite.Group()
    all_sprites.add(player)

    # Sequence of tiles (0 = Red, 1 = Green, 2 = Blue, 3 = Yellow)
    tile_sequence = [0, 1, 2, 3, 1,3,2,0,3,2,3,2,1,0,2,1,2,3,0,1,1,2,0,3,2,1,2,1,0,3,1,2,1,0,2,3,1,2,0,3,2,0,1,3,2,1,3,2,3,1,0,2,1,0,1,2,3,2,0,1,2,0,1,2,0,3,1,0]  # Adjust the sequence as needed
    current_tile_index = 0
    tile_spawn_timer = 0

    # Music
    voice = pygame.mixer.Sound('Voice.mp3')
    voice.set_volume(0.0)
    voice.play()
    
    # Initial positions for each tile
    tile_positions = [
        (WIDTH // 6+5, -150),      # Tile 1 position
        (WIDTH // 2 - 55, -150),  # Tile 2 position
        (WIDTH // 2 + 10, -150),  # Tile 3 position
        (WIDTH * 4 // 6+10, -150),   # Tile 5 position
    ]

    # Counter variable
    collision_count = 0
    total_tiles_spawned = 0

    # Score font
    font = pygame.font.Font(None, 36)  # You can customize the font and size
    
    # Player image change threshold
    image_change_threshold = 265
    
    # Background images
    background_images = [
        pygame.image.load("bgimg2.png"),  # Original background image
        pygame.image.load("bgimg3.png"),  # New background image
    ]
    
    # Current background index
    current_background_index = 0

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
        if tile_spawn_timer >= 20:  # Adjust the delay between tile spawns
            tile_image = tile_images[tile_sequence[current_tile_index]]
            initial_x, initial_y = tile_positions[tile_sequence[current_tile_index]]
            new_tile = Tile(WIDTH, tile_image, voice, initial_x, initial_y)
            
            total_tiles_spawned += 1

            if total_tiles_spawned == image_change_threshold:
                current_background_index = 1  # Change the background image
            elif total_tiles_spawned > image_change_threshold:
                player.image = pygame.image.load("anastasia2.png")  # Replace with the path to the new player image
                player.image = pygame.transform.scale(player.image, (50, 70))  # Resize the new player image if needed



            overlap = pygame.sprite.spritecollideany(new_tile, tiles)
            if not overlap:
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
        for tile in tiles:
            if pygame.sprite.collide_rect(player, tile):
                player.is_colliding = True
                scaling_factor = tile.get_scaling_factor(player)
                voice.set_volume(min(1.0, scaling_factor))  # Adjust the volume based on the scaling factor
                if not tile.is_colliding:  # Increment the counter only once per collision
                    collision_count += 1
                    tile.is_colliding = True
            else:
                player.is_colliding = False
                tile.is_colliding = False

        # Draw everything
        screen.blit(background_images[current_background_index], (0, 0))  # Draw the background image
        
        # Draw the score
        score_text = font.render("Score: {}".format(collision_count), True, (255, 255, 255))  # White text
        screen.blit(score_text, (10, 10))  # Adjust the position as needed

        all_sprites.draw(screen)
        tiles.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
