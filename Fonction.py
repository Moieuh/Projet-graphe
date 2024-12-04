def choisir_graph():
    x=int(input("Entrer le numero du Test que vous vouler afficher"))
    fichier=f"Test/Test {x}.txt"
    print(fichier)
    return fichier

def lire_tableau(fichier):
    tableau = []  
    try:
        with open(fichier, 'r') as f:
            lignes = f.readlines()  # Lire toutes les lignes du fichier
            for ligne in lignes:
                # Convertir chaque ligne en une liste d'entiers et l'ajouter au tableau
                tableau.append(list(map(int, ligne.split())))
    except FileNotFoundError:
            print("Erreur : Fichier introuvable.")
    except ValueError:
            print("Erreur : Format incorrect dans le fichier.")
    return tableau

def print_tab(tableau):
   
    print("\nTableau de contraintes:")
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        print(f"Tâche {tache_id} | Durée : {duree} | Prédécesseurs : {predecesseurs if predecesseurs else 'Aucun'}")

def print_graphe_ordonancement(tableau):
    print("\nGraphe d'ordonnancement :")
    print("Liste des arcs (prédécesseur -> successeur) :")

    n = max(t[0] for t in tableau)  # Nombre total de tâches (le plus grand ID de tâche)

    # Ajouter les arcs fictifs du sommet 0 vers les tâches sans prédécesseurs
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        if not predecesseurs:  # Si la tâche n'a aucun prédécesseur
            print(f"0 -> {tache_id}")

    # Ajouter les arcs du tableau principal
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        if predecesseurs:
            for pred in predecesseurs:
                print(f"{pred} -> {tache_id}")
    
    # Ajouter les arcs fictifs des tâches sans successeurs vers le sommet N+1
    for tache in tableau:
        tache_id = tache[0]
        if all(tache_id not in t[2:] for t in tableau):  # Si la tâche n'est pas prédécesseur
            print(f"{tache_id} -> {n + 1}")

def construire_matrice(tableau, n):

    n = max(t[0] for t in tableau)  # Nombre total de tâches (le plus grand ID de tâche)
    taille = n + 2  # Inclure les sommets fictifs α (0) et ω (n+1)

    # Initialiser une matrice de taille (n+2) x (n+2) avec des None (absence de connexion)
    matrice = [[None] * taille for _ in range(taille)]

    # Ajouter les arcs fictifs du sommet 0 (α) vers les tâches sans prédécesseurs
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        if not predecesseurs:  # Si la tâche n'a aucun prédécesseur
            matrice[0][tache_id] = 0  # Utilise 0 comme valeur

    # Ajouter les arcs selon les prédécesseurs définis dans le tableau
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        for pred in predecesseurs:
            matrice[pred][tache_id] = pred  # Utilise l'ID du prédécesseur comme valeur

    # Ajouter les arcs fictifs des tâches sans successeurs vers le sommet N+1 (ω)
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        if all(tache_id not in t[2:] for t in tableau):  # Si la tâche n'est pas prédécesseur
            matrice[tache_id][n + 1] = tache_id  # Utilise l'ID de la tâche comme valeur

    return matrice




def print_matrice(matrice):
    print("\nMatrice des valeurs :")
    # Afficher les entêtes des colonnes
    print("    " + " ".join(f"{i:>3}" for i in range(len(matrice))))
    for i, ligne in enumerate(matrice):
        # Afficher chaque ligne avec son numéro
        print(f"{i:>3} " + " ".join(f"{x if x is not None else '*':>3}" for x in ligne))



def circuits(matrice):
    """
    On part de ce principe : Tant que c'est possible, supprimer du graphe un sommet sans
    prédécesseur. Si on réussit a supprimer tous les sommets, le graphe est
    sans circuit.
    """

    matricetemp = []
    for row in matrice:
        row_temp=[]
        for element in row:
            row_temp.append(element)
        matricetemp.append(row_temp)  #copie de la matrice pour ne pas l'altérer
    
    test=True
    circ= False
    sommets_restant=[]

    for cpt in range(len(matricetemp)):          # initialisation de chaque tâche
        sommets_restant.append(cpt)

    while test:
        n= len(matricetemp)  
        #Trouver les points d'entrées:
        points_entree=[]
        for i in range(n):
            test1=True
            for j in range(n):
                if matricetemp[j][i] not in  (None,'*') :       # pas vide ou déjà parcouru
                    test1 =False
                    break   #quitte la boucle j
            if test1 and sommets_restant[i] is not None :
                points_entree.append(i)


        if len(points_entree)>0:

            print("Points d'entrée :",end=" " )
            
            for cpt2 in points_entree:
                if sommets_restant[cpt2] is not None :
                    print(cpt2, end=" ")
            print()

        else: #cas 0 point 
            for k in range(n):
                for l in range(n):
                    if matricetemp[k][l] not in (None,'*') :  #Vérifie si il reste des points non parcouru
                        circ = True  # il reste encore des états mais  0 état sans prédécesseurs
                        break
                if circ:
                    break
            test =False 
            
        
        #"Suppression" des points d'entrée avec des '*'
        print("Suppression des points d'entrée")
        for el in points_entree:
            for col in range(n):
                matricetemp[el][col] ='*'

            for row in range(n):
                matricetemp[row][el]='*'
            sommets_restant[el]=None

        # On s'assure qui reste des sommets pour continuer
        reste_sommet = False
        for sommet in sommets_restant:
            if sommet is not None:
                reste_sommet = True
                break
        if not reste_sommet:
            test = False
        
        print("Sommets restants :", end=" ")
        reste_affichage = False
        for cpt in sommets_restant:
            if cpt is not None:
                print(cpt, end=" ")
                reste_affichage = True
        
        if not reste_affichage:
            print("Aucun", end="")
        print()

       
    return circ



def arc_neg(matrice):
    n = len(matrice)
    test = False
    for i in range(n):
        for j in range(n):
            if matrice[i][j] is not None and matrice[i][j]< 0: #On vérifie d'abord que c'est bien un nombre
                test = True
                break  # On quitte la boucle interne dès qu'on trouve un arc négatif
        if test:
            break  # On quitte la boucle externe si l'arc négatif a été trouvé
    return test