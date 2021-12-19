"""
Auteur : Traore Amara
matricule : 000542150
section : BA1-info 
Date : 13/12/21
Titre du jeu : jeu du Breakthrough  
Entrer : i(haut) ,j(gauche) ,k(bas) , l(droite), y(confirmafion du pion choisie)  
Sortie : plateau de jeu avec les différents mouvement des joueurs
"""

import os, sys
from random import choice

def winner(board):
    """
    Vérifie si l'un des deux joueur à gagné la partie
    """
    n = len(board)
    if 1 in board[0]: # Cas ou les blancs gagne
        gagnant = 1
    elif 2 in board[n-1]: # Cas ou les noirs gagne 
        gagnant = 2
    else:
        gagnant = None # Cas ou il n'y a pas de gagnant ou pas encore(partie pas encore terminé)
    return gagnant

def extract_pos(n, str_pos):
    """
    Traduit les positions des pions enregistré 
    dans le fichier texte en position de matrice
    """
    cpt = 1 
    capital = "a"
    while capital != str_pos[0]:
        cpt += 1
        capital = chr(ord(capital)+1)
    colonne = cpt - 1 # Colonne
    ligne = n - int(str_pos[1:]) # Ligne 
    return (ligne, colonne)

def init_board(file):
    """
    Permet de créer la matrice représentant le plateau 
    """
    matrice = []
    if type(file) == int or file == None: # Plateau par defaut (7 * 7)
        n = 7
        matrice = []
        for plateau in range(n):
            el = []
            for i in range(n):
                if plateau == 0 or plateau == 1: # Placement des pions noirs 
                    el.append(2)
                elif plateau == n-2 or plateau == n-1: # Placement des pions blanc 
                    el.append(1)
                else: # Placement des case vide 
                    el.append(0)
            matrice.append(el)
    else: # Cas ou la taille du plateau est donner par un fichier texte 
        fichier = open(file, encoding="utf-8")
        lignes = fichier.readlines() # Lecture ligne par ligne du fichier texte 
        nb_ligne = len(lignes)
        
        # Création de la matrice
        taille_plateau = lignes[0].strip("\n")
        taille_plateau = taille_plateau.split(" ")
        n = int(taille_plateau[0]) # Nombre de ligne dans le plateau 
        m = int(taille_plateau[1]) # Nombre de collone dans le plateau
        for matrice_1 in range(n):
            el = []
            for matrice_2 in range(m):
                el.append(0)
            matrice.append(el)
    
        # Positionnement des pions blanc 
        ligne2 = lignes[1].split(",")
        for pos_w in ligne2:
            pos = extract_pos(n, pos_w) # Convertie la position dans le fichier en position matriciel
            matrice[pos[0]][pos[1]] = 1
        
        # Positionnement des pions noir
        ligne2 = lignes[2].split(",")
        for pos_w in ligne2:
            pos = extract_pos(n, pos_w) # Convertie la position dans le fichier en position matriciel
            matrice[pos[0]][pos[1]] = 2
    return matrice
        
    
def print_board(board):
    """Affiche la matrice dans le terminal"""
    m = len(board) # Longeur de la matrice (plateau)
    n = len(board[0])
    print(" "*5 + n*"— ")
    for i in range(m):
        if n-i <= 9: # Cas ou le plateau ferai inférieur ou égale à 9
            print(" "+str(m-i)+" "+"|",end=" ")
        else:
            print(str(n-i)+" "+"|",end=" ")
        for j in range(len(board[i])): # 
            if board[i][j] == 1: # Placement des pions blancs
                print("W", end=" ")
            elif board[i][j] == 0: # Cas ou il n'y a pas de pion à cette position là en début de partie 
                print(".", end=" ")
            elif board[i][j] == 3: # Marque que le pion peu être sellectionner ou marque les position d'arriver du pion selectionner 
                print("#", end=" ")
            elif board[i][j] == 4: # Marque la position d'arrivé
                print("@", end=" ")
            else: # Placement des pionts noir 
                print("B", end=" ")
        print("|")
    print(" "*5 + n*"— ")
    print(" "*5,end="")
    for k in range(n):
        print(chr(ord("a")+k), end=" ") # Affichage des différentes lettres(représente les colonnes)
    print()

