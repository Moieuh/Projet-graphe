def choisir_graph():
        x=int(input("Entrer le numero du Test que vous vouler afficher"))
        fichier=f"Test/Test {x}.txt"
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
def construire_matrice(tableau, n):
   
    # Initialiser une matrice (n+2)x(n+2) remplie de None (ou d'une valeur spéciale)
    matrice = [[None] * (n + 2) for _ in range(n + 2)]

    # Parcourir chaque tâche pour ajouter ses arcs
    for tache in tableau:
        tache_id, duree, *predecesseurs = tache
        # Ajouter des arcs des prédécesseurs vers la tâche courante
        for pred in predecesseurs:
            matrice[pred][tache_id] = duree

    # Ajouter des arcs fictifs (point d'entrée et point de sortie)
    for tache in tableau:
        tache_id = tache[0]
        # Arc fictif du point de départ (0) vers les tâches sans prédécesseurs
        if not any(tache_id in t[2:] for t in tableau):
            matrice[0][tache_id] = 0
        # Arc fictif des tâches sans successeurs vers le point de sortie (N+1)
        if all(tache_id not in t[2:] for t in tableau):
            matrice[tache_id][n + 1] = 0

    return matrice


def print_matrice(matrice):
    print("\nMatrice de valuer :")
    # Afficher les entêtes des colonnes
    print("   " + " ".join(f"{i:>3}" for i in range(len(matrice))))
    for i, ligne in enumerate(matrice):
        # Afficher chaque ligne avec son numéro
        print(f"{i:>3} " + " ".join(f"{x if x is not None else '*':>3}" for x in ligne))


