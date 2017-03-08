import math
import random

class Cell:
    def __init__(self, myID, posX, posY, myOrigin, GRIDSIZE, LIMITX, LIMITY, initSand, myFixState, CELLHEIGHT, WINDSHADOW, BUILDHEIGHT):
        self.cellId             = myID
        self.pos                = [posX, posY]                                  #position in 2D data structure
        self.cellOrigin         = myOrigin
        self.sandHeight         = initSand                                      #no. of units of sand on cell
        self.cellFixed          = myFixState
        self.cellCoord          = self.find_my_coord(GRIDSIZE)
        self.inShadow           = False
        self.justShadow         = False                                         #is casting shadow, even if it is itself in shadow
        self.probDeposition     = 1                                             #probability of deposition
        self.limitX             = LIMITX
        self.limitY             = LIMITY
        self.neighbIds          = self.find_my_neighbours()
        self.gridSize           = GRIDSIZE
        self.cellHeight         = CELLHEIGHT
        self.windShadow         = WINDSHADOW
        self.buildHeight        = BUILDHEIGHT
        
    def find_my_coord(self, gridSize):
        pt = self.cellOrigin
        pt0 = [pt[0], pt[1], pt[2]]
        pt1 = [pt[0]+gridSize, pt[1], pt[2]]
        pt2 = [pt[0]+gridSize, pt[1]+gridSize, pt[2]]
        pt3 = [pt[0], pt[1]+gridSize, pt[2]]
        myPts = [pt0, pt1, pt2, pt3, pt0]
        return myPts
        
    def find_my_neighbours(self):
        nowPos = self.pos
        gridX = self.limitX
        gridY = self.limitY
        print gridX, gridY
        cell0pos = [(nowPos[0]-1)%gridX, (nowPos[1]+1)%gridY]
        cell1pos = [nowPos[0], (nowPos[1]+1)%gridY]
        cell2pos = [(nowPos[0]+1)%gridX, (nowPos[1]+1)%gridY]
        cell3pos = [(nowPos[0]+1)%gridX, nowPos[1]]
        cell4pos = [(nowPos[0]+1)%gridX, (nowPos[1]-1)%gridY]
        cell5pos = [nowPos[0], (nowPos[1]-1)%gridY]
        cell6pos = [(nowPos[0]-1)%gridX, (nowPos[1]-1)%gridY]
        cell7pos = [(nowPos[0]-1)%gridX, nowPos[1]]
        neighbCells = [cell0pos, cell1pos, cell2pos, cell3pos, cell4pos, cell5pos, cell6pos, cell7pos]
        return neighbCells
        
    def shadowLine_distance(self):
        if (self.cellFixed==False):
            distance = (self.sandHeight*self.cellHeight)/math.tan(math.radians(self.windShadow))
        elif (self.cellFixed==True):
            #if building is higher than sand
            distance = (self.buildHeight*self.cellHeight)/math.tan(math.radians(self.windShadow))
            #if sand is higher than building
        return distance
        
    def am_I_casting_shadows(self, CELLLIST):
        if (self.inShadow==False) or (self.justShadow==True):
            distanceAhead   = self.shadowLine_distance()
            stepsAhead      = int(distanceAhead/self.gridSize)
            #keep checking steps ahead, as long as following step is still influenced by current shadow cell
            shadowInfluence = True
            endofRow        = False
            neighbours      = self.neighbIds
            nowCheckedCell  = CELLLIST[neighbours[3][0]][neighbours[3][1]]
            k               = 0                                                 #k used as counter
            
            while (k<stepsAhead) and (shadowInfluence==True):
                shadowLineStart = (distanceAhead-(self.gridSize*k))*math.tan(math.radians(self.windShadow))
                shadowLineMid   = (distanceAhead-((0.5+k)*self.gridSize))*math.tan(math.radians(self.windShadow))
                shadowLineEnd   = (distanceAhead-(self.gridSize*(k+1)))*math.tan(math.radians(self.windShadow))
                
                #if nowCheckedCell is not fixed
                if nowCheckedCell.cellFixed==False:
                    nowSHeight      = float(nowCheckedCell.sandHeight)*nowCheckedCell.cellHeight
                #if nowCheckedCell is fixed
                elif nowCheckedCell.cellFixed==True:
                    #if sandheight<buildheight
                    nowSHeight      = float(nowCheckedCell.buildHeight)*nowCheckedCell.cellHeight
                    #if sandheight>buildheight
                
                #compare shadowline height to height of sand at cell
                if (shadowLineMid>nowSHeight) and (shadowLineEnd>nowSHeight):
                    #update cell inShadow and justShadow
                    nowCheckedCell.inShadow   = True
                    nowCheckedCell.justShadow = False
                    shadowInfluence           = True
                elif (shadowLineMid>nowSHeight) and (shadowLineEnd<nowSHeight):
                    nowCheckedCell.inShadow   = True
                    nowCheckedCell.justShadow = True
                    shadowInfluence           = False
                elif (shadowLineStart>nowSHeight) and (shadowLineMid<nowSHeight):
                    nowCheckedCell.inShadow   = False
                    nowCheckedCell.justShadow = True
                    shadowInfluence           = False
                elif  (shadowLineStart<=nowSHeight):
                    nowCheckedCell.inShadow   = False
                    nowCheckedCell.justShadow = False
                    shadowInfluence           = False
                #update celllist
                CELLLIST[nowCheckedCell.pos[0]][nowCheckedCell.pos[1]] = nowCheckedCell
                #find next neighbour
                nowCheckedCell  = CELLLIST[nowCheckedCell.neighbIds[3][0]][nowCheckedCell.neighbIds[3][1]]
                #update counter k
                k = k+1
        
    def avalanche_check(self, CELLLIST):
        check = False
        #deterministic Von Neumann check
        for i in range(4):
            neighbPos = self.neighbIds[(i*2)+1]
            nowNeighb = CELLLIST[neighbPos[0]][neighbPos[1]]
            
            if (self.cellFixed==False):
                #OPTION 1: I am not fixed, neighb is not fixed
                if (nowNeighb.cellFixed==False):
                    #check avalanche towards me
                    if (nowNeighb.sandHeight>(self.sandHeight+2)):
                        self.sandHeight         = self.sandHeight+1
                        nowNeighb.sandHeight    = nowNeighb.sandHeight-1
                        check                   = True
                    #check avalanche away from me
                    elif (self.sandHeight>(nowNeighb.sandHeight+2)):
                        self.sandHeight         = self.sandHeight-1
                        nowNeighb.sandHeight    = nowNeighb.sandHeight+1
                        check                   = True
                #OPTION 2: I am not fixed, neighb is fixed
                elif (nowNeighb.cellFixed==True):
                    #check avalanche towards me from fixed cell - cannot happen! (unless sand is above fixed structure)
                    
                    #check avalance away from me to fixed cell - only if sand is higher than building
                    if (self.sandHeight>(nowNeighb.buildHeight+2)):
                        print "sand moves onto building!"
            elif (self.cellFixed==True):
                #OPTION 3: I am fixed, neighb is not fixed
                if (nowNeighb.cellFixed==False):
                    #check avalanche towards me - only if sand is higher than building
                    if (nowNeighb.sandHeight>(nowNeighb.sandHeight+2)):
                        print "sand moves onto building!"
                    #check avalanche away from me - only if sand is higher than building
                #OPTION 4: I am fixed, neighb is fixed
                elif (nowNeighb.cellFixed==True):
                    print "not for now!"
                    #check avalanche towards me - only if sand is higher than building
                    
                    #check avalanche away from me - only if sand is higher than building
                    
        return check
        
    def erode_cell(self, CELLLIST):
        #find neighbour cell
        neighbCellPos = self.neighbIds[3]
        neighbCell      = CELLLIST[neighbCellPos[0]][neighbCellPos[1]]
        
        #OPTION 1: erosion happens if cell is not fixed
        if self.cellFixed==False:
            #erosion takes place if next cell is not fixed
            if neighbCell.cellFixed==False:
                #erosion takes place if cell not in wind shadow and cell contains sand (sandHeight>0)
                if (self.inShadow==False) and (self.sandHeight>0):
                    self.sandHeight = self.sandHeight-1
                    #check local sand avalanche
                    self.avalanche_check(CELLLIST)
                    depositSuccess  = False
                    targetCellPos   = self.neighbIds[3]
                    targetCell      = CELLLIST[targetCellPos[0]][targetCellPos[1]]
                    #attempt a deposit
                    depositSuccess  = targetCell.deposit_cell(CELLLIST)
                    #if deposit unsuccessful keep trying cells in row
                    while (depositSuccess==False):
                        #find new neighbour
                        newTargetCellPos    = targetCell.neighbIds[3]
                        newTargetCell       = CELLLIST[newTargetCellPos[0]][newTargetCellPos[1]]
                        depositSuccess      = newTargetCell.deposit_cell(CELLLIST)
            #erosion takes place if next cell is fixed
            elif neighbCell.cellFixed==True:
                if (self.sandHeight>neighbCell.buildHeight):
                    print "sand may move over building"
                else:
                    print "do nothing"
        #OPTION 2: erosion happens when cell is fixed if sand is over building
        
    def deposit_cell(self, CELLLIST):
        deposited = False
        #call function to calculate probability of deposition
        self.calculate_prob_deposition(CELLLIST)
        #randomise deposition
        randomChance = random.random()
        #condition using probDeposition
        randomChance = randomChance-self.probDeposition+0.5
        if (randomChance<0.5):
            self.sandHeight = self.sandHeight+1
            #check local sand avalanche
            self.avalanche_check(CELLLIST)
            deposited = True
        else:
            deposited = False
        return deposited
        
    def calculate_prob_deposition(self, CELLLIST):
        #find neighbour cell
        neighbCellPos = self.neighbIds[3]
        neighbCell      = CELLLIST[neighbCellPos[0]][neighbCellPos[1]]
        
        #OPTION 1: neighbour is not fixed
        if (neighbCell.cellFixed==False):
            if (self.inShadow==True):
                self.probDeposition = 1
            elif (self.inShadow==False) and (self.sandHeight>0):
                self.probDeposition = 0.6
            else:
                self.probDeposition = 0.4
        
        #OPTION 2: neighbour is fixed
        elif (neighbCell.cellFixed==True):
            #sand gets stuck there if sand is lower than building
            if self.sandHeight<neighbCell.buildHeight:
                self.probDeposition = 1
            
            #sand is higher than building so can move onto building
            """
            elif self.sandHeight>neighbCell.buildHeight:
                if (self.inShadow==True):
                    self.probDeposition = 1
                elif (self.inShadow==False) and (self.sandHeight>0):
                    self.probDeposition = 0.6
                else:
                    self.probDeposition = 0.4 """