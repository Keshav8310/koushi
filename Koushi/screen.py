import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hacker Shield")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
DARK_BLUE = (0, 100, 200)
RED = (255, 51, 51)
GREEN = (0, 200, 0)

# Fonts
font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 28)

# Load images
background_img = pygame.image.load("HACKER SHIELD.png")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

logo_img = pygame.image.load("logo.png")
logo_img = pygame.transform.scale(logo_img, (200, 200))

# Load music
pygame.mixer.music.load("game screen.mpeg")
pygame.mixer.music.play(-1)
music_on = True

# Load icons for module selection
lock_icon = pygame.image.load("lock.png")
phishing_icon = pygame.image.load("phishing.png")
malware_icon = pygame.image.load("malware.png")
social_icon = pygame.image.load("social.png")
data_icon = pygame.image.load("data.png")
mobile_icon = pygame.image.load("mobile.png")
iot_icon = pygame.image.load("iot.png")
ransomware_icon = pygame.image.load("ransomware.png")

icons = [
    lock_icon, phishing_icon, malware_icon, social_icon,
    data_icon, mobile_icon, iot_icon, ransomware_icon
]

modules = [
    "Password Security", "Phishing Awareness", "Malware Protection",
    "Social Engineering Defense", "Data Privacy", "Mobile Security",
    "IoT Device Security", "Ransomware Awareness"
]

# Game state
screen_mode = "main_menu"

# ==== Button class ====
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = DARK_BLUE if self.rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        text_surf = small_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

