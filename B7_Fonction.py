from collections import deque

def tri_topologique(matrice):
    # Calculer les degrés entrants
    n = len(matrice)
    degres_entrants = [0] * n
    for i in range(n):
        for j in range(n):
            if matrice[i][j] is not None:
                degres_entrants[j] += 1
    
    # Initialiser la file pour les sommets de degré entrant 0
    file = deque([i for i in range(n) if degres_entrants[i] == 0])
    ordre_topologique = []
    
    while file:
        tache = file.popleft()
        ordre_topologique.append(tache)
        
        # Réduire le degré entrant des voisins
        for j in range(n):
            if matrice[tache][j] is not None:
                degres_entrants[j] -= 1
                if degres_entrants[j] == 0:
                    file.append(j)
    
    if len(ordre_topologique) != n:
        raise ValueError("Le graphe contient un cycle, impossible de faire un tri topologique.")
    
    return ordre_topologique



def choisir_graph():
    x=int(input("Entrer le numero du Test que vous vouler afficher: "))
    fichier=f"Test/table {x}.txt"
    print("Le fichier tester est ",fichier)
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
            print(f"0 -> {tache_id} = 0")

    # Ajouter les arcs du tableau principal
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        if predecesseurs:
            for pred in predecesseurs:
                # Trouver la durée de la tâche prédécesseur
                pred_duree = next(d for id_tache, d, *p in tableau if id_tache == pred)
                print(f"{pred} -> {tache_id} = {pred_duree}")
    
    # Ajouter les arcs fictifs des tâches sans successeurs vers le sommet N+1
    for tache in tableau:
        tache_id = tache[0]
        if all(tache_id not in t[2:] for t in tableau):  # Si la tâche n'est pas prédécesseur
            print(f"{tache_id} -> {n + 1} = {tache[1]}")

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
            pred_duree = next(d for id_tache, d, *p in tableau if id_tache == pred)
            matrice[pred][tache_id] = pred_duree  # Utilise l'ID du prédécesseur comme valeur

    # Ajouter les arcs fictifs des tâches sans successeurs vers le sommet N+1 (ω)
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        if all(tache_id not in t[2:] for t in tableau):  # Si la tâche n'est pas prédécesseur
            matrice[tache_id][n + 1] = tache[1]  # Utilise l'ID de la tâche comme valeur

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
        if circ:
            break
        
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

def calculer_rangs(tableau, n):
    print("Rangs des sommets :")
    print(f"Sommet 0 : Rang 0")
    # Créer un dictionnaire de degrés entrants (d-1) pour les tâches, excluant 0
    degres_entrants = {i: 0 for i in range(1, n+1)}

    # Créer un dictionnaire des successeurs pour chaque tâche, excluant 0
    successeurs = {i: [] for i in range(1, n+1)}

    # Remplir les structures de données à partir du tableau
    for tache in tableau:
        tache_id, _, *predecesseurs = tache
        for pred in predecesseurs:
            degres_entrants[tache_id] += 1  # Augmenter le degré entrant du successeur
            successeurs[pred].append(tache_id)  # Ajouter le successeur au prédécesseur

    # Initialiser le rang pour chaque tâche, excluant 0
    rang = {i: None for i in range(1, n+1)}

    # Initialisation de l'ensemble S0 (les tâches sans prédécesseur, d-1 = 0)
    S_k = {i for i in range(1, n+1) if degres_entrants[i] == 0}
    
    k = 0  # Le rang initial

    # Tant qu'il existe des tâches à traiter
    while S_k:
        # Attribuer le rang à chaque tâche de S_k
        for i in S_k:
            rang[i] = k
        
        # Créer un nouvel ensemble Sk+1 vide
        S_k_plus_1 = set()

        # Pour chaque tâche dans S_k, traiter ses successeurs
        for i in S_k:
            for j in successeurs[i]:
                degres_entrants[j] -= 1  # Décrémenter le degré entrant du successeur
                if degres_entrants[j] == 0:  # Si d-1(j) devient 0, l'ajouter à Sk+1
                    S_k_plus_1.add(j)
        
        # Passer à l'itération suivante
        S_k = S_k_plus_1
        k += 1

    # Attribuer le rang max + 1 au sommet n+1
    rang[n+1] = k

    return rang


