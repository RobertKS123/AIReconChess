from reconchess import *
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci('./stockfish/stockfish.exe', setpgrp=True)

num_states = int(input())
possible_states = []
for i in range(num_states):
    possible_states.append(input())

possible_moves = []

for state in possible_states:
    board = chess.Board(state)

    # Pseudo_legal_moves also contains all legal moves
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
    possible_moves.append(best_move)

move_frequency = {move: possible_moves.count(move) for move in possible_moves}
possible_moves = sorted(move_frequency, key=lambda move: (-move_frequency[move], move.uci()))

print(possible_moves[0].uci())

engine.quit()


