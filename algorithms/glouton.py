import time

def nearest_neighbor(distance_mat, start=0):
    """
    Heuristique du Plus Proche Voisin (Nearest Neighbor)
    :param distance_mat: matrice de distances n x n
    :param start: index de la ville de départ
    :return: tour (liste des indices), coût total, temps d'exécution
    """
    n = len(distance_mat)
    unvisited = set(range(n))
    tour = [start]
    unvisited.remove(start)
    total_cost = 0
    current = start

    start_time = time.time()

    while unvisited:
        # trouver la ville la plus proche
        next_city = min(unvisited, key=lambda city: distance_mat[current][city])
        total_cost += distance_mat[current][next_city]
        current = next_city
        tour.append(current)
        unvisited.remove(current)

    # revenir au point de départ
    total_cost += distance_mat[current][start]
    tour.append(start)

    elapsed = time.time() - start_time

    return tour, total_cost, elapsed
