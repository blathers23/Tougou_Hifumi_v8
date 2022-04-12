#这个库就是程序真正的核心库，简单来说，我写的程序的第一个版本，就是没有GUI，只有命令行窗口的那种版本，就是这个
#文件，现在有了GUI，就把一些只有命令行才需要的语句删除了而已，至于文件名字，翻译叫东乡一二三是一个游戏里的人物，她的
#人物原型加藤一二三，是日本将棋的棋手，既擅长规则一步内不能思考很久的快棋，也擅长在棋盘前长时间思考的慢棋，
#与这个程序很相似，如果用神经网络直接输出结果，那么一步棋不需要0.01s，而且准确率挺高，加上蒙特卡洛算法之后，运行速度
#大幅下降，但是棋力也有很大提升。

import numpy as np  #非常重要的数组操作库
import os           #文件交互用的库，python用这个库读写文件
import MCTS         #MTCS算法
import math         #数学库，这里引用它主要是用几个数学常数
from tqdm import tqdm   #tqdm库是一个简单进度条的库，运行的时候命令行（如果有的话）里的进度条就是用的这个库
import Net              #神经网络
from VEGAME import Game as VGame    #虚拟棋盘，蒙特卡洛的模拟都走在虚拟棋盘上

VGame = VGame(np.zeros((5,5)))  #初始化虚拟棋盘

