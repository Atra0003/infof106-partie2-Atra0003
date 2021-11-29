import os, sys
from random import choice

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
    if type(file) == int:
        for matrice_1 in range(file):
            el = []
            for matrice_2 in range(file):
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
        
    
def print_board(n, board):
    """Affiche la matrice dans le terminal"""
    m = len(board) # Longeur de la matrice(plateau)
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
    
def jouabilite(board, t):
    board = len(board)
    move_avant = board[t[0]+1][t[1]] == 0
    move_dia_gauche = board[t[0]+1][t[1]-1] == 0 or board[t[0]+1][t[1]-1] == 1
    move_dia_droit = board[t[0]+1][t[1]+1] == 0 or board[t[0]+1][t[1]+1] == 1
    print(t[0]+1, t[1])
    print(type(t[0]+1))
    res = is_in_board(board, (t[0]+1, t[1])) \
    or is_in_board(board, (t[0]+1, t[1]-1)) \
    or is_in_board(board, (t[0]+1, t[1]+1))
    return res 


def main():
    if os.path.isfile("board.txt") == True:
        board = init_board("board.txt")
    else:
        board = init_board(7)
    res_colonne_board = len(board[0])
    print(print_board(res_colonne_board, board))
    print(ai_select_peg(board, 2))
        


if __name__ == "__main__":
    main()