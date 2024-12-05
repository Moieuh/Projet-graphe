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


  
def fefef():
    