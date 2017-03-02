import rhinoscriptsyntax as rs
import math
import random
import gt0022_classes as gt002
import gt0032_functions as gt003
import pprint, pickle

#to draw cell info and dunes geometry from pickled data file

#open pickle file
path = "simulation data/"
fileName = raw_input('Open which file?')
fullPath = path+fileName+".pkl"
reference_file = open(fullPath, 'rb')
cellList = pickle.load(reference_file)
reference_file.close()

#draw cell boxes
#gt003.draw_cells(cellList)

#draw dunes
gt003.draw_dunes(cellList)