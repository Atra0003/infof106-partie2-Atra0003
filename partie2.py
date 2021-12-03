import os, sys
from random import choice, seed

def extract_pos(n, str_pos):
    """Traduit le coup rentrer en input en coordonné ligne colone pour la matrice"""
    cpt = 1 
    capital = "a"
    while capital != str_pos[0]:
        cpt += 1
        capital = chr(ord(capital)+1)
    colonne = cpt - 1 # Colonne
    ligne = n - int(str_pos[1:]) # Ligne 
    return (ligne, colonne)

def init_board(file):
    """Création de la matrice de taille n*n"""
    matrice = []
    if type(file) == int or file == None:
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
    else:
        fichier = open(file, encoding="utf-8")
        lignes = fichier.readlines()
        nb_ligne = len(lignes)
        
        # Création de la matrice
        taille_plateau = lignes[0].strip("\n")
        taille_plateau = taille_plateau.split(" ")
        n = int(taille_plateau[0])
        m = int(taille_plateau[1])
        for matrice_1 in range(n):
            el = []
            for matrice_2 in range(m):
                el.append(0)
            matrice.append(el)
    
        # Positionnement des pions blanc 
        ligne2 = lignes[1].split(",")
        for pos_w in ligne2:
            pos = extract_pos(n, pos_w)
            matrice[pos[0]][pos[1]] = 1
        
        # Positionnement des pions noir
        ligne2 = lignes[2].split(",")
        for pos_w in ligne2:
            pos = extract_pos(n, pos_w)
            matrice[pos[0]][pos[1]] = 2
    return matrice
        
    
def print_board(board):
    """Affiche la matrice dans le terminal"""
    m = len(board) # Longeur de la matrice(plateau)
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
            elif board[i][j] == 3:
                print("#", end=" ")
            else: # Placement des pions noir 
                print("B", end=" ")
        print("|")
    print(" "*5 + n*"— ")
    print(" "*5,end="")
    for k in range(n):
        print(chr(ord("a")+k), end=" ") # Affichage des différentes lettres(représent les colonne)
    print()

def ai_select_peg(board, player):
    verificateur = 0
    pion = []
    for i in range(len(board)-1, 0, -1):
        for j in range(len(board[i])):
            if board[i][j] == player:
                jouable = jouabilite(board, (i, j))
                if jouable == True:
                    pion.append((i, j))
                    verificateur = 1
        if len(pion) != 0:
            res = choice(pion)
        else:
            pass 
        if verificateur == 1:
            return res 
    
def is_in_board(board, t):
    board = len(board)
    if 0<= t[0]< board and 0<= t[1]< board:
        res = True
    else:
        res = False
    return res
    
def jouabilite(plateau, t):
    move_avant, move_dia_gauche, move_dia_droit = False, False, False
    if is_in_board(plateau, (t[0]+1, t[1])):
        move_avant = plateau[t[0]+1][t[1]] == 0
    if is_in_board(plateau, (t[0]+1, t[1]-1)):
        move_dia_gauche = plateau[t[0]+1][t[1]-1] == 0 or plateau[t[0]+1][t[1]-1] == 1
    if is_in_board(plateau, (t[0]+1, t[1]+1)):
        move_dia_droit = plateau[t[0]+1][t[1]+1] == 0 or plateau[t[0]+1][t[1]+1] == 1
    res = move_avant or move_dia_gauche or move_dia_droit
    return res 

