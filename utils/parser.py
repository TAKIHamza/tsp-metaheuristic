def read_tsplib(filename):
    """
    Lit une instance TSPLIB au format EUC_2D et retourne une liste de coordonnées [(x1,y1), ...]
    """
    coords = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        coord_section = False
        for line in lines:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                coord_section = True
                continue
            if line == "EOF":
                break
            if coord_section:
                parts = line.split()
                if len(parts) >= 3:
                    x = float(parts[1])
                    y = float(parts[2])
                    coords.append((x, y))
    return coords
