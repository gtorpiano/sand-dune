import rhinoscriptsyntax as rs
import math
import random
import pprint, pickle
import gt0021_classes as gt002
import gt0031_functions as gt003

#functions

#global variables

gridX           = 100           #cells
gridY           = 100           #cells
gridSize        = 1000          #mm
avrSand         = 2             #units of sand
var             = 1
cellHeight      = gridSize/3    #height of unit of sand
windShadow      = 15            #degrees

#prevailing wind blowing from left to right!

cellList = []                   #this will become a 2D data structure

#generate grid of cells
cellList = gt003.generate_grid_cells(gridX, gridY, gridSize, avrSand, var, cellHeight, windShadow)

#output data to text file
path = "simulation data/"
fileName = raw_input('File Name?')
fullPath = path+fileName+"0.pkl"
output = open(fullPath, 'wb')
pickle.dump(cellList, output)
output.close()