import os
import copy
import numpy as np
import pandas as pd 
import torch            #深度学习库
from torch import nn, optim 
from torch.nn import functional as F 
import torchsummary

class Net(nn.Module):
    def __init__(self): 
        super().__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128), 
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128), 
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128), 
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128), 
            nn.ReLU(),
        )      
        self.outlayer = nn.Conv2d(128, 1, kernel_size=5, stride=1, padding=0)

    def forward(self, x):
        x = self.conv1(x)
        x = torch.sigmoid(self.outlayer(x))
        x = x.view(-1, 1)

        return x

device = torch.device('cuda:0')
model = Net().to(device)
model.load_state_dict(torch.load('Model/Model2.pkl'))
print('-----------load model----------')
def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
torchsummary.summary(model, (1, 5, 5))
print('parameters_count:',count_parameters(model))
model.eval()
model.half()

def Mark(Board):
    Board = np.where(Board == -0, 0, Board).reshape(-1,5,5)
    #model.eval()
    with torch.no_grad():
        x = Board / 6.
        x = torch.from_numpy(x)
        x = x.view(-1, 1, 5, 5).half()
        x = x.to(device)
        pred = model(x)
        pred = pred.cpu().numpy()
        x = -np.flip(Board,[1,2]) / 6.
        x = np.where(x==-0,0,x)
        x = torch.from_numpy(x)
        x = x.view(-1, 1, 5, 5).half()
        x = x.to(device)
        pred_ = model(x)
        pred_ = pred_.cpu().numpy()
    try:
        pred = float(pred.reshape(-1))
        pred_ = 1 - float(pred_.reshape(-1))
    except:
        pred = pred.reshape(-1)
        pred_ = 1 - pred_.reshape(-1)

    return (pred + pred_) / 2

def RedMove(board, position, direction):
    x, y = position
    if direction == 0:
        board[x][y + 1] = board[x][y]
        board[x][y] = 0.
    elif direction == 1:
        board[x + 1][y] = board[x][y]
        board[x][y] = 0.
    elif direction == 2:
        board[x + 1][y + 1] = board[x][y]
        board[x][y] = 0.
    
    return board

def BlueMove(board, position, direction):
    x, y = position
    if direction == 0:
        board[x][y - 1] = board[x][y]
        board[x][y] = 0.
    elif direction == 1:
        board[x - 1][y] = board[x][y]
        board[x][y] = 0.
    elif direction == 2:
        board[x - 1][y - 1] = board[x][y]
        board[x][y] = 0.
    
    return board

def softmax(x):
    return np.exp(x)/sum(np.exp(x))

def Get_P(Board, MoveList):
    x, y = MoveList[0][0]
    #print(Board)
    if Board[x][y] > 0:
        BoardList = []
        for position, direction in MoveList:
            BoardList.append(RedMove(copy.copy(Board), position, direction))
        Board_ = np.vstack(BoardList)
        Value = Mark(Board_)

        return softmax(Value)

    elif Board[x][y] < 0:
        BoardList = []
        for position, direction in MoveList:
            BoardList.append(BlueMove(copy.copy(Board), position, direction))
        Board_ = np.vstack(BoardList)
        Value = Mark(Board_)

        return softmax(1 - np.array(Value))

    

