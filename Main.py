#Mian.py 文件是程序的主入口，主要内容是GUI的绘制、还有调用Tougou_Hifumi.py的功能。

import tkinter as tk            #python自带的GUI库
import tkinter.messagebox       #tkinter的库
import numpy as np              #处理数组的常用库，很重要
import time                     #大概是输出AI思考用时的吧，忘了
import os                       #OS是文件操作用的库
import numpy as np              #import 重复了，删了就行
import random                   #python自带的随机库，用于生成随机数

#该部分是保存了一些全局变量，生成棋盘、保存棋谱的时候会调用
TEAM1_NAME = '命运石之门'       #队伍名称
TEAM2_NAME = '代码敲得对'
GAME_NAME = '2020 CCGC'         #比赛名称
GAME_LOCATION = '线上'          #比赛地点
global ListB, ListR             #声明全局变量
ListR = [1,6,5,4,2,3]           #R 就是 Red，红方默认布局，GUI里新开一局游戏，布局就是读的这里
ListB = [3,5,1,4,2,6]           #蓝方默认布局

#引入AI文件和棋盘文件
from Tougou_Hifumi import EinStein_Game #AI的所有功能都写在Touhou_Hifumi.py文件里，详见这个文件。
Game = EinStein_Game()                  #创建棋盘类，相当于真正的棋盘，在程序里的体现，详见这个文件。

#下面很长都是GUI绘制，可以不看。
Board00 = [30, 40]                      #这是棋子定点用的列表，例：Board00就是00棋子的左上角的位置（x:30,y:40）
Board01 = [Board00[0]+90, Board00[1]]   #这里再简要说一下GUI的思路，为了方便点击，所有的地方都是棋子
Board02 = [Board01[0]+90, Board01[1]]   #棋子有三种，红方，蓝方，和表示没棋子的灰色棋子
Board03 = [Board02[0]+90, Board02[1]]   #所以场面上永远都有25个棋子
Board04 = [Board03[0]+90, Board03[1]]   #这些个定点列表就是定出他们的左上角，方便绘制在程序的窗口上
Board10 = [Board00[0], Board00[1]+80]
Board11 = [Board10[0]+90, Board10[1]]
Board12 = [Board11[0]+90, Board11[1]]
Board13 = [Board12[0]+90, Board12[1]]
Board14 = [Board13[0]+90, Board13[1]]
Board20 = [Board10[0], Board10[1]+80]
Board21 = [Board20[0]+90, Board20[1]]
Board22 = [Board21[0]+90, Board21[1]]
Board23 = [Board22[0]+90, Board22[1]]
Board24 = [Board23[0]+90, Board23[1]]
Board30 = [Board20[0], Board20[1]+80]
Board31 = [Board30[0]+90, Board30[1]]
Board32 = [Board31[0]+90, Board31[1]]
Board33 = [Board32[0]+90, Board32[1]]
Board34 = [Board33[0]+90, Board33[1]]
Board40 = [Board30[0], Board30[1]+80]
Board41 = [Board40[0]+90, Board40[1]]
Board42 = [Board41[0]+90, Board41[1]]
Board43 = [Board42[0]+90, Board42[1]]
Board44 = [Board43[0]+90, Board43[1]]

main_window = tk.Tk()           #这是程序真正的主窗口，是一个很小的窗口，下面会详细解释。
main_window.geometry('200x30')
main_window.title(':)')
Selected = []                   #有无选定的棋子，选定的棋子会变色，以及移动，都会把棋子的位置暂存到这个列表当中，空就是没选中棋子
winner = 0                      #有无赢家，0就是没有，1是红方获胜，-1是蓝方       