# ==== Mini-games data structure ====
# Each module has 2 mini-games; each mini-game has 3 multiple-choice questions
mini_games = {
    "Password Security": [
        {
            "questions": [
                {"question": "What is a strong password?",
                 "options": ["123456", "Password", "P@ssw0rd!", "abcdef"],
                 "answer": 2},
                {"question": "How often change password?",
                 "options": ["Every day", "Every month", "Every year", "Never"],
                 "answer": 1},
                {"question": "Avoid passwords with?",
                 "options": ["Your name", "Random chars", "Numbers", "Symbols"],
                 "answer": 0}
            ],
            "theme": "🔒"
        },
        {
            "questions": [
                {"question": "Use of password manager?",
                 "options": ["Insecure", "Recommended", "Illegal", "Unnecessary"],
                 "answer": 1},
                {"question": "Password length should be?",
                 "options": ["4 digits", "8+ chars", "2 chars", "One word"],
                 "answer": 1},
                {"question": "Reusing passwords is?",
                 "options": ["Safe", "Risky", "Mandatory", "Unavoidable"],
                 "answer": 1}
            ],
            "theme": "🔒"
        }
    ],
    "Phishing Awareness": [
        {
            "questions": [
                {"question": "Phishing is?",
                 "options": ["Fishing", "Scam emails", "Virus", "Hack tool"],
                 "answer": 1},
                {"question": "Identify phishing emails?",
                 "options": ["Urgent request", "Generic greeting", "Suspicious link", "All of above"],
                 "answer": 3},
                {"question": "Action on phishing email?",
                 "options": ["Click link", "Delete", "Reply", "Forward"],
                 "answer": 1}
            ],
            "theme": "📧"
        },
        {
            "questions": [
                {"question": "Phishing tries to get your?",
                 "options": ["Password", "Phone", "Car", "None"],
                 "answer": 0},
                {"question": "Secure way to check link?",
                 "options": ["Click directly", "Hover and check URL", "Ignore", "Copy text"],
                 "answer": 1},
                {"question": "Use of antivirus helps against?",
                 "options": ["Phishing", "Malware", "Both", "None"],
                 "answer": 2}
            ],
            "theme": "📧"
        }
    ],
    "Malware Protection": [
        {
            "questions": [
                {"question": "Malware means?",
                 "options": ["Malicious software", "Hardware", "Secure app", "None"],
                 "answer": 0},
                {"question": "Protect malware by?",
                 "options": ["Use antivirus", "Ignore updates", "Download unknown", "None"],
                 "answer": 0},
                {"question": "Common malware type?",
                 "options": ["Virus", "Firewall", "Router", "None"],
                 "answer": 0}
            ],
            "theme": "🐛"
        },
        {
            "questions": [
                {"question": "Ransomware is?",
                 "options": ["Encrypts files", "Delete files", "Safe software", "None"],
                 "answer": 0},
                {"question": "Update software to?",
                 "options": ["Fix bugs", "Add malware", "Nothing", "None"],
                 "answer": 0},
                {"question": "Malware can spread via?",
                 "options": ["Email attachments", "Safe sites", "Legit software", "None"],
                 "answer": 0}
            ],
            "theme": "🐛"
        }
    ],
    "Social Engineering Defense": [
        {
            "questions": [
                {"question": "Social engineering is?",
                 "options": ["Manipulating people", "Software", "Hardware", "None"],
                 "answer": 0},
                {"question": "Defend by?",
                 "options": ["Be skeptical", "Share info freely", "Trust everyone", "Ignore"],
                 "answer": 0},
                {"question": "Common tactic?",
                 "options": ["Phishing", "Encryption", "Firewall", "None"],
                 "answer": 0}
            ],
            "theme": "🕵️‍♂️"
        },
        {
            "questions": [
                {"question": "Never share passwords with?",
                 "options": ["Official IT", "Friends", "Strangers", "Both 2 & 3"],
                 "answer": 3},
                {"question": "Verify caller by?",
                 "options": ["Hang up and call back", "Trust calls", "Share info", "Ignore entirely"],
                 "answer": 0},
                {"question": "Social engineering attacks rely on?",
                 "options": ["Human error", "Software bugs", "Hardware faults", "None"],
                 "answer": 0}
            ],
            "theme": "🕵️‍♂️"
        }
    ],
    "Data Privacy": [
        {
            "questions": [
                {"question": "Data privacy is?",
                 "options": ["Protect info", "Share info", "Ignore info", "None"],
                 "answer": 0},
                {"question": "Protect data by?",
                 "options": ["Strong passwords", "Share passwords", "Ignore privacy", "None"],
                 "answer": 0},
                {"question": "Data breach means?",
                 "options": ["Unauthorized access", "Secure data", "None", "Mistake"],
                 "answer": 0}
            ],
            "theme": "🔐"
        },
        {
            "questions": [
                {"question": "Encryption protects?",
                 "options": ["Data", "Hardware", "Software", "None"],
                 "answer": 0},
                {"question": "Privacy settings on apps?",
                 "options": ["Should be checked", "Ignored", "Disabled", "None"],
                 "answer": 0},
                {"question": "Public Wi-Fi is?",
                 "options": ["Risky for data", "Safe", "Encrypted", "None"],
                 "answer": 0}
            ],
            "theme": "🔐"
        }
    ],
    "Mobile Security": [
        {
            "questions": [
                {"question": "Common mobile threat?",
                 "options": ["Malware", "Strong passwords", "2FA", "None"],
                 "answer": 0},
                {"question": "Secure mobile by?",
                 "options": ["Lock screen", "Unknown app install", "Ignore updates", "None"],
                 "answer": 0},
                {"question": "Two-factor auth is?",
                 "options": ["Extra security", "Virus", "App", "None"],
                 "answer": 0}
            ],
            "theme": "📱"
        },
        {
            "questions": [
                {"question": "Public charging ports?",
                 "options": ["Risky", "Safe", "Recommended", "None"],
                 "answer": 0},
                {"question": "Lock phone using?",
                 "options": ["PIN/Pattern", "None", "Always unlocked", "None"],
                 "answer": 0},
                {"question": "Avoid?",
                 "options": ["Unknown Bluetooth", "Known devices", "Phone cases", "None"],
                 "answer": 0}
            ],
            "theme": "📱"
        }
    ],
    "IoT Device Security": [
        {
            "questions": [
                {"question": "IoT means?",
                 "options": ["Internet of Things", "Internet of Tech", "None", "None"],
                 "answer": 0},
                {"question": "Secure IoT by?",
                 "options": ["Change default password", "Keep default", "Ignore", "None"],
                 "answer": 0},
                {"question": "Unsecured IoT causes?",
                 "options": ["Hacks", "Safety", "Speed up", "None"],
                 "answer": 0}
            ],
            "theme": "📡"
        },
        {
            "questions": [
                {"question": "IoT devices connected via?",
                 "options": ["Internet", "Bluetooth", "Both", "None"],
                 "answer": 2},
                {"question": "Update IoT firmware?",
                 "options": ["Yes", "No", "Sometimes", "Never"],
                 "answer": 0},
                {"question": "Disable unused features?",
                 "options": ["Yes", "No", "Maybe", "None"],
                 "answer": 0}
            ],
            "theme": "📡"
        }
    ],
    "Ransomware Awareness": [
        {
            "questions": [
                {"question": "Ransomware is?",
                 "options": ["Encrypts files", "Deletes files", "Secures files", "None"],
                 "answer": 0},
                {"question": "Pay ransom?",
                 "options": ["Not recommended", "Recommended", "Mandatory", "None"],
                 "answer": 0},
                {"question": "Backup important data?",
                 "options": ["Yes", "No", "Maybe", "None"],
                 "answer": 0}
            ],
            "theme": "💰"
        },
        {
            "questions": [
                {"question": "Avoid ransomware by?",
                 "options": ["Not clicking unknown links", "Clicking all links", "Ignoring software updates", "None"],
                 "answer": 0},
                {"question": "Ransomware spreads via?",
                 "options": ["Email", "Phone call", "SMS", "None"],
                 "answer": 0},
                {"question": "Keep software updated?",
                 "options": ["Yes", "No", "Sometimes", "None"],
                 "answer": 0}
            ],
            "theme": "💰"
        }
    ]
}

