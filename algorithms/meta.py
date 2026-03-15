# import os
# import matplotlib.pyplot as plt
# from utils.parser import read_tsplib
# from utils.distance import distance_matrix
# from algorithms.glouton import nearest_neighbor
# from algorithms.meta import simulated_annealing

# # Configuration (Choisis une instance moyenne pour les tests)
# instance_test = "instances/berlin52.tsp" 
# plots_folder = "plots"
# os.makedirs(plots_folder, exist_ok=True)

# print(f"--- Analyse des paramètres sur {instance_test} ---")
# coords = read_tsplib(instance_test)
# dist_mat = distance_matrix(coords)
# tour_glouton, cost_glouton, _ = nearest_neighbor(dist_mat)
# print(f"Coût de base (Glouton) : {cost_glouton}\n")

# # ==========================================
# # GRAPHE 1 : Avant vs Après (Itérations par palier)
# # ==========================================
# print("Test 1 : Ancienne version vs Nouvelle version (Itérations)")
# paliers = [1, 10, 50, 100, 200]  # 1 = Ancienne version
# couts_palier = []

# for p in paliers:
#     _, cost, _ = simulated_annealing(dist_mat, tour_glouton, alpha=0.95, iter_par_palier=p)
#     couts_palier.append(cost)
#     if p == 1:
#         print(f"-> AVANT (1 itération) : {cost}")
#     elif p == 100:
#         print(f"-> APRÈS (100 itérations) : {cost}")

# plt.figure(figsize=(10, 5))
# plt.plot(paliers, couts_palier, marker='s', color='blue', linewidth=2)
# plt.axhline(y=cost_glouton, color='gray', linestyle='--', label="Coût Glouton (Sans Recuit)")
# plt.axvline(x=1, color='red', linestyle=':', label="Ancienne version (Avant)")
# plt.axvline(x=100, color='green', linestyle=':', label="Nouvelle version (Après)")
# plt.title('Influence du nombre de voisins testés (Palier)')
# plt.xlabel('Itérations par palier')
# plt.ylabel('Coût final')
# plt.legend()
# plt.grid(True)
# plt.savefig(os.path.join(plots_folder, "avant_apres_palier.png"))
# plt.show()

# # ==========================================
# # GRAPHE 2 : Influence de Alpha (Refroidissement)
# # ==========================================
# print("\nTest 2 : Influence de Alpha")
# alphas = [0.80, 0.90, 0.95, 0.99, 0.999]
# couts_alpha = []

# for a in alphas:
#     _, cost, _ = simulated_annealing(dist_mat, tour_glouton, alpha=a, iter_par_palier=50)
#     couts_alpha.append(cost)

# plt.figure(figsize=(10, 5))
# plt.plot(alphas, couts_alpha, marker='o', color='red', linewidth=2)
# plt.axhline(y=cost_glouton, color='gray', linestyle='--', label="Coût Glouton")
# plt.title('Influence du facteur de refroidissement Alpha')
# plt.xlabel('Alpha (Proche de 1 = refroidissement lent)')
# plt.ylabel('Coût final')
# plt.legend()
# plt.grid(True)
# plt.savefig(os.path.join(plots_folder, "influence_alpha.png"))
# plt.show()

# # ==========================================
# # GRAPHE 3 : Influence de la Température Initiale
# # ==========================================
# print("\nTest 3 : Influence de la Température Initiale")
# temperatures = [10, 100, 1000, 5000, 10000]
# couts_temp = []

# for t in temperatures:
#     _, cost, _ = simulated_annealing(dist_mat, tour_glouton, T=t, alpha=0.95, iter_par_palier=50)
#     couts_temp.append(cost)

# plt.figure(figsize=(10, 5))
# plt.plot(temperatures, couts_temp, marker='^', color='green', linewidth=2)
# plt.axhline(y=cost_glouton, color='gray', linestyle='--', label="Coût Glouton")
# plt.xscale('log')
# plt.title('Influence de la Température Initiale (T0)')
# plt.xlabel('Température (Échelle Logarithmique)')
# plt.ylabel('Coût final')
# plt.legend()
# plt.grid(True)
# plt.savefig(os.path.join(plots_folder, "influence_T0.png"))
# plt.show()

# print("\nTous les graphiques ont été générés dans le dossier 'plots/' !")

import random
import math
import time
from algorithms.local import two_opt_swap

def simulated_annealing(distance_mat, initial_tour, T=1000, alpha=0.995, stopping_T=1e-3, iter_par_palier=100):
    """
    Recuit simulé pour améliorer un tour initial.
    
    :param distance_mat: matrice de distances
    :param initial_tour: tour initial (généré par le glouton)
    :param T: température initiale (très chaude pour explorer)
    :param alpha: facteur de refroidissement
    :param stopping_T: température finale d'arrêt
    :param iter_par_palier: nombre de voisins testés avant de baisser la température
    :return: meilleur tour, coût, temps d'exécution
    """
    # Initialisation avec la solution gloutonne
    current_tour = initial_tour[:]
    current_cost = sum(distance_mat[current_tour[i]][current_tour[i+1]] for i in range(len(current_tour)-1))
    
    # Mémoire du meilleur résultat global trouvé
    best_tour = current_tour[:]
    best_cost = current_cost
    
    start_time = time.time()
    
    # Boucle principale de refroidissement
    while T > stopping_T:
        
        # Palier d'équilibre : on teste plusieurs voisins à la même température
        for _ in range(iter_par_palier):
            # Tirage au sort de deux indices pour inverser un chemin
            i, k = sorted(random.sample(range(1, len(current_tour)-1), 2))
            
            # Création du voisin avec 2-opt
            new_tour = two_opt_swap(current_tour, i, k)
            
            # Calcul du coût du nouveau tour
            new_cost = sum(distance_mat[new_tour[j]][new_tour[j+1]] for j in range(len(new_tour)-1))
            
            # Différence de coût
            delta = new_cost - current_cost
            
            # Critère de Metropolis : on accepte si c'est meilleur (delta < 0) 
            # OU avec une certaine probabilité si c'est pire
            if delta < 0 or random.random() < math.exp(-delta / T):
                current_tour = new_tour
                current_cost = new_cost
                
                # Mise à jour du record absolu
                if current_cost < best_cost:
                    best_tour = current_tour[:]
                    best_cost = current_cost
                    
        # Refroidissement : on baisse la température APRÈS le palier
        T *= alpha
    
    elapsed = time.time() - start_time
    
    return best_tour, best_cost, elapsed