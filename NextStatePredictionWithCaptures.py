# %%
import chess

FEN = input()
tile = input()
# FEN = "k1n1n3/p2p1p2/P2P1P2/8/8/8/8/7K b - - 23 30"
# tile = "d6"

board = chess.Board(FEN)

# Pseudo_legal_moves also contains all legal moves
pseudo_legal_moves = list(board.pseudo_legal_moves)
#attack_on_tile = filter(lambda move: move.uci()[:-2] == tile, pseudo_legal_moves)
attack_on_tile = [move for move in pseudo_legal_moves if move.uci()[-2:] == tile]  #move.uci gets the string of the move


#can store whole boards 
moves_fen = []
for move in attack_on_tile:
    board.push(move)
    moves_fen.append(board.fen())
    board.pop()

moves_fen = sorted(moves_fen, key = lambda fen : fen)

for fen in moves_fen:
    print(fen)

# %%



