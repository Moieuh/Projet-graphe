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
    print("\nMatrice de valuer :")
    # Afficher les entêtes des colonnes
    print("    " + " ".join(f"{i:>3}" for i in range(len(matrice))))
    for i, ligne in enumerate(matrice):
        # Afficher chaque ligne avec son numéro
        print(f"{i:>3} " + " ".join(f"{x if x is not None else '*':>3}" for x in ligne))

