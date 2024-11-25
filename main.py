from Fonction import *


#Faire une boucle avec la commande choix fichier
fichier=choisir_graph()
tableau = lire_tableau(fichier)
print_tab(tableau)
print_graphe_ordonancement(tableau)
# Construire et afficher la matrice
if tableau:
    n = len(tableau)  # Nombre de tâches
    matrice = construire_matrice(tableau, n)
    print_matrice(matrice)
