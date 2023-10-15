# %%
import chess

FEN = input()
move_input = input()
board = chess.Board(FEN)
move = chess.Move.from_uci(move_input)
board.push(move)
print(board.fen())



