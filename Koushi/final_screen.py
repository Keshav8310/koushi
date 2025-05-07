
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cybersecurity Awareness - Final Report")
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def show_final_screen(games_cleared, total_games):
    percentage = int((games_cleared / total_games) * 100)
    screen.fill((30, 30, 60))
    draw_text("Final Cyber Safety Report", font, (255, 255, 255), screen, 400, 100)
    draw_text(f"Games Cleared: {games_cleared}/{total_games}", small_font, (200, 255, 200), screen, 400, 250)
    draw_text(f"Cyber Safety Percentage: {percentage}%", small_font, (200, 200, 255), screen, 400, 300)
    draw_text("Thanks for playing!", small_font, (255, 255, 150), screen, 400, 400)
    draw_text("Press ESC to exit", small_font, (180, 180, 180), screen, 400, 500)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

# Example usage:
# show_final_screen(14, 16)  # Call this when the user completes the game
