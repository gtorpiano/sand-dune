import gt0022_classes as gt002
import rhinoscriptsyntax as rs
import math
import random
import pprint, pickle

#functions
#to draw points if necessary
def drawPts(PTLIST):
    rs.EnableRedraw(False)
    for i in range(len(PTLIST)):
        for j in range(len(PTLIST[i])):
            pt = rs.AddPoint(PTLIST[i][j][0])
            if PTLIST[i][j][1]:
                rs.ObjectLayer(pt, "buildings")
    rs.EnableRedraw(True)

#identify surface
srf = "19b86393-86ce-42ff-a016-f211226d1a16"
#identify buildings
blds = rs.GetObjects("select buildings")
#get plants

#bounding box
bbox = rs.BoundingBox(srf)
#create vectors and compare to X and Y vectors
for i in range(len(bbox)):
    for j in range(i+1, len(bbox)):
        #create vector
        nowVEC = rs.VectorCreate(bbox[j],bbox[i])
        xAngle = rs.VectorAngle(nowVEC, [1,0,0])
        yAngle = rs.VectorAngle(nowVEC, [0,1,0])
        if xAngle == 0:
            distX = rs.VectorLength(nowVEC)
        elif yAngle == 0:
            distY = rs.VectorLength(nowVEC)

#set sample resolution
cellResolution = 1000 #mm

#plot 2D grid over surface
stepsY = int(distY/cellResolution)+1
stepsX = int(distX/cellResolution)+1

#project points to sand surface
ptList = []
for i in range(0, stepsY):
    row = []
    for j in range(0, stepsX):
        nowPt = [j*cellResolution, i*cellResolution, 0]
        #project points to sand surface
        ptOnSrf = rs.ProjectPointToSurface (nowPt, srf, [0,0,1])
        #project points to buildings
        ptOnBld = []
        if blds:
            for k in range(len(blds)):
                tempPtOnBld = rs.ProjectPointToSurface (nowPt, blds[k], [0,0,1])
                if len(ptOnBld)==0:
                    ptOnBld = tempPtOnBld
                #print tempPtOnBld, ptOnBld
        if ptOnSrf:
            
            #check for plant
            
            row.append([ptOnSrf[0], ptOnBld]) #append plant to this list
            
            
            
        """else:
            print "no point!" """
    ptList.append(row)


GRIDSIZE = 1000             #in mm, size of cell
GRIDX = len(ptList[0])      #no. of cells in x dir
GRIDY = len(ptList)         #no. of cells in y dir
cellHeight = GRIDSIZE/3
windShadow      = 15        #degrees

cellList = []


for i in range(len(ptList)):
    colList = []
    for j in range(len(ptList[i])):
        #cell origin
        nowCellOrigin   = [j*GRIDSIZE, i*GRIDSIZE, 0]
        #sand at cell
        zCoord = ptList[i][j][0][2]
        fixMe = False
        BUILDH = -9999
        
        #enable plants
        
        if ptList[i][j][1]:
            fixMe = True
            BUILDH = int(ptList[i][j][1][1][2]/cellHeight)
            #make sure plant is FALSE
            
        SAND = int(zCoord/cellHeight) #no. of sand units on cell
        
        #introduce something about plant in next line (cell constructor)
        nowCell = gt002.Cell(((i*GRIDY)+j), i, j, nowCellOrigin, GRIDSIZE, GRIDX, GRIDY, SAND, fixMe, cellHeight, windShadow, BUILDH)
        #append our cells to a list
        colList.append(nowCell)
    cellList.append(colList)

"""
rs.EnableRedraw(False)
for i in range(len(cellList)):
    for j in range(len(cellList[i])):
        nowPt = cellList[i][j].cellOrigin
        nowPt[2] = cellList[i][j].sandHeight*cellList[i][j].cellHeight
        pt = rs.AddPoint(nowPt)
        if cellList[i][j].cellFixed==True:
            nowPt[2] = cellList[i][j].buildHeight*cellList[i][j].cellHeight
            rs.ObjectLayer(pt, "buildings")
rs.EnableRedraw(True)
"""

#output data to text file
path = "simulation data/"
fileName = raw_input('File Name?')
fullPath = path+fileName+"0.pkl"
output = open(fullPath, 'wb')
pickle.dump(cellList, output)
output.close()