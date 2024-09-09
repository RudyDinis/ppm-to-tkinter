# imports
from assets.fltk import *


def rgb_to_hex(rgb):
    r, g, b = rgb
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def new_frame(tableau):
    cree_fenetre(1700, 700)

    for (x, y), couleur in tableau:
        ax = x * 20
        ay = y * 20
        bx = ax + 20
        by = ay + 20
        rectangle(ax, ay, bx, by, couleur, couleur)

    attend_ev()
    ferme_fenetre()





def initialise_ppm(fileName):
    try:
        with open(fileName, "r") as f:
            # Variables
            lignes = f.readlines()
            typeImage = lignes[0].strip()
            dimensions = lignes[1].strip().split()
            
            # Vérification du format ppm
            if typeImage == "P6":
                print("format P6 non pris en charge")
            elif typeImage == "P3":
                pixels = []  # image finale en pixels
                rgb_count = 0  # compteur qui reviendra à 0
                temp_rgb = []  # tableau temporaire contenant des RGB
                
                width, height = (int(dimensions[0]), int(dimensions[1]))
                x, y = 0, 0
                
                # Rassembler toutes les valeurs RGB en une liste
                rgb_values = ' '.join(lignes[3:]).split()
                
                for value in rgb_values:
                    rgb_count += 1
                    temp_rgb.append(int(value))
                    
                    if rgb_count == 3:
                        if y < height:
                            pixels.append(((x, y), rgb_to_hex(tuple(temp_rgb))))
                        rgb_count = 0
                        temp_rgb = []
                        
                        x += 1
                        if x == width:
                            x = 0
                            y += 1
                
                new_frame(pixels)
                
    except FileNotFoundError:
        print(f"Le fichier '{fileName}' n'existe pas.")


    except FileNotFoundError:
        print(f"Le fichier '{fileName}' n'existe pas.")
