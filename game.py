from PyQt5.QtWidgets import QApplication,QWidget,QGridLayout,QLabel,QFrame,QPushButton,QVBoxLayout,QMainWindow,QStatusBar
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap,QIcon
from typing import Tuple
from random import randint
from six.moves import xrange
from numpy import array as npa
import numpy as np
import sys
from threading import Timer
from agent import Agent,RandomAgent

rows=9
cols=8

class GameButton(QPushButton):
    def __init__(self,parent:'Game',r,c):
        super().__init__(parent.mainW)
        self.r=r
        self.c=c
        self.game=parent
        self.clicked.connect(self.move)
        
        
    def move(self):
        if not self.game.takeInput:
            return
        if self.game.mode==Game.AI_MODE:
            print("Playing")
            move=self.game.random_agent.play(self.game.state,self.game.player)
            self.game.makeMove(move[0],move[1])
            print("Played")
            return
        if self.game.cr==-1 and self.game.cc==-1:
            if self.game.state[self.r][self.c]==self.game.player:
                self.game.cr=self.r
                self.game.cc=self.c
                self.game.turnStatus()
            else:
                self.game.statusBar.showMessage("Invalid Choice")
        else:
            if self.game.moveLegal((self.game.cr,self.game.cc),(self.r,self.c)):
                self.game.makeMove((self.game.cr,self.game.cc),(self.r,self.c))
                self.game.statusBar.showMessage("Valid Move")
            else:
                self.game.statusBar.showMessage("Invalid Move")
            self.game.cr=-1
            self.game.cc=-1
    
class GameOptionsButton(QPushButton):
    def __init__(self,txt:str,parent:'GameOptions',mode:str):
        super().__init__(txt,parent)
        self.mode=mode
        self.clicked.connect(self.startGame)
        self.parent=parent
    def startGame(self):
        Game(self.mode)
        self.parent.close()

class Game(QMainWindow):
    #constants
    AI_MODE="ai"
    HUMAN_MODE="human"
    HUMAN_HUMAN_MODE="human_human"
    playerToColor={1:"Red",-1:"Blue"}
    def __init__(self,mode:str):
        super().__init__()
        self.state=np.full((rows,cols),0)
        self.blocks=np.full((rows,cols),None)
        self.cr=-1
        self.cc=-1
        self.mode=mode
        self.player=1
        if randint(0,1)==0:
            self.player=-1
        self.takeInput=True
        if mode==Game.HUMAN_MODE and self.player==1:
            self.takeInput=False
        self.ai_agent=None
        self.random_agent=None
        #print(self.mode)
        if not(self.mode==Game.HUMAN_HUMAN_MODE):
            self.ai_agent=Agent(rows,cols)
        if self.mode==Game.AI_MODE:
            print("init")
            self.random_agent=RandomAgent(rows,cols)
            print("inited")
        self.initUI()

            
    
    def initUI(self):
        grid=QGridLayout()
        self.mainW=QWidget()
        self.mainW.setLayout(grid)
        self.setCentralWidget(self.mainW)
        self.statusBar:QStatusBar=self.statusBar()
        self.turnStatus()
        windowTitle="Tutle Jump - "
        if self.mode==Game.HUMAN_MODE:
            windowTitle+="AI vs Human"
        elif self.mode==Game.AI_MODE:
            windowTitle+="AI vs Random AI"
        else:
            windowTitle+="Human vs Human"

        for r in xrange(rows):
            for c in xrange(cols):
                block=GameButton(self,r,c)
                block.setFixedSize(80,80)
                if r<=1:
                    img=QIcon("images/player1.png")
                    block.setIcon(img)
                    self.state[r][c]=1
                elif r>=rows-2:
                    img=QIcon("images/player-1.png")
                    block.setIcon(img)
                    self.state[r][c]=-1
                else:
                    self.state[r][c]=0
                block.setIconSize(QSize(70,70))
                self.blocks[r][c]=block
                grid.addWidget(block,r,c)
        self.move(0,0)
        self.setWindowTitle(windowTitle)
        self.show()
        if self.player==1 and self.mode!=Game.HUMAN_HUMAN_MODE:
            move=self.ai_agent.play(self.state,self.player)
            self.makeMove(move[0],move[1])

    def moveLegal(self,cur:Tuple,fut:Tuple)->bool:
        if self.state[cur[0]][cur[1]]!=self.player:
            return False
        y=abs(fut[0]-cur[0])
        x=abs(fut[1]-cur[1])
        if (y==1 and x==1) or (y==0 and x==1) or (y==1 and x==0):
            if self.state[fut[0]][fut[1]]==0:
                return True
            else:
                return False
        elif (y==2 and x==2) or (y==0 and x==2) or (y==2 and x==0):
            my=(cur[0]+fut[0])//2
            mx=(cur[1]+fut[1])//2
            if self.state[my][mx]==-self.player and self.state[fut[0]][fut[1]]==0:
                return True
            else:
                return False
        else:
            return False

    def makeMove(self,cur:Tuple,fut:Tuple):
        self.blocks[cur[0]][cur[1]].setIcon(QIcon())
        self.state[cur[0]][cur[1]]=0
        
        self.blocks[fut[0]][fut[1]].setIcon(QIcon("images/player"+str(self.player)+".png"))
        self.state[fut[0]][fut[1]]=self.player

        y,x=abs(cur[0]-fut[0]),abs(cur[1]-fut[1])
        if y==2 or x==2:
            #print(my,mx,cur[0],cur[1])
            my,mx=(cur[0]+fut[0])//2,(cur[1]+fut[1])//2
            self.blocks[my][mx].setIcon(QIcon("images/player"+str(self.player)+".png"))
            self.state[my][mx]=self.player
        if self.won():
            self.statusBar.showMessage(Game.playerToColor[self.player]+" Player WON")
        else:
            self.player=-self.player
            if self.mode!=Game.HUMAN_HUMAN_MODE:
                self.takeInput=not self.takeInput
            self.turnStatus()
            print(self.player,self.mode)
            if self.mode!=Game.HUMAN_HUMAN_MODE and self.player==1:
                move=self.ai_agent.play(self.state,self.player)
                self.makeMove(move[0],move[1])

    def won(self):
        w=True
        for r in xrange(rows):
            for c in xrange(cols):
                if self.state[r][c]==-self.player:
                    w=False
                    break
        return w

    def turnStatus(self):
        self.statusBar.showMessage(Game.playerToColor[self.player]+" Player Turn")

class GameOptions(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        vbox=QVBoxLayout(self)
        self.setLayout(vbox)
        human=GameOptionsButton("AI vs Human",self,Game.HUMAN_MODE)
        ai=GameOptionsButton("AI vs Random AI",self,Game.AI_MODE)
        human_human=GameOptionsButton("Human vs Human",self,Game.HUMAN_HUMAN_MODE)
        vbox.addWidget(human)
        vbox.addWidget(ai)
        vbox.addWidget(human_human)
        self.show()
    def close(self):
        super().close()




if __name__=="__main__":
    app = QApplication(sys.argv)
    options=GameOptions()
    sys.exit(app.exec_())