def start_game():               #游戏开始的函数
    global winner
    window = tk.Toplevel(main_window)   #这里新建了一个子窗口，才是程序运行的界面，这个窗口是依托在51行的主窗口上的
    window.title('Welcome!')            #Tkinter有个特点，就是主窗口一旦关闭，程序就会退出运行
    window.geometry('660x500')          #这样做的目的主要是为了偷懒，每次新开一局，只要把上一局子窗口直接关闭
    window.resizable(False, False)      #再新建一个子窗口就好，主窗口不关闭，程序也不会退出运行。
    winner = 0                          #大大减少了我的思考量

    def hit00():                        #麻木时刻开始，hit**即为点击对应位置的棋子
        global Selected, winner
        x = 0
        y = 0
        if winner != 0:                 #如果已经分出胜负了，再点击棋盘就没反应（return 0）
            return 0
        if Game.board[x][y] == 0:       #Game.board是一个二维数组，按位置保存了棋子，该行的意思就是点了个空棋子，或者没棋子的地方
            if Selected == []:          #如果你忘了空棋子是什么意思，请看26-28行
                pass                    #该if语句就是说如果我们点了个寂寞，原本就没点过别的棋子，就什么也不做，这里要结合程序来理解。
            elif Selected != []:        #如果我们之前选过别的棋子，就把棋子移动过去。
                Game.board[x][y] = Selected[0]              #Selected列表[0]位置的值就是选择过的棋子，把这个棋子移动到你点击的位置（0，0）
                Game.board[Selected[1]][Selected[2]] = 0.   #选择过的棋子原本的地方就扣掉
                Selected = []                               #清空选择过的，如果你难以理解，就打开软件自己点点，如果一个棋子被选择了，那么他会变色，变色会在下面讲到
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))   #这里是个傻瓜语句，try就是尝试，如果没报错就try，try报错了就except
                except:                                                 #这个RandomLB就是随机数列表的意思，就是绘制在屏幕上的那个选择随机数的栏
                    rand = Game.board[x][y]                             #try的内容就是获取你选择的随机数，记录下来，如果你没选，就假装你走的那个棋子就是你摇到的随机数。
                    #太长了我开一行新的写，这个随机数接下来是用来记录棋谱的（棋谱要保存你摇出来的随机数），写这个try主要是我懒得每次都选随机数才能走子，如果我懒的没选的话，就默认我走的就是摇出来的数
                Game.appendCI(x,y,rand)     #记录棋谱用的append Chess Information
                Game.PI.append(list(Game.board.reshape(25)))    #这个是方便悔棋记录的，就是把当前棋盘这个二维数组打平成一维，然后记录下来，到时候再讲
                winner = Game.GetWinner()   #判断输赢
                congratulation(winner)      #庆祝输赢，判断语句在函数里面
        elif Game.board[x][y] != 0:     #如果我们点的位置有棋子（指红or蓝）
            if Selected == []:          #如果我们之前没点过别的棋子（指红or蓝），那么我们点的这个棋子就要保存下来
                Selected.append(Game.board[x][y])   #Selected数组第一个位置是 棋子是啥
                Selected.append(x)                  #第二个位置是x坐标
                Selected.append(y)                  #三 y
            elif Selected != []:                    #如果之前点过别的棋子
                if Selected[0] == Game.board[x][y]: #如果现在点的和以前点的是一个棋子
                    Selected = []                   #那就假装事情没有发生过
                else:                               #否则 就是点的别的棋子
                    Game.board[x][y] = Selected[0]  #吃子
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()  #show指令用来刷新GUI上的棋盘

    #总结，hit函数就是点击棋子在不同情况下会做什么反应的函数，hit01就是点01位置用到的函数
    #就是说这么这样的函数总共有5*5=50个
    #这些函数的差别只有函数名和x，y这两个数不同，聪明如你可能已经发现这个x，y就是为了方便我复制粘贴写起来方便才这么写的
    #至于为什么要用50个函数，这个接下来讲到。跳过这些重复代码到1144行。
    def hit01():
        global Selected, winner
        x = 0
        y = 1
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit02():
        global Selected, winner
        x = 0
        y = 2
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit03():
        global Selected, winner
        x = 0
        y = 3
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit04():
        global Selected, winner
        x = 0
        y = 4
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit10():
        global Selected, winner
        x = 1
        y = 0
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit11():
        global Selected, winner
        x = 1
        y = 1
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit12():
        global Selected, winner
        x = 1
        y = 2
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit13():
        global Selected, winner
        x = 1
        y = 3
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit14():
        global Selected, winner
        x = 1
        y = 4
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit20():
        global Selected, winner
        x = 2
        y = 0
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit21():
        global Selected, winner
        x = 2
        y = 1
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit22():
        global Selected, winner
        x = 2
        y = 2
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit23():
        global Selected, winner
        x = 2
        y = 3
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit24():
        global Selected, winner
        x = 2
        y = 4
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit30():
        global Selected, winner
        x = 3
        y = 0
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit31():
        global Selected, winner
        x = 3
        y = 1
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit32():
        global Selected, winner
        x = 3
        y = 2
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit33():
        global Selected, winner
        x = 3
        y = 3
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit34():
        global Selected, winner
        x = 3
        y = 4
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit40():
        global Selected, winner
        x = 4
        y = 0
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit41():
        global Selected, winner
        x = 4
        y = 1
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit42():
        global Selected, winner
        x = 4
        y = 2
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int((RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit43():
        global Selected, winner
        x = 4
        y = 3
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    def hit44():
        global Selected, winner
        x = 4
        y = 4
        if winner != 0:
            return 0
        if Game.board[x][y] == 0:
            if Selected == []:
                pass 
            elif Selected != []:
                Game.board[x][y] = Selected[0]
                Game.board[Selected[1]][Selected[2]] = 0.
                Selected = []
                try:
                    rand = int(RandomLB.get(RandomLB.curselection()))
                except:
                    rand = Game.board[x][y]
                Game.appendCI(x,y,rand)
                Game.PI.append(list(Game.board.reshape(25)))
                winner = Game.GetWinner()
                congratulation(winner)
        elif Game.board[x][y] != 0:
            if Selected == []:
                Selected.append(Game.board[x][y])
                Selected.append(x)
                Selected.append(y)
            elif Selected != []:
                if Selected[0] == Game.board[x][y]:
                    Selected = []
                else:
                    Game.board[x][y] = Selected[0]
                    Game.board[Selected[1]][Selected[2]] = 0.
                    Selected = []
                    try:
                        rand = int(RandomLB.get(RandomLB.curselection()))
                    except:
                        rand = Game.board[x][y]
                    Game.appendCI(x,y,rand)
                    Game.PI.append(list(Game.board.reshape(25)))
                    winner = Game.GetWinner()
                    congratulation(winner)
        show()

    #show函数是刷新棋盘界面用的，每点一下棋子，要是棋盘有什么变化，那就是调用了show函数，刷新了界面
    def show(): #red pink AliceBlue RoyalBlue 这是以前注释的棋子颜色吧
        global Selected
        BoardChess = Game.board #Game.board就是按位置保存的棋子都是啥
        #print(BoardChess)
        if Selected == []:      #如果之前没选棋子
            x = 'D'             #忘了为什么是‘D’了，可能是我写着玩的吧，可能只要不是数就行，不重要，忘了
            y = 'D'
        elif Selected != []:    #如果之前选过棋子就把棋子位置取出来
            x = Selected[1]
            y = Selected[2]
        if BoardChess[0][0] == 0:   #如果00位置没有棋子
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit00).place(x=Board00[0],y=Board00[1])  #新建一个按钮（就是棋子）在这里放一个灰色无名按钮，当棋盘。place放在Board00位置（若忘，参见25行）
            #讲一下按钮的参数：window就是把棋子放在window这个窗口上，text是按钮文本，bg是按钮颜色，padxpady是按钮长宽，虽然数不一样但是看起来就是正方形，如果数一样看起来就不是正方形
            #font是文本的字体，最坑的就是comman，指按下这个按钮会触发什么函数，如果写成hit00()，那么只要执行到这个创建按钮的命令，就会执行hit00()，正常来说应该是点了按钮才会触发。导致不能输入括号，就不能传递参数，才有上面的重复代码
            #后来了解到tk.Button指令里应该会有一个专门用来给command传递参数用的参数，谁知道呢，我都写完了，哎，懒得改了，也不差。
        elif BoardChess[0][0] > 0 and [x, y] != [0, 0]: #如果该棋子是个正数（指红方）且不是00位置，就在00位置放个红色该棋子
            tk.Button(window, text=str(int(BoardChess[0][0]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit00).place(x=Board00[0],y=Board00[1])
        elif BoardChess[0][0] < 0 and [x, y] != [0, 0]: #同理，放个蓝的
            tk.Button(window, text=str(int(-BoardChess[0][0]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit00).place(x=Board00[0],y=Board00[1])
        elif BoardChess[0][0] > 0 and [x, y] == [0, 0]: #如果被选择的棋子就是00位置，正数（红方）棋子就变粉色
            tk.Button(window, text=str(int(BoardChess[0][0]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit00).place(x=Board00[0],y=Board00[1])
        elif BoardChess[0][0] < 0 and [x, y] == [0, 0]: #蓝方棋子就变浅蓝，表示被选上了
            tk.Button(window, text=str(int(-BoardChess[0][0]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit00).place(x=Board00[0],y=Board00[1])

            #经典重复代码，1436行见
        if BoardChess[0][1] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit01).place(x=Board01[0],y=Board01[1])
        elif BoardChess[0][1] > 0 and [x, y] != [0, 1]:
            tk.Button(window, text=str(int(BoardChess[0][1]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit01).place(x=Board01[0],y=Board01[1])
        elif BoardChess[0][1] < 0 and [x, y] != [0, 1]:
            tk.Button(window, text=str(int(-BoardChess[0][1]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit01).place(x=Board01[0],y=Board01[1])
        elif BoardChess[0][1] > 0 and [x, y] == [0, 1]:
            tk.Button(window, text=str(int(BoardChess[0][1]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit01).place(x=Board01[0],y=Board01[1])
        elif BoardChess[0][1] < 0 and [x, y] == [0, 1]:
            tk.Button(window, text=str(int(-BoardChess[0][1]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit01).place(x=Board01[0],y=Board01[1])

        if BoardChess[0][2] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit02).place(x=Board02[0],y=Board02[1])
        elif BoardChess[0][2] > 0 and [x, y] != [0, 2]:
            tk.Button(window, text=str(int(BoardChess[0][2]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit02).place(x=Board02[0],y=Board02[1])
        elif BoardChess[0][2] < 0 and [x, y] != [0, 2]:
            tk.Button(window, text=str(int(-BoardChess[0][2]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit02).place(x=Board02[0],y=Board02[1])
        elif BoardChess[0][2] > 0 and [x, y] == [0, 2]:
            tk.Button(window, text=str(int(BoardChess[0][2]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit02).place(x=Board02[0],y=Board02[1])
        elif BoardChess[0][2] < 0 and [x, y] == [0, 2]:
            tk.Button(window, text=str(int(-BoardChess[0][2]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit02).place(x=Board02[0],y=Board02[1])

        if BoardChess[0][3] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit03).place(x=Board03[0],y=Board03[1])
        elif BoardChess[0][3] > 0 and [x, y] != [0, 3]:
            tk.Button(window, text=str(int(BoardChess[0][3]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit03).place(x=Board03[0],y=Board03[1])
        elif BoardChess[0][3] < 0 and [x, y] != [0, 3]:
            tk.Button(window, text=str(int(-BoardChess[0][3]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit03).place(x=Board03[0],y=Board03[1])
        elif BoardChess[0][3] > 0 and [x, y] == [0, 3]:
            tk.Button(window, text=str(int(BoardChess[0][3]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit03).place(x=Board03[0],y=Board03[1])
        elif BoardChess[0][3] < 0 and [x, y] == [0, 3]:
            tk.Button(window, text=str(int(-BoardChess[0][3]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit03).place(x=Board03[0],y=Board03[1])

        if BoardChess[0][4] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit04).place(x=Board04[0],y=Board04[1])
        elif BoardChess[0][4] > 0 and [x, y] != [0, 4]:
            tk.Button(window, text=str(int(BoardChess[0][4]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit04).place(x=Board04[0],y=Board04[1])
        elif BoardChess[0][4] < 0 and [x, y] != [0, 4]:
            tk.Button(window, text=str(int(-BoardChess[0][4]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit04).place(x=Board04[0],y=Board04[1])
        elif BoardChess[0][4] > 0 and [x, y] == [0, 4]:
            tk.Button(window, text=str(int(BoardChess[0][4]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit04).place(x=Board04[0],y=Board04[1])
        elif BoardChess[0][4] < 0 and [x, y] == [0, 4]:
            tk.Button(window, text=str(int(-BoardChess[0][4]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit04).place(x=Board04[0],y=Board04[1])


        if BoardChess[1][0] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit10).place(x=Board10[0],y=Board10[1])
        elif BoardChess[1][0] > 0 and [x, y] != [1, 0]:
            tk.Button(window, text=str(int(BoardChess[1][0]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit10).place(x=Board10[0],y=Board10[1])
        elif BoardChess[1][0] < 0 and [x, y] != [1, 0]:
            tk.Button(window, text=str(int(-BoardChess[1][0]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit10).place(x=Board10[0],y=Board10[1])
        elif BoardChess[1][0] > 0 and [x, y] == [1, 0]:
            tk.Button(window, text=str(int(BoardChess[1][0]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit10).place(x=Board10[0],y=Board10[1])
        elif BoardChess[1][0] < 0 and [x, y] == [1, 0]:
            tk.Button(window, text=str(int(-BoardChess[1][0]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit10).place(x=Board10[0],y=Board10[1])

        if BoardChess[1][1] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit11).place(x=Board11[0],y=Board11[1])
        elif BoardChess[1][1] > 0 and [x, y] != [1, 1]:
            tk.Button(window, text=str(int(BoardChess[1][1]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit11).place(x=Board11[0],y=Board11[1])
        elif BoardChess[1][1] < 0 and [x, y] != [1, 1]:
            tk.Button(window, text=str(int(-BoardChess[1][1]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit11).place(x=Board11[0],y=Board11[1])
        elif BoardChess[1][1] > 0 and [x, y] == [1, 1]:
            tk.Button(window, text=str(int(BoardChess[1][1]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit11).place(x=Board11[0],y=Board11[1])
        elif BoardChess[1][1] < 0 and [x, y] == [1, 1]:
            tk.Button(window, text=str(int(-BoardChess[1][1]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit11).place(x=Board11[0],y=Board11[1])

        if BoardChess[1][2] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit12).place(x=Board12[0],y=Board12[1])
        elif BoardChess[1][2] > 0 and [x, y] != [1, 2]:
            tk.Button(window, text=str(int(BoardChess[1][2]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit12).place(x=Board12[0],y=Board12[1])
        elif BoardChess[1][2] < 0 and [x, y] != [1, 2]:
            tk.Button(window, text=str(int(-BoardChess[1][2]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit12).place(x=Board12[0],y=Board12[1])
        elif BoardChess[1][2] > 0 and [x, y] == [1, 2]:
            tk.Button(window, text=str(int(BoardChess[1][2]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit12).place(x=Board12[0],y=Board12[1])
        elif BoardChess[1][2] < 0 and [x, y] == [1, 2]:
            tk.Button(window, text=str(int(-BoardChess[1][2]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit12).place(x=Board12[0],y=Board12[1])

        if BoardChess[1][3] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit13).place(x=Board13[0],y=Board13[1])
        elif BoardChess[1][3] > 0 and [x, y] != [1, 3]:
            tk.Button(window, text=str(int(BoardChess[1][3]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit13).place(x=Board13[0],y=Board13[1])
        elif BoardChess[1][3] < 0 and [x, y] != [1, 3]:
            tk.Button(window, text=str(int(-BoardChess[1][3]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit13).place(x=Board13[0],y=Board13[1])
        elif BoardChess[1][3] > 0 and [x, y] == [1, 3]:
            tk.Button(window, text=str(int(BoardChess[1][3]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit13).place(x=Board13[0],y=Board13[1])
        elif BoardChess[1][3] < 0 and [x, y] == [1, 3]:
            tk.Button(window, text=str(int(-BoardChess[1][3]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit13).place(x=Board13[0],y=Board13[1])

        if BoardChess[1][4] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit14).place(x=Board14[0],y=Board14[1])
        elif BoardChess[1][4] > 0 and [x, y] != [1, 4]:
            tk.Button(window, text=str(int(BoardChess[1][4]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit14).place(x=Board14[0],y=Board14[1])
        elif BoardChess[1][4] < 0 and [x, y] != [1, 4]:
            tk.Button(window, text=str(int(-BoardChess[1][4]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit14).place(x=Board14[0],y=Board14[1])
        elif BoardChess[1][4] > 0 and [x, y] == [1, 4]:
            tk.Button(window, text=str(int(BoardChess[1][4]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit14).place(x=Board14[0],y=Board14[1])
        elif BoardChess[1][4] < 0 and [x, y] == [1, 4]:
            tk.Button(window, text=str(int(-BoardChess[1][4]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit14).place(x=Board14[0],y=Board14[1])

        if BoardChess[2][0] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit20).place(x=Board20[0],y=Board20[1])
        elif BoardChess[2][0] > 0 and [x, y] != [2, 0]:
            tk.Button(window, text=str(int(BoardChess[2][0]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit20).place(x=Board20[0],y=Board20[1])
        elif BoardChess[2][0] < 0 and [x, y] != [2, 0]:
            tk.Button(window, text=str(int(-BoardChess[2][0]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit20).place(x=Board20[0],y=Board20[1])
        elif BoardChess[2][0] > 0 and [x, y] == [2, 0]:
            tk.Button(window, text=str(int(BoardChess[2][0]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit20).place(x=Board20[0],y=Board20[1])
        elif BoardChess[2][0] < 0 and [x, y] == [2, 0]:
            tk.Button(window, text=str(int(-BoardChess[2][0]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit20).place(x=Board20[0],y=Board20[1])

        if BoardChess[2][1] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit21).place(x=Board21[0],y=Board21[1])
        elif BoardChess[2][1] > 0 and [x, y] != [2, 1]:
            tk.Button(window, text=str(int(BoardChess[2][1]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit21).place(x=Board21[0],y=Board21[1])
        elif BoardChess[2][1] < 0 and [x, y] != [2, 1]:
            tk.Button(window, text=str(int(-BoardChess[2][1]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16),  command=hit21).place(x=Board21[0],y=Board21[1])
        elif BoardChess[2][1] > 0 and [x, y] == [2, 1]:
            tk.Button(window, text=str(int(BoardChess[2][1]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit21).place(x=Board21[0],y=Board21[1])
        elif BoardChess[2][1] < 0 and [x, y] == [2, 1]:
            tk.Button(window, text=str(int(-BoardChess[2][1]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16),  command=hit21).place(x=Board21[0],y=Board21[1])

        if BoardChess[2][2] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit22).place(x=Board22[0],y=Board22[1])
        elif BoardChess[2][2] > 0 and [x, y] != [2, 2]:
            tk.Button(window, text=str(int(BoardChess[2][2]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit22).place(x=Board22[0],y=Board22[1])
        elif BoardChess[2][2] < 0 and [x, y] != [2, 2]:
            tk.Button(window, text=str(int(-BoardChess[2][2]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit22).place(x=Board22[0],y=Board22[1])
        elif BoardChess[2][2] > 0 and [x, y] == [2, 2]:
            tk.Button(window, text=str(int(BoardChess[2][2]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit22).place(x=Board22[0],y=Board22[1])
        elif BoardChess[2][2] < 0 and [x, y] == [2, 2]:
            tk.Button(window, text=str(int(-BoardChess[2][2]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit22).place(x=Board22[0],y=Board22[1])

        if BoardChess[2][3] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit23).place(x=Board23[0],y=Board23[1])
        elif BoardChess[2][3] > 0 and [x, y] != [2, 3]:
            tk.Button(window, text=str(int(BoardChess[2][3]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit23).place(x=Board23[0],y=Board23[1])
        elif BoardChess[2][3] < 0 and [x, y] != [2, 3]:
            tk.Button(window, text=str(int(-BoardChess[2][3]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit23).place(x=Board23[0],y=Board23[1])
        elif BoardChess[2][3] > 0 and [x, y] == [2, 3]:
            tk.Button(window, text=str(int(BoardChess[2][3]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit23).place(x=Board23[0],y=Board23[1])
        elif BoardChess[2][3] < 0 and [x, y] == [2, 3]:
            tk.Button(window, text=str(int(-BoardChess[2][3]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit23).place(x=Board23[0],y=Board23[1])

        if BoardChess[2][4] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit24).place(x=Board24[0],y=Board24[1])
        elif BoardChess[2][4] > 0 and [x, y] != [2, 4]:
            tk.Button(window, text=str(int(BoardChess[2][4]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit24).place(x=Board24[0],y=Board24[1])
        elif BoardChess[2][4] < 0 and [x, y] != [2, 4]:
            tk.Button(window, text=str(int(-BoardChess[2][4]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit24).place(x=Board24[0],y=Board24[1])
        elif BoardChess[2][4] > 0 and [x, y] == [2, 4]:
            tk.Button(window, text=str(int(BoardChess[2][4]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit24).place(x=Board24[0],y=Board24[1])
        elif BoardChess[2][4] < 0 and [x, y] == [2, 4]:
            tk.Button(window, text=str(int(-BoardChess[2][4]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit24).place(x=Board24[0],y=Board24[1])

        if BoardChess[3][0] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit30).place(x=Board30[0],y=Board30[1])
        elif BoardChess[3][0] > 0 and [x, y] != [3, 0]:
            tk.Button(window, text=str(int(BoardChess[3][0]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit30).place(x=Board30[0],y=Board30[1])
        elif BoardChess[3][0] < 0 and [x, y] != [3, 0]:
            tk.Button(window, text=str(int(-BoardChess[3][0]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit30).place(x=Board30[0],y=Board30[1])
        elif BoardChess[3][0] > 0 and [x, y] == [3, 0]:
            tk.Button(window, text=str(int(BoardChess[3][0]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit30).place(x=Board30[0],y=Board30[1])
        elif BoardChess[3][0] < 0 and [x, y] == [3, 0]:
            tk.Button(window, text=str(int(-BoardChess[3][0]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit30).place(x=Board30[0],y=Board30[1])

        if BoardChess[3][1] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit31).place(x=Board31[0],y=Board31[1])
        elif BoardChess[3][1] > 0 and [x, y] != [3, 1]:
            tk.Button(window, text=str(int(BoardChess[3][1]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit31).place(x=Board31[0],y=Board31[1])
        elif BoardChess[3][1] < 0 and [x, y] != [3, 1]:
            tk.Button(window, text=str(int(-BoardChess[3][1]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit31).place(x=Board31[0],y=Board31[1])
        elif BoardChess[3][1] > 0 and [x, y] == [3, 1]:
            tk.Button(window, text=str(int(BoardChess[3][1]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit31).place(x=Board31[0],y=Board31[1])
        elif BoardChess[3][1] < 0 and [x, y] == [3, 1]:
            tk.Button(window, text=str(int(-BoardChess[3][1]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit31).place(x=Board31[0],y=Board31[1])

        if BoardChess[3][2] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit32).place(x=Board32[0],y=Board32[1])
        elif BoardChess[3][2] > 0 and [x, y] != [3, 2]:
            tk.Button(window, text=str(int(BoardChess[3][2]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit32).place(x=Board32[0],y=Board32[1])
        elif BoardChess[3][2] < 0 and [x, y] != [3, 2]:
            tk.Button(window, text=str(int(-BoardChess[3][2]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit32).place(x=Board32[0],y=Board32[1])
        elif BoardChess[3][2] > 0 and [x, y] == [3, 2]:
            tk.Button(window, text=str(int(BoardChess[3][2]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit32).place(x=Board32[0],y=Board32[1])
        elif BoardChess[3][2] < 0 and [x, y] == [3, 2]:
            tk.Button(window, text=str(int(-BoardChess[3][2]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit32).place(x=Board32[0],y=Board32[1])

        if BoardChess[3][3] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit33).place(x=Board33[0],y=Board33[1])
        elif BoardChess[3][3] > 0 and [x, y] != [3, 3]:
            tk.Button(window, text=str(int(BoardChess[3][3]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit33).place(x=Board33[0],y=Board33[1])
        elif BoardChess[3][3] < 0 and [x, y] != [3, 3]:
            tk.Button(window, text=str(int(-BoardChess[3][3]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit33).place(x=Board33[0],y=Board33[1])
        elif BoardChess[3][3] > 0 and [x, y] == [3, 3]:
            tk.Button(window, text=str(int(BoardChess[3][3]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit33).place(x=Board33[0],y=Board33[1])
        elif BoardChess[3][3] < 0 and [x, y] == [3, 3]:
            tk.Button(window, text=str(int(-BoardChess[3][3]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit33).place(x=Board33[0],y=Board33[1])

        if BoardChess[3][4] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit34).place(x=Board34[0],y=Board34[1])
        elif BoardChess[3][4] > 0 and [x, y] != [3, 4]:
            tk.Button(window, text=str(int(BoardChess[3][4]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit34).place(x=Board34[0],y=Board34[1])
        elif BoardChess[3][4] < 0 and [x, y] != [3, 4]:
            tk.Button(window, text=str(int(-BoardChess[3][4]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit34).place(x=Board34[0],y=Board34[1])
        elif BoardChess[3][4] > 0 and [x, y] == [3, 4]:
            tk.Button(window, text=str(int(BoardChess[3][4]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit34).place(x=Board34[0],y=Board34[1])
        elif BoardChess[3][4] < 0 and [x, y] == [3, 4]:
            tk.Button(window, text=str(int(-BoardChess[3][4]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit34).place(x=Board34[0],y=Board34[1])

        if BoardChess[4][0] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit40).place(x=Board40[0],y=Board40[1])
        elif BoardChess[4][0] > 0 and [x, y] != [4, 0]:
            tk.Button(window, text=str(int(BoardChess[4][0]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit40).place(x=Board40[0],y=Board40[1])
        elif BoardChess[4][0] < 0 and [x, y] != [4, 0]:
            tk.Button(window, text=str(int(-BoardChess[4][0]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit40).place(x=Board40[0],y=Board40[1])
        elif BoardChess[4][0] > 0 and [x, y] == [4, 0]:
            tk.Button(window, text=str(int(BoardChess[4][0]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit40).place(x=Board40[0],y=Board40[1])
        elif BoardChess[4][0] < 0 and [x, y] == [4, 0]:
            tk.Button(window, text=str(int(-BoardChess[4][0]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit40).place(x=Board40[0],y=Board40[1])

        if BoardChess[4][1] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit41).place(x=Board41[0],y=Board41[1])
        elif BoardChess[4][1] > 0 and [x, y] != [4, 1]:
            tk.Button(window, text=str(int(BoardChess[4][1]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit41).place(x=Board41[0],y=Board41[1])
        elif BoardChess[4][1] < 0 and [x, y] != [4, 1]:
            tk.Button(window, text=str(int(-BoardChess[4][1]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit41).place(x=Board41[0],y=Board41[1])
        elif BoardChess[4][1] > 0 and [x, y] == [4, 1]:
            tk.Button(window, text=str(int(BoardChess[4][1]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit41).place(x=Board41[0],y=Board41[1])
        elif BoardChess[4][1] < 0 and [x, y] == [4, 1]:
            tk.Button(window, text=str(int(-BoardChess[4][1]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit41).place(x=Board41[0],y=Board41[1])

        if BoardChess[4][2] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit42).place(x=Board42[0],y=Board42[1])        #paj
        elif BoardChess[4][2] > 0 and [x, y] != [4, 2]:
            tk.Button(window, text=str(int(BoardChess[4][2]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit42).place(x=Board42[0],y=Board42[1])
        elif BoardChess[4][2] < 0 and [x, y] != [4, 2]:
            tk.Button(window, text=str(int(-BoardChess[4][2]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit42).place(x=Board42[0],y=Board42[1])
        elif BoardChess[4][2] > 0 and [x, y] == [4, 2]:
            tk.Button(window, text=str(int(BoardChess[4][2]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit42).place(x=Board42[0],y=Board42[1])
        elif BoardChess[4][2] < 0 and [x, y] == [4, 2]:
            tk.Button(window, text=str(int(-BoardChess[4][2]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit42).place(x=Board42[0],y=Board42[1])

        if BoardChess[4][3] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit43).place(x=Board43[0],y=Board43[1])
        elif BoardChess[4][3] > 0 and [x, y] != [4, 3]:
            tk.Button(window, text=str(int(BoardChess[4][3]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit43).place(x=Board43[0],y=Board43[1])
        elif BoardChess[4][3] < 0 and [x, y] != [4, 3]:
            tk.Button(window, text=str(int(-BoardChess[4][3]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit43).place(x=Board43[0],y=Board43[1])
        elif BoardChess[4][3] > 0 and [x, y] == [4, 3]:
            tk.Button(window, text=str(int(BoardChess[4][3]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit43).place(x=Board43[0],y=Board43[1])
        elif BoardChess[4][3] < 0 and [x, y] == [4, 3]:
            tk.Button(window, text=str(int(-BoardChess[4][3]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit43).place(x=Board43[0],y=Board43[1])

        if BoardChess[4][4] == 0:
            tk.Button(window, text='  ', bg='AliceBlue', padx=32, pady=30, font=('Arial', 16), command=hit44).place(x=Board44[0],y=Board44[1])
        elif BoardChess[4][4] > 0 and [x, y] != [4, 4]:
            tk.Button(window, text=str(int(BoardChess[4][4]))+'', bg='red', padx=32, pady=30, font=('Arial', 16), command=hit44).place(x=Board44[0],y=Board44[1])
        elif BoardChess[4][4] < 0 and [x, y] != [4, 4]:
            tk.Button(window, text=str(int(-BoardChess[4][4]))+'', bg='RoyalBlue', padx=32, pady=30, font=('Arial', 16), command=hit44).place(x=Board44[0],y=Board44[1])
        elif BoardChess[4][4] > 0 and [x, y] == [4, 4]:
            tk.Button(window, text=str(int(BoardChess[4][4]))+'', bg='pink', padx=32, pady=30, font=('Arial', 16), command=hit44).place(x=Board44[0],y=Board44[1])
        elif BoardChess[4][4] < 0 and [x, y] == [4, 4]:
            tk.Button(window, text=str(int(-BoardChess[4][4]))+'', bg='LightCyan', padx=32, pady=30, font=('Arial', 16), command=hit44).place(x=Board44[0],y=Board44[1])
        #print(Game.board)

    show()  #进入start_game函数以来，从63行新建了窗口之后，定义了一堆函数，这是头一次执行某个函数。

    def New_Game(): #new game函数对应的是程序中新开局这个按钮，点这个按钮会触发这个命令
        NG_window = tk.Toplevel(window) #新建一个子窗口
        NG_window.title('New Game Setting') 
        NG_window.geometry('340x300')
        NG_window.resizable(False, False)
        Var_ListR = tk.StringVar()  
        Var_ListB = tk.StringVar()
        Var_ListR.set(ListR)
        Var_ListB.set(ListB)
        
        #下面这些懒得解释了，就是实现了程序的新开局功能，比较傻，自己对照程序应该能理解
        def clickR1():
            global ListR, ListB
            if 1 in ListR:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListR.append(1)
                Var_ListR.set(ListR)
        def clickR2():
            global ListR, ListB
            if 2 in ListR:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListR.append(2)
                Var_ListR.set(ListR)
        def clickR3():
            global ListR, ListB
            if 3 in ListR:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListR.append(3)
                Var_ListR.set(ListR)
        def clickR4():
            global ListR, ListB
            if 4 in ListR:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListR.append(4)
                Var_ListR.set(ListR)
        def clickR5():
            global ListR, ListB
            if 5 in ListR:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListR.append(5)
                Var_ListR.set(ListR)
        def clickR6():
            global ListR, ListB
            if 6 in ListR:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListR.append(6)
                Var_ListR.set(ListR)
        def clickB1():
            global ListR, ListB
            if 1 in ListB:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListB.append(1)
                Var_ListB.set(ListB)
        def clickB2():
            global ListR, ListB
            if 2 in ListB:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListB.append(2)
                Var_ListB.set(ListB)
        def clickB3():
            global ListR, ListB
            if 3 in ListB:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListB.append(3)
                Var_ListB.set(ListB)
        def clickB4():
            global ListR, ListB
            if 4 in ListB:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListB.append(4)
                Var_ListB.set(ListB)
        def clickB5():
            global ListR, ListB
            if 5 in ListB:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListB.append(5)
                Var_ListB.set(ListB)
        def clickB6():
            global ListR, ListB
            if 6 in ListB:
                tk.messagebox.showinfo('Error !','你已经选过该数字， 不可重复')
            else:
                ListB.append(6)
                Var_ListB.set(ListB)

        def app():
            global winner, ListB, ListR
            if len(ListR) == 6 and len(ListB) == 6:
                Game.createBoard(ListR, ListB)
                NG_window.destroy()
                window.destroy()
                winner = 0
                start_game()
            else:
                tk.messagebox.showinfo('Error !','缺少信息！ 请先完善')

        def clear():
            global ListR
            global ListB
            ListR = []
            ListB = []
            Var_ListR.set(ListR)
            Var_ListB.set(ListB)
            #tk.messagebox.showinfo('Successful !','列表已经清空')

        rb1 = tk.Button(NG_window, text='1', bg='red', command=clickR1, height=2, width=5).place(x=20,y=20)
        rb2 = tk.Button(NG_window, text='2', bg='red', command=clickR2, height=2, width=5).place(x=70,y=20)
        rb3 = tk.Button(NG_window, text='3', bg='red', command=clickR3, height=2, width=5).place(x=120,y=20)
        rb4 = tk.Button(NG_window, text='4', bg='red', command=clickR4, height=2, width=5).place(x=170,y=20)
        rb5 = tk.Button(NG_window, text='5', bg='red', command=clickR5, height=2, width=5).place(x=220,y=20)
        rb6 = tk.Button(NG_window, text='6', bg='red', command=clickR6, height=2, width=5).place(x=270,y=20)
        bb1 = tk.Button(NG_window, text='1', bg='RoyalBlue', command=clickB1, height=2, width=5).place(x=20,y=80)
        bb2 = tk.Button(NG_window, text='2', bg='RoyalBlue', command=clickB2, height=2, width=5).place(x=70,y=80)
        bb3 = tk.Button(NG_window, text='3', bg='RoyalBlue', command=clickB3, height=2, width=5).place(x=120,y=80)
        bb4 = tk.Button(NG_window, text='4', bg='RoyalBlue', command=clickB4, height=2, width=5).place(x=170,y=80)
        bb5 = tk.Button(NG_window, text='5', bg='RoyalBlue', command=clickB5, height=2, width=5).place(x=220,y=80)
        bb6 = tk.Button(NG_window, text='6', bg='RoyalBlue', command=clickB6, height=2, width=5).place(x=270,y=80)

        l1 = tk.Label(NG_window, text='红方布局').place(x=40,y=140)
        lbr = tk.Listbox(NG_window, listvar=Var_ListR,height=6,width=7).place(x=40,y=160)
        l2 = tk.Label(NG_window, text='蓝方布局').place(x=240,y=140)
        lbb = tk.Listbox(NG_window, listvar=Var_ListB,height=6,width=7).place(x=240,y=160)

        C = tk.Button(NG_window, text='清空列表', command=clear).place(x=133,y=170)
        B = tk.Button(NG_window, text='确    定', command=app).place(x=137,y=230)

    def Save_Record():      #保存棋谱功能入口
        if (Game.board == 0).all():
            print(':)')
            return 0
        SR_window = tk.Toplevel(window)     #绘制GUI
        SR_window.title('Save Record')
        SR_window.geometry('600x300')
        SR_window.resizable(False, False)

        fhTempVar = tk.StringVar()
        fhTempVar.set('0')
        winnerTempVar = tk.StringVar()
        winnerTempVar.set('0')

        Team1TempVar = tk.StringVar()
        Team2TempVar = tk.StringVar()
        LocationTempVar = tk.StringVar()
        NameTempVar = tk.StringVar()

        Team1TempVar.set(TEAM1_NAME)
        Team2TempVar.set(TEAM2_NAME)
        NameTempVar.set(GAME_NAME)
        LocationTempVar.set(GAME_LOCATION)

        def save():                         #点击保存按钮
            try:
                Team1 = str(Team1TempVar.get())
                Team2 = str(Team2TempVar.get())
                Location = str(LocationTempVar.get())
                Name = str(NameTempVar.get())
                Winner = winnerTempVar.get()
                FirstHand = fhTempVar.get()
            except:
                tk.messagebox.showinfo('Error !','数据不完整.')
                return 0
            if Winner == FirstHand:
                Winner = '先手方'
            elif Winner != FirstHand:
                Winner = '后手方'

            FileName = Team1 + 'vs' + Team2 + '-' + Winner + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.txt'
            Text1 = '#[' + Team1 + '][' + Team2 + '][' + time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()) + ' ' + Location + '][' + Name + '];'
            File = open(FileName, 'w')
            File.write(Text1)
            File.write('\r')
            for RC in Game.RCSS:
                File.write(RC)
            File.write('\r')
            for BC in Game.BCSS:
                File.write(BC)
            File.write('\r')
            for Step in range(len(Game.CI)):
                File.write(str(Step + 1))
                File.write(Game.CI[Step])
                File.write('\r')
            File.close()
            SR_window.destroy()

        Team1 = tk.Entry(SR_window ,width=36,font=('Arial', 12), textvariable=Team1TempVar).place(x=80, y=40)
        Team2 = tk.Entry(SR_window, width=36,font=('Arial', 12), textvariable=Team2TempVar).place(x=80, y=100)

        Location = tk.Entry(SR_window,width=36, font=('Arial', 12), textvariable=LocationTempVar).place(x=80, y=160)
        Name = tk.Entry(SR_window, width=36, font=('Arial', 12), textvariable=NameTempVar).place(x=80, y=220)

        yes = tk.Button(SR_window, height=1, width = 12, text='确定', command=save).place(x=450, y=220)

        tk.Label(SR_window, height=1,width=6, font=('Arial', 10), text='先后手').place(x=430,y=160)
        tk.Label(SR_window, height=1,width=6, font=('Arial', 10), text='胜负方').place(x=520,y=160)

        tk.Radiobutton(SR_window, text="", variable=fhTempVar, value='-1').place(x=450, y=100)
        tk.Radiobutton(SR_window, text="", variable=fhTempVar, value='1').place(x=450, y=40)
        tk.Radiobutton(SR_window, text="", variable=winnerTempVar, value='-1').place(x=540, y=100)
        tk.Radiobutton(SR_window, text="", variable=winnerTempVar, value='1').place(x=540, y=40)
        tk.Label(SR_window, height=1,width=8, font=('Arial', 10), text='队伍一：').place(x=10,y=40)
        tk.Label(SR_window, height=1,width=8, font=('Arial', 10), text='队伍二：').place(x=10,y=100)
        tk.Label(SR_window, height=1,width=8, font=('Arial', 10), text='地  点：').place(x=10,y=160)
        tk.Label(SR_window, height=1,width=8, font=('Arial', 10), text='名  称：').place(x=10,y=220)

    def NewRandNum():       #随机数
        RandNumVar.set(np.random.randint(1,7))  #python的区间表示一般前闭后开
        #Game.Sc()

    RandNumVar = tk.StringVar()
    RandNumVar.set('QwQ')
    RandNumList = tk.StringVar()
    RandNumList.set([' 1',' 2',' 3',' 4',' 5',' 6',-1,-2,-3,-4,-5,-6])
    RandomLB = tk.Listbox(window, listvar = RandNumList, height=12, width=10)
    RandomLB.place(x=540, y=80)

    def congratulation(winner):
        if winner == 1:
            tk.messagebox.showinfo('Congratulation !','红方胜利！')
        elif winner == -1:
            tk.messagebox.showinfo('Congratulation !','蓝方胜利！')
        else:
            pass

    def AIMove():           #核心函数，AI走子
        global Selected, winner
        if (Game.board == 0).all():
            return 0
        if winner != 0:
            return 0
        try:
            rand = int(RandomLB.get(RandomLB.curselection()))
        except:
            tk.messagebox.showinfo('Error !','请先在右方选择随机数 ！') #AI走子的时候一定有选好的随机数
            return 0
        RandomLB.selection_clear(0,'end')       #清空随机数候选框的已选
        chessPosition0, chessPosition1 = Game.ChooseChess(rand)     #根据随机数得到AI可以走的棋子的位置，可能有一个，或者两个。如果是一个那么这两个Position值就是一样的。
        tic = time.time()   #记录AI思考开始的时间
        position, moveDirection = Game.Eight_Move(chessPosition0, chessPosition1)   #AI思考，输入可以走的棋子的位置，输出走的棋子的位置和移动的方向。
        toc = time.time()   #记录AI结束思考的时间
        print('AI思考用时：', toc-tic, 's.')
        Game.Move(position, moveDirection, rand)    #根据AI思考结果移动数组棋盘
        Game.PI.append(list(Game.board.reshape(25)))    #记录棋子位置信息
        Selected = []
        winner = Game.GetWinner()
        if winner != 0:
            congratulation(winner)
        show()

    def Regret():   #悔棋
        global Selected, winner
        if len(Game.PI) > 1:    #如果棋子位置信息里有两条及以上的记录
            del Game.PI[len(Game.PI) - 1]   #删除棋子位置信息的最新记录
            del Game.CI[len(Game.CI) - 1]   #删除棋谱信息的最新记录
            Game.board = np.array(Game.PI[len(Game.PI) - 1]).reshape([5,5]) #根据棋子位置信息还原棋谱
            #print(Game.board)  #简单来说，PI的意义就是方便悔棋，CI的意义是记录棋谱，比赛的时候要交的那个
            Selected = []
            winner = Game.GetWinner()
            show()
        else:
            tk.messagebox.showinfo('Error !','别悔了别悔了，再悔人没了')


    tk.Label(window, text='随机数：').place(x=540, y=50)
    tk.Label(window, textvariable=RandNumVar, font=('Arial', 16), width=7, height=2).place(x=540, y=380)
    tk.Button(window, text='电脑走子',width=9, height=1, command=AIMove).place(x=540, y=320)
    tk.Button(window, text='产生随机数', width=9, height=1, command=NewRandNum).place(x=540, y=430)

    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='选项', menu=filemenu)
    filemenu.add_command(label='新游戏', command=New_Game)
    filemenu.add_command(label='保存棋谱', command=Save_Record)
    filemenu.add_command(label='悔棋', command=Regret)
    filemenu.add_command(label='退出', command=main_window.quit)
    window.config(menu=menubar)

if __name__ == '__main__':
    start_game()
    main_window.mainloop()  #这个是个固定语句，就是让窗口持续运行，tk的固定写法

#接下来可以看Tougou_Hifumi.py