def ai_select_peg(board, player):
    """
    L'ia selectionne le pion le plus proche de la victoire
    et qui est capable de bouger capable bouger
    """
    if player == 1:
        DEBUT, FIN, PAS = 0, len(board), 1 # Cas ou l'ai serait les blancs
    else:
        DEBUT, FIN, PAS = len(board)-1, 0, -1 # Cas ou l'ai serait les noirs  
    verificateur = 0
    pion = []
    for i in range(DEBUT, FIN, PAS):
        for j in range(len(board[0])):
            if board[i][j] == player:
                jouable = jouabilite(board, (i, j), player) # Vérifie si le pion est jouable (boujeable)
                if jouable == True:
                    pion.append((i, j)) # Liste contenant tout les pions d'une même ligne
                    verificateur = 1 # Permet de return le premier pion jouable
        if len(pion) != 0:
            res = choice(pion) # Choisie un pion de manière alèatoire quand plusieur pion son sur la même ligne
        else:
            pass 
        if verificateur == 1:
            return res 
    
def is_in_board(board, t):
    """
    Permet de savoir si un tuple de
     position est dans la matrice 
    """
    board = len(board)
    if 0<= t[0]< board and 0<= t[1]< board:
        res = True # La position est présente dans la matrice
    else:
        res = False # La position n'est pas présente dans la matrice
    return res
    
def jouabilite(plateau, t, player):
    """
    Renvoie vrai ou faux en fonction de si le
    pion sélectionner est capable de bouger 
    """
    move_avant, move_dia_gauche, move_dia_droit = False, False, False # Initialise tout les mouvement de pion a faux 
    if player == 2: # Joueur 2 
        if is_in_board(plateau, (t[0]+1, t[1])):
            move_avant = plateau[t[0]+1][t[1]] == 0 # Met le move_avant à vrai si les position donné à is_in_board son prèsent dans la matrice et que celle-ci est vide (0) 
        if is_in_board(plateau, (t[0]+1, t[1]-1)):
            move_dia_gauche = plateau[t[0]+1][t[1]-1] == 0 or plateau[t[0]+1][t[1]-1] == 1 # Met le move_dia_gauche à vrai si les position donné à is_in_board son prèsent dans la matrice et que celle-ci est vide (0) ou occupé par l'adversaire (1)
        if is_in_board(plateau, (t[0]+1, t[1]+1)):
            move_dia_droit = plateau[t[0]+1][t[1]+1] == 0 or plateau[t[0]+1][t[1]+1] == 1 # Met le move_dia_droit à vrai si les position donné à is_in_board son prèsent dans la matrice et que celle-ci est vide (0) ou occupé par l'adversaire (1)
    else: # Joueur 1 
        if is_in_board(plateau, (t[0]-1, t[1])):
            move_avant = plateau[t[0]-1][t[1]] == 0 # Met le move_avant à vrai si les position donné à is_in_board son prèsent dans la matrice et que celle-ci est vide (0) 
        if is_in_board(plateau, (t[0]-1, t[1]-1)):
            move_dia_gauche = plateau[t[0]-1][t[1]-1] == 0 or plateau[t[0]-1][t[1]-1] == 2 # Met le move_dia_gauche à vrai si les position donné à is_in_board son prèsent dans la matrice et que celle-ci est vide (0) ou occupé par l'adversaire (2)
        if is_in_board(plateau, (t[0]-1, t[1]+1)):
            move_dia_droit = plateau[t[0]-1][t[1]+1] == 0 or plateau[t[0]-1][t[1]+1] == 2 # Met le move_dia_droit à vrai si les position donné à is_in_board son prèsent dans la matrice et que celle-ci est vide (0) ou occupé par l'adversaire (2)
    res = move_avant or move_dia_gauche or move_dia_droit
    return res 

