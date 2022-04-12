import numpy as np
import random

class Game():           #棋盘类，定义了棋盘和一些功能，是下棋时显示出来的棋盘
    def __init__(self):
        self.board = np.zeros([5,5])

    def RandResetBoard(self):
        self.board = np.zeros([5,5])
        boardlist0 = [1., 2., 3., 4., 5., 6.]
        boardlist1 = [-1., -2., -3., -4., -5., -6.]
        random.shuffle(boardlist0)
        random.shuffle(boardlist1)
        self.board[0][0] = boardlist0[0]
        self.board[0][1] = boardlist0[1]
        self.board[0][2] = boardlist0[2]
        self.board[1][0] = boardlist0[3]
        self.board[1][1] = boardlist0[4]
        self.board[2][0] = boardlist0[5]
        self.board[4][4] = boardlist1[0]
        self.board[3][4] = boardlist1[1]
        self.board[2][4] = boardlist1[2]
        self.board[4][3] = boardlist1[3]
        self.board[3][3] = boardlist1[4]
        self.board[4][2] = boardlist1[5]
        
    def ResetBoard(self):
        self.board = np.zeros([5,5])
        self.board[0][0] = 1.
        self.board[0][1] = 2.
        self.board[0][2] = 3.
        self.board[1][0] = 4.
        self.board[1][1] = 5.
        self.board[2][0] = 6.
        self.board[4][4] = -1.
        self.board[3][4] = -2.
        self.board[2][4] = -3.
        self.board[4][3] = -4.
        self.board[3][3] = -5.
        self.board[4][2] = -6.

    def Move(self, position, direction):    #0水平，1竖直，2斜方向
        x = position[0]
        y = position[1]
        if self.board[x][y] > 0:
            if direction == 0:
                self.board[x][y + 1] = self.board[x][y]
                self.board[x][y] = 0.
            elif direction == 1:
                self.board[x + 1][y] = self.board[x][y]
                self.board[x][y] = 0.
            elif direction == 2:
                self.board[x + 1][y + 1] = self.board[x][y]
                self.board[x][y] = 0.
        elif self.board[x][y] < 0:
            if direction == 0:
                self.board[x][y - 1] = self.board[x][y]
                self.board[x][y] = 0.
            elif direction == 1:
                self.board[x - 1][y] = self.board[x][y]
                self.board[x][y] = 0.
            elif direction == 2:
                self.board[x - 1][y - 1] = self.board[x][y]
                self.board[x][y] = 0.

    def ChooseChess(self, Randnum):
        tempboard = self.board.copy()
        if Randnum > 0:
            tempboard = np.where(tempboard < 0, 0, tempboard)
        elif Randnum < 0:
            tempboard = np.where(tempboard > 0, 0, tempboard)
            Randnum = -Randnum
            tempboard = -tempboard
        tempboard -= Randnum
        #print(tempboard)
        if 0 in tempboard:
            return [np.where(tempboard == 0)[0][0], np.where(tempboard == 0)[1][0]], [np.where(tempboard == 0)[0][0], np.where(tempboard == 0)[1][0]]
        else:
            if (tempboard < 0).all():
                return [np.where(tempboard == tempboard.max())[0][0], np.where(tempboard == tempboard.max())[1][0]], [np.where(tempboard == tempboard.max())[0][0], np.where(tempboard == tempboard.max())[1][0]]
            elif (np.where(tempboard == -Randnum, 12, tempboard)>0).all():
                tempboard = np.where(tempboard == -Randnum, 12, tempboard)
                return [np.where(tempboard == tempboard.min())[0][0], np.where(tempboard == tempboard.min())[1][0]], [np.where(tempboard == tempboard.min())[0][0], np.where(tempboard == tempboard.min())[1][0]]
            else:
                min = np.where(tempboard < 0, 12, tempboard)
                max = np.where(tempboard > 0, -12, tempboard)
                return [np.where(min == min.min())[0][0], np.where(min == min.min())[1][0]], [np.where(max == max.max())[0][0], np.where(max == max.max())[1][0]]

    def GetWinner(self):
        if self.board[0][0] < 0 or (self.board <= 0).all():
            Winner = -1
        elif self.board[4][4] > 0 or (self.board >= 0).all():
            Winner = 1
        else:
            Winner = 0

        return Winner