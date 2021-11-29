"""
Auteur : Traore Amara
matricule : 000542150
section : BA1-info 
Date : 03/11/21
Usage : jeu du Breakthrough  
Entrer : taille du plateau, coup joueur1, coup joueur 2 
Sortie : plateau de jeu avec les différents mouvement des joueurs
"""

def init_board(n : int):
    """Création de la matrice de taille n*n"""
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
    return matrice


def print_board(board):
    """Affiche la matrice dans le terminal"""
    n = len(board) # Longeur de la matrice(plateau)
    print(" "*5 + len(board)*"— ")
    for i in range(n):
        if n-i <= 9: # Cas ou le plateau ferai inférieur ou égale à 9
            print(" "+str(n-i)+" "+"|",end=" ")
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
    print(" "*5 + len(board)*"— ")
    print(" "*5,end="")
    for k in range(n):
        print(chr(ord("a")+k), end=" ") # Affichage des différentes lettres(représent les colonne)
    print()


def winner(board):
    """Vérifie si l'un des deux joueur à gagné la partie"""
    n = len(board)
    if 1 in board[0]: # Cas ou les blancs gagne
        gagnat = 1
    elif 2 in board[n-1]: # Cas ou les noirs gagne 
        gagnat = 2
    else:
        gagnat = None # Cas ou il n'y a pas de gagnat ou pas encore(partie pas encore terminé)
    return gagnat


def is_in_board(n, pos):
    if 0<=pos[0]<n and 0<=pos[1]<n:# ligne et colonne sont compatible avec le plateau
        res = True
    else:
        res = False
    return res


def input_move():
    """Vérifie que le coup joué par le joueur respecte l'encodage demandé"""
    coup_correct = False
    while coup_correct == False:
        coup = input("Entre votre coup : ")
        if ">" not in coup:
            print("Il manque le symbole >")
            coup = input("Entre votre coup : ")
        else:
            var = coup.split(">")
            depart , arriver = var
            if len(depart) < 2 or len(arriver) < 2:
                print("Tu dois spécifer la ligne et la colone ")
            else:
                if depart[0].isalpha() == True and depart[1:].isdigit() == True and arriver[0].isalpha() == True and arriver[1:].isdigit() == True:
                    coup_correct = True
                else:
                    print("Une case est composée de la lettre de la colonne et du numéro de ligne")
                    coup = input("Entre votre coup : ")
    return coup
    

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


def check_move(board, player, str_move):
    """La fonction verifie que le coup joué est permis(respecte les règles du jeu)""" 
    n = len(board)
    pos_one, pos_two = str_move.split(">")
    depart, arriver = extract_pos(n, pos_one), extract_pos(n ,pos_two) # Coordonné ligne et la colonne
    res = is_in_board(n, depart) and is_in_board(n, arriver)
    if res == True:
        if player == 1:
            move_avant_W = (arriver[0] - depart[0]) == -1 and (arriver[1] == depart[1]) and board[arriver[0]][arriver[1]] == 0 # Pion blanc avancer tout droit
            move_dia_gauche_W = (arriver[0] == depart[0]-1) and (arriver[1] == depart[1]-1) and ((board[arriver[0]][arriver[1]] == 0) or (board[arriver[0]][arriver[1]] == 2)) and board[arriver[0]][arriver[1]] == board[depart[0]-1][depart[1]-1]# Pion blanc avancer diagonal gauche
            move_dia_droite_W = (arriver[0] == depart[0]-1) and (arriver[1] == depart[1]+1) and ((board[arriver[0]][arriver[1]] == 0) or (board[arriver[0]][arriver[1]] == 2)) and board[arriver[0]][arriver[1]] == board[depart[0]-1][depart[1]+1]# Pion blanc avancer diagonal droit
            res = move_avant_W or move_dia_gauche_W or move_dia_droite_W
        else:
            move_avant_B = (arriver[0] - depart[0]) == 1 and arriver[1] == depart[1] and board[arriver[0]][arriver[1]] == 0 # Pion blanc avancer tout droit
            move_dia_gauche_B = (arriver[0] - depart[0] == 1) and (depart[1] - arriver[1] == 1) and ((board[arriver[0]][arriver[1]] == 0) or (board[arriver[0]][arriver[1]] == 1)) and board[arriver[0]][arriver[1]] == board[depart[0]+1][depart[1]-1] # Pion noir avancer diagonal gauche
            move_dia_droite_B = (arriver[0] == depart[0]+1) and (arriver[1] == depart[1]+1) and ((board[arriver[0]][arriver[1]] == 0) or (board[arriver[0]][arriver[1]] == 1)) and board[arriver[0]][arriver[1]] == board[depart[0]+1][depart[1]+1] # Pion noir avancer diagonal drooit
            res = move_avant_B or move_dia_gauche_B or move_dia_droite_B
    return res


def play_move(board, move, player):
    """Execute le mouvement sur le plateau"""
    if player == 1:
        board[move[0][0]][move[0][1]] = 0 # Position de départ des pion blanc
        board[move[1][0]][move[1][1]] = 1 # Position d'arriver des pion blanc
    else:
         board[move[0][0]][move[0][1]] = 0 # Position de départ des pion noir
         board[move[1][0]][move[1][1]] = 2 # Position d'arriver des pion noir
    return board


def main(n):
    """Fonction principale"""
    board = init_board(n)
    n = len(board)
    print_board(board) # Présent le plateau à l'état initial 
    gagnant = None
    compteur = 0
    while gagnant == None: # Nous dis si il y a un gagnat
        player = (compteur % 2) + 1
        verificateur = False
        while verificateur == False:
            coup = input_move()
            verificateur = check_move(board, player, coup)
        if player == 1: # Joueur blanc 
            one, two = coup.split(">")
            c_one, c_two = extract_pos(n, one), extract_pos(n,two)
            var = play_move(board, (c_one, c_two), player)
        else: # Joueur noir
            one, two = coup.split(">")
            c_one, c_two = extract_pos(n, one), extract_pos(n,two)
            var = play_move(board, (c_one, c_two), player)
        print_board(var) # Print l'état actuel du plateau 
        gagnant = winner(var) # Permet de savoir si il y a un gagnant ou non
        compteur += 1
    if gagnant == 1: # Permet de savoir qui est le gagnant si il y n'a un
        print("Victoire des blancs")
    else:
        print("Victoire des noirs")
        

if __name__ == "__main__":
    verificateur = False
    while verificateur == False: # Vérifie que la taille du tableau est égale ou supérien à 4
        taille_plateau = int(input("Entrer la valeur de la taille du plateau : "))
        if taille_plateau >= 4:
            main(taille_plateau)