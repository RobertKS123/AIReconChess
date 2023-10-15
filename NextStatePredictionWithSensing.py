# %%
import chess

# Split the sensed move into a list of (square,piece)
def get_sensed_squares(sense):
    tile_list = sense.split(';')
    tile_list = [(pair.split(':')[0], pair.split(':')[1]) for pair in tile_list]
    return tile_list

# Check if the sensed region lines up with what we have in the state
def check_valid_state(board, sensed_tiles):
    for tile in sensed_tiles:
        square = chess.parse_square(tile[0]) # returns the index of a squares given its names
        on_board = board.piece_at(square)
        if (tile[1] == "?" and on_board is None):
            continue
        if (tile[1] == str(on_board)):
            continue
        return False
    return True

num_states = int(input())
possible_states = []
for i in range(num_states):
    possible_states.append(input())
sense = input()

viewed_squares = get_sensed_squares(sense)

actual_states = []
for state in possible_states:
    board = chess.Board(state)
    if (check_valid_state(board,viewed_squares)):
        actual_states.append(state)

actual_states = sorted(actual_states, key = lambda fen : fen)

for state in actual_states:
    print(state)


