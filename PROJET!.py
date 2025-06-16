from turtle import *
import copy
import time
import math

#>>>>>>>> Partie A : plateau de jeu et listes <<<<<<<<

def init(n): # Initialise un plateau avec n disques sur la première tour.
    i = n  # i represente le numero du disque.
    source = []
    while i > 0:
        source.append(i)
        i -= 1
    plateau = [source, [], []]
    return plateau

def nbDisques(plateau, numtour):
    return len(plateau[numtour]) # Retourne le nombre de disques sur la tour spécifiée.

def disqueSup(plateau, numtour): # Retourne le disque supérieur sur la tour spécifiée, ou -1 si vide ou invalide.
    if numtour in range(3):
        tour = plateau[numtour]
        if tour == []:
            return -1
        else:
            return tour[-1] # Represente le dernier disque dans la liste de tour qui est le disque superieur.
    else:
        return -1

def posDisque(plateau, numdisque): #Retourne la tour sur laquelle se trouve le disque spécifié.
    for tour in range(3):
        if numdisque in plateau[tour]:
            return tour

def verifDepl(plateau, nt1, nt2): #Vérifie la validité du déplacement entre deux tours.
    if (plateau[nt1] != []) and ((disqueSup(plateau, nt1) < disqueSup(plateau, nt2)) or (disqueSup(plateau, nt2) == -1)):
        # Verifie que le tour de départ n'est pas vide et le disque de départ est plus petit que celle d'arrivée ou bien le tour d'arrivée est vide.
        return True
    else:
        return False

def verifVictoire(plateau, n): #Vérifie si la configuration actuelle du plateau correspond à une victoire.
    if plateau[2] == init(n)[0] and plateau[1] == [] and plateau[0] == []:
        return True
    else:
        return False



#>>>>>>>> Partie B: graphisme avec Turtle <<<<<<<<

def dessinePlateau(n): # Cette fonction dessine un plateau de jeu pour le jeu des Tours de Hanoï avec n disques.
    diametre = 40 + 30*(n-1) # Calcul du diamètre en fonction de n.
    up()
    color("black")
    goto(-320, -220)
    down()
    width(3)
    # Dessin de la base du plateau.
    for i in range(2):
        forward(3*diametre + 120)
        left(90)
        forward(447)
        left(90)
        begin_fill()
    width(1)
    color("MidnightBlue")
    up()
    goto(-300, -200)
    down()
    i = 2
    while i > 0:
        forward(3*diametre + 80)
        left(90)
        forward(20)
        left(90)
        i -= 1
    i = 3
    end_fill()
    up()
    left(90)
    forward(20)
    right(90)
    down()
    forward(17 + diametre/2)
    # Dessin des 3 tours du plateau.
    while i > 0:
        begin_fill()
        color("MidnightBlue")
        left(90)
        forward((21*(n+1))-1)
        right(90)
        forward(6)
        right(90)
        forward((21*(n+1))-1)
        left(90)
        end_fill()
        if i != 1:
            forward(diametre+14)
        else:
            forward(diametre/2 + 17)
        i -= 1

def dessineDisque(nd, plateau, n): # Cette fonction dessine un disque sur le plateau avec la couleur déterminée par son numéro (nd).
    diametre = 40 + 30*(nd-1)
    diametre_max = 40 + 30*(n-1) # Diamètre maximale représente le diamètre du disque numéro n.
    pos = posDisque(plateau, nd)
    rang = plateau[pos].index(nd) + 1
    colors = ["purple1", "blue1", "cyan1", "green1", "yellow1", "goldenrod1", "red1"] # La couleur du disque est déterminée par une liste prédéfinie de couleurs.
    up()
    goto((20*(pos+1))+(diametre_max*(pos+0.5))-300, (21*rang - 200))
    down()
    begin_fill()
    color(colors[7-nd])
    forward(diametre/2)
    left(90)
    forward(20)
    left(90)
    forward(diametre)
    left(90)
    forward(20)
    left(90)
    forward(diametre/2)
    end_fill()
    up()
    goto(-300, -200)

