import pygame
import random
pygame.init()

# window
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
    screen.blit(text, (50, 250))

# Charger l'image du cœur
heart_image = pygame.image.load("assets/images/img-detoured/coeur.png")
heart_size = (40, 40)  # Taille des cœurs
heart_image = pygame.transform.scale(heart_image, heart_size)

# Fonction pour afficher les cœurs
def display_hearts(attempts_left_level_1):
    heart_spacing = 10  # Espace entre les cœurs
    start_x = 20  # Position de départ pour le premier cœur
    y = 20  # Position verticale fixe pour les cœurs

    for i in range(attempts_left_level_1 - 1):
        x = start_x + i * (heart_size[0] + heart_spacing)
        screen.blit(heart_image, (x, y))


# ----------------------------------------------------------------------------
# Main loop
running = True
game_over = False
end_message = ""
first_image_visible = False
third_image = False
forth_image = False

while running:
    # Efface l'écran avec le fond
    screen.blit(background, (center_x, center_y))

    if not game_over:
        # Affiche les mots et les images si le jeu est en cours
        display_word()
        display_hearts(attempts_left_level_1)
        draw_hangman(attempts_left_level_1, first_image_visible, third_image, forth_image)
    else:
        # Affiche le message de fin de jeu
        text = FONT.render(end_message, True, BLACK)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        screen.blit(text, text_rect)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.unicode.isalpha():
                letter = event.unicode.upper()
                if letter not in guessed_letters:
                    guessed_letters.add(letter)
                    if letter not in word_to_guess:
                        attempts_left_level_1 -= 1
                        if attempts_left_level_1 <= 8 and not first_image_visible:
                            first_image_visible = True
                        if attempts_left_level_1 <= 6 and not third_image:
                            third_image = True
                        if attempts_left_level_1 <= 5 and not forth_image:
                            forth_image = True

    # Vérification de victoire ou défaite
    if not game_over:
        if "_" not in [letter if letter in guessed_letters else "_" for letter in word_to_guess]:
            end_message = f"Well done ! C'est gagneee! Le mot etait: {word_to_guess}"
            game_over = True
        elif attempts_left_level_1 == 0:
            end_message = f"Vous avez perdu... Le mot etait : {word_to_guess}"
            game_over = True

    # Met à jour l'affichage
    pygame.display.flip()

pygame.quit()

