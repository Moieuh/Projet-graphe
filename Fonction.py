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

def calendrier_plus_tot_bellman(tableau, n):
    """
    Calcule les dates au plus tôt pour chaque sommet à l'aide de l'algorithme de Bellman-Ford.
    tableau : Liste de tâches sous forme [ID_tâche, durée, prédécesseurs...].
    n : Nombre total de tâches (exclut les sommets fictifs 0 et n+1).
    """
    # Initialisation
    dates_tot = [float('-inf')] * (n + 2)  # Inclut α (0) et ω (n+1)
    dates_tot[0] = 0  # Le sommet source α est initialisé à 0

    # Ajouter les arcs fictifs pour le sommet de fin (ω)
    arcs_fictifs_fin = [
        (tache[0], n + 1, tache[1]) for tache in tableau
        if all(tache[0] not in other[2:] for other in tableau)
    ]

    # Ensemble des arcs pour Bellman-Ford
    arcs = []
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        for pred in predecesseurs:
            arcs.append((pred, tache_id, duree))
    arcs.extend(arcs_fictifs_fin)  # Ajouter les arcs fictifs

    # Boucle principale (au plus n-1 itérations)
    for iteration in range(n + 1):
        changements = False  # Vérifie si une mise à jour est effectuée
        for u, v, w in arcs:
            if dates_tot[u] != float('-inf') and dates_tot[v] < dates_tot[u] + w:
                dates_tot[v] = dates_tot[u] + w
                changements = True

        # Si aucune mise à jour n'a été faite, on peut s'arrêter
        if not changements:
            break

        # Après n itérations, vérifier si des changements subsistent (détection de circuits absorbants)
        if iteration == n and changements:
            print("Circuit absorbant détecté.")
            return None

    return dates_tot
<<<<<<< Updated upstream
=======
# Calculer le calendrier au plus tard
def calendrier_plus_tard(dates_tot,matrice):
    
    # Initialiser à l'infini
    n = len(matrice)
    dates_tard = [float('inf')] * n
    dates_tard[-1] = dates_tot[-1]
    
    # Parcourir les tâches dans l'ordre décroissant des rangs
    for i in range(n - 2, -1, -1):
        for j in range(n):
            if matrice[i][j] is not None and matrice[i][j] != '*':
                dates_tard[i] = min(dates_tard[i], dates_tard[j] - matrice[i][j])

    return dates_tard

# Calculer les marges
def calculer_marges(dates_tot, dates_tard):
    
    marges = []
    for tot, tard in zip(dates_tot, dates_tard):
        marges.append(tard-tot)
        
    return marges

def calcul_dates_au_plus_tot(tableau):
    """
    Calcul des dates au plus tôt pour chaque tâche à l'aide de la méthode de Bellman.

    Args:
        tableau (list): Une liste contenant les informations des tâches sous forme :
                        [ID_tâche, durée, prédécesseur1, prédécesseur2, ...]

    Returns:
        list: Une liste des dates au plus tôt pour chaque tâche (incluant les sommets fictifs).
    """
    # Identifier toutes les tâches et leurs prédécesseurs
    ids_taches = set(t[0] for t in tableau)
    for t in tableau:
        ids_taches.update(t[2:])

    # Déterminer le sommet fictif final (n+1)
    n = max(ids_taches)

    # Initialisation des dates au plus tôt
    dates_au_plus_tot = [float('-inf')] * (n + 1)
    dates_au_plus_tot[0] = 0  # Sommet fictif initial

    # Construire la liste des arcs (u, v, poids)
    arcs = []
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        if not predecesseurs:
            # Arc fictif depuis le sommet initial
            arcs.append((0, tache_id, 0))
        for pred in predecesseurs:
            arcs.append((pred, tache_id, duree))

    # Algorithme de Bellman-Ford
    for _ in range(len(ids_taches)):  # Au plus n-1 itérations
        updated = False
        for u, v, poids in arcs:
            if dates_au_plus_tot[u] != float('-inf') and dates_au_plus_tot[v] < dates_au_plus_tot[u] + poids:
                dates_au_plus_tot[v] = dates_au_plus_tot[u] + poids
                updated = True
        if not updated:
            break

    # Remplacer les -inf restants par 0 (cas des sommets isolés)
    dates_au_plus_tot = [max(0, d) for d in dates_au_plus_tot]

    return dates_au_plus_tot
>>>>>>> Stashed changes