def calcul_dates_au_plus_tot(tableau):
    # Trouver les identifiants uniques des tâches
    ids_taches = set(t[0] for t in tableau)
    for t in tableau:
        ids_taches.update(t[2:])  # Ajouter tous les prédécesseurs
    n = max(ids_taches)  # Identifier la tâche avec le plus grand identifiant

    # Initialiser les dates au plus tôt
    dates_au_plus_tot = [0] * (n + 2)  # Inclut le sommet fictif final n+1

    # Construire une table des prédécesseurs
    predecesseurs = {i: [] for i in range(n + 1)}
    successeurs = {i: [] for i in range(n + 1)}
    durees = {tache[0]: tache[1] for tache in tableau}

    for tache in tableau:
        tache_id, duree, *preds = tache
        if not preds:  # Si pas de prédécesseurs, dépend du sommet fictif 0
            predecesseurs[tache_id].append(0)
            successeurs[0].append(tache_id)
        else:
            for pred in preds:
                predecesseurs[tache_id].append(pred)
                successeurs[pred].append(tache_id)

    # Tri topologique
    ordre_topologique = []
    degres_entrants = {i: len(predecesseurs[i]) for i in range(n + 1)}
    pile = [i for i in range(n + 1) if degres_entrants[i] == 0]

    while pile:
        tache = pile.pop()
        ordre_topologique.append(tache)
        for succ in successeurs[tache]:
            degres_entrants[succ] -= 1
            if degres_entrants[succ] == 0:
                pile.append(succ)

    # Calculer les dates au plus tôt
    for tache_id in ordre_topologique:
        if tache_id in durees:  # Ignorer les sommets fictifs sans durée
            for pred in predecesseurs[tache_id]:
                dates_au_plus_tot[tache_id] = max(
                    dates_au_plus_tot[tache_id],
                    dates_au_plus_tot[pred] + durees.get(pred, 0)
                )

    # Gérer le sommet fictif final
    for tache_id in range(1, n + 1):
        if all(tache_id not in t[2:] for t in tableau):  # Si la tâche n'a pas de successeur
            dates_au_plus_tot[n + 1] = max(
                dates_au_plus_tot[n + 1],
                dates_au_plus_tot[tache_id] + durees[tache_id]
            )

    return dates_au_plus_tot



# Calculer le calendrier au plus tard
def calendrier_plus_tard(dates_tot, matrice):
    n = len(matrice)
    dates_tard = [float('inf')] * n
    dates_tard[-1] = dates_tot[-1]  # La dernière tâche a sa date au plus tard égale à sa date au plus tôt

    # Effectuer un tri topologique inversé
    ordre_topologique_inverse = tri_topologique(matrice)[::-1]  # Inverser l'ordre

    # Calculer les dates au plus tard
    for tache_id in ordre_topologique_inverse:
        for successeur_id in range(n):
            if matrice[tache_id][successeur_id] is not None:  # Si un arc existe de tache_id vers successeur_id
                dates_tard[tache_id] = min(dates_tard[tache_id], dates_tard[successeur_id] - matrice[tache_id][successeur_id])

    return dates_tard


# Calculer les marges
def calculer_marges(dates_tot, dates_tard):
    
    marges = []
    for tot, tard in zip(dates_tot, dates_tard):
        marges.append(tard-tot)
        
    return marges

def chemin_critique(marge,matrice):
    
    #recherche tache critique == celle dont la marge ==0
    taches_critique=[]
    for i in range(len(marge)):
        if marge[i]==0:
            taches_critique.append(i)

    
    chemins_critique =[]
    
    #Fonction qui permet de retracer la racine 
    def suivre_chemin(tache_id, chemin):
        
        # Ajouter la tâche au chemin
        chemin.append(tache_id)

        # Vérifier les prédécesseurs de cette tâche
        for i in range(len(matrice)):
            if matrice[i][tache_id] not in (None,'*') and marge[i] == 0:
                suivre_chemin(i, chemin.copy())  # Appel récursif pour suivre le prédécesseur
    
    
    # Pour chaque tâche du chemin critique, reconstruire les chemins
    for tache_id in taches_critique:
        
        chemin = []
        suivre_chemin(tache_id, chemin)
        # Ajouter le chemin à la liste des chemins critiques (éviter les doublons)
        if chemin not in chemins_critique:
            chemins_critique.append(chemin) 
    
    # Retourner la liste des chemins critiques
    return chemins_critique