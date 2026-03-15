import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.parser import read_tsplib
from utils.distance import distance_matrix
from algorithms.glouton import nearest_neighbor
from algorithms.meta import simulated_annealing

# --------------------------
# 1. Préparation des dossiers
# --------------------------
instance_folder = "instances"
results_folder = "results"
plots_folder = "plots"

os.makedirs(results_folder, exist_ok=True)
os.makedirs(plots_folder, exist_ok=True)

csv_base = os.path.join(results_folder, "1_glouton_vs_meta.csv")
csv_iter = os.path.join(results_folder, "2_influence_iterations.csv")
csv_alpha = os.path.join(results_folder, "3_influence_alpha.csv")
csv_t0 = os.path.join(results_folder, "4_influence_T0.csv")

instances = [f for f in os.listdir(instance_folder) if f.endswith(".tsp")]

# --------------------------
# 2. Génération des CSV (Calculs)
# --------------------------
with open(csv_base, 'w', newline='') as f_base, \
     open(csv_iter, 'w', newline='') as f_iter, \
     open(csv_alpha, 'w', newline='') as f_alpha, \
     open(csv_t0, 'w', newline='') as f_t0:

    w_base = csv.writer(f_base, delimiter=';')
    w_iter = csv.writer(f_iter, delimiter=';')
    w_alpha = csv.writer(f_alpha, delimiter=';')
    w_t0 = csv.writer(f_t0, delimiter=';')

    w_base.writerow(["Instance", "Cout_Glouton", "Cout_Meta_Optimal", "Gain(%)"])
    w_iter.writerow(["Instance", "Cout_Avant", "Cout_Apres", "Amelioration(%)"])
    w_alpha.writerow(["Instance", "Cout_Avant", "Cout_Apres", "Amelioration(%)"])
    w_t0.writerow(["Instance", "Cout_Avant", "Cout_Apres", "Amelioration(%)"])

    for inst in instances:
        print(f"\n--- Traitement de {inst} ---")
        coords = read_tsplib(os.path.join(instance_folder, inst))
        dist_mat = distance_matrix(coords)

        # A. Base
        tour_g, cost_g, _ = nearest_neighbor(dist_mat)
        _, cost_opti, _ = simulated_annealing(dist_mat, tour_g, T=1000, alpha=0.995, iter_par_palier=100)
        gain_base = 100 * (cost_g - cost_opti) / cost_g
        w_base.writerow([inst, round(cost_g, 2), round(cost_opti, 2), round(gain_base, 2)])

        # B. Itérations (1 vs 100)
        _, cost_iter_1, _ = simulated_annealing(dist_mat, tour_g, T=1000, alpha=0.995, iter_par_palier=1)
        gain_iter = 100 * (cost_iter_1 - cost_opti) / cost_iter_1
        w_iter.writerow([inst, round(cost_iter_1, 2), round(cost_opti, 2), round(gain_iter, 2)])

        # C. Alpha (0.90 vs 0.995)
        _, cost_alpha_90, _ = simulated_annealing(dist_mat, tour_g, T=1000, alpha=0.90, iter_par_palier=100)
        gain_alpha = 100 * (cost_alpha_90 - cost_opti) / cost_alpha_90
        w_alpha.writerow([inst, round(cost_alpha_90, 2), round(cost_opti, 2), round(gain_alpha, 2)])

        # D. Température T0 (10 vs 1000)
        _, cost_t0_10, _ = simulated_annealing(dist_mat, tour_g, T=10, alpha=0.995, iter_par_palier=100)
        gain_t0 = 100 * (cost_t0_10 - cost_opti) / cost_t0_10
        w_t0.writerow([inst, round(cost_t0_10, 2), round(cost_opti, 2), round(gain_t0, 2)])

# --------------------------
# 3. Génération des Courbes (Plots)
# --------------------------
def tracer_courbes(csv_file, label_avant, label_apres, titre_base, prefixe):
    df = pd.read_csv(csv_file, delimiter=';')
    x = df['Instance']
    
    # --- GRAPHE DU COÛT ---
    plt.figure(figsize=(10,5))
    plt.plot(x, df.iloc[:, 1], marker='o', color='red', linestyle='--', label=label_avant)
    plt.plot(x, df.iloc[:, 2], marker='s', color='green', linewidth=2, label=label_apres)
    plt.xticks(rotation=45)
    plt.ylabel('Coût de la tournée')
    plt.title(f'Comparaison des Coûts : {titre_base}')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_folder, f"{prefixe}_cout.png"))
    plt.close()

    # --- GRAPHE DU GAIN ---
    plt.figure(figsize=(10,5))
    plt.plot(x, df.iloc[:, 3], marker='^', color='blue', linewidth=2, label='Gain / Amélioration (%)')
    plt.xticks(rotation=45)
    plt.ylabel('Gain (%)')
    plt.title(f'Amélioration obtenue : {titre_base}')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_folder, f"{prefixe}_gain.png"))
    plt.close()

# Appel de la fonction pour générer les 8 images
tracer_courbes(csv_base, 'Glouton (Base)', 'Recuit Simulé (Opti)', 'Glouton vs Métaheuristique', '1_glouton_vs_meta')
tracer_courbes(csv_iter, 'Avant (1 iter)', 'Après (100 iter)', 'Influence des Itérations', '2_iterations')
tracer_courbes(csv_alpha, 'Avant (Alpha=0.90)', 'Après (Alpha=0.995)', 'Influence de Alpha', '3_alpha')
tracer_courbes(csv_t0, 'Avant (T0=10)', 'Après (T0=1000)', 'Influence de la Température Initiale', '4_T0')

print("\n🚀 C'est terminé ! Vérifie ton dossier 'plots/' pour voir les 8 nouvelles courbes.")