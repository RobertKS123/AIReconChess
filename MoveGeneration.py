
from reconchess import *
import chess.engine
engine = chess.engine.SimpleEngine.popen_uci('./stockfish', setpgrp=True)

FEN = input()
#FEN = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

board = chess.Board(FEN)

pseudo_legal_moves = list(board.pseudo_legal_moves)

best_move = None

for move in pseudo_legal_moves:
    square = chess.parse_square(move.uci()[-2:])
    if (str(board.piece_at(square)).lower() == "k" ):
        best_move = move.uci()

if (best_move is None):
    try:
        board.clear_stack()
        result = engine.play(board, chess.engine.Limit(time=0.5))
        best_move = result.move
    except chess.engine.EngineTerminatedError:
        print('Stockfish Engine died')
    except chess.engine.EngineError:
        print('Stockfish Engine bad state at "{}"'.format(board.fen()))

print(best_move)

engine.quit()