# ==== Game tracking variables ====
selected_module_index = None
current_minigame_index = 0
current_question_index = 0
score_in_minigame = 0
passed_minigames = 0
total_minigames = sum(len(games) for games in mini_games.values())
total_score_possible = total_minigames * 3  # 3 questions per mini-game

# ==== Screen mode variables for mini-games ====
# screen_mode values used: "main_menu", "settings", "module_selection", "mini_game", "results"

# ==== Functions to start mini-games ====
def start_module_minigames(module_idx):
    global screen_mode, selected_module_index, current_minigame_index
    selected_module_index = module_idx
    current_minigame_index = 0
    start_minigame()

def start_minigame():
    global screen_mode, current_question_index, score_in_minigame
    current_question_index = 0
    score_in_minigame = 0
    screen_mode = "mini_game"

def show_intro_message():
    screen.fill(BLACK)
    message = small_font.render("If you want to be secure from cyber threats play this wonderful game", True, WHITE)
    screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2))
    pygame.display.flip()
    time.sleep(3)
    global screen_mode
    screen_mode = "module_selection"

def go_back_to_main():
    global screen_mode
    screen_mode = "main_menu"

def quit_game():
    pygame.quit()
    sys.exit()

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

# ==== Buttons ====
main_buttons = [
    Button("Start", 310, 320, 180, 50, lambda: show_intro_message()),
    Button("Settings", 310, 390, 180, 50, lambda: set_screen_mode("settings")),
    Button("Quit", 310, 460, 180, 50, quit_game)
]

settings_buttons = [
    Button("Toggle Music", 310, 320, 180, 50, toggle_music),
    Button("Back", 310, 390, 180, 50, go_back_to_main)
]

def set_screen_mode(mode):
    global screen_mode
    screen_mode = mode

# ==== Drawing module buttons ====
scroll_offset = 0
scroll_speed = 20
max_scroll = 0

def draw_module_buttons():
    global max_scroll
    screen.fill(BLACK)
    title = font.render("Module Selection", True, WHITE)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 40))

    button_width = 600
    button_height = 60
    spacing = 20
    start_y = 120

    total_height = len(modules) * (button_height + spacing)
    max_scroll = max(0, total_height - (screen_height - start_y - 40))

    mouse_pos = pygame.mouse.get_pos()
    clicked_module_idx = None

    for i, module in enumerate(modules):
        x = screen_width // 2 - button_width // 2
        y = start_y + i * (button_height + spacing) - scroll_offset
        if -button_height < y < screen_height:  # Only draw if on screen
            rect = pygame.Rect(x, y, button_width, button_height)
            pygame.draw.rect(screen, RED, rect, border_radius=15)
            icon = pygame.transform.scale(icons[i], (40, 40))
            screen.blit(icon, (x + 20, y + 10))
            text_surface = small_font.render(module, True, WHITE)
            screen.blit(text_surface, (x + 80, y + 15))
            if rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    clicked_module_idx = i

    if clicked_module_idx is not None:
        start_module_minigames(clicked_module_idx)