def effaceDisque(nd, plateau, n): # Cette fonction efface un disque du plateau en le recouvrant avec un rectangle de couleur du fond.
    diametre = 40 + 30 * (nd - 1)
    diametre_max = 40 + 30 * (n - 1)
    pos = posDisque(plateau, nd)
    rang = plateau[pos].index(nd) + 1
    up()
    goto((20 * (pos + 1)) + (diametre_max * (pos + 0.5)) - 300, (21*rang - 200))
    down()
    begin_fill()
    color("LightBlue1") # Couleur du fond.
    # Effacement du disque.
    forward(diametre / 2)
    left(90)
    forward(20)
    left(90)
    forward(diametre)
    left(90)
    forward(20)
    left(90)
    forward(diametre / 2)
    end_fill()
    up()
    # Redessinage du tour.
    begin_fill()
    color("MidnightBlue")
    forward(3)
    left(90)
    down()
    forward(20)
    left(90)
    forward(6)
    left(90)
    forward(20)
    left(90)
    forward(6)
    end_fill()
    up()
    goto(-300, -200)

def dessineConfig(plateau, n): # Cette fonction dessine l'ensemble des disques sur le plateau en utilisant la fonction dessineDisque().
    numdisque = n
    while numdisque > 0:
        dessineDisque(numdisque, plateau, n)
        numdisque -= 1

def effaceTout(plateau, n): # Efface tous les disques du plateau en appelant la fonction effaceDisque.
    # Parcourt tous les disques sur le plateau et les efface un par un
    for pos in range(len(plateau)):
        for nd in plateau[pos]:
            effaceDisque(nd, plateau, n)



#>>>>>>>> Partie C: interactions avec le joueur <<<<<<<<

def lireCoords(plateau): # Cette fonction permet à l'utilisateur de saisir les coordonnées pour un déplacement sur le plateau et vérifie la validité du mouvement.
    tours = [0, 1, 2]
    tours_i = list(tours)
    n = nbDisques(plateau, 0) + nbDisques(plateau, 1) + nbDisques(plateau, 2) # Calcul de nombre de disques en utilisant le plateau.
    x = 0
    y = 0
    n_depart = 1
    n_arrivee = -1
    commence = True # Drapeau pour rentrer dans la boucle.
    while n_depart not in range(-1, 3) or ((disqueSup(plateau, n_depart) > x) and (disqueSup(plateau, n_depart) > y)) or commence:
        commence = False
        n_depart = int(input("Tour de départ? (-1 pour abandonner) : "))
        tours = list(tours_i)
        if n_depart in range(3):
            tours.remove(n_depart)
        x = disqueSup(plateau, tours[0])
        if x == -1:
            x = n + 1
        y = disqueSup(plateau, tours[1])
        if y == -1:
            y = n + 1
        # Option d'abandonner.
        if n_depart == -1:
            abandonner = input("Tu souhaites abandonner (o/n)? ")
            if abandonner.lower() == "n":
                commence = True
        # Vérification des conditions de jeu.
        elif n_depart not in range(3):
            print("Tour invalide.")
        elif plateau[n_depart] == []:
            print("Invalide, tour vide.")
            commence = True
        elif disqueSup(plateau, n_depart) > x and disqueSup(plateau, n_depart) > y:
            print("Impossible de déplacer ce disque.")
    if n_depart != -1:
        while n_arrivee not in range(3) or verifDepl(plateau, n_depart, n_arrivee) != True:
            n_arrivee = int(input("Tour d’arrivée? : "))
            if verifDepl(plateau, n_depart, n_arrivee) != True:
                print("Invalide, disque plus petit.")
            elif n_arrivee not in range(3):
                print("Tour invalide.")
        return [n_depart, n_arrivee]
    else:
        return n_depart  # la valeur de n_depart ici = -1

def jouerUnCoup(plateau,n): # Cette fonction coordonne un coup dans le jeu. Elle appelle lireCoords() pour obtenir les coordonnées du déplacement.
    deplacement = lireCoords(plateau) # La valeur de deplacement et soit une liste des deux tours ou -1.
    if deplacement == -1:
        return -1
    else: # Si deplacement est égale à la liste des deux tours.
        print("Je déplace le disque", disqueSup(plateau,deplacement[0]), "de la tour", deplacement[0], "à la tour", deplacement[1])
        effaceDisque(disqueSup(plateau,deplacement[0]), plateau, n)
        plateau[deplacement[1]].append(plateau[deplacement[0]][-1])
        plateau[deplacement[0]].pop(-1)
        dessineDisque(disqueSup(plateau,deplacement[1]), plateau, n)

