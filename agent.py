from typing import List
import numpy as np
from numpy import array as npa
from copy import deepcopy

PLAYER_MAX="MAX"
PLAYER_MIN="MIN"
inf:int=1000000000

MOVES=[npa([-1,0]),npa([1,0]),npa([0,-1]),npa([0,1])]

class Agent:
    def play(self,state:List[List[int]],player:int):
        moves=[move for move in self.legalMoves(state,player)]
        nextStatesPts=npa([self.MiniMax(self.nextState(state,move),-player,PLAYER_MIN) for move in moves])
        nextMove=moves[np.argmax(nextStatesPts)]
        return self.nextState(self,state,nextMove)
        
    def nextState(state:List[List[int]],move)->List[List[int]]:
        nextSte=deepcopy(state)
        nextSte[move[1][0]][move[1][1]]=nextSte[move[0][0]][move[0][1]]
        nextSte[move[0][0]][move[0][1]]=0
        return nextSte

         
    def legalMoves(self,state:List[List[int]],player:int):
        row,col=len(state),len(state[0])
        for r in row:
            for c in col:
                if state[r][c]==player:
                    pos=npa([r,c])
                    for move in MOVES:
                        nexPos=pos+move
                        nr,nc=nexPos[0],nexPos[1]
                        if nr<row and nr>=0 and nc<col and nc>=0:
                            if state[nr][nc]==0:
                                yield ((r,c),(nr,nc))
                            else if state[nr][nc]==-player:
                                nexPos+=move
                                nr,nc=nextPos[0],nextPos[1]
                                if state[nr][nc]==0:
                                    yield((r,c),(nr,nc))


    def MiniMax(self,state:List[List[int]],player:int,playerType:str,depth=1,alpha:int=-inf,beta:int=inf)->float:
        if playerType==PLAYER_MAX:
            return self.Max(state,player,depth,alpha,beta)
        else:
            return self.Min(state,player,depth,alpha,beta)

    def eval(self,state,player:int,playerType:str)->float:
        pass

    def Max(self,state:List[List[int]],player:int,depth=1,alpha:int=-inf,beta:int=inf)->float:
        for moves in self.legalMoves(state,player):
            v=self.MiniMax(self.nextState(state,move),-player,depth+1,alpha,beta)
            if v>beta:
                return -inf
            alpha=max(v,alpha)
        return v
    def Min(self,state:List[List[int]],player:int,depth=1,alpha:int=-inf,beta:int=inf)->float:
        for moves in self.legalMoves(state,player):
            v=self.MiniMax(self.nextState(state,move),-player,depth+1,alpha,beta)
            if v<alpha:
                return inf
            beta=min(v,alpha)
        return v