# ==== Mini-game drawing and logic ====

def draw_text_multi_line(text, x, y, font, color, surface, line_spacing=5):
    words = text.split(' ')
    line = ""
    line_height = font.size("Tg")[1]
    lines = []

    # Create lines respecting the width limit (here 720)
    max_width = 720
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] > max_width:
            lines.append(line)
            line = word + " "
        else:
            line = test_line
    lines.append(line)

    for i, l in enumerate(lines):
        text_surface = font.render(l, True, color)
        surface.blit(text_surface, (x, y + i * (line_height + line_spacing)))

def draw_minigame():
    global screen_mode, current_question_index, score_in_minigame, current_minigame_index, selected_module_index, passed_minigames
    screen.fill(BLACK)

    module_name = modules[selected_module_index]
    minigame = mini_games[module_name][current_minigame_index]
    theme_icon = minigame["theme"]
    question_data = minigame["questions"][current_question_index]

    # Draw theme icon large
    theme_font = pygame.font.SysFont("Arial", 100)
    theme_surface = theme_font.render(theme_icon, True, BLUE)
    screen.blit(theme_surface, (screen_width // 2 - theme_surface.get_width() // 2, 20))

    # Draw module and mini-game info
    module_text = small_font.render(f"Module: {module_name}", True, WHITE)
    screen.blit(module_text, (20, 140))
    minigame_text = small_font.render(f"Mini-game {current_minigame_index + 1} of {len(mini_games[module_name])}", True, WHITE)
    screen.blit(minigame_text, (20, 170))

    # Draw question text (multi-line if long)
    draw_text_multi_line(question_data["question"], 40, 220, font, WHITE, screen)

    # Draw options as buttons
    option_rects = []
    base_y = 320
    button_w = 700
    button_h = 50
    spacing = 20
    for i, option in enumerate(question_data["options"]):
        rect = pygame.Rect(50, base_y + i * (button_h + spacing), button_w, button_h)
        pygame.draw.rect(screen, DARK_BLUE, rect, border_radius=12)
        option_text = small_font.render(f"{i+1}. {option}", True, WHITE)
        text_rect = option_text.get_rect(center=rect.center)
        screen.blit(option_text, text_rect)
        option_rects.append(rect)

    pygame.display.update()
    return option_rects, question_data["answer"]

# ==== Show feedback screen ====
def show_feedback(correct):
    screen.fill(BLACK)
    feedback_text = "Correct!" if correct else "Wrong!"
    color = GREEN if correct else RED
    text_surface = font.render(feedback_text, True, color)
    screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, screen_height // 2))
    pygame.display.update()
    pygame.time.wait(1500)

# ==== Show final results ====
def show_results():
    screen.fill(BLACK)
    clear_text = f"Mini-Games Passed: {passed_minigames} / {total_minigames}"
    percentage = (passed_minigames / total_minigames) * 100 if total_minigames > 0 else 0
    percentage_text = f"Cyber Safety Percentage: {percentage:.2f}%"
    clear_surf = font.render(clear_text, True, WHITE)
    perc_surf = font.render(percentage_text, True, WHITE)
    screen.blit(clear_surf, (screen_width // 2 - clear_surf.get_width() // 2, screen_height // 2 - 40))
    screen.blit(perc_surf, (screen_width // 2 - perc_surf.get_width() // 2, screen_height // 2 + 20))

    info_text = small_font.render("Press any key to go back to Module Selection", True, WHITE)
    screen.blit(info_text, (screen_width // 2 - info_text.get_width() // 2, screen_height - 80))
    pygame.display.update()

# ==== Main Menu and other functions ====
def show_intro_message():
    screen.fill(BLACK)
    message = small_font.render("If you want to be secure from cyber threats play this wonderful game", True, WHITE)
    screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2))
    pygame.display.flip()
    time.sleep(3)
    global screen_mode
    screen_mode = "module_selection"

def set_screen_mode(mode):
    global screen_mode
    screen_mode = mode

def go_back_to_main():
    global screen_mode
    screen_mode = "main_menu"

def quit_game():
    pygame.quit()
    sys.exit()

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

main_buttons = [
    Button("Start", 310, 320, 180, 50, show_intro_message),
    Button("Settings", 310, 390, 180, 50, lambda: set_screen_mode("settings")),
    Button("Quit", 310, 460, 180, 50, quit_game)
]

settings_buttons = [
    Button("Toggle Music", 310, 320, 180, 50, toggle_music),
    Button("Back", 310, 390, 180, 50, go_back_to_main)
]

# ==== Main Game Loop ====

scroll_offset = 0

running = True
waiting_for_feedback = False
waiting_for_results = False

while running:
    option_rects = []
    correct_answer = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if screen_mode == "main_menu":
            for button in main_buttons:
                button.check_click(event)

        elif screen_mode == "settings":
            for button in settings_buttons:
                button.check_click(event)

        elif screen_mode == "module_selection":
            # Scroll with keys or mouse wheel
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + 20, max(0, len(modules) * 80 - (screen_height - 160)))
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - 20, 0)
            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset = max(0, min(scroll_offset - event.y * 20, max(0, len(modules) * 80 - (screen_height - 160))))

            # Mouse click detection handled in draw_module_buttons

        elif screen_mode == "mini_game":
            if not waiting_for_feedback:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for idx, rect in enumerate(option_rects):
                        if rect.collidepoint(mouse_pos):
                            # Check answer
                            if idx == correct_answer:
                                score_in_minigame += 1
                                show_feedback(True)
                            else:
                                show_feedback(False)

                            # Next question or mini-game
                            current_question_index += 1
                            if current_question_index >= 3:
                                # Mini-game finished
                                if score_in_minigame >= 2:
                                    passed_minigames += 1
                                current_minigame_index += 1
                                if current_minigame_index >= len(mini_games[modules[selected_module_index]]):
                                    # All mini-games in this module done
                                    # Check if all modules done
                                    # If all modules done, show results
                                    modules_done = sum(len(mini_games[m]) for m in mini_games)
                                    if passed_minigames >= modules_done:
                                        waiting_for_results = True
                                        screen_mode = "results"
                                    else:
                                        screen_mode = "module_selection"
                                else:
                                    # Next mini-game in this module
                                    current_question_index = 0
                                    score_in_minigame = 0
                                break

            # Wait for any key to continue from results screen
        elif screen_mode == "results":
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                screen_mode = "module_selection"

    # === Drawing ===
    if screen_mode == "main_menu":
        screen.blit(background_img, (0, 0))
        screen.blit(logo_img, (screen_width // 2 - 100, 50))
        title_surface = font.render("HACKER SHIELD", True, WHITE)
        screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 270))
        for button in main_buttons:
            button.draw(screen)

    elif screen_mode == "settings":
        screen.blit(background_img, (0, 0))
        settings_title = font.render("Settings", True, WHITE)
        screen.blit(settings_title, (screen_width // 2 - settings_title.get_width() // 2, 100))
        music_status = "Music: ON" if music_on else "Music: OFF"
        music_status_text = small_font.render(music_status, True, WHITE)
        screen.blit(music_status_text, (screen_width // 2 - music_status_text.get_width() // 2, 270))
        for button in settings_buttons:
            button.draw(screen)

    elif screen_mode == "module_selection":
        screen.fill(BLACK)
        title = font.render("Module Selection", True, WHITE)
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 40))

        button_width = 600
        button_height = 60
        spacing = 20
        start_y = 120

        total_height = len(modules) * (button_height + spacing)
        max_scroll = max(0, total_height - (screen_height - start_y - 40))

        mouse_pos = pygame.mouse.get_pos()

        for i, module in enumerate(modules):
            x = screen_width // 2 - button_width // 2
            y = start_y + i * (button_height + spacing) - scroll_offset
            if -button_height < y < screen_height:  # Only draw if on screen
                rect = pygame.Rect(x, y, button_width, button_height)
                pygame.draw.rect(screen, RED, rect, border_radius=15)
                icon = pygame.transform.scale(icons[i], (40, 40))
                screen.blit(icon, (x + 20, y + 10))
                text_surface = small_font.render(module, True, WHITE)
                screen.blit(text_surface, (x + 80, y + 15))
                # Check click is handled earlier by start_module_minigames via mouse clicks

    elif screen_mode == "mini_game":
        option_rects, correct_answer = draw_minigame()

    elif screen_mode == "results":
        show_results()

    pygame.display.update()

pygame.quit()
sys.exit()
