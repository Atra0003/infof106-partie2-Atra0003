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



def main():
    #sys.stdout.write("board.txt")
    #sys.stdout.write("-ai")
    #if len(argv) == 2:
        
    if os.path.isfile("test_board_1.txt") == True:
        board = init_board("test_board_1.txt")
    else:
        board = init_board(7)
    res_colonne_board = len(board[0])
    print_board(res_colonne_board, board)
    #pos = ai_select_peg(board, 2)
    #print(ai_move(board, pos, 2))
        
#py -m pytest test_partie2.py -vv

if __name__ == "__main__":
    main()