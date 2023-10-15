from reconchess import *
import chess.engine
import random

class MyAgent(Player):
    def __init__(self):
        self.board = None
        self.color = None
        self.possible_states = None
        self.engine = chess.engine.SimpleEngine.popen_uci('./stockfish/stockfish.exe', setpgrp=True)
        self.start = True

    def handle_game_start(self, color, board, opponent_name):
        self.board = board
        self.color = color

        new_states = set()
        if (color) :
            new_states.add(board.fen())
        else :
            #every opening move white can do
            pseudo_legal_moves = list(board.pseudo_legal_moves)
            for move in pseudo_legal_moves:
                board.push(move)
                new_states.add(board.fen())
                board.pop()
        self.possible_states = new_states

    def handle_opponent_move_result(self, captured_my_piece, capture_square):
        if (self.start == True) :
            self.start = False
            return
        new_states = set()
        if (captured_my_piece) :
            capture_square_name = chess.square_name(capture_square)
            # remove any state where that capture was impossible and add any states where the move was possible
            for state in self.possible_states:
                board = chess.Board(state)
                pseudo_legal_moves = list(board.pseudo_legal_moves)
                attack_on_tile = [move for move in pseudo_legal_moves if move.uci()[-2:] == capture_square_name]
                for move in attack_on_tile:
                    board.push(move)
                    new_states.add(board.fen())
                    board.pop()
        else :
            #make every move an opponent can make without capture ()
            for state in self.possible_states:
                board = chess.Board(state)
                pseudo_legal_moves = list(board.pseudo_legal_moves)
                attack_on_tile = [move for move in pseudo_legal_moves if not board.piece_at(chess.parse_square(move.uci()[-2:]))]  
                for move in attack_on_tile:
                    board.push(move)
                    new_states.add(board.fen())
                    board.pop()
        self.possible_states = new_states

    def choose_sense(self, sense_actions, move_actions, seconds_left):
        # uniform random sense
        edges = [0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,559,60,61,62,63]
        not_edges = [value for value in sense_actions if value not in edges]
        sense = random.choice(not_edges) 
        return sense
    
    def check_valid_state(self, state, sense_result):
        # Check if all the squares in a board match the sensed area
        board = chess.Board(state)
        for result in sense_result:
            square = result[0]
            on_board = board.piece_at(square)
            if (result[1] is None and on_board is None):
                continue
            if (str(result[1]) == str(on_board)):
                continue
            return False
        return True

    def handle_sense_result(self, sense_result):
        # remove any state where pieces do not match sense
        new_possible_states = {state for state in self.possible_states if self.check_valid_state(state, sense_result)}
        self.possible_states = new_possible_states


    def choose_move(self, move_actions, seconds_left):
        # stockfish get most popular move
        possible_moves = []
        N = len(self.possible_states)
        run_time = 10/N
        for state in self.possible_states:
            board = chess.Board(state)
            pseudo_legal_moves = list(board.pseudo_legal_moves)
            best_move = None
            for move in pseudo_legal_moves:
                square = chess.parse_square(move.uci()[-2:])
                if (str(board.piece_at(square)).lower() == "k" ):
                    best_move = move.uci()
            if (best_move is None):
                try:
                    board.clear_stack()
                    result = self.engine.play(board, chess.engine.Limit(time=run_time))
                    best_move = result.move
                except chess.engine.EngineTerminatedError:
                    print('Stockfish Engine died')
                except chess.engine.EngineError:
                    print('Stockfish Engine bad state at "{}"'.format(board.fen()))
            possible_moves.append(best_move)
        
        # get frequency of moves and filter list so only moves wit the highest frequency are left 
        move_frequency = {move: possible_moves.count(move) for move in possible_moves}
        max_frequency = max(move_frequency.values())
        best_moves = [move for move, frequency in move_frequency.items() if frequency == max_frequency]

        # pich random rome from best candidates
        best_move= random.choice(best_moves) 

        return best_move

    def handle_move_result(self, requested_move, taken_move, captured_opponent_piece, capture_square):
        # I don't think it matters what requested_move was 
        new_states = set()
        if (captured_opponent_piece) :
            # add every state when a capture was possible (if a piece was taken based on actual move)
            move = chess.parse_square(taken_move.uci()[-2:])
            for state in self.possible_states:
                board = chess.Board(state)
                if (move == capture_square and board.is_capture(taken_move)) :
                    board.push(taken_move)
                    new_states.add(board.fen())
        else:
            # add every state where no capture took place
            move = taken_move.uci()[:-2]
            for state in self.possible_states:
                board = chess.Board(state)
                if (not board.is_capture(taken_move)) :
                    board.push(taken_move)
                    new_states.add(board.fen())
        self.possible_states = new_states


    def handle_game_end(self, winner_color, win_reason, game_history):
        self.engine.quit()