def ai_move(board, pos, player):
    """
    Sélectionne de manière aléatiore la position
    d'arriverdu pion choisie dans ai_select_peg
    et return la positionde dépard et d'arriver du pion
    """
    liste_ia_move = [] # Création d'une liste qui contiendra tout les coup jouable par l'ia
    if player == 2: # Cas ou l'ia serait le joueur 2 
        move_1, move_2, move_3 = (pos[0]+1,pos[1]), (pos[0]+1,pos[1]+1), (pos[0]+1,pos[1]-1)
    else: # Cas ou l'ia serait le joueur 1
        move_1, move_2, move_3 = (pos[0]-1,pos[1]), (pos[0]-1,pos[1]-1), (pos[0]-1,pos[1]+1)

    coup_avant, coup_dia_d, coup_dia_g = False, False, False # Initialise tout les mouvement de pion a faux
    if 0 <= move_1[0] <= len(board) and 0 <= move_1[1] <= len(board):
        coup_avant = board[move_1[0]][move_1[1]] == 0 # Check que la case devant le pion choisie soit jouable
    if is_in_board(board, (pos[0]+1,pos[1]-1)):
        if 0 <= move_2[0] <= len(board) and 0 <= move_2[1] <= len(board):
            coup_dia_g = board[move_2[0]][move_2[1]] != player # Check que la case en diagonale gauche soit différent de un de c'est pion  
    if is_in_board(board, (pos[0]+1,pos[1]-1)):
        if 0 <= move_3[0] <= len(board) and 0 <= move_3[1] <= len(board):
            coup_dia_d = board[move_3[0]][move_3[1]] != player # Check que la case en diagonale droit soit différent de un de c'est pion
            
    # Liste contenant tout les positions jouable
    if coup_avant == True:
        liste_ia_move.append(move_1)
    if coup_dia_d == True:
        liste_ia_move.append(move_2)
    if coup_dia_g == True:
        liste_ia_move.append(move_3)
    return pos, (choice(sorted(liste_ia_move)))

def select_peg_pion(board, player, DEBUT, FIN, PAS):
    """
    Sélectionne le pion le plus proche de la victoire (joueur)
    """
    for i in range(DEBUT, FIN, PAS):
        for j in range(len(board[0])):
            if board[i][j] == player:
                jouable = jouabilite(board, (i, j), player) # Check si le pion est jouable (bougeable)
                if jouable == True:
                    return i, j

def reverse_manhattan(liste, pos, choix):
    """
    Renvoie la position du pion potentiellement sélectionner 
    """
    cpt = 0
    controle = 0
    for i in liste:
        for j in i:
            if controle == 0:
                if pos == j[1]:
                    index_pos = cpt # Permet de trouver l'indice de la sous liste dans laquelle se trouve le pion
                    controle = 1 
        cpt += 1
    if choix == "i": # Mouvement vers le haut 
        index_new_pos = (index_pos - 1) % len(liste) # Donne l'indice de la prochaine sous liste dans laquelle on doit chercher le prochain pion
    else: # Mouvement vers le bas 
        index_new_pos = (index_pos + 1) % len(liste) # Donne l'indice de la prochaine sous liste dans laquelle on doit chercher le prochain pion
    plus_proche = liste[index_new_pos][0] 
    for i in liste[index_new_pos]:
        if i[0] < plus_proche[0]:
            plus_proche = i # Nous donne le pion le plus proche du pion potentiellement sélectionner
    return plus_proche[1]