def boucleJeu(plateau,n): # Cette fonction gère la boucle principale du jeu des Tours de Hanoï.
    compteur = 0
    essais = 2**n + n
    x = 0
    coups = {0: init(n)} # Premiere position des disques.
    debut_jeu = time.time() # Compteur du temps (debut).
    diametre = 40 + 30 * (n - 1)
    while verifVictoire(plateau, n) != True and x != -1:
        print("Coup numéro", compteur+1)
        up()
        goto(-325+(3*diametre +80)/2, 10)
        down()
        # Ecriture sur l'ecran de jeu le numero de coup.
        color("LightBlue1")
        begin_fill()
        for i in range(4):
            forward(100)
            left(90)
        end_fill()
        color("DarkViolet")
        write("Coup " + str(compteur+1), font=("calibri", 15, "bold"))
        up()
        goto(-300,-200)
        down()
        x = jouerUnCoup(plateau, n)
        compteur += 1
        coups[compteur] = copy.deepcopy(plateau)
        if x != -1 and not verifVictoire(plateau, n):
            # Option d'annuler le dernier coup.
            annuler = input("Voulez vous annuler ce coup? (o/n) ")
            if annuler.lower() == "o":
                annulerDernierCoup(coups)
                dern = max(list(coups.keys()))
                plateau = copy.deepcopy(list(coups[dern]))
                compteur -= 1
    temps_jeu = round((time.time() - debut_jeu)*10)/10
    essais -= compteur
    # Traitement des différentes cas après le fin de jeu.
    if x == -1:
        print("Abandon de la partie après", compteur-1, "coups.","\n"+"Temps de jeu :", temps_jeu, "secondes")
        print("Au-revoir.")
        return False, compteur, temps_jeu
    elif essais < 0:
        print("Perdu, nombre de coups optimal :", 2 ** n - 1, "Ton nombre de coups :", compteur, "\n"+"Temps de jeu :", temps_jeu, "secondes")
        print("Au-revoir.")
        return False, compteur, temps_jeu
    elif essais >= 0:
        print("Gagné, nombre de coups optimal :", 2 ** n - 1, "Ton nombre de coups :", compteur, "\n"+"Temps de jeu :", temps_jeu, "secondes")
        print("Au-revoir.")
        return True, compteur, temps_jeu



#>>>>>>>> Partie D: annulation de coups <<<<<<<<

def dernierCoup(coups): # Cette fonction détermine les détails du dernier coup joué en parcourant les clés du dictionnaire 'coups'.
    dern = max(list(coups.keys()))
    av_dern = dern - 1
    for i in range(3): # Comparaison des configurations avant et après le dernier coup pour trouver les tours de départ et d'arrivée,
        if len(coups[dern][i]) > len(coups[av_dern][i]):
            arrivee = i
        elif len(coups[dern][i]) < len(coups[av_dern][i]):
            depart = i
    return depart, arrivee, dern, av_dern

def annulerDernierCoup(coups): # Cette fonction annule le dernier coup joué en utilisant les informations fournies par la fonction dernierCoup().
    depart, arrivee, dern, av_dern = dernierCoup(coups)
    maxi = 0
    for i in coups[dern]:
        for d in i:
            if maxi < d:
                maxi = d
    effaceDisque(disqueSup(coups[dern], arrivee), coups[dern], maxi)
    dessineDisque(disqueSup(coups[av_dern], depart), coups[av_dern], maxi)
    del(coups[dern]) # Modification du dictionnaire comme avant le coup annulé.



#>>>>>>>> Partie E: comparaison des scores et temps de jeu <<<<<<<<

def sauvScore(nom, n, n_coups, scores): # Cette fonction sauvegarde un score dans le dictionnaire 'scores'.
    if n not in scores: # Si la configuration (n) n'existe pas dans 'scores', elle l'ajoute avec le nom du joueur et le nombre de coups.
        scores[n] = {nom: [n_coups]}
    else:
        if nom in scores[n]: # Si la configuration existe, elle met à jour le nombre de coups du joueur.
            scores[n][nom].append(n_coups)
        else:
            scores[n][nom] = [n_coups]
    # La structure du dictionnaire est {n: {nom_joueur: [n_coups_1, n_coups_2,...etc]}}.