class EinStein_Game():  #python的类写法，不理解的话先看python类的概念，有编程基础应该看看就会了
    def __init__(self):
        self.board = np.zeros([5,5])    #初始化真实棋盘
        self.PI = []                
        self.CI = []
        self.RCSS = []              #红色棋子初始设定
        self.BCSS = []
        self.Player = 0             #当前轮到谁走了
        self.UCTSTEPS = 1000        #蒙特卡洛模拟次数，有几个节点需要模拟，总模拟次数就是这个数的倍数
        self.STEP_COUNT = 4         #前4步的蒙特卡罗模拟中，棋子移动方向的概率由神经网络决定    #为什么让前几步的移动方向按某种概率决定呢？我猜的，可以试试让后几步试试看看效果好不好，具体思路我在MCTS.py里写
        self.P_Threshold = 1/4      #概率阈值需小于1/3  #如果一个走法被神经网络认为概率很低，那就直接不模拟，25%就是这个阈值
        self.Move_By_P = False      #是否按方向概率模拟，现在是否，就是26行说的这个
        self.Threshold_Mode = False #时候根据阈值否决走法，现在是否，就是27行说的这个
        self.Search = True          #是否搜索，不搜索的话就是神经网络直接走子
        if self.P_Threshold > 1/3:  #这个概率，是个相对概率，如果有三个走法，他们概率相同，那么他们的走子概率都是33.3%，这就是为什么这个阈值不能小于33.3%，其实也可以试试大于33.3%，功能我都写好了，去年比赛前要是有比较长的时间对程序进行测试，说不定棋力能好些，可惜我写完程序都8月中了。
            self.P_Threshold = 1/3

    def Change_Mode(self):          #上面介绍两种模式，都有自己的参数（26，27行），这个代码可以让AI根据棋面情况自动调整这两个参数
        if (self.board[:2,:2] < 0).any() or (self.board[-2:,-2:] > 0).any():    #开始涉及numpy数组的内容（board[:2,:2]等）这些个自学吧，比较重要
            self.STEP_COUNT = 0     
            self.P_Threshold = 0
        elif (self.board[:3,:3] < 0).any() or (self.board[-3:,-3:] > 0).any():
            self.STEP_COUNT = 3
            self.P_Threshold = 1/4
        else:
            self.STEP_COUNT = 6
            self.P_Threshold = 1/4
        
                    
    def createBoard(self, red, blue):   #新建棋盘，传入红蓝两个参数，就是新棋盘开始时候的布局，这里用的是GUI文件里传进来的，具体看新开局那一块，善用VSCODE的Ctrl+F
        self.PI = []
        self.CI = []
        self.RCSS = ['R:']              #写了这一大堆，就是棋谱那个txt文件头部的位置那两行，RCSS、BCSS保存棋谱的时候会调用。
        self.BCSS = ['B:']
        self.board = np.zeros([5,5])
        self.board[0][0] =  red[0]
        self.RCSS.append('A5-')
        self.RCSS.append(str(int(red[0])))
        self.RCSS.append(';')
        self.board[0][1] =  red[1]
        self.RCSS.append('B5-')
        self.RCSS.append(str(int(red[1])))
        self.RCSS.append(';')
        self.board[0][2] =  red[2]
        self.RCSS.append('C5-')
        self.RCSS.append(str(int(red[2])))
        self.RCSS.append(';')
        self.board[1][0] =  red[3]
        self.RCSS.append('A4-')
        self.RCSS.append(str(int(red[3])))
        self.RCSS.append(';')
        self.board[1][1] =  red[4]
        self.RCSS.append('B4-')
        self.RCSS.append(str(int(red[4])))
        self.RCSS.append(';')
        self.board[2][0] =  red[5]
        self.RCSS.append('A3-')
        self.RCSS.append(str(int(red[5])))
        self.RCSS.append(';')
        self.board[2][4] = -abs(blue[0])
        self.BCSS.append('E3-')
        self.BCSS.append(str(int(abs(blue[0]))))
        self.BCSS.append(';')
        self.board[3][3] = -abs(blue[1])
        self.BCSS.append('D2-')
        self.BCSS.append(str(int(abs(blue[1]))))
        self.BCSS.append(';')
        self.board[3][4] = -abs(blue[2])
        self.BCSS.append('E2-')
        self.BCSS.append(str(int(abs(blue[2]))))
        self.BCSS.append(';')
        self.board[4][2] = -abs(blue[3])
        self.BCSS.append('C1-')
        self.BCSS.append(str(int(abs(blue[3]))))
        self.BCSS.append(';')
        self.board[4][3] = -abs(blue[4])
        self.BCSS.append('D1-')
        self.BCSS.append(str(int(abs(blue[4]))))
        self.BCSS.append(';')
        self.board[4][4] = -abs(blue[5])
        self.BCSS.append('E1-')
        self.BCSS.append(str(int(abs(blue[5]))))
        self.BCSS.append(';')
        self.PI.append(list(self.board.reshape(25)))

    def ChooseChess(self, Randnum):     #根据随机数选择棋子，我写的这个算法可能时间复杂度太高了，没学过数据结构的人是这样的，如果可以的话可以优化一下。
        if Randnum > 0:
            self.Player = 1
            tempboard = np.where(self.board < 0, 0, self.board)
        elif Randnum < 0:
            self.Player = -1
            tempboard = np.where(self.board > 0, 0, self.board)
            Randnum = -Randnum
            tempboard = -tempboard
        tempboard -= Randnum
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

    def Move(self, position, direction, rand):  #移动棋子函数，需要移动的棋子的位置，移动的方向，还有摇出来的随机数
        x = position[0]
        y = position[1]
        #print(self.board[x][y])
        if self.board[x][y] > 0:                            #
            if direction == 0:                              #移动的方向0横1竖2斜
                self.board[x][y + 1] = self.board[x][y]     #再讲一下numpy的坐标轴，坐标轴是个右手系，可以看
                self.board[x][y] = 0.                       #https://pic.liesio.com/2021/02/21/ce781746923b9.png
                y += 1
            elif direction == 1:
                self.board[x + 1][y] = self.board[x][y]
                self.board[x][y] = 0.
                x += 1
            elif direction == 2:
                self.board[x + 1][y + 1] = self.board[x][y]
                self.board[x][y] = 0.
                x += 1 
                y += 1
        elif self.board[x][y] < 0:
            if direction == 0:
                self.board[x][y - 1] = self.board[x][y]
                self.board[x][y] = 0.
                y -= 1
            elif direction == 1:
                self.board[x - 1][y] = self.board[x][y]
                self.board[x][y] = 0.
                x -= 1
            elif direction == 2:
                self.board[x - 1][y - 1] = self.board[x][y]
                self.board[x][y] = 0.
                x -= 1
                y -= 1

        self.appendCI(x, y, rand)   #随机数走个过场，主要是为了送进棋谱生成函数。

    def GetWinner(self):            #看看谁获胜了
        if self.board[0][0] < 0 or (self.board <= 0).all():
            Winner = -1
        elif self.board[4][4] > 0 or (self.board >= 0).all():
            Winner = 1
        else:
            Winner = 0

        return Winner

    def appendCI(self, x, y, rand):     #新增一条棋谱记录，最后只要把CI打印出来就是棋谱了
        chess = self.board[x][y]
        if chess > 0:
            chess = 'R' + str(int(chess))
        else:
            chess = 'B' + str(int(-chess))
        x = str(int(5 - x))
        if y == 0:
            y = 'A'
        elif y == 1:
            y = 'B'
        elif y == 2:
            y = 'C'
        elif y == 3:
            y = 'D'
        elif y == 4:
            y = 'E'
        self.CI.append(':' + str(int(abs(rand))) + ';(' + chess + ',' + y + x + ')')

    def UCTbyList(self, MoveList, Step_Count):  #根据传入的列表来设计节点个数进行蒙特卡洛算法
        Num = len(MoveList)
        N = [0.] * Num
        UCTValue = [0.] * Num
        WinSum = [0.] * Num
        for _ in tqdm(range(self.UCTSTEPS * Num), ncols=50):
            board = self.board.copy()   #copy一下要进行模拟的棋盘，python是面向对象的，不按值传递也不按引用传递
            i = np.argmax(UCTValue)
            value = MCTS.MCTS(board, MoveList[i][0], MoveList[i][1], VGame, STEPS=1, STEP_COUNTS=Step_Count, Move_By_P=self.Move_By_P)  #value简单来说1就是获胜，0就是失败，从而重新计算uct值
            WinSum[i] += value
            N[i] += 1
            for i in range(Num):
                UCTValue[i] = 0.4 * WinSum[i] / (N[i] + 1e-99) + (math.log(np.sum(N))/(N[i] + 1e-99)) ** 0.5        
        index = np.argmax(np.array(WinSum) / np.array(N))
        position = MoveList[index][0]
        moveDirection = MoveList[index][1]
        print(MoveList.reshape(-1))
        print(np.array(WinSum) / np.array(N))

        return position, moveDirection  #返回走子和走子方向
    
    def GetWay(self, Position):     #获得走子方向，在一些位置上，棋子只能走一个方向
        if Position[0] == 4 and self.board[Position[0]][Position[1]] > 0:
            way = [0]
        elif Position[1] == 4 and self.board[Position[0]][Position[1]] > 0:
            way = [1]
        elif Position[0] == 0 and self.board[Position[0]][Position[1]] < 0:
            way = [0]
        elif Position[1] == 0 and self.board[Position[0]][Position[1]] < 0:
            way = [1]
        else:
            way = [0,1,2]
        return way

    def Eight_Move(self, Position0, Position1): #8Move是因为我写的程序自己迭代了八个版本
        self.Position0 = Position0      #可以移动的两个棋子的位置
        self.Position1 = Position1
        if self.Threshold_Mode:
            self.Change_Mode()
        if Position0 == Position1:      #如果这两个位置一样，那就是只用考虑一个棋子
            Position = Position0
            way = self.GetWay(Position) #获取走子方向
            if len(way) == 1:           
                moveDirection = way[0]
            else:    
                MoveList = []   #MoveList是UCTbyList的参数，方便我写UCT代码的产物
                for i in range(len(way)):
                    MoveList.append([Position, way[i]])
                if self.Search:
                    if self.Threshold_Mode:
                        P = Net.Get_P(self.board.copy(), MoveList)
                        P = np.where(P<self.P_Threshold, False, True)
                        MoveList = np.array(MoveList)[P]
                        if len(MoveList) == 1:
                            moveDirection = MoveList[0][1]
                        else:
                            _, moveDirection = self.UCTbyList(MoveList, Step_Count=self.STEP_COUNT)
                    else:
                        MoveList = np.array(MoveList)
                        _, moveDirection = self.UCTbyList(MoveList, Step_Count=self.STEP_COUNT)
                else:
                    moveDirection = np.argmax(Net.Get_P(self.board.copy(), MoveList))
        else:
            way0 = self.GetWay(Position0)
            way1 = self.GetWay(Position1)
            MoveList = []
            for i in range(len(way0)):
                MoveList.append([Position0, way0[i]])
            for i in range(len(way1)):
                MoveList.append([Position1, way1[i]])
            if self.Search:
                if self.Threshold_Mode:
                    P = Net.Get_P(self.board.copy(), MoveList)
                    P = np.where(P<self.P_Threshold/2, False, True)
                    MoveList = np.array(MoveList)[P]
                    if len(MoveList) == 1:
                        moveDirection = MoveList[0][1]
                    else:
                        _, moveDirection = self.UCTbyList(MoveList, Step_Count=self.STEP_COUNT)
                else:
                    MoveList = np.array(MoveList)
                    Position, moveDirection = self.UCTbyList(MoveList, Step_Count=self.STEP_COUNT)
            else:
                Index = np.argmax(Net.Get_P(self.board.copy(), MoveList))
                if Index <= 2:
                    Position = MoveList[0][0]
                    moveDirection = Index
                else:
                    Position = MoveList[3][0]
                    moveDirection = Index - 3

        return Position, moveDirection
    
    def Sc(self):       #debug用的
        print(Net.Mark(self.board))