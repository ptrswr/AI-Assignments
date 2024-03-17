from objects import Board
from engine import *
import sys
from time import sleep


def main():
    b = Board()

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    engine = Engine(main_window, b)
    for i in range(5):
        engine.ai_vs_ai(True, 4)
        engine.game_restart()
        print()

    # main_window.show()
    # sys.exit(app.exec_())


if __name__ == '__main__':
    main()