def afficheScores(scores): # Cette fonction affiche le tableau des scores.
    coups = {} # Création d'un nouveau dictionnaire qui reorganise les informations du dictionnaire scores.
    for i in scores:
        coups[i] = []
        for p in scores[i]:
            for c in scores[i][p]:
                coups[i].append([p, c])
    maxi = 0 # Maximum nombre de lignes dans le tableau.
    for i in coups:
        if maxi < len(coups[i]):
            maxi = len(coups[i])
    clear()
    # Dessin de l'encadrement du page.
    color("MidnightBlue")
    up()
    goto(-355, -(((maxi + 1) * 50) + 55))
    down()
    width(3)
    for i in range(2):
        forward(3 * (len(scores) * 50) + 120)
        left(90)
        forward(240 + 50*(maxi+1))
        left(90)
        begin_fill()
    width(1)
    up()
    # Affichage.
    goto(-300+(((len(scores)*150) - 270)/2), 90)
    color("DeepPink")
    write("Bien joué", font=('Courier', 50, 'italic'))
    goto(-300+(((len(scores)*150) - 330)/2), 10)
    color("DarkGreen")
    write(" Tableau de coups ", font=("calibri", 40, "italic"))
    goto(-300, 0)
    down()
    width(2)
    #Dessin du tableau.
    for i in range(2):
        forward(len(scores)*150)
        right(90)
        forward(50+(maxi*50))
        right(90)
    for i in range(len(scores)-1):
        up()
        forward(150)
        down()
        right(90)
        forward(50 + (maxi * 50))
        up()
        back(50 + (maxi * 50))
        left(90)
    goto(-300, 0)
    for i in range(maxi):
        right(90)
        forward(50)
        left(90)
        down()
        forward(len(scores) * 150)
        up()
        back(len(scores) * 150)
    n = 0
    width(1)
    # Ecriture dans le tableau.
    for i in coups:
        color("DarkGreen")
        goto(-278+((n)*150), -38)
        write(str(i)+" disques", font=("calibri", 25, "normal"))
        sorted_list = sorted(coups[i], key=lambda x: x[1])
        n += 1
        for c in sorted_list:
            color("red1")
            goto(-300+((n-1)*150)+10, -35-(50*(sorted_list.index(c)+1)))
            write(c[0]+": "+str(c[1])+" coups", font=("calibri", 20, "normal"))

def afficheChronos(chronos): # Cette fonction affiche le tableau des chronos.
    temps = {} # Création d'un nouveau dictionnaire qui reorganise les informations du dictionnaire chronos.
    for i in chronos:
        temps[i] = []
        for p in chronos[i]:
            for c in chronos[i][p]:
                temps[i].append([p, c])
    maxi = 0 # Maximum nombre de lignes dans le tableau.
    for i in temps:
        if maxi < len(temps[i]):
            maxi = len(temps[i])
    clear()
    # Dessin de l'encadrement du page.
    color("MidnightBlue")
    up()
    goto(-355, -(((maxi + 1) * 50) + 55))
    down()
    width(3)
    for i in range(2):
        forward(3 * (len(chronos) * 50) + 120)
        left(90)
        forward(240 + 50*(maxi+1))
        left(90)
        begin_fill()
    width(1)
    up()
    # Affichage.
    goto(-300 + (((len(chronos) * 150) -270) / 2), 90)
    color("DeepPink")
    write("Bien joué", font=('Courier', 50, 'italic'))
    goto(-300 + (((len(chronos) * 150) - 360) / 2), 10)
    color("DarkGreen")
    write(" Tableau de chronos ", font=("calibri", 40, "italic"))
    goto(-300, 0)
    down()
    width(2)
    # Dessin du tableau.
    for i in range(2):
        forward(len(chronos) * 150)
        right(90)
        forward(50 + (maxi * 50))
        right(90)
    for i in range(len(chronos) - 1):
        up()
        forward(150)
        down()
        right(90)
        forward(50 + (maxi * 50))
        up()
        back(50 + (maxi * 50))
        left(90)
    goto(-300, 0)
    for i in range(maxi):
        right(90)
        forward(50)
        left(90)
        down()
        forward(len(chronos) * 150)
        up()
        back(len(chronos) * 150)
    n = 0
    width(1)
    # Ecriture dans le tableau.
    for i in temps:
        color("DarkGreen")
        goto(-278 + ((n) * 150), -38)
        write(str(i) + " disques", font=("calibri", 25, "normal"))
        sorted_list = sorted(temps[i], key=lambda x: x[1])
        n += 1
        for c in sorted_list:
            color("red1")
            goto(-300 + ((n - 1) * 150) + 10, -35 - (50 * (sorted_list.index(c) + 1)))
            write(c[0] + ": " + str(c[1]) + " sec", font=("calibri", 20, "normal"))

