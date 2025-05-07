
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cybersecurity Awareness Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 48)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, LIGHT_BLUE, self.rect)
        pygame.draw.rect(surface, DARK_BLUE, self.rect, 2)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Question bank (Password Security module only for demo)
mini_games = {
    "Password Security": [
        {
            "title": "Password Strength Tester",
            "theme": "🔒",
            "questions": [
                {"q": "Which password is strongest?", "options": ["123456", "qwerty", "P@ssw0rd!23", "abcdef"], "answer": "P@ssw0rd!23"},
                {"q": "How often should you change your password?", "options": ["Never", "Every 6 months", "Only when hacked", "Once a year"], "answer": "Every 6 months"},
                {"q": "What should you avoid in passwords?", "options": ["Symbols", "Personal info", "Numbers", "Uppercase letters"], "answer": "Personal info"}
            ]
        },
        {
            "title": "Password Puzzle",
            "theme": "🧩",
            "questions": [
                {"q": "What is 2FA?", "options": ["Second password", "Two Facebook Accounts", "Two-Factor Authentication", "Two-step App"], "answer": "Two-Factor Authentication"},
                {"q": "What makes a password weak?", "options": ["Length", "Complexity", "Common phrases", "Randomness"], "answer": "Common phrases"},
                {"q": "Which is safest?", "options": ["MyPetName", "John123", "Xy!92@Kp", "Password"], "answer": "Xy!92@Kp"}
            ]
        }
    ]
}

# Game functions
def draw_text_centered(text, y, surface, size=36):
    font_obj = pygame.font.Font(None, size)
    text_surf = font_obj.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(screen_width // 2, y))
    surface.blit(text_surf, text_rect)

def run_mini_game(game_data):
    questions = game_data["questions"]
    correct = 0
    for q in questions:
        answer = ask_question(q["q"], q["options"])
        if answer == q["answer"]:
            correct += 1
    return correct

def ask_question(question, options):
    running = True
    while running:
        screen.fill(WHITE)
        draw_text_centered(question, 100, screen, 40)
        for i, opt in enumerate(options):
            opt_rect = pygame.Rect(200, 200 + i*70, 400, 50)
            pygame.draw.rect(screen, LIGHT_BLUE, opt_rect)
            pygame.draw.rect(screen, DARK_BLUE, opt_rect, 2)
            opt_text = font.render(opt, True, BLACK)
            screen.blit(opt_text, (opt_rect.x + 10, opt_rect.y + 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, opt in enumerate(options):
                    rect = pygame.Rect(200, 200 + i*70, 400, 50)
                    if rect.collidepoint(event.pos):
                        return opt

def run_module(module_name):
    total_correct = 0
    for game in mini_games[module_name]:
        total_correct += run_mini_game(game)
    return total_correct

def final_screen(score, total_questions):
    running = True
    percentage = int((score / total_questions) * 100)
    while running:
        screen.fill(WHITE)
        draw_text_centered("Game Completed!", 100, screen, 50)
        draw_text_centered(f"Your Cyber Safety Score: {percentage}%", 200, screen, 40)
        draw_text_centered(f"Correct Answers: {score}/{total_questions}", 280, screen, 36)
        draw_text_centered("Press any key to exit...", 500, screen, 30)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
    pygame.quit()
    sys.exit()

def main():
    module_buttons = []
    spacing = 10
    btn_w, btn_h = 350, 60
    modules = list(mini_games.keys())
    for i, module in enumerate(modules):
        x = (screen_width - btn_w) // 2
        y = 150 + i * (btn_h + spacing)
        module_buttons.append(Button(x, y, btn_w, btn_h, module, lambda m=module: m))

    selected_modules = []
    total_score = 0

    while True:
        screen.fill(WHITE)
        draw_text_centered("Select a Module to Play", 80, screen, 48)
        for btn in module_buttons:
            if btn.text not in selected_modules:
                btn.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in module_buttons:
                    if btn.is_clicked(event.pos) and btn.text not in selected_modules:
                        score = run_module(btn.text)
                        total_score += score
                        selected_modules.append(btn.text)
                        if len(selected_modules) == len(modules):
                            final_screen(total_score, len(modules) * 6)

if __name__ == "__main__":
    main()
