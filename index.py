##-------Bibliothèque-------
from fltk import *
import argparse

#-------Modules-------
from Fonctions.zoom_dezoom import zoom_dezoom
from Fonctions.boutons import *
from Fonctions.file_selector import file_selector

#-------Variables globales-------
final=[] # liste des couleurs et position de chaque pixel
filigrane = "Ne pas copier !"



cree_fenetre(1000,1000)

#Lecture du fichier
def lecture (fichier):
    global final 
    final = []
    if fichier != "NoFileSelected":
        with open(fichier) as f:
            txt = f.read()
            txt = txt.split()
            fenetre(txt,10)
    else :
        with open("./Images/image_par_defaut.ppm") as f:
            txt = f.read().split()
            fenetre(txt,10)

    #Création de la fenêtre et gestion des clics
def fenetre(fichier,zoom):
    if fichier.pop(0) == 'P3':
        mise_a_jour()
        x_max = int(fichier.pop(0))
        y_max = int(fichier.pop(0))
        del (fichier[0])
        couleur (fichier,x_max,y_max,zoom)
        pannel()
        mise_a_jour()
        
        while True:
            ev = donne_ev()
            tev = type_ev(ev)

            if tev == "ClicGauche":
                
                #Clic sur zoom/dezoom
                valeur = zoom_dezoom(abscisse(ev),ordonnee(ev),zoom,fichier,x_max,y_max)
                if valeur :
                    zoom = valeur[3]
                    couleur(valeur[0],valeur[1],valeur[2],valeur[3])
                    
                #Clic sur rouge
                if 760 <= abscisse(ev) <= 800 and 100 <= ordonnee(ev) <= 140:
                    lancerouge(final, zoom)

                #Clic sur vert
                elif 805 <= abscisse(ev) <= 845 and 100 <= ordonnee(ev) <= 140:
                    lancevert(final, zoom)

                #Clic sur bleu
                elif 850 <= abscisse(ev) <= 890 and 100 <= ordonnee(ev) <= 140:
                    lancebleu(final, zoom)
                
                #Application du filigrane
                elif 775 <= abscisse(ev) <= 875 and 150 <= ordonnee(ev) <= 190:
                    lancefiligrane(filigrane)

                #Retour à 0 (Effacer les modifs)
                elif 775 <= abscisse(ev) <= 875 and 200 <= ordonnee(ev) <= 240:
                    lanceretour(final, zoom)

                #Changer de fichier (selecteur de fichier)
                elif 750 <= abscisse(ev) <= 900 and 260 <= ordonnee(ev) <= 300:
                    selectedFile = file_selector()
                    if selectedFile != "NoFileSelected":
                        efface("image")
                        lecture(selectedFile)
                pannel()
                
            elif tev == 'Quitte':
                break
            else:
                pass

            mise_a_jour()

        #ferme_fenetre()

    else:
        return('Format P3 uniquement')


        #Récupération des couleurs et positions de chaque pixel
def couleur(tab,x_max,y_max,zoom):
    rgb=[] # liste temporaire des couleurs rgb du pixel i en hexadécimal
    cpt=0 # compteur pour localiser les couleurs du pixel
    
    for j in range (y_max):
        for i in range (x_max):
            rgb_i = [int(tab[3*cpt]),int(tab[3*cpt+1]),int(tab[3*cpt+2])]
            r,g,b= rgb_i
            rgb = "#{:02x}{:02x}{:02x}".format(r, g, b)
            cpt+=1
            final.append((rgb,(i,j)))
        
    affichage_im (final,zoom)


    #Affichage de l'image
def affichage_im (tab2,zoom):
    for color,(ax,ay) in tab2:
        ax= ax*zoom
        ay= ay*zoom
        bx= ax+zoom
        by= ay+zoom
        rectangle(ax,ay,bx,by,color,color, tag='image')

def main():
    parser = argparse.ArgumentParser(
        description="Afficheur d'image",
        epilog="Exemple d'utilisation: python main.py --image image.ppm --filigrane 'ne pas copier'"
    )
    parser.add_argument('--image', type=str, help="Chemin du fichier d'entrée")
    parser.add_argument('--filigrane', type=str, help="Le texte a afficher en filigrane")

    args = parser.parse_args()

    if args.filigrane:
        global filigrane
        filigrane = args.filigrane

    if args.image:
        lecture(args.image)
    else:
        lecture(file_selector())

if __name__ == "__main__":
    main()