def reflexionMoy(n, nom, moy, classements): # Cette fonction met à jour la moyenne des temps de réflexion pour un joueur et une configuration donnés.
    if n in classements: # Si la configuration existe, elle met à jour la moyenne des temps de réflexion.
        if nom in classements[n]:
            classements[n][nom] = (classements[n][nom] + moy)/2
        else :
            classements[n][nom] = moy
    else: # Si la configuration n'existe pas dans 'classements', elle l'ajoute avec le nom du joueur et la moyenne.
        classements[n] = {nom: moy}
    return classements[n][nom] # Elle renvoie la moyenne mise à jour.
    # La structure du dictionnaire est {n: {nom_joueur: moyenne_temps_reflexion}}.

def afficheClassements(classements): # Cette fonction affiche le tableau des classements.
    ordre = {} # Création d'un nouveau dictionnaire qui reorganise les informations du dictionnaire classements.
    for i in classements:
        ordre[i] = []
        for p in classements[i]:
            ordre[i].append([p, classements[i][p]])
    maxi = 0 # Maximum nombre de lignes dans le tableau.
    for i in ordre:
        if maxi < len(ordre[i]):
            maxi = len(ordre[i])
    clear()
    # Dessin de l'encadrement du page.
    color("MidnightBlue")
    up()
    goto(-355, -(((maxi + 1) * 50) + 55))
    down()
    width(3)
    for i in range(2):
        forward(3 * (len(classements) * 50) + 120)
        left(90)
        forward(240 + 50*(maxi+1))
        left(90)
        begin_fill()
    width(1)
    up()
    # Affichage.
    goto(-300 + (((len(classements) * 150) - 270) / 2), 90)
    color("DeepPink")
    write("Bien joué", font=('Courier', 50, 'italic'))
    goto(-300 + (((len(classements) * 150) - 440) / 2), 10)
    color("DarkGreen")
    write(" Tableau de classements ", font=("calibri", 40, "italic"))
    goto(-300, 0)
    down()
    width(2)
    # Dessin du tableau.
    for i in range(2):
        forward(len(classements) * 150)
        right(90)
        forward(50 + (maxi * 50))
        right(90)
    for i in range(len(classements) - 1):
        up()
        forward(150)
        down()
        right(90)
        forward(50 + (maxi * 50))
        up()
        back(50 + (maxi * 50))
        left(90)
    goto(-300, 0)
    for i in range(maxi):
        right(90)
        forward(50)
        left(90)
        down()
        forward(len(classements) * 150)
        up()
        back(len(classements) * 150)
    n = 0
    width(1)
    # Ecriture dans le tableau.
    for i in ordre:
        color("DarkGreen")
        goto(-278 + ((n) * 150), -38)
        write(str(i) + " disques", font=("calibri", 25, "normal"))
        sorted_list = sorted(ordre[i], key=lambda x: x[1])
        n += 1
        for l in range(len(sorted_list)):
            color("red1")
            goto(-300 + ((n - 1) * 150) + 10, -35 - (50 * (l + 1)))
            write(sorted_list[l][0] + ": " + str(round(sorted_list[l][1]*10)/10) + " sec", font=("calibri", 20, "normal"))



#>>>>>>>> Partie F: jeu automatique, fonction récursive <<<<<<<<

def resout(n, i=0, j=2, k=1, m=None):
    # Cette fonction résout les Tours de Hanoï pour n disques.
    # Elle utilise une approche récursive où elle déplace n-1 disques de la source à l'auxiliaire, puis déplace le disque restant de la source à la destination,
    # et enfin déplace les n-1 disques de l'auxiliaire à la destination. Les mouvements sont enregistrés dans la liste 'mouvements'.
    if m == None:
        m = []
    if n == 1:
        m.append([i, j])
    else:
        resout(n-1, i, k, j, m)
        resout(1, i, j, k, m)
        resout(n-1, k, j, i, m)
    return m # La configuration finale est renvoyée sous la forme d'une liste de mouvements.