def input_select_peg(board, player):
    """
    Renvoie la position du pion sélectionner 
    """
    if player == 1: # Joueur 1 
        DEBUT, FIN, PAS = 0, len(board), 1
    else: # joueur 2 
        DEBUT, FIN, PAS = len(board)-1, 0, -1
    pion_select = select_peg_pion(board, player, DEBUT, FIN, PAS) # Donne la position du pion le plus proche de la victoire 
    board[pion_select[0]][pion_select[1]] = 3 # Change le pion le plus proche de la victoire en "#" pour pouvoir le repèrer
    print_board(board)

    # Cas ou le joueur veux choisir un autre pion
    print("Le y pour selectionner")
    print("Le l pour aller à droite")
    print("Le j pour aller à gauche")
    print("Le i pour aller à en haut")
    print("Le k pour aller à en bas")
    choix = input("Voulez vous sélectionner se pion : ")
    
    res = pion_select[:]
    while choix != "y":
        
        # Deplacement droite (l)
        board[res[0]][res[1]] = player
        if choix == "l":
            res = deplacement_droit(board, res, player)
            
        # Deplacement gauche (j)
        if choix == "j":
            res = deplacement_gauche(board, res, player)
           
        # Deplacement haut (i)
        if choix == "i":
            res = deplacement_haut(board, res, player, DEBUT, FIN, PAS)

        # Deplacement bas (k)
        if choix == "k":
            res = deplacement_bas(board, res, player, DEBUT, FIN, PAS)
        
        if choix != "i" and choix != "j" and choix != "k" and choix != "l":
            board[pion_select[0]][pion_select[1]] = 3
            print_board(board)

        print_board(board)
        print("Le y pour selectionner")
        print("Le l pour aller à droite")
        print("Le j pour aller à gauche")
        print("Le i pour aller à en haut")
        print("Le k pour aller à en bas")
        choix = input("entrer votre deplacement : ")
        
    board[res[0]][res[1]] = player # Redonne l'encienne apparence de pion 
    return res

def deplacement_droit(board, emplacement, player):
    """
    Deplacement à droite (l)
    """
    cpt = 1
    while board[emplacement[0]][(emplacement[1]+cpt) % len(board[0])] != player:
        cpt += 1
    board[emplacement[0]][(emplacement[1]+cpt) % len(board[0])] = 3 # Change le nouveau pion selectionner en "#" 
    emplacement = emplacement[0], (emplacement[1] + cpt ) % len(board[0]) # Position du nouveau pion potentielement selectionner
    return emplacement

def deplacement_gauche(board, emplacement, player):
    """
    Deplacement à gauche (l)
    """
    cpt = 1
    while board[emplacement[0]][(emplacement[1]-cpt) % len(board[0])] != player:
        cpt -= 1
    board[emplacement[0]][(emplacement[1]-cpt) % len(board[0])] = 3 # Change le nouveau pion selectionner en "#" 
    emplacement = emplacement[0], (emplacement[1] - cpt) % len(board[0]) # Position du nouveau pion potentielement selectionner
    return emplacement

def deplacement_haut(board, emplacement, player, DEBUT, FIN, PAS):
    """
    Deplacement en haut (i)
    """
    liste_vertical_1 = [] # Liste qui contiendra des sous liste de tout les pions jouable du plateau
    for i in range(DEBUT, FIN, PAS):
        liste_vertical_2 = [] # Liste contenant les pions jouablle d'une ligne
        for j in range(len(board[0])):
            if (board[i][j] == player or board[i][j] == 3):
                if jouabilite(board, (i,j), 1) == True: # Vérifie si le pion est jouable
                    pos_arriver = (i , j)
                    d_m = abs(pos_arriver[0] - emplacement[0]) + abs(pos_arriver[1] - emplacement[1]) # Calcul la distance manhattan
                    liste_vertical_2.append((d_m ,(i, j)))
        if len(liste_vertical_2) > 0:
            liste_vertical_1.append(liste_vertical_2)
    manhattan = reverse_manhattan(liste_vertical_1, emplacement, "i")
    board[manhattan[0]][manhattan[1]] = 3 # Change le nouveau pion selectionner en "#" 
    emplacement = manhattan # Position du nouveau pion potentielement selectionner
    return emplacement

