import gt0021_classes as gt002
import rhinoscriptsyntax as rs
import math
import random

#find centroid of set of points
def centroid(ptList):
    x = 0
    y = 0
    z = 0
    for i in range (0, len(ptList)):
        x = x + ptList[i][0]
        y = y + ptList[i][1]
        z = z + ptList[i][2]
    x = x/len(ptList)
    y = y/len(ptList)
    z = z/len(ptList)
    centPt = [x,y,z]
    return centPt

#generate grid of cells starting from origin
def generate_grid_cells(GRIDX, GRIDY, GRIDSIZE, AVRSAND, VAR, CELLHEIGHT, WINDSHADOW):
    LISTOFCELLS = [] #2D data structure
    for i in range(0, GRIDX):
        colList = []
        for j in range (0, GRIDY):
            #cell origin
            nowCellOrigin   = [i*GRIDSIZE, j*GRIDSIZE, 0]
            #sand at cell - randomly generated
            SAND            = random.randint(AVRSAND-VAR, AVRSAND+VAR)
            nowCell         = gt002.Cell(((i*GRIDY)+j), i, j, nowCellOrigin, GRIDSIZE, GRIDX, GRIDY, SAND, False, CELLHEIGHT, WINDSHADOW)                #create instance of cell
            colList.append(nowCell)
        LISTOFCELLS.append(colList)
    return LISTOFCELLS

#find cell shadows
def find_all_shadows(LISTOFCELLS):
    #set shadows to false
    for i in range(len(LISTOFCELLS)):
        for j in range(len(LISTOFCELLS[i])):
            nowCell             = LISTOFCELLS[i][j]
            nowCell.inShadow    = False
            nowCell.justShadow  = False
            
    #find shadows
    #for each row
    for i in range(len(LISTOFCELLS[0])):
        #for each cell in row
        for j in range(len(LISTOFCELLS)):
            nowShadowCell = LISTOFCELLS[j][i]
            if (nowShadowCell.inShadow==False) or (nowShadowCell.justShadow==True):
                nowShadowCell.am_I_casting_shadows(LISTOFCELLS)

#find sand redistribution after avalanching, in all cells
def avalanche_all_cells(LISTOFCELLS):
    counter = 1
    while counter>0:
        counter = 0
        for i in range(len(LISTOFCELLS)):
            for j in range(len(LISTOFCELLS[i])):
                nowCell     = LISTOFCELLS[i][j]
                nowCheck    = nowCell.avalanche_check(LISTOFCELLS)
                if (nowCheck==True):
                    counter = counter+1
        print "avalanches in cells:", counter
    total_sand(LISTOFCELLS)

#erosion/deposition in all cells for a specified number of iterations
def erosion_deposition(LISTOFCELLS, ITERATIONS):
    print ""
    print ""
    print "erosion/deposition process"
    for i in range(ITERATIONS):
        print "iteration:", i
        #create random order
        randomOrder = []
        colList = range(len(LISTOFCELLS))
        random.shuffle(colList)
        for i in colList:
            rowList = range(len(LISTOFCELLS[i]))
            random.shuffle(rowList)
            for j in rowList:
                randomOrder.append([i,j])
        random.shuffle(randomOrder)
        
        #erode/deposit cells
        for i in range(len(randomOrder)):
            nowErodingCell = LISTOFCELLS[randomOrder[i][0]][randomOrder[i][1]]
            nowErodingCell.erode_cell(LISTOFCELLS)
        
        #update shadows
        find_all_shadows(LISTOFCELLS)

#draw text dots of sand content for each cell
def draw_cells(LISTOFCELLS):
    rs.EnableRedraw(False)
    for i in range(len(LISTOFCELLS)):
        for j in range(len(LISTOFCELLS[i])):
            nowPts = LISTOFCELLS[i][j].cellCoord
            crv = rs.AddCurve(nowPts, 1)
            pt = rs.CurveAreaCentroid(crv)[0]
            rs.DeleteObject(crv)
            sandTxt = rs.AddTextDot(LISTOFCELLS[i][j].sandHeight, pt)
            if (LISTOFCELLS[i][j].sandHeight==0):
                rs.ObjectLayer(sandTxt, layer="Zero")
            elif (LISTOFCELLS[i][j].inShadow==True):
                rs.ObjectLayer(sandTxt, layer="ShadowNum")
            else:
                rs.ObjectLayer(sandTxt, layer="Num")
    rs.EnableRedraw(True)

#draw resulting sand dunes
def draw_dunes(LISTOFCELLS):
    ptList = []
    #find points in 3D space
    for i in range(len(LISTOFCELLS)):
        rows = []
        for j in range(len(LISTOFCELLS[i])):
            nowCell = LISTOFCELLS[i][j]
            nowPts  = list(nowCell.cellCoord)
            nowPts.pop()                                                        #remove repeated last point
            nowCent = centroid(nowPts)
            #set point height
            nowSHeight = nowCell.sandHeight*nowCell.cellHeight
            nowCent[2] = nowSHeight
            rows.append(nowCent)
        ptList.append(rows)
    
    #draw
    rs.EnableRedraw(False)
    for i in range(len(ptList)-1):
        for j in range(len(ptList[i])-1):
            pt0 = ptList[i][j]
            pt1 = ptList[i+1][j]
            pt2 = ptList[i+1][j+1]
            pt3 = ptList[i][j+1]
            rs.AddSrfPt([pt0, pt1, pt2, pt3])
    rs.EnableRedraw(True)

#calculate total number of units of sand in simulation at a given moment
def total_sand(LISTOFCELLS):
    totalSand = 0
    for i in range(len(LISTOFCELLS)):
        for j in range(len(LISTOFCELLS[i])):
            nowCell     = LISTOFCELLS[i][j]
            totalSand   = totalSand+nowCell.sandHeight
    print "total sand:", totalSand

#find total number of cells in shadow at a given moment
def find_total_cells_inShadow(LISTOFCELLS):
    totInShadow = 0
    for i in range(len(LISTOFCELLS)):
        for j in range((len(LISTOFCELLS[i]))):
            nowCell = LISTOFCELLS[i][j]
            if (nowCell.inShadow==True):
                totInShadow = totInShadow+1
    print "totInShadow", totInShadow

#open file

#write new file