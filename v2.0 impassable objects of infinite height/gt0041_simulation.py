import rhinoscriptsyntax as rs
import math
import random
import gt0021_classes as gt002
import gt0031_functions as gt003
import pprint, pickle

supercounter    = 200         #number of process iterations

#open pickle file for simulation initial conditions data
path = "simulation data/"
fileName = raw_input('Open which file?')
fullPath = path+fileName+".pkl"
reference_file = open(fullPath, 'rb')
cellList = pickle.load(reference_file)
reference_file.close()


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

#output data to text file
#find new extension
newExtension = int(fileName[len(fileName)-1])+1
#remove old extension
newName = fileName[:-1]+str(newExtension)+".pkl"
newPath = path+newName
output = open(newPath, 'wb')
pickle.dump(cellList, output)
output.close()