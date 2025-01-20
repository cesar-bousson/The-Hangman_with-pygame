import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre (largeur, hauteur)
screen = pygame.display.set_mode((800, 600))

# Définir un titre pour la fenêtre
pygame.display.set_caption("Mon Jeu avec Pygame")

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Fermer la fenêtre
            running = False

    # Remplir l'écran avec une couleur
    screen.fill((0, 0, 0))  # Noir (R, G, B)

    # Mettre à jour l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
