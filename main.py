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
 
    test_circuit=circuits(matrice)
    

    if test_circuit :
        print("Il y a un circuit ")
        print("C'est n'est pas un graphe d'ordonnancement")
        
    else :
        print("Il n'y a pas de circuit ")
        test_arc=arc_neg(matrice)
        if test_arc ==False:
            print("Il n'y a pas d'arcs négatifs")
            print("C'est un graphe d'ordonnancement")
            rangs=calculer_rangs(tableau,n)
            for sommet, rang in rangs.items():
                print(f"Sommet {sommet} : Rang {rang+1}")
        else:
            print("Il a des arcs négatifs")
            print("C'est n'est pas un graphe d'ordonnancement")


dates_tot = [0,0,0, 2, 6, 17, 5,7,12,17,26,7,25,26,33]     # Exemple de dates au plus tôt
dates_tard = calendrier_plus_tard(dates_tot, matrice)
print("Dates au plus tard :", dates_tard)

    # Calcul des marges
marges = calculer_marges(dates_tot, dates_tard)
print("Marges :", marges)
            
