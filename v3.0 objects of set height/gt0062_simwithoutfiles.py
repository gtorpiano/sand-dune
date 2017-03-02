import rhinoscriptsyntax as rs
import math
import random
import pprint, pickle
import gt0022_classes as gt002
import gt0032_functions as gt003

#functions

#global variables

gridX           = 100           #cells
gridY           = 100           #cells
gridSize        = 1000          #mm
avrSand         = 10            #units of sand
var             = 1
cellHeight      = gridSize/3    #height of unit of sand
windShadow      = 15            #degrees

#prevailing wind blowing from left to right!

cellList = []                   #this will become a 2D data structure

#generate grid of cells
cellList = gt003.generate_grid_cells(gridX, gridY, gridSize, avrSand, var, cellHeight, windShadow)

supercounter    = 10            #number of process iterations

#check total sand
gt003.total_sand(cellList)

#calculate initial avalanche until settles
gt003.avalanche_all_cells(cellList)

#calculate initial wind shadows
gt003.find_all_shadows(cellList)

#erosion/deposition process goes through all cells at random
gt003.erosion_deposition(cellList, supercounter)

#final avalanches to test if local avalanches are working
gt003.avalanche_all_cells(cellList)

#final shadows
gt003.find_all_shadows(cellList)

#total number of cells in shadow
gt003.find_total_cells_inShadow(cellList)

#draw cell boxes
#gt003.draw_cells(cellList)

#draw dunes
gt003.draw_dunes(cellList)