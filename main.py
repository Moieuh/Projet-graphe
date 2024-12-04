from Fonction import *


#Faire une boucle avec la commande choix fichier
fichier="Test/table 2.txt"
tableau = lire_tableau(fichier)
print_tab(tableau)
print_graphe_ordonancement(tableau)
# Construire et afficher la matrice
if tableau:
    n = len(tableau)  # Nombre de tâches
    matrice = construire_matrice(tableau, n)
    
    print_matrice(matrice)

    
rangs=calculer_rangs(tableau,n)
for sommet, rang in rangs.items():
    print(f"Sommet {sommet} : Rang {rang+1}")

    

  
            