def animation(mouvements): # Cette fonction anime la résolution du puzzle des Tours de Hanoï en utilisant les mouvements fournis.
    n = int(math.log(len(mouvements)+1, 2)) # Calcul du nombre de disques.
    # Elle initialise le plateau, dessine le plateau initial et la configuration de départ.
    plateau = init(n)
    dessinePlateau(n)
    dessineConfig(plateau, n)
    diametre = 40 + 30 * (n - 1)
    compteur = 0
    for i in mouvements: # Ensuite, elle parcourt la liste de mouvements et affiche chaque déplacement avec une animation.
        deplacement = i
        print("Je déplace le disque", disqueSup(plateau, deplacement[0]), "de la tour", deplacement[0], "à la tour", deplacement[1])
        up()
        goto(-325 + (3 * diametre + 80) / 2, 10)
        down()
        color("LightBlue1")
        begin_fill()
        for i in range(4):
            forward(100)
            left(90)
        end_fill()
        color("DarkViolet")
        write("Coup " + str(compteur + 1), font=("calibri", 15, "bold"))
        up()
        goto(-300, -200)
        compteur += 1
        down()
        effaceDisque(disqueSup(plateau, deplacement[0]), plateau, n)
        plateau[deplacement[1]].append(plateau[deplacement[0]][-1])
        plateau[deplacement[0]].pop(-1)
        dessineDisque(disqueSup(plateau, deplacement[1]), plateau, n)


if __name__ == '__main__':
    # Initialisation de la vitesse du dessin et de la couleur de fond
    speed(9999)
    bgcolor("LightBlue1")
    # Affichage du message de bienvenue
    write('Bienvenue dans Les tours de Hanoi'"\n""Appuyez n'importe où pour jouer", font=('Courier', 20, 'italic'), align='center')
    print("Bienvenue dans les Tours de Hanoi")
    def game(x, y):
        # Efface le contenu actuel de la fenêtre
        clear()
        # Initialisation des dictionnaires pour les scores, chronos et classements
        scores = {}
        chronos = {}
        classements = {}
        # Variable de contrôle pour rejouer
        rejouer = True
        while rejouer:
            # Saisie du nombre de disques
            n = int(input("Combien de disques? "))
            # Initialisation du plateau et affichage initial
            plateau = init(n)
            dessinePlateau(n)
            dessineConfig(plateau, n)
            # Boucle de jeu
            booleene, n_coups, chrono = boucleJeu(plateau, n)
            # Traitement des résultats du jeu
            if booleene == True:
                nom = input("Quel est ton nom? : ")
                sauvScore(nom, n, n_coups, scores)
                sauvScore(nom, n, chrono, chronos)
                classements[n][nom] = reflexionMoy(n, nom, chrono/n_coups, classements)
            # Option pour voir la solution animée
            resolut = input("Voir solution? (o/n): ")
            if resolut.lower() == "o":
                clear()
                animation(resout(n))
            # Option pour rejouer
            demande = input("Jouer encore? (o/n): ")
            if demande.lower() == "n":
                rejouer = False
                rep = 1
                # Affichage des tableaux demandés par l'utilisateur
                while rep in range(1, 4):
                    rep = int(input("Pour afficher : "+"\n"+" Tableau de coups entrer (1)"+"\n"+" Tableau de chronos entrer (2)"+"\n"+" Tableau de classement entrer (3)"+"\n"+"Pour terminer entrer (-1) "))
                    scores = dict(sorted(scores.items()))
                    chronos = dict(sorted(chronos.items()))
                    classements = dict(sorted(classements.items()))
                    if rep == 1:
                        afficheScores(scores)
                    elif rep == 2:
                        afficheChronos(chronos)
                    elif rep == 3:
                        afficheClassements(classements)
            # Option pour terminer le programme
            elif demande.lower() != "o":
                while demande.lower() != "o" or demande.lower() != "n":
                    if demande.lower() == "n":
                        rejouer = False
                        rep = 1
                        while (rep in range(1, 4)):
                            rep = int(input("Pour afficher : " + "\n" + " Tableau de coups entrer (1)" + "\n" + " Tableau de chronos entrer (2)" + "\n" + " Tableau de classement entrer (3)" + "\n" + "Pour terminer entrer (-1) "))
                            scores = dict(sorted(scores.items()))
                            chronos = dict(sorted(chronos.items()))
                            classements = dict(sorted(classements.items()))
                            if rep == 1:
                                afficheScores(scores)
                            elif rep == 2:
                                afficheChronos(chronos)
                            elif rep == 3:
                                afficheClassements(classements)
            if demande.lower() == "o":
                clear()
    # Attente du clic pour démarrer le jeu
    onscreenclick(game)
    mainloop()
