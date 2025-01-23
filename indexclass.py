import pygame
import random


class HangmanGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("The Hangman (py)game")
        self.background = pygame.image.load("assets/desert.jpg")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT = pygame.font.Font("assets/GildiaTitulSlNormal.Ttf", 50)

        self.load_resources()
        self.reset_game()

    def load_resources(self):
        self.pictures = [
            pygame.image.load("assets/images/img-detoured/tree.png"),
            pygame.image.load("assets/images/img-detoured/hangman.png"),
            pygame.image.load("assets/images/img-detoured/noeud.png"),
            pygame.image.load("assets/images/img-detoured/Design sans titre (1)-Photoroom.png"),
            pygame.image.load("assets/images/img-detoured/Design sans titre-Photoroom.png"),
            pygame.image.load("assets/images/img-detoured/preyman1-.png"),
            pygame.image.load("assets/images/img-detoured/standman1.png"),
            pygame.image.load("assets/images/img-detoured/onchairman1.png"),
            pygame.image.load("assets/images/img-detoured/sitman1.png"),
        ]
        self.pic_sizes = [
            (700, 700),
            (120, 270),
            (50, 50),
            (100, 100),
            (200, 200),
            (190, 190),
            (240, 240),
            (200, 200),
            (200, 200),
        ]
        self.positions = [
            (200, 20),
            (600, 430),
            (600, 430),
            (750, 40),
            (350, 530),
            (550, 540),
            (620, 490),
            (720, 530),
            (850, 530),
        ]

        with open("words_list.txt") as file:
            self.words = [word.rstrip("\n").upper() for word in file]

    def reset_game(self):
        self.word_to_guess = random.choice(self.words)
        self.guessed_letters = set()
        self.attempts_left = 9
        self.first_image_visible = False
        self.third_image = False
        self.forth_image = False
        self.game_over = False
        self.end_message = ""

    def draw_hangman(self):
        # Dessine les images en fonction des erreurs
        if self.first_image_visible:
            first_picture = pygame.transform.scale(self.pictures[0], self.pic_sizes[0])
            self.screen.blit(first_picture, self.positions[0])

        for i in range(1, 9 - self.attempts_left + 1):
            if i < len(self.pictures):
                picture = pygame.transform.scale(self.pictures[i], self.pic_sizes[i])
                self.screen.blit(picture, self.positions[i])

        if self.third_image:
            third_image = pygame.transform.scale(self.pictures[3], self.pic_sizes[3])
            self.screen.blit(third_image, self.positions[3])

        if self.forth_image:
            forth_image = pygame.transform.scale(self.pictures[4], self.pic_sizes[4])
            self.screen.blit(forth_image, self.positions[4])

    def display_word(self):
        displayed = " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word_to_guess])
        text = self.FONT.render(displayed, True, self.BLACK)
        self.screen.blit(text, (50, 250))

    def check_game_over(self):
        if "_" not in [letter if letter in self.guessed_letters else "_" for letter in self.word_to_guess]:
            self.end_message = "Well done! Vous avez gagné!"
            self.game_over = True
        elif self.attempts_left == 0:
            self.end_message = f"Vous avez perdu... Le mot était : {self.word_to_guess}"
            self.game_over = True

    def handle_input(self, event):
        if event.unicode.isalpha() and not self.game_over:
            letter = event.unicode.upper()
            if letter not in self.guessed_letters:
                self.guessed_letters.add(letter)
                if letter not in self.word_to_guess:
                    self.attempts_left -= 1
                    if self.attempts_left <= 8:
                        self.first_image_visible = True
                    if self.attempts_left <= 6:
                        self.third_image = True
                    if self.attempts_left <= 5:
                        self.forth_image = True

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))

            if not self.game_over:
                self.display_word()
                self.draw_hangman()
            else:
                text = self.FONT.render(self.end_message, True, self.BLACK)
                text_rect = text.get_rect(center=(540, 360))
                self.screen.blit(text, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_input(event)

            self.check_game_over()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = HangmanGame()
    game.run()
