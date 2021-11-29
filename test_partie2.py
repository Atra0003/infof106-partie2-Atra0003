from pytest import MonkeyPatch
from partie2 import *
from random import seed


def test_print_board():
    """
    Test du print de plateau avec taille custom.
    """
    from contextlib import redirect_stdout
    from io import StringIO
    board = [
        [2, 2, 0],
        [2, 2, 2],
        [2, 2, 2],
        [0, 0, 0],
        [0, 1, 1],
        [1, 1, 0]
    ]
    with StringIO() as buffer, redirect_stdout(buffer):
        print_board(board)
        _buffer = str(buffer.getvalue())
    expected_with_edges = '     — — — \n\
 6 | B B . |\n\
 5 | B B B |\n\
 4 | B B B |\n\
 3 | . . . |\n\
 2 | . W W |\n\
 1 | W W . |\n\
     — — — \n\
     a b c'

    assert _buffer.strip() == expected_with_edges.strip()


def test_init_board_1():
    """
    Test de génération du plateau.
    """
    file_name = "test_board_1.txt"
    config_board = init_board(file_name)
    expected_board = [[2, 2, 0, 2, 2],
                      [2, 2, 2, 2, 2],
                      [0, 0, 0, 0, 0],
                      [1, 0, 1, 1, 1],
                      [1, 1, 1, 0, 1]]
    assert config_board == expected_board


def test_init_board_2():
    """
    Test de génération du plateau.
    """
    file_name = None
    generated_board = init_board(file_name)
    expected_board = [[2, 2, 2, 2, 2, 2, 2],
                      [2, 2, 2, 2, 2, 2, 2],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 1]]
    assert generated_board == expected_board


def test_ai_select_peg_1():
    """
    Test du choix de mouvement de l'IA
    # 1: Un seul pion choisissable
    """
    seed(12)
    board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 2, 0, 2, 0],
             [0, 0, 0, 2, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0]]
    player = 2
    selected_move = ai_select_peg(board, player)
    expected_move = (2, 3)
    assert selected_move == expected_move


def test_ai_select_peg_2():
    """
    Test du choix de mouvement de l'IA
    # 2: Plusieurs pions choisissables
    """
    seed(7)
    board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 2, 0, 2, 0],
             [2, 0, 2, 2, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0]]
    player = 2
    selected_move = ai_select_peg(board, player)
    expected_move = (2, 2)
    assert selected_move == expected_move


def test_ai_move_1():
    """
    Teste la selection du pion le plus avancé par l'IA
    """
    seed(12)
    board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 2, 0, 2, 0],
             [0, 0, 0, 2, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0]]
    player = 2
    peg = (2, 3)
    selected_move = ai_move(board, peg, player)
    expected_move = ((2, 3), (3, 4))
    assert selected_move == expected_move


def test_ai_move_2():
    """
    Teste la selection du pion le plus avancé par l'IA
    """
    seed(8)
    board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 2, 0, 2, 0],
             [2, 0, 2, 2, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0]]
    player = 2
    peg = (2, 2)
    selected_move = ai_move(board, peg, player)
    expected_move = ((2, 2), (3, 2))
    assert selected_move == expected_move


def test_input_select_peg_1(monkeypatch):
    """
    Teste la sélection sur une ligne et la boucle de sélection
    """
    board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 2, 0, 2, 0],
             [2, 0, 2, 2, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 1],
             [0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0]]
    player = 1
    inputs = (inpt for inpt in ['l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'y'])
    monkeypatch.setattr('builtins.input', lambda x: next(inputs))
    selected_move = input_select_peg(board, player)
    expected_selected = (4, 1)
    assert selected_move[0] == expected_selected[0]


def test_input_select_peg_2(monkeypatch):
    """
    Teste la sélection d'un pion de la ligne inférieure en
    fonction de la distance des pions
    """
    board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 2, 0, 2, 0],
             [2, 0, 2, 2, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0],
             [0, 0, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0]]
    player = 1
    inputs = (inpt for inpt in ['k', 'y'])
    monkeypatch.setattr('builtins.input', lambda x: next(inputs))
    selected_move = input_select_peg(board, player)
    expected_selected = (5, 3)
    assert selected_move == expected_selected


def test_input_select_peg_3(monkeypatch):
    """
    Test la boucle de sélection des lignes
    """
    board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 2, 0, 2, 0],
             [2, 0, 2, 2, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0],
             [0, 0, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0]]
    player = 1
    inputs = (inpt for inpt in ['k', 'k', 'k', 'y'])
    monkeypatch.setattr('builtins.input', lambda x: next(inputs))
    selected_move = input_select_peg(board, player)
    expected_selected = (4, 3)
    assert selected_move == expected_selected
