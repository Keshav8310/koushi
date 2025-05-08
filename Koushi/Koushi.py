import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hacker Shield")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
DARK_BLUE = (0, 100, 200)
LIGHT_BLUE = (0, 100, 150)
RED = (255, 51, 51)
GREEN = (0, 200, 0)

font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 28)

background_img = pygame.image.load("HACKER SHIELD.png")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

logo_img = pygame.image.load("logo.png")
logo_img = pygame.transform.scale(logo_img, (200, 200))

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

# Utility
def draw_text_centered(text, y, surface, size=36):
    font_obj = pygame.font.Font(None, size)
    text_surf = font_obj.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(screen_width // 2, y))
    surface.blit(text_surf, text_rect)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        color = BLUE if is_hovered else DARK_BLUE
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        text_surf = font.render(self.text, True, BLACK if is_hovered else WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Question system (minimal sample for demo)
mini_games = {
  "Password Security": [
    {
      "title": "Password Strength Tester",
      "theme": "🔒",
      "questions": [
        {
          "q": "Which password is strongest?",
          "options": ["123456", "qwerty", "P@ssw0rd!23", "abcdef"],
          "answer": "P@ssw0rd!23"
        },
        {
          "q": "How often should you change your password?",
          "options": ["Never", "Every 6 months", "Only when hacked", "Once a year"],
          "answer": "Every 6 months"
        },
        {
          "q": "What should you avoid in passwords?",
          "options": ["Symbols", "Personal info", "Numbers", "Uppercase letters"],
          "answer": "Personal info"
        }
      ]
    }
  ],
  "Phishing Awareness": [
    {
      "title": "Spot the Phish",
      "theme": "🎣",
      "questions": [
        {
          "q": "You get an email claiming you won a lottery. What should you do?",
          "options": ["Click the link", "Reply with your info", "Ignore/Delete it", "Call them"],
          "answer": "Ignore/Delete it"
        },
        {
          "q": "A real sign of phishing is:",
          "options": ["Perfect grammar", "Familiar email address", "Urgent language", "HTTPS in URL"],
          "answer": "Urgent language"
        },
        {
          "q": "You’re asked to verify bank info by email. It’s likely:",
          "options": ["A joke", "A security update", "Phishing", "From your friend"],
          "answer": "Phishing"
        },
        {
          "q": "An email from 'admin@micr0soft.com' is likely:",
          "options": ["Genuine", "Promotional", "Spam", "Phishing"],
          "answer": "Phishing"
        },
        {
          "q": "Which one is a common phishing trick?",
          "options": ["Asking for money", "Spelling errors", "Urgency", "All of the above"],
          "answer": "All of the above"
        },
        {
          "q": "How to check if a link is suspicious?",
          "options": ["Click it", "Hover over it", "Ignore always", "Bookmark it"],
          "answer": "Hover over it"
        }
      ]
    },
    {
      "title": "Escape the Phish",
      "theme": "🛡️",
      "questions": [
        {
          "q": "Best way to confirm an email's authenticity?",
          "options": ["Click the link", "Reply asking", "Call official number", "Ignore always"],
          "answer": "Call official number"
        },
        {
          "q": "Which email is most suspicious?",
          "options": ["From boss with typos", "From friend", "From newsletter", "From IT with correct details"],
          "answer": "From boss with typos"
        },
        {
          "q": "Phishing attacks often ask you to:",
          "options": ["Secure your PC", "Click unknown links", "Sleep early", "Play games"],
          "answer": "Click unknown links"
        },
        {
          "q": "The best defense against phishing is:",
          "options": ["Antivirus", "Changing passwords", "User awareness", "Backup data"],
          "answer": "User awareness"
        },
        {
          "q": "What is 'spear phishing'?",
          "options": ["Fishing technique", "Targeted phishing", "Spam email", "Safe link"],
          "answer": "Targeted phishing"
        },
        {
          "q": "A legit company will usually:",
          "options": ["Ask passwords", "Have spelling errors", "Use official domains", "Send threats"],
          "answer": "Use official domains"
        }
      ]
    }
  ],
  "Malware Protection": [
    {
      "title": "Virus Hunter",
      "theme": "🧬",
      "questions": [
        {"q": "What is malware?", "options": ["A type of software", "A website", "An antivirus", "A firewall"], "answer": "A type of software"},
        {"q": "Which is NOT a type of malware?", "options": ["Trojan", "Ransomware", "Firewall", "Spyware"], "answer": "Firewall"},
        {"q": "What does ransomware do?", "options": ["Boosts speed", "Encrypts files for ransom", "Cleans memory", "Sends updates"], "answer": "Encrypts files for ransom"},
        {"q": "What helps detect malware?", "options": ["Music player", "Antivirus software", "USB drives", "Fake emails"], "answer": "Antivirus software"},
        {"q": "A keylogger records:", "options": ["Your screen", "Your location", "Your keystrokes", "Your voice"], "answer": "Your keystrokes"},
        {"q": "Malware often spreads through:", "options": ["Official websites", "Email attachments", "Bank visits", "Textbooks"], "answer": "Email attachments"}
      ]
    },
    {
      "title": "Spot the Malware",
      "theme": "🧪",
      "questions": [
        {"q": "Which file is most suspicious?", "options": ["Invoice.pdf", "GameSetup.exe", "Resume.docx", "Movie.mp4"], "answer": "GameSetup.exe"},
        {"q": "How often should you scan for malware?", "options": ["Never", "Only when PC is slow", "Weekly", "Yearly"], "answer": "Weekly"},
        {"q": "Which action can reduce malware risk?", "options": ["Clicking ads", "Ignoring updates", "Opening random emails", "Installing updates"], "answer": "Installing updates"},
        {"q": "Which device can carry malware?", "options": ["Pen drive", "Keyboard", "Mouse", "Monitor"], "answer": "Pen drive"},
        {"q": "What does antivirus software do?", "options": ["Heats the system", "Finds and removes malware", "Shows movies", "Crashes programs"], "answer": "Finds and removes malware"},
        {"q": "Best source for safe software downloads?", "options": ["Unknown forums", "Official websites", "Email links", "Friend's pen drive"], "answer": "Official websites"}
      ]
    }
  ],
  "Social Engineering Defense": [
    {
      "title": "Hack the Hacker",
      "theme": "🕵️‍♂️",
      "questions": [
        {"q": "What is social engineering?", "options": ["A coding language", "Manipulation to gain confidential info", "Game cheat", "Antivirus method"], "answer": "Manipulation to gain confidential info"},
        {"q": "A common social engineering tactic?", "options": ["Firewall", "Phishing email", "Password manager", "Encrypted message"], "answer": "Phishing email"},
        {"q": "How can you avoid social engineering attacks?", "options": ["Share passwords", "Ignore security", "Verify sources", "Click on every link"], "answer": "Verify sources"},
        {"q": "What should you do if you suspect social engineering?", "options": ["Ignore it", "Tell friends", "Report to authority", "Click it quickly"], "answer": "Report to authority"},
        {"q": "Social engineers often target:", "options": ["Technical vulnerabilities", "Physical strength", "Human behavior", "Computer speed"], "answer": "Human behavior"},
        {"q": "Tailgating refers to:", "options": ["A car trick", "Following someone into a secure area", "Spam", "Backup data"], "answer": "Following someone into a secure area"}
      ]
    },
    {
      "title": "Manipulation Escape Room",
      "theme": "🎭",
      "questions": [
        {"q": "Which is a red flag of a social engineering attempt?", "options": ["Polite email", "Urgent request", "Correct grammar", "Contact from IT"], "answer": "Urgent request"},
        {"q": "Social engineers trick you into giving:", "options": ["Water", "Confidential info", "Food", "Entertainment"], "answer": "Confidential info"},
        {"q": "Which is the best way to confirm a request?", "options": ["Trust email", "Ignore it", "Verify via call", "Reply instantly"], "answer": "Verify via call"},
        {"q": "Should you share login info with coworkers?", "options": ["Yes, always", "Only when needed", "Only managers", "No"], "answer": "No"},
        {"q": "Which method reduces social engineering risk?", "options": ["Sharing OTPs", "Ignoring emails", "Employee training", "Storing passwords in Notepad"], "answer": "Employee training"},
        {"q": "What is baiting?", "options": ["Physical attack", "Offering fake rewards to steal data", "Network filtering", "Encryption"], "answer": "Offering fake rewards to steal data"}
      ]
    }
  ],
  "Data Privacy": [
    {
      "title": "Privacy Shield",
      "theme": "🛡️",
      "questions": [
        {"q": "What is personal data?", "options": ["Name and address", "Game scores", "System files", "RAM size"], "answer": "Name and address"},
        {"q": "What is the best way to protect data?", "options": ["Backup", "Sharing online", "Opening attachments", "Encrypting"], "answer": "Encrypting"},
        {"q": "Which is a key principle of data privacy?", "options": ["Always share data", "Limit access to data", "Use strong passwords", "Ignore data leaks"], "answer": "Limit access to data"},
        {"q": "What does GDPR focus on?", "options": ["Game designs", "Data protection", "Network security", "Cloud storage"], "answer": "Data protection"},
        {"q": "What does encryption do?", "options": ["Speeds up data", "Locks data with a key", "Backup data", "Erases data"], "answer": "Locks data with a key"},
        {"q": "Which device might leak your data?", "options": ["Encrypted USB", "Smartphone", "Old PC", "Offline paper"], "answer": "Smartphone"}
      ]
    }
  ],
  "Mobile Security": [
    {
      "title": "Mobile Defender",
      "theme": "📱",
      "questions": [
        {"q": "Which app is safe to download?", "options": ["Official app stores", "Unverified websites", "Friend's recommendation", "Email links"], "answer": "Official app stores"},
        {"q": "What can a weak password cause?", "options": ["Faster battery", "Mobile theft", "Data leaks", "App crash"], "answer": "Data leaks"},
        {"q": "Which of these is NOT a security risk?", "options": ["Untrusted apps", "Public Wi-Fi", "Encrypted messages", "Unknown links"], "answer": "Encrypted messages"},
        {"q": "How can you secure a mobile device?", "options": ["Disable updates", "Use a screen lock", "Ignore permissions", "Download everything"], "answer": "Use a screen lock"},
        {"q": "What is the best action if your mobile is lost?", "options": ["Lock it remotely", "Call the thief", "Do nothing", "Use it immediately"], "answer": "Lock it remotely"},
        {"q": "Which is a mobile security risk?", "options": ["Mobile backup", "Unencrypted apps", "Update alerts", "Password manager"], "answer": "Unencrypted apps"}
      ]
    }
  ],
  "IoT Device Security": [
    {
      "title": "IoT Sentinel",
      "theme": "🔌",
      "questions": [
        {"q": "IoT devices can be a target because:", "options": ["They're cheap", "They're connected to the internet", "They're complex", "They're rarely used"], "answer": "They're connected to the internet"},
        {"q": "To secure IoT devices, always:", "options": ["Change default passwords", "Share with friends", "Leave them exposed", "Ignore updates"], "answer": "Change default passwords"},
        {"q": "What is a good practice for IoT security?", "options": ["Install antivirus", "Disable unnecessary features", "Share data freely", "Use default passwords"], "answer": "Disable unnecessary features"},
        {"q": "Which of these is NOT an IoT device?", "options": ["Smart thermostat", "Wi-Fi router", "Car battery", "Smartwatch"], "answer": "Car battery"},
        {"q": "How to secure an IoT network?", "options": ["Strong passwords", "Open access", "Wi-Fi sharing", "Weak encryption"], "answer": "Strong passwords"},
        {"q": "What does IoT vulnerability often lead to?", "options": ["Data theft", "More devices", "Game speed", "Battery drain"], "answer": "Data theft"}
      ]
    }
  ]
}


def ask_question(question, options):
    running = True
    while running:
        screen.fill(WHITE)
        draw_text_centered(question, 100, screen, 40)
        for i, opt in enumerate(options):
            rect = pygame.Rect(200, 200 + i*70, 400, 50)
            pygame.draw.rect(screen, LIGHT_BLUE, rect)
            pygame.draw.rect(screen, DARK_BLUE, rect, 2)
            text_surf = font.render(opt, True, BLACK)
            screen.blit(text_surf, (rect.x + 10, rect.y + 10))
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

def run_mini_game(game_data):
    questions = game_data["questions"]
    correct = 0
    for q in questions:
        answer = ask_question(q["q"], q["options"])
        if answer == q["answer"]:
            correct += 1
    return correct

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

def show_start_screen():
    running = True
    start_button = Button(275, 300, 250, 60, "Start Game", lambda: "start")
    while running:
        screen.fill(WHITE)
        draw_text_centered("Welcome to Cybersecurity Awareness Game", 150, screen, 36)
        draw_text_centered("Click 'Start Game' to begin", 220, screen, 30)
        start_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    return

def main():
    show_start_screen()
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
                            final_screen(total_score, len(modules) * 3)  # 3 is number of questions per module in demo

if __name__ == "__main__":
    main()
