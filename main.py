from Fonction import *

#Faire une boucle avec la commande cj=hoix fichier
fichier="Test/Test 1.txt"
tableau = lire_tableau(fichier)
print_tab(tableau)

# Construire et afficher la matrice
if tableau:
    n = len(tableau)  # Nombre de tâches
    matrice = construire_matrice(tableau, n)
    print_matrice(matrice)

