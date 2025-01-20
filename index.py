import pygame
import sys
import random

# CONSIGNES -----------------------------------------------------------------------

#  Structure de base du programme:

# 1) Initialisation de Pygame.
# 2) Une boucle principale pour gérer les événements et mettre à jour l'affichage.
# 3) Gestion des entrées utilisateur.
# 4) Affichage des éléments visuels.

# Étapes pour créer le jeu:

# A. Initialisation:
#   1-Définissez la fenêtre de jeu.
#   2-Chargez les polices et couleurs.

# B. Logique du jeu
#   3-Définissez une liste de mots pour le jeu.
#   4-Ajoutez une logique pour choisir un mot aléatoire.
#   5-Suivez les lettres devinées et les tentatives restantes.

# C. Graphismes
#   6-Affichez le mot en cours avec des underscores _.
#   7-Dessinez le pendu en fonction des erreurs.
#   8-Affichez les lettres déjà devinées.

# D. Gestion des événements
#   9-Captez les entrées clavier pour deviner les lettres.
#   10-Gérez les victoires et les défaites.

# ------------------------------------------------------------------


# Initialisation de Pygame
pygame.init()

# Création de la fenêtre (largeur, hauteur)
screen = pygame.display.set_mode((400, 400))

# Définir un titre pour la fenêtre
pygame.display.set_caption("The Hangman with pygame")


# cesar's features----------------------------------------------------------------------------

# def random_words_list(word,namefile="words_list.txt"):
words=[]
with open("words_list.txt") as file:
    for word in file:
        words.append(word.rstrip("\n"))
word_played = random.choice(words)

for letters in word_played:
    print(' _ ', end="")
        
        
# --------------------------------------------------------------------------------------------

# Boucle principale du jeu
def main_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Fermer la fenêtre
                running = False
        screen.fill((0, 0, 0))  #fond noir (R, G, B)

        # Mettre à jour l'écran
        pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
