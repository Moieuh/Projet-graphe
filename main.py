from Fonction import *
r=0
while(r==0):
    #Faire une boucle avec la commande choix fichier
    fichier=choisir_graph()
    tableau = lire_tableau(fichier)
    print_tab(tableau)
    
    print("\n")
    print(tableau)
    print_graphe_ordonancement(tableau)
    print("\n")

    # Construire et afficher la matrice
    if tableau:
        n = len(tableau)  # Nombre de tâches
        matrice = construire_matrice(tableau, n)
        print(matrice)
        
        print_matrice(matrice)
        print("\n")
   
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
                print("\n")

                rangs=calculer_rangs(tableau,n)
                for sommet, rang in rangs.items():
                    print(f"Sommet {sommet} : Rang {rang+1}")
                print("\n")
                
                print("Calendrier au plus tôt:")
                dates_tot = calcul_dates_au_plus_tot(tableau) 
                for sommet, date in enumerate(dates_tot):
                    print(f"Sommet {sommet} : Date au plus tôt {date}")  # Exemple de dates au plus tôt
                print("\n")
                print(dates_tot)

                print("Calendrier au plus tard:")
                dates_tard = calendrier_plus_tard(dates_tot, matrice)
                for sommet, date in enumerate(dates_tard):
                    print(f"Sommet {sommet} : Date au plus tard {date}")
                print(dates_tard)
                print("\n")
                
                    # Calcul des marges
                marges = calculer_marges(dates_tot, dates_tard)
                print("Marges :", marges)
                liste_chemin_critique=chemin_critique(marges,matrice)
                print("Le chemin critique : ", end='')
                for ele in liste_chemin_critique:
                    print(ele[0],end=' ')
            
            else:
                print("Il a des arcs négatifs")
                print("C'est n'est pas un graphe d'ordonnancement")
    
    print("\n")
    r=int(input("Voulez essayer un autre fichier?\n oui:0\n non:1 "))


                
