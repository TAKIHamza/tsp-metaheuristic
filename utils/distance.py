import math

def euclidean_distance(a, b):
    """Distance euclidienne entre deux points a=(x1,y1), b=(x2,y2) arrondie à l'entier"""
    return round(math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))

def distance_matrix(coords):
    """Crée une matrice de distance complète pour toutes les villes"""
    n = len(coords)
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = euclidean_distance(coords[i], coords[j])
    return matrix
