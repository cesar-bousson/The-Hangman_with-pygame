import pygame
import random
pygame.init()

# window
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("The Hangman (py)game")
background = pygame.image.load("assets/desert.jpg")

window_width, window_height = screen.get_size()
background_width, background_height = background.get_size()

center_x = (window_width - background_width) // 2
center_y = (window_height - background_height) // 2

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font("assets/GildiaTitulSlNormal.Ttf", 50)

# -------------------------------------------------------------------------------------
# Words
words = []
with open("words_list.txt") as file:
    for word in file:
        words.append(word.rstrip("\n"))
word_to_guess = random.choice(words).upper()

guessed_letters = set()

attempts_left_level_1 = 9
# -------------------------------------------------------------------------------------
# Draw hangman
def draw_hangman(attempts, first_image_visible, third_image, forth_image):
    pictures = [
        pygame.image.load("assets/images/img-detoured/tree.png"),  # 1 arbre
        pygame.image.load("assets/images/img-detoured/hangman.png"),  # 9 pendu
        pygame.image.load("assets/images/img-detoured/noeud.png"),  # 7 noeud
        pygame.image.load("assets/images/img-detoured/Design sans titre (1)-Photoroom.png"),  # 8 corbeaux
        pygame.image.load("assets/images/img-detoured/Design sans titre-Photoroom.png"),  # 6 faucheuse
        pygame.image.load("assets/images/img-detoured/preyman1-.png"),  # 5 homme qui prie
        pygame.image.load("assets/images/img-detoured/standman1.png"),  # 4 homme debout
        pygame.image.load("assets/images/img-detoured/onchairman1.png"),  # 3 homme affalé
        pygame.image.load("assets/images/img-detoured/sitman1.png"),  # 2 homme assis
        
    ]

    pic_sizes = [
        (700, 700), #1
        (120, 270), #9
        (50, 50),   #7
        (100, 100), #8
        (200, 200), #6
        (190, 190), #5
        (240, 240), #4
        (200, 200), #3
        (200, 200), #2
    ]

    positions = [
        (200, 20), #1
        (600, 430),#9
        (600, 430), #7
        (750, 40), #8
        (350, 530), #6
        (550, 540), #5
        (620, 490), #4
        (720, 530), #3
        (850, 530), #2
    ]

    # Affiche la première image après la première erreur
    if first_image_visible and attempts > 0:
        first_picture = pygame.transform.scale(pictures[0], pic_sizes[0])
        screen.blit(first_picture, positions[0])

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
        
    pygame.display.update()
# -----------------------------------------------------------------------------------
# Display word
def display_word():
    displayed = ""
    for letter in word_to_guess:
        if letter in guessed_letters:
            displayed += f"{letter} "
        else:
            displayed += "_ "
    text = FONT.render(displayed.strip(), True, BLACK)
    screen.blit(text, (50, 400))
# ----------------------------------------------------------------------------

# Main loop
running = True
game_over = False
end_message = ""
first_image_visible = False
third_image = False
forth_image = False

while running:
    screen.blit(background, (center_x, center_y))

    if not game_over:
        display_word()
        draw_hangman(attempts_left_level_1, first_image_visible, third_image, forth_image)
    else:
        text = FONT.render(end_message, True, BLACK)
        screen.blit(text, (center_x, center_y))

    # Event management
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                letter = event.unicode.upper()
                if letter not in guessed_letters:
                    guessed_letters.add(letter)
                    if letter not in word_to_guess:
                        attempts_left_level_1 -= 1
                        
                        # Active la première image après la première erreur
                        if attempts_left_level_1 <= 8 and not first_image_visible:
                            first_image_visible = True
                        # Active l'image des corbeaux à 6 tentatives restantes
                        if attempts_left_level_1 <= 6 and not third_image:
                            third_image = True
                        # Active l'image de la faucheuse à 5 tentatives restantes
                        if attempts_left_level_1 <= 5 and not forth_image:
                            forth_image = True

    # Check victory
    if "_" not in [letter if letter in guessed_letters else "_" for letter in word_to_guess]:
        end_message = "Well done ! Vous avez gagneee!"
        game_over = True
    elif attempts_left_level_1 == 0:
        end_message = f"Vous avez perdu... Le mot etait : {word_to_guess}"
        game_over = True

    pygame.display.flip()

pygame.quit()
