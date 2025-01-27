import pygame
import random
import os
pygame.init()

# Window
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("The Hangman (py)game")
background = pygame.image.load("assets/images/desert.jpg")

window_width, window_height = screen.get_size()
background_width, background_height = background.get_size()

center_x = (window_width - background_width) // 2
center_y = (window_height - background_height) // 2

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font("assets/GildiaTitulSlNormal.Ttf", 50)

# Words
words_file = "words_list.txt"
words = []
if os.path.exists(words_file):
    with open(words_file) as file:
        for word in file:
            words.append(word.rstrip("\n"))
else:
    open(words_file, 'w').close()

# Draw hangman

def draw_hangman(attempts, first_image_visible, third_image, forth_image):
    pictures = [
        pygame.image.load("assets/images/img-detoured/hangman.png"),  # 9 pendu
        pygame.image.load("assets/images/img-detoured/noeud.png"),  # 7 noeud
        pygame.image.load("assets/images/img-detoured/Design sans titre (1)-Photoroom.png"),  # 8 corbeaux
        pygame.image.load("assets/images/img-detoured/Design sans titre-Photoroom.png"),  # 6 faucheuse
        pygame.image.load("assets/images/img-detoured/preyman1-.png"),  # 5 homme qui prie
        pygame.image.load("assets/images/img-detoured/standman1.png"),  # 4 homme debout
        pygame.image.load("assets/images/img-detoured/onchairman1.png"),  # 3 homme affalé
        pygame.image.load("assets/images/img-detoured/sitman1.png"),  # 2 homme assis
        pygame.image.load("assets/images/img-detoured/tree.png"),  # 1 arbre
        
    ]

    pic_sizes = [
        (120, 270), #9
        (50, 50), #7
        (100, 100), #8
        (200, 200), #6
        (190, 190), #5
        (240, 240), #4
        (200, 200), #3
        (200, 200), #2
        (700, 700), #1
    ]

    positions = [
        (600, 430),#9
        (600, 430), #7
        (750, 40), #8
        (350, 530), #6
        (550, 540), #5
        (620, 490), #4
        (720, 530), #3
        (850, 530), #2
        (200, 20), #1
    ]

    # Affiche la première image après la première erreur
    if first_image_visible and attempts > 0:
        first_picture = pygame.transform.scale(pictures[8], pic_sizes[8])
        screen.blit(first_picture, positions[8])

    # Affiche les autres images dans l'ordre croissant à partir de la deuxième image
    if 1 <= attempts < len(pictures):  # On commence après la première image
        picture = pygame.transform.scale(pictures[attempts], pic_sizes[attempts])
        screen.blit(picture, positions[attempts])

    if third_image and attempts >= 3:
        third_image = pygame.transform.scale(pictures[3], pic_sizes[3])
        screen.blit(third_image, positions[3])
        
    if forth_image and attempts >= 4:
        forth_image = pygame.transform.scale(pictures[4], pic_sizes[4])
        screen.blit(forth_image, positions[4])
        
# Display word
def display_word(word, guessed_letters):
    displayed = ""
    for letter in word:
        if letter in guessed_letters:
            displayed += f"{letter} "
        else:
            displayed += "_ "
    text = FONT.render(displayed.strip(), True, BLACK)
    screen.blit(text, (50, 250))

# Display guessed letters
def display_guessed_letters(guessed_letters):
    guessed_text = "- ".join(sorted(guessed_letters))
    text = FONT.render(f"Guessed: {guessed_text}", True, BLACK)
    screen.blit(text, (50, 400))

# Display hearts
def display_hearts(attempts):
    heart_image = pygame.image.load("assets/images/img-detoured/coeur.png")
    heart_size = (40, 40)
    heart_image = pygame.transform.scale(heart_image, heart_size)
    heart_spacing = 10
    start_x = 20
    y = 20

    for i in range(attempts):
        x = start_x + i * (heart_size[0] + heart_spacing)
        screen.blit(heart_image, (x, y))

# Menu to add words and start game
def menu():
    input_active = False
    input_text = ""
    clock = pygame.time.Clock()
    menu_running = True

    while menu_running:
        screen.blit(background, (center_x, center_y))
        menu_welcome = FONT.render("Welcome to the hangman game ! :)", True, BLACK)
        menu_text = FONT.render("Add words (lowercase only). Press Enter to save it.", True, BLACK)
        input_box = pygame.Rect(50, 300, 400, 50)
        start_button = pygame.Rect(50, 400, 220, 70)

        pygame.draw.rect(screen, BLACK, input_box, 4)
        pygame.draw.rect(screen, BLACK, start_button, 4)

        input_render = FONT.render(input_text, True, BLACK)
        start_text = FONT.render("Start*Game", True, BLACK)

        screen.blit(menu_welcome, (200, 50))
        screen.blit(menu_text, (50, 200))
        screen.blit(input_render, (input_box.x, input_box.y))
        screen.blit(start_text, (start_button.x, start_button.y ))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
                if start_button.collidepoint(event.pos):
                    menu_running = False
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.isalpha() and input_text.islower():
                        with open(words_file, 'a') as file:
                            file.write(input_text + "\n")
                        words.append(input_text)
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        pygame.display.flip()
        clock.tick(30)

menu()

# Game loop
running = True
while running:
    word_to_guess = random.choice(words).upper()
    guessed_letters = set()
    attempts_left = 9
    game_over = False
    end_message = ""
    first_image_visible = False
    third_image = False
    forth_image = False

    while not game_over:
        screen.blit(background, (center_x, center_y))
        display_word(word_to_guess, guessed_letters)
        display_guessed_letters(guessed_letters)
        display_hearts(attempts_left)
        draw_hangman(attempts_left, first_image_visible, third_image, forth_image)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.unicode.isalpha():
                    letter = event.unicode.upper()
                    if letter not in guessed_letters:
                        guessed_letters.add(letter)
                        if letter not in word_to_guess:
                            attempts_left -= 1
                            if attempts_left <= 8 and not first_image_visible:
                                first_image_visible = True
                            if attempts_left <= 6 and not third_image:
                                third_image = True
                            if attempts_left <= 5 and not forth_image:
                                forth_image = True


        if "_" not in [letter if letter in guessed_letters else "_" for letter in word_to_guess]:
            end_message = "You Win! * \nPress R to Restart or Q to Quit."
            game_over = True
        elif attempts_left == 0:
            end_message = f"You Lose! * The word was: {word_to_guess}.\nPress R to Restart or Q to Quit."
            game_over = True

        pygame.display.flip()

    while game_over:
        screen.blit(background, (center_x, center_y))
        text = FONT.render(end_message.split("\n")[0], True, BLACK)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2 - 30))
        screen.blit(text, text_rect)

        restart_text = FONT.render(end_message.split("\n")[1], True, BLACK)
        restart_rect = restart_text.get_rect(center=(window_width // 2, window_height // 2 + 30))
        screen.blit(restart_text, restart_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                elif event.key == pygame.K_q:
                    running = False
                    game_over = False

        pygame.display.flip()

pygame.quit()
