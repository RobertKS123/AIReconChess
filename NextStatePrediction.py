import chess

FEN = input()
#FEN = "8/8/8/8/k7/8/7K/3B4 w - - 48 32"

board = chess.Board(FEN)

# Pseudo_legal_moves also contains all legal moves
pseudo_legal_moves = list(board.pseudo_legal_moves)
#pseudo_legal_moves = sorted(pseudo_legal_moves, key=lambda move: move.uci()) #move.uci gets the string of the move

moves_fen = []
for move in pseudo_legal_moves:
    board.push(move)
    moves_fen.append(board.fen())
    board.pop()

moves_fen = sorted(moves_fen, key = lambda fen : fen)

for fen in moves_fen:
    print(fen)


