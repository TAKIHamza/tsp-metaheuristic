def two_opt_swap(tour, i, k):
    """Échange deux arêtes pour créer un nouveau tour"""
    new_tour = tour[:i] + tour[i:k+1][::-1] + tour[k+1:]
    return new_tour

def two_opt(tour, distance_mat):
    """
    Optimisation locale 2-opt
    :param tour: tour initial
    :param distance_mat: matrice de distances
    :return: tour amélioré
    """
    n = len(tour)
    improved = True
    while improved:
        improved = False
        for i in range(1, n-2):
            for k in range(i+1, n-1):
                new_tour = two_opt_swap(tour, i, k)
                old_cost = sum(distance_mat[tour[j]][tour[j+1]] for j in range(n-1))
                new_cost = sum(distance_mat[new_tour[j]][new_tour[j+1]] for j in range(n-1))
                if new_cost < old_cost:
                    tour = new_tour
                    improved = True
    return tour
