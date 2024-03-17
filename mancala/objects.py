import math
import copy
from random import getrandbits

g_nodes_top_player = 0
g_nodes_bottom_player = 0


class Hole:
    def __init__(self, number):
        self.number = number
        self.stones = 4
        self.next = None
        self.opposite = None

    def remove_stones(self, players_turn):
        removed_stones = self.stones
        self.stones = 0
        return Hole.put_stones(self.next, removed_stones, players_turn)

    @staticmethod
    def put_stones(hole, stones, players_turn):
        hole.stones += 1
        if stones == 1:
            return hole.number
        if (players_turn and hole.number != 13) or (not players_turn and hole.number != 6):
            return Hole.put_stones(hole.next, stones - 1, players_turn)
        else:
            return Hole.put_stones(hole.next, stones, players_turn)

    def get_stones_str(self):
        if self.stones == 0:
            return ""
        return str(self.stones)

    def __str__(self):
        if self.opposite:
            return f'{self.number} - next: {self.next.number} | opposite: {self.opposite.number}'
        else:
            return f'Hole {self.number} - next: {self.next.number}'


class Board:
    def __init__(self):
        # studnie: 6 - player / 13 - ai
        self.bottoms_turn = bool(getrandbits(1))
        self.total_game_time = 0
        self.first_move_made = False
        self.holes = [Hole(i) for i in range(14)]
        self.holes[6].stones = 0
        self.holes[13].stones = 0
        self.connect_holes()

    def connect_holes(self):
        for (p, n) in zip(self.holes, self.holes[1:]):
            p.next = n
        self.holes[-1].next = self.holes[0]

        for (f, s) in zip(self.holes[:6], self.holes[12:6:-1]):
            f.opposite = s
            s.opposite = f

    def get_available_holes(self, maximizing_player):
        if maximizing_player:
            return [h.number for h in self.holes[:6] if h.stones > 0]
        return [h.number for h in self.holes[7:13] if h.stones > 0]

    def is_beating(self, number):
        if (self.bottoms_turn and not 0 <= number <= 5) or (not self.bottoms_turn and not 7 <= number <= 12):
            return

        if self.holes[number].stones == 1 and self.holes[number].opposite.stones > 0:
            if self.bottoms_turn:
                self.holes[6].stones += self.holes[number].opposite.stones + 1
            else:
                self.holes[13].stones += self.holes[number].opposite.stones + 1
            self.holes[number].stones = 0
            self.holes[number].opposite.stones = 0

    def switch_turn(self):
        self.bottoms_turn = not self.bottoms_turn

    def is_finishing_in_well(self, hole_number):
        if self.bottoms_turn and hole_number == 6:
            return True
        if not self.bottoms_turn and hole_number == 13:
            return True
        return False

    def is_ending(self):
        if all(h.stones == 0 for h in self.holes[:6]):
            total_stones = 0
            for h in self.holes[7:13]:
                total_stones += h.stones
                h.stones = 0
            self.holes[13].stones += total_stones
            return True
        elif all(h.stones == 0 for h in self.holes[7:13]):
            total_stones = 0
            for h in self.holes[:6]:
                total_stones += h.stones
                h.stones = 0
            self.holes[6].stones += total_stones
            return True
        return False

    def end_check(self):
        return all(h.stones == 0 for h in self.holes[:6]) or all(h.stones == 0 for h in self.holes[7:13])

    def eval_function(self):
        return self.holes[6].stones - self.holes[13].stones

    def heuristic_eval_function(self, bottoms_turn, number_of_moves):
        eval = self.eval_function()
        h1 = self.get_right_most_stones(bottoms_turn)
        if bottoms_turn:
            return eval * 2 + h1 * 0.198649 + number_of_moves * 0.370793
        else:
            return eval * 2 - h1 * 0.198649 - number_of_moves * 0.370793

    def get_right_most_stones(self, bottoms_turn):
        return self.holes[5].stones if bottoms_turn else self.holes[12].stones

    def minimax(self, depth, maximizing_player):
        moves = []
        if depth == 0 or self.is_ending():
            return self.eval_function(), moves
        if maximizing_player:
            global g_nodes_bottom_player
            max_val = -math.inf
            for av_moves in self.get_moves(maximizing_player):
                g_nodes_bottom_player += 1
                board_cpy = copy.deepcopy(self)
                board_cpy.execute_moves(av_moves)
                val, _ = board_cpy.minimax(depth - 1, False)
                del board_cpy
                if val > max_val:
                    max_val = val
                    moves = av_moves
            return max_val, moves
        else:
            global g_nodes_top_player
            min_val = math.inf
            for av_moves in self.get_moves(maximizing_player):
                g_nodes_top_player += 1
                board_cpy = copy.deepcopy(self)
                board_cpy.execute_moves(av_moves)
                val, _ = board_cpy.minimax(depth - 1, True)
                del board_cpy
                if val < min_val:
                    min_val = val
                    moves = av_moves
            return min_val, moves

    def heuristic_minimax(self, depth, maximizing_player, bottoms_turn, number_of_moves):
        moves = []
        if depth == 0 or self.is_ending():
            return self.eval_function(), moves
        if maximizing_player:
            global g_nodes_bottom_player
            max_val = -math.inf
            for av_moves in self.get_moves(maximizing_player):
                g_nodes_bottom_player += 1
                board_cpy = copy.deepcopy(self)
                board_cpy.execute_moves(av_moves)
                if bottoms_turn == maximizing_player:
                    number_of_moves += len(av_moves)
                val, _ = board_cpy.minimax(depth - 1, False)
                del board_cpy
                if val > max_val:
                    max_val = val
                    moves = av_moves
            return max_val, moves
        else:
            global g_nodes_top_player
            min_val = math.inf
            for av_moves in self.get_moves(maximizing_player):
                g_nodes_top_player += 1
                board_cpy = copy.deepcopy(self)
                board_cpy.execute_moves(av_moves)
                if bottoms_turn != maximizing_player:
                    number_of_moves += len(av_moves)
                val, _ = board_cpy.minimax(depth - 1, True)
                del board_cpy
                if val < min_val:
                    min_val = val
                    moves = av_moves
            return min_val, moves

    def minimax_alpha_beta(self, depth, alpha, beta, maximizing_player):
        moves = []
        if depth == 0 or self.is_ending():
            return self.eval_function(), moves
        if maximizing_player:
            global g_nodes_bottom_player
            max_val = -math.inf
            for av_moves in self.get_moves(maximizing_player):
                g_nodes_bottom_player += 1
                board_cpy = copy.deepcopy(self)
                board_cpy.execute_moves(av_moves)
                val, _ = board_cpy.minimax_alpha_beta(depth - 1, alpha, beta, False)
                del board_cpy
                if val > max_val:
                    max_val = val
                    moves = av_moves

                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return max_val, moves
        else:
            global g_nodes_top_player
            min_val = math.inf
            for av_moves in self.get_moves(maximizing_player):
                g_nodes_top_player += 1
                board_cpy = copy.deepcopy(self)
                board_cpy.execute_moves(av_moves)
                val, _ = board_cpy.minimax_alpha_beta(depth - 1, alpha, beta, True)
                del board_cpy
                if val < min_val:
                    min_val = val
                    moves = av_moves

                beta = min(beta, val)
                if beta <= alpha:
                    break
            return min_val, moves

    def heuristic_minimax_alpha_beta(self, depth, alpha, beta, maximizing_player, bottoms_turn, number_of_moves):
        moves = []
        if depth == 0 or self.is_ending():
            return self.eval_function(), moves
        if maximizing_player:
            global g_nodes_bottom_player
            max_val = -math.inf
            for av_moves in self.get_moves(maximizing_player):
                g_nodes_bottom_player += 1
                board_cpy = copy.deepcopy(self)
                board_cpy.execute_moves(av_moves)
                if bottoms_turn == maximizing_player:
                    number_of_moves += len(av_moves)
                val, _ = board_cpy.minimax_alpha_beta(depth - 1, alpha, beta, False)
                del board_cpy
                if val > max_val:
                    max_val = val
                    moves = av_moves

                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return max_val, moves
        else:
            global g_nodes_top_player
            min_val = math.inf
            for av_moves in self.get_moves(maximizing_player):
                g_nodes_top_player += 1
                board_cpy = copy.deepcopy(self)
                board_cpy.execute_moves(av_moves)
                if bottoms_turn != maximizing_player:
                    number_of_moves += len(av_moves)
                val, _ = board_cpy.minimax_alpha_beta(depth - 1, alpha, beta, True)
                del board_cpy
                if val < min_val:
                    min_val = val
                    moves = av_moves

                beta = min(beta, val)
                if beta <= alpha:
                    break
            return min_val, moves

    def execute_moves(self, moves):
        is_ending = False
        for hole_number in moves:
            _, is_ending = self.execute_move(hole_number)
        return is_ending

    def execute_move(self, hole_number):
        last = self.holes[hole_number].remove_stones(self.bottoms_turn)
        self.is_beating(last)
        is_ending = self.is_ending()
        return last, is_ending

    def get_moves(self, maximizing_player):
        all_moves = [[i] for i in self.get_available_holes(maximizing_player)]
        output_moves = []
        self.add_moves(all_moves, output_moves, maximizing_player)
        return output_moves

    def add_moves(self, moves, output, maximizing_player):
        for move in moves:
            hole_number = move[-1]
            board_cpy = copy.deepcopy(self)
            last_hole, is_ending = board_cpy.execute_move(hole_number)
            if not is_ending and board_cpy.is_finishing_in_well(last_hole):
                holes = board_cpy.get_available_holes(maximizing_player)
                next_moves = [move + [h] for h in holes]
                board_cpy.add_moves(next_moves, output, maximizing_player)
            else:
                output.append(move)
            del board_cpy

    @staticmethod
    def get_game_stats():
        return g_nodes_bottom_player, g_nodes_top_player

    @staticmethod
    def reset_counters():
        global g_nodes_top_player
        global g_nodes_bottom_player
        g_nodes_top_player = 0
        g_nodes_bottom_player = 0
