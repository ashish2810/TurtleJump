from typing import List
import numpy as np
from numpy import array as npa
from copy import deepcopy
from six.moves import xrange
from random import randint

PLAYER_MAX="MAX"
PLAYER_MIN="MIN"
inf:int=1000000000
LIMIT_DEPTH=3

MOVES=[npa([-1,0]),npa([1,0]),npa([0,-1]),npa([0,1]),npa([-1,-1]),npa([1,1]),npa([1,-1]),npa([-1,1])]

class Agent:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols

    def play(self,state:List[List[int]],player:int):
        moves=[move for move in self.legalMoves(state,player)]

        nextStatesPts=npa([self.MiniMax(self.nextState(state,move),-player,PLAYER_MIN) for move in moves])
        # for i in xrange(len(nextStatesPts)):
        #     print(moves[i],nextStatesPts[i])
        maxx=np.amax(nextStatesPts)
        nextMoves=np.argwhere(nextStatesPts==maxx).flatten().tolist()
        nextMove=moves[nextMoves[randint(0,len(nextMoves)-1)]]
        #print(nextMove)
        return nextMove
        
    def nextState(self,state:List[List[int]],move)->List[List[int]]:
        nextSte=deepcopy(state)
        r,c=move[0][0],move[0][1]
        nr,nc=move[1][0],move[1][1]
        mr,mc=(r+nr)//2,(c+nc)//2
        nextSte[nr][nc]=nextSte[r][c]
        if mr!=r or mc!=c:
            nextSte[mr][mc]=nextSte[r][c]
        nextSte[r][c]=0

        return nextSte

         
    def legalMoves(self,state:List[List[int]],player:int):
        for r in xrange(self.rows):
            for c in xrange(self.cols):
                if state[r][c]==player:
                    pos=npa([r,c])
                    for move in MOVES:
                        nexPos=pos+move
                        nr,nc=nexPos[0],nexPos[1]
                        if self.posValid(nr,nc):
                            if state[nr][nc]==0:
                                yield ((r,c),(nr,nc))
                            elif state[nr][nc]==-player:
                                nexPos+=move
                                nr,nc=nexPos[0],nexPos[1]
                                if(self.posValid(nr,nc)):
                                    if state[nr][nc]==0:
                                        yield ((r,c),(nr,nc))
        # y=0
        # ret=[]
        # for r in xrange(self.rows):
        #     for c in xrange(self.cols):
        #         if state[r][c]==player:
        #             pos=npa([r,c])
        #             for move in MOVES:
        #                 nexPos=pos+move
        #                 nr,nc=nexPos[0],nexPos[1]
        #                 if self.posValid(nr,nc):
        #                     if state[nr][nc]==0:
        #                         # if r==2 and c==0:
        #                         #     print("nocap",r,c,nr,nc,state[nr][nc])
        #                         #print(y)
        #                         y+=1
        #                         ret.append(((r,c),(nr,nc)))
        #                     elif state[nr][nc]==-player:
        #                         nexPos+=move
        #                         nr,nc=nexPos[0],nexPos[1]
        #                         if(self.posValid(nr,nc)):
        #                             # if r==2 and c==0:
        #                             #     print("cap",r,c,nr,nc,state[nr][nc])
        #                             if state[nr][nc]==0:
        #                                 #print(y)
        #                                 y+=1
        #                                 ret.append(((r,c),(nr,nc)))
        # return ret

    def MiniMax(self,state:List[List[int]],player:int,playerType:str,depth=1,alpha:int=-inf,beta:int=inf)->float:
        if depth==LIMIT_DEPTH:
            return self.eval(state,player,playerType)
        if playerType==PLAYER_MAX:
            return self.Max(state,player,depth+1,alpha,beta)
        else:
            return self.Min(state,player,depth+1,alpha,beta)

    def eval(self,state:List[List[int]],player:int,playerType:str)->float:
        noOfPawn=0
        for r in xrange(len(state)):
            for c in xrange(len(state[0])):
                if state[r][c]==player:
                    noOfPawn+=1
        value=noOfPawn+self.captures(state,player)
        if playerType==PLAYER_MIN:
            value=-value
        return value
    
    def captures(self,state,player):
        capt=0
        for r in xrange(len(state)):
            for c in xrange(len(state[0])):
                if state[r][c]==-player:
                    pos=npa([r,c])
                    noOfC=0
                    for move in MOVES:
                        pos1=pos+move
                        pos2=pos-move
                        nr1,nc1=pos1[0],pos1[1]
                        nr2,nc2=pos2[0],pos2[1]
                        if self.posValid(nr1,nc1) and self.posValid(nr2,nc2) and (state[nr1][nc1]==player and state[nr2][nc2]==0):
                            noOfC+=1
                    if noOfC==1:
                        capt+=0.5
                    elif noOfC==2:
                        capt+=0.75
        return capt

    def Max(self,state:List[List[int]],player:int,depth=1,alpha:int=-inf,beta:int=inf)->float:
        if depth==LIMIT_DEPTH:
            return self.eval(state,player,PLAYER_MAX)
        v=-inf
        for move in self.legalMoves(state,player):
            v=max(v,self.Min(self.nextState(state,move),-player,depth+1,alpha,beta))
            #if depth==1:
                #print("Max",move,v,alpha,beta)
            if v>beta:
                #print("pruning")
                return inf
            alpha=max(v,alpha)
        return v

    def Min(self,state:List[List[int]],player:int,depth=1,alpha:int=-inf,beta:int=inf)->float:
        #print("place 1 "+str(depth))
        if depth==LIMIT_DEPTH:
            return self.eval(state,player,PLAYER_MIN)
        #print("place 2")
        v=inf
        for move in self.legalMoves(state,player):
            v=min(v,self.Max(self.nextState(state,move),-player,depth+1,alpha,beta))
            #if depth==1:
                #print("Min",move,v,alpha,beta)
            # print("place 3 ",v,alpha,beta,depth)
            if v<alpha:
                #print("pruning")
                return -inf
            #print("place 4")
            beta=min(v,beta)
            #print("place 5")
        return v

    def posValid(self,r,c):
        return r<self.rows and r>=0 and c<self.cols and c>=0

class RandomAgent:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols

    def play(self,state:List[List[int]],player:int):
        moves=[move for move in self.legalMoves(state,player)]
        nextMove=moves[randint(0,len(moves)-1)]
        return nextMove
        
    def legalMoves(self,state:List[List[int]],player:int):
        for r in xrange(self.rows):
            for c in xrange(self.cols):
                if state[r][c]==player:
                    pos=npa([r,c])
                    for move in MOVES:
                        nexPos=pos+move
                        nr,nc=nexPos[0],nexPos[1]
                        if self.posValid(nr,nc):
                            if state[nr][nc]==0:
                                yield ((r,c),(nr,nc))
                            elif state[nr][nc]==-player:
                                nexPos+=move
                                nr,nc=nexPos[0],nexPos[1]
                                if(self.posValid(nr,nc)):
                                    if state[nr][nc]==0:
                                        yield ((r,c),(nr,nc))
    def posValid(self,r,c):
        return r<self.rows and r>=0 and c<self.cols and c>=0