def deplacement_bas(board, emplacement, player, DEBUT, FIN, PAS):
    """
    Deplacement en bas
    """
    liste_vertical_1 = [] # Liste qui contiendra des sous liste de tout les pions jouable du plateau
    for i in range(DEBUT, FIN, PAS):
        liste_vertical_2 = [] # Liste contenant les pions jouablle d'une ligne 
        for j in range(len(board[0])):
            if (board[i][j] == player or board[i][j] == 3):
                if jouabilite(board,(i, j), 1) == True: # Vérifie si la pion est jouable 
                    pos_arriver = (i , j)
                    d_m = abs(pos_arriver[0] - emplacement[0]) + abs(pos_arriver[1] - emplacement[1]) # Calcul la distance manhattan
                    liste_vertical_2.append((d_m, (i, j)))
        if len(liste_vertical_2) > 0:
            liste_vertical_1.append(liste_vertical_2)
    manhattan = reverse_manhattan(liste_vertical_1, emplacement,"k")
    board[manhattan[0]][manhattan[1]] = 3 # Change le nouveau pion selectionner en "#" 
    emplacement = manhattan # Position du nouveau pion potentielement selectionner
    return emplacement

def pos_arriver(board, pos, player):
    """
    Renvoie la position d'arrive
    que le joueur à choisie
    """
    liste =[] # Liste contenant les positions jouable du pion selectionner par le joueur 
    move_avant, move_dia_gauche, move_dia_droit = False, False, False # Initialisation de tout les mouvement à faux 
    if player == 2: # Joueur 2 
        coup_a, coup_d_g, coup_d_d = (pos[0]+1,pos[1]), (pos[0]+1,pos[1]+1), (pos[0]+1,pos[1]-1)
    else:  # Joueur 1 
        coup_a, coup_d_g, coup_d_d = (pos[0]-1,pos[1]), (pos[0]-1,pos[1]-1), (pos[0]-1,pos[1]+1)

    if is_in_board(board, (coup_a[0],coup_a[1])): 
        move_avant = board[coup_a[0]][coup_a[1]] == 0 
        if move_avant == True:
            liste.append([(coup_a[0], coup_a[1]), board[coup_a[0]][coup_a[1]]]) # Met le move_avant dans la liste si sa position est prèsente dans la matrice et que la valeur de move_avant dans la matrice est 0
            board[coup_a[0]][coup_a[1]] = 3
    if is_in_board(board, (coup_d_g[0],coup_d_g[1])):
        move_dia_gauche = board[coup_d_g[0]][coup_d_g[1]] == 0 or board[coup_d_g[0]][coup_d_g[1]] != player
        if move_dia_gauche == True:
            liste.append([(coup_d_g[0], coup_d_g[1]), board[coup_d_g[0]][coup_d_g[1]]]) # Met le move_dia_g dans la liste si sa position est prèsente dans la matrice et que la valeur de move_dia_g dans la matrice est différent de elle même
            board[coup_d_g[0]][coup_d_g[1]] = 3
    if is_in_board(board, (coup_d_d[0],coup_d_d[1])):
        move_dia_droit = board[coup_d_d[0]][coup_d_d[1]] == 0 or board[coup_d_d[0]][coup_d_d[1]] != player
        if move_dia_droit == True:
            liste.append([(coup_d_d[0], coup_d_d[1]), board[coup_d_d[0]][coup_d_d[1]]]) # Met le move_dia_d dans la liste si sa position est prèsente dans la matrice et que la valeur de move_dia_d dans la matrice est différent de elle même
            board[coup_d_d[0]][coup_d_d[1]] = 3
    choix_pos = select_pos_arriver(board, liste) # Choix de la position parmit les position dans la liste 
    return choix_pos

