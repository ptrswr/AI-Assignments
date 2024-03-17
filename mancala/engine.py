import random
import time
from math import inf

from PyQt5 import QtCore, QtWidgets
from objects import Board
from random import getrandbits


class Engine(object):
    def __init__(self, main_window, board):
        self.board = board
        main_window.setObjectName("MainWindow")
        main_window.resize(1115, 347)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.p_hole_0 = QtWidgets.QPushButton(self.centralwidget)
        self.p_hole_0.setGeometry(QtCore.QRect(100, 220, 131, 71))
        self.p_hole_0.setToolTip("")
        self.p_hole_0.setObjectName("p_hole_0")
        self.p_hole_0.clicked.connect(lambda: self.hole_button_pressed(0))
        self.p_hole_1 = QtWidgets.QPushButton(self.centralwidget)
        self.p_hole_1.setGeometry(QtCore.QRect(250, 220, 131, 71))
        self.p_hole_1.setToolTip("")
        self.p_hole_1.setObjectName("p_hole_1")
        self.p_hole_1.clicked.connect(lambda: self.hole_button_pressed(1))
        self.p_hole_2 = QtWidgets.QPushButton(self.centralwidget)
        self.p_hole_2.setGeometry(QtCore.QRect(400, 220, 131, 71))
        self.p_hole_2.setToolTip("")
        self.p_hole_2.setObjectName("p_hole_2")
        self.p_hole_2.clicked.connect(lambda: self.hole_button_pressed(2))
        self.p_hole_3 = QtWidgets.QPushButton(self.centralwidget)
        self.p_hole_3.setGeometry(QtCore.QRect(550, 220, 131, 71))
        self.p_hole_3.setToolTip("")
        self.p_hole_3.setObjectName("p_hole_3")
        self.p_hole_3.clicked.connect(lambda: self.hole_button_pressed(3))
        self.p_hole_4 = QtWidgets.QPushButton(self.centralwidget)
        self.p_hole_4.setGeometry(QtCore.QRect(700, 220, 131, 71))
        self.p_hole_4.setToolTip("")
        self.p_hole_4.setObjectName("p_hole_4")
        self.p_hole_4.clicked.connect(lambda: self.hole_button_pressed(4))
        self.p_hole_5 = QtWidgets.QPushButton(self.centralwidget)
        self.p_hole_5.setGeometry(QtCore.QRect(850, 220, 131, 71))
        self.p_hole_5.setToolTip("")
        self.p_hole_5.setObjectName("p_hole_5")
        self.p_hole_5.clicked.connect(lambda: self.hole_button_pressed(5))
        self.ai_well = QtWidgets.QLabel(self.centralwidget)
        self.ai_well.setGeometry(QtCore.QRect(50, 170, 71, 41))
        self.ai_well.setToolTip("")
        self.ai_well.setObjectName("ai_well")
        self.player_well = QtWidgets.QLabel(self.centralwidget)
        self.player_well.setGeometry(QtCore.QRect(1010, 170, 71, 41))
        self.player_well.setToolTip("")
        self.player_well.setObjectName("player_well")
        self.ai_hole_12 = QtWidgets.QLabel(self.centralwidget)
        self.ai_hole_12.setGeometry(QtCore.QRect(100, 90, 131, 71))
        self.ai_hole_12.setToolTip("")
        self.ai_hole_12.setStyleSheet("background-color: rgb(225, 225, 225);color: rgb(0, 0, 0);")
        self.ai_hole_12.setAlignment(QtCore.Qt.AlignCenter)
        self.ai_hole_12.setObjectName("ai_hole_12")
        self.ai_hole_11 = QtWidgets.QLabel(self.centralwidget)
        self.ai_hole_11.setGeometry(QtCore.QRect(250, 90, 131, 71))
        self.ai_hole_11.setToolTip("")
        self.ai_hole_11.setStyleSheet("background-color: rgb(225, 225, 225);color: rgb(0, 0, 0);")
        self.ai_hole_11.setAlignment(QtCore.Qt.AlignCenter)
        self.ai_hole_11.setObjectName("ai_hole_11")
        self.ai_hole_10 = QtWidgets.QLabel(self.centralwidget)
        self.ai_hole_10.setGeometry(QtCore.QRect(400, 90, 131, 71))
        self.ai_hole_10.setToolTip("")
        self.ai_hole_10.setStyleSheet("background-color: rgb(225, 225, 225);color: rgb(0, 0, 0);")
        self.ai_hole_10.setAlignment(QtCore.Qt.AlignCenter)
        self.ai_hole_10.setObjectName("ai_hole_10")
        self.ai_hole_9 = QtWidgets.QLabel(self.centralwidget)
        self.ai_hole_9.setGeometry(QtCore.QRect(550, 90, 131, 71))
        self.ai_hole_9.setToolTip("")
        self.ai_hole_9.setStyleSheet("background-color: rgb(225, 225, 225);color: rgb(0, 0, 0);")
        self.ai_hole_9.setAlignment(QtCore.Qt.AlignCenter)
        self.ai_hole_9.setObjectName("ai_hole_9")
        self.ai_hole_8 = QtWidgets.QLabel(self.centralwidget)
        self.ai_hole_8.setGeometry(QtCore.QRect(700, 90, 131, 71))
        self.ai_hole_8.setToolTip("")
        self.ai_hole_8.setStyleSheet("background-color: rgb(225, 225, 225);color: rgb(0, 0, 0);")
        self.ai_hole_8.setAlignment(QtCore.Qt.AlignCenter)
        self.ai_hole_8.setObjectName("ai_hole_8")
        self.ai_hole_7 = QtWidgets.QLabel(self.centralwidget)
        self.ai_hole_7.setGeometry(QtCore.QRect(850, 90, 131, 71))
        self.ai_hole_7.setToolTip("")
        self.ai_hole_7.setStyleSheet("background-color: rgb(225, 225, 225);color: rgb(0, 0, 0);")
        self.ai_hole_7.setAlignment(QtCore.Qt.AlignCenter)
        self.ai_hole_7.setObjectName("ai_hole_7")
        self.turn_label = QtWidgets.QLabel(self.centralwidget)
        self.turn_label.setGeometry(QtCore.QRect(20, 20, 91, 41))
        self.turn_label.setObjectName("turn_label")
        self.end_turn = QtWidgets.QPushButton(self.centralwidget)
        self.end_turn.setGeometry(QtCore.QRect(1000, 20, 93, 28))
        self.end_turn.setObjectName("end_turn")
        self.end_turn.clicked.connect(self.ai_turn)
        self.start_game = QtWidgets.QPushButton(self.centralwidget)
        self.start_game.setGeometry(QtCore.QRect(900, 20, 93, 28))
        self.start_game.setObjectName("start_game")
        self.start_game.clicked.connect(self.game_start)

        self.switch_ai = QtWidgets.QPushButton(self.centralwidget)
        self.switch_ai.setGeometry(QtCore.QRect(1000, 90, 93, 28))
        self.switch_ai.setObjectName("switch_ai")
        self.switch_ai.clicked.connect(lambda: self.ai_vs_ai(False))
        self.switch_ai_a_b = QtWidgets.QPushButton(self.centralwidget)
        self.switch_ai_a_b.setGeometry(QtCore.QRect(1000, 120, 93, 28))
        self.switch_ai_a_b.setObjectName("switch_ai_a_b")
        self.switch_ai_a_b.clicked.connect(lambda: self.ai_vs_ai(True))

        self.restart_game = QtWidgets.QPushButton(self.centralwidget)
        self.restart_game.setGeometry(QtCore.QRect(1000, 50, 93, 28))
        self.restart_game.setObjectName("restart_game")
        self.restart_game.clicked.connect(self.game_restart)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1115, 26))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        main_window.setWindowTitle("Mancala")

        self.end_turn.setText("End turn")
        self.start_game.setText("START")
        self.restart_game.setText("RESTART")
        self.switch_ai.setText("AI")
        self.switch_ai_a_b.setText("AI A/B")

        self.disable_buttons()
        self.update_ui()
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def update_ui(self):
        self.p_hole_0.setText(self.board.holes[0].get_stones_str())
        self.p_hole_1.setText(self.board.holes[1].get_stones_str())
        self.p_hole_2.setText(self.board.holes[2].get_stones_str())
        self.p_hole_3.setText(self.board.holes[3].get_stones_str())
        self.p_hole_4.setText(self.board.holes[4].get_stones_str())
        self.p_hole_5.setText(self.board.holes[5].get_stones_str())
        self.player_well.setText(self.board.holes[6].get_stones_str())
        self.ai_well.setText(self.board.holes[13].get_stones_str())
        self.ai_hole_12.setText(self.board.holes[12].get_stones_str())
        self.ai_hole_11.setText(self.board.holes[11].get_stones_str())
        self.ai_hole_10.setText(self.board.holes[10].get_stones_str())
        self.ai_hole_9.setText(self.board.holes[9].get_stones_str())
        self.ai_hole_8.setText(self.board.holes[8].get_stones_str())
        self.ai_hole_7.setText(self.board.holes[7].get_stones_str())
        if self.board.bottoms_turn:
            self.turn_label.setText("Your turn")
        else:
            self.turn_label.setText("Enemy's turn")

    def enable_buttons(self):
        self.p_hole_0.setEnabled(self.board.holes[0].stones != 0)
        self.p_hole_1.setEnabled(self.board.holes[1].stones != 0)
        self.p_hole_2.setEnabled(self.board.holes[2].stones != 0)
        self.p_hole_3.setEnabled(self.board.holes[3].stones != 0)
        self.p_hole_4.setEnabled(self.board.holes[4].stones != 0)
        self.p_hole_5.setEnabled(self.board.holes[5].stones != 0)
        self.end_turn.setEnabled(True)

    def disable_buttons(self):
        self.p_hole_0.setEnabled(False)
        self.p_hole_1.setEnabled(False)
        self.p_hole_2.setEnabled(False)
        self.p_hole_3.setEnabled(False)
        self.p_hole_4.setEnabled(False)
        self.p_hole_5.setEnabled(False)

    def hole_button_pressed(self, hole_number):
        self.disable_buttons()
        last_hole = self.board.holes[hole_number].remove_stones(self.board.bottoms_turn)
        self.board.is_beating(last_hole)
        if self.board.is_ending():
            self.end_game()
            return
        if self.board.is_finishing_in_well(last_hole):
            self.enable_buttons()
        self.update_ui()

    def ai_turn(self):
        self.board.bottoms_turn = False
        self.end_turn.setEnabled(False)
        _, moves = Board.minimax(self.board, 4, False)
        is_ending = self.board.execute_moves(moves)
        if is_ending:
            self.end_game()
            return
        self.board.bottoms_turn = True
        self.update_ui()
        self.enable_buttons()

    def game_start(self):
        self.start_game.setEnabled(False)
        if self.board.bottoms_turn:
            self.enable_buttons()
        else:
            self.ai_turn()

    def game_restart(self):
        self.disable_buttons()
        for h in self.board.holes:
            h.stones = 4
        self.board.holes[6].stones = 0
        self.board.holes[13].stones = 0
        self.board.bottoms_turn = bool(getrandbits(1))
        self.board.nodes_top_player = 0
        self.board.nodes_bottom_player = 0
        self.board.total_game_time = 0
        self.board.first_move_made = False
        Board.reset_counters()
        # self.start_game.setEnabled(True)
        # self.update_ui()

    def ai_vs_ai(self, alpha_beta, tree_depth):
        bottom_moves = 0
        top_moves = 0
        while True:
            start_time = time.time()
            if not self.board.first_move_made:
                last_hole = self.random_move()
                if (self.board.bottoms_turn and last_hole == 6) or (not self.board.bottoms_turn and last_hole == 13):
                    _ = self.random_move()
                self.board.switch_turn()
                self.board.first_move_made = True

            if not alpha_beta:
                # _, moves = Board.minimax(self.board, 2, self.board.bottoms_turn)
                _, moves = Board.heuristic_minimax(self.board, tree_depth, self.board.bottoms_turn,
                                                   self.board.bottoms_turn, 0)
            else:
                # _, moves = Board.minimax_alpha_beta(self.board, 2, -inf, inf,  self.board.bottoms_turn)
                _, moves = Board.heuristic_minimax_alpha_beta(self.board, tree_depth, -inf, inf,
                                                              self.board.bottoms_turn, self.board.bottoms_turn, 0)
            is_ending = self.board.execute_moves(moves)
            if self.board.bottoms_turn:
                bottom_moves += len(moves)
            else:
                top_moves += len(moves)
            end_time = time.time()
            self.board.total_game_time += (end_time - start_time)
            if is_ending:
                self.end_game(top_moves, bottom_moves)
                break
            self.board.switch_turn()
            # self.update_ui()

    def random_move(self):
        choice = random.choice(self.board.get_available_holes(self.board.bottoms_turn))
        return self.board.holes[choice].remove_stones(self.board.bottoms_turn)

    def end_game(self, top_moves, bottom_moves):
        self.end_turn.setEnabled(False)
        self.update_ui()
        self.disable_buttons()
        bott_nodes, top_nodes = Board.get_game_stats()
        if self.board.holes[6].stones > self.board.holes[13].stones:
            print(f'Visited nodes: {bott_nodes}\nMoves: {bottom_moves}')
        else:
            print(f'Visited nodes: {top_nodes}\nMoves: {top_moves}')
        print(f'Total game time: {self.board.total_game_time}')