def ai_move(board, pos, player):
    liste_ia_move = []
    if player == 2:
        move_1, move_2, move_3 = (pos[0]+1,pos[1]), (pos[0]+1,pos[1]+1), (pos[0]+1,pos[1]-1)
    else:
        move_1, move_2, move_3 = (pos[0]-1,pos[1]), (pos[0]-1,pos[1]-1), (pos[0]-1,pos[1]+1)
    coup_avant, coup_dia_d, coup_dia_g = False, False, False
    if 0 <= move_1[0] <= len(board) and 0 <= move_1[0] <= len(board):
        coup_avant = board[move_1[0]][move_1[1]] == 0
    if 0 <= move_2[0] <= len(board) and 0 <= move_2[1] <= len(board):
        coup_dia_g = board[move_2[0]][move_2[1]] != player
    if 0 <= move_3[0] <= len(board) and 0 <= move_3[1] <= len(board):
        coup_dia_d = board[move_3[0]][move_3[1]] != player
    if coup_avant == True:
        liste_ia_move.append(move_1)
    if coup_dia_d == True:
        liste_ia_move.append(move_2)
    if coup_dia_g == True:
        liste_ia_move.append(move_3)
    return pos, (choice(sorted(liste_ia_move)))

def select_peg_pion(board, player, DEBUT, FIN, PAS):
    verificateur = 0
    pion = []
    for i in range(DEBUT, FIN, PAS):
        for j in range(len(board[0])):
            if board[i][j] == player:
                jouable = jouabilite(board, (i, j))
                if jouable == True:
                    return i, j
                

def input_select_peg(board, player):
    if player == 1:
        DEBUT, FIN, PAS = 0, len(board)-1, 1
    else:
        DEBUT, FIN, PAS = len(board)-1, 0, -1
    pion_select = select_peg_pion(board, player, DEBUT, FIN, PAS)
    board[pion_select[0]][pion_select[1]] = 3
    print(print_board(board))
    
    # Cas ou le joueur veux choisir un autre pion
    choix = input("entrer une valeur : ")
    res = pion_select[:]
    while choix != "y":
        #deplacement droite (l)
        cpt = 0
        if choix == "l":
            cpt = 1
            copy_pion_select = pion_select[:]
            while board[pion_select[0]][(pion_select[1]+cpt) % len(board[0])] != player:
                cpt += 1
            board[copy_pion_select[0]][copy_pion_select[1]] = player
            board[pion_select[0]][(pion_select[1]+cpt) % len(board[0])] = 3
            res = pion_select[0], pion_select[1]+cpt
            pion_select = [pion_select[0], (pion_select[1]+cpt) % len(board[0])]
            print(print_board(board))
           
        #deplacement gauche (j)
        if choix == "j":
            cpt = 1
            copy_pion_select = pion_select[:]
            while board[pion_select[0]][(pion_select[1]-cpt) % len(board[0])] != player:
                cpt -= 1
            board[copy_pion_select[0]][copy_pion_select[1]] = player
            board[pion_select[0]][(pion_select[1]-cpt) % len(board[0])] = 3
            res = pion_select[0], pion_select[1]-cpt
            pion_select = [pion_select[0], (pion_select[1]-cpt) % len(board[0])]
            print(print_board(board))

        #deplacement haut (i)
        if choix == "i":
            pos_player = []
            for i in range(DEBUT, FIN, PAS):
                for j in range(len(board[0])):
                    if board[i][j] == player:
                        pos_arriver = board[i][j]
                        d = (abs(res[0] - pos_arriver[0]), abs(res[1] - pos_arriver[1]))
                        pos_player.append((d[0], d[1]))
            print(pos_player)
        
            print(print_board(board))

        #deplacement bas (k)
        if choix == "k":
            
            print(print_board(board))

        choix = input("entrer une valeur : ")
    return res


def lancer_jeu(file):
    board = init_board(file)
    print_board(board)
    pos = ai_select_peg(board, 2)
    print(ai_move(board, pos, 2))
    input_select_peg(board, 1)


def main():
    argument = sys.argv
    if len(argument) == 1:
        lancer_jeu(7)
    elif len(argument) == 2:  
        if os.path.isfile(argument[1]) == True:
            lancer_jeu(argument[1])
        else:
            print("mauvais non de fichier")
    elif len(argument) == 3:
        if os.path.isfile(argument[2]) == True:
            lancer_jeu(argument[2])
        else:
            pass
        print("trop d'argument")
#py -m pytest test_partie2.py -vv

if __name__ == "__main__":
    main()