def select_pos_arriver(board, liste):
    liste.sort() # Trie la liste de position 
    liste_index_one = liste[0][0] # Donne le premier tuple de la liste 
    board[liste_index_one[0]][liste_index_one[1]] = 4 # Transforme la première position présent dans la liste en "@"
    
    print_board(board) # Affiche l'état actuel dans plateau 
    print("Le y pour selectionner")
    print("Le l pour aller à droite")
    print("Le j pour aller à gauche")
    choix = input("selectionner votre position d'arriver : ")

    res = liste[0][0] # Position du pion 
    cpt = 0
    while choix != "y":

        # Deplacement droite (l)
        if choix == "l":
            cpt = cpt + 1
            new_index_pos = cpt % len(liste) # Indice du nouveau potentiellement sélectionner
            ele = liste[new_index_pos][0] # Position du nouveau potentiellement sélectionner 
            board[res[0]][res[1]] = 3 # Redonne l'encienne valeur matriciel de la position du pion 
            board[ele[0]][ele[1]] = 4 # Transforme la première position présent dans la liste en "@"
            res = (ele[0], ele[1]) # Valeur de la position nouvellement choisie
            
        #deplacement gauche (j)
        if choix == "j":
            cpt = cpt - 1 
            new_index_pos = cpt % len(liste) # Indice du nouveau potentiellement sélectionner
            ele = liste[new_index_pos][0] # Position du nouveau potentiellement sélectionner 
            board[res[0]][res[1]] = 3 # Redonne l'encienne valeur matriciel de la position du pion 
            board[ele[0]][ele[1]] = 4 # Transforme la première position présent dans la liste en "@"
            res = (ele[0], ele[1]) # Valeur de la position nouvellement choisie
            
        print_board(board) # Affichage de l'état actuel de la matrice
        print("Le y pour selectionner")
        print("Le l pour aller à droite")
        print("Le j pour aller à gauche")
        choix = input("selectionner votre position d'arriver : ")
        
    for elem in liste:
        position = elem[0]
        if position == res:
            pass 
        else:
            post_pos = elem[1] 
            board[position[0]][position[1]] = post_pos # Redonne l'encienne valeur matriciel de la position du pion non sélectionner 
    return res

def play_move(board, move, player):
    """
    Execute le mouvement sur le plateau
    """
    if player == 1:
        board[move[0][0]][move[0][1]] = 0 # Position de départ des pion blanc
        board[move[1][0]][move[1][1]] = 1 # Position d'arriver des pion blanc
    else:
        board[move[0][0]][move[0][1]] = 0 # Position de départ des pion noir
        board[move[1][0]][move[1][1]] = 2 # Position d'arriver des pion noir

def lancer_jeu(file, num):
    """
    Lance la partie de jeu 
    """
    board = init_board(file) # Initialisation de la matrice 
    print_board(board) # Afficher l'état initial du plateau (aucun n'a encore été jouer)
    gagnant = None
    compteur = 0
    while gagnant == None: # Permet de stoper la partie quand il y a un gagant 
        player = (compteur % 2) + 1 # Détermine le tour de chaque joueur 
        if player == 2: # joueur 2 
            if num == 0 or num == 1: # Le joueur 2 est un joueur 
                pos = input_select_peg(board, 2)
                arriver = pos_arriver(board, pos, player)
            if num == 2: # Le joueur 2 est un joueur
                pos = ai_select_peg(board, 2)
                arriver = ai_move(board, pos, player)[1]
        else: # Joueur 1 
            pos = input_select_peg(board, 1)
            arriver = pos_arriver(board, pos, player)
        play_move(board, (pos, arriver), player)
        print_board(board)
        compteur += 1
        gagnant = winner(board) # Permet de savoir si il y a un gagnant ou non
    if gagnant == 1 or gagnant == 3: # Permet de savoir qui est le gagnant si il y n'a un
        print("Victoire des blancs")
    if gagnant == 2 or gagnant == 3:
        print("Victoire des noirs")
        
def main():
    """
    Donne les paramètres de jeu
    (taille du plateau, possibilité de jouer contre l'ia)
    """
    argument = sys.argv
    print(argument)
    if len(argument) == 1: # Plateau par defaut, mode joueur contre joueur
        lancer_jeu(7, 0)
    elif len(argument) == 2: # Le plateau est donner par un fichier texte, mode joueur contre joueur 
        if os.path.isfile(argument[1]) == True:
            lancer_jeu(argument[1], 1)
        else:
            print("mauvais non de fichier")
    elif len(argument) == 3: # Le plateau est donner par un fichier texte, joueur contre ia
        if os.path.isfile(argument[1]) == True:
            lancer_jeu(argument[1], 2)
        else:
            pass
        print("trop d'argument")

if __name__ == "__main__":
    main()