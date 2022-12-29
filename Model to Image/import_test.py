from datetime import datetime, time
import projection
from random import random
import math
from plyfile import PlyData, PlyElement
import os
    
def ply_render_faces(file, length):
    #read ply file
    points = []
    faces = []
    with open(file, 'rb') as f:
        plydata = PlyData.read(f)

    if 'red' in plydata['vertex']: 
        for i in range(len(plydata['vertex']['x'])):
            points.append([plydata['vertex'][i][0], plydata['vertex'][i][1], plydata['vertex'][i][2]])

        #for every face that has a list of vertexes, gather all of the corners and the color of the face
        for i in range(len(plydata['face'])):
            corners = []
            
            red_avg = 0
            green_avg = 0
            blue_avg = 0
            count = 0
            #the first number in the face is the number of corners so count from 0+1 to the first number -1 
            for j in range(len(plydata['face'][i][0])):
                corners.append(plydata['face'][i][0][j])
                red_avg += plydata['vertex']['red'][plydata['face'][i][0][j]]
                green_avg += plydata['vertex']['green'][plydata['face'][i][0][j]]
                blue_avg += plydata['vertex']['blue'][plydata['face'][i][0][j]]
                count += 1
            
            red_avg = red_avg / count
            green_avg = green_avg / count
            blue_avg = blue_avg / count
            
            color = (red_avg, green_avg, blue_avg)
            faces.append([corners,color])
        
        folder_name = file[0:(len(file)-4)]
        projection.render_faces(points, faces, length, folder_name)    
    if 'red' in plydata['face']: 
        for i in range(len(plydata['vertex']['x'])):
            points.append([plydata['vertex'][i][0], plydata['vertex'][i][1], plydata['vertex'][i][2]])

    #for every face that has a list of vertexes, gather all of the corners and the color of the face
    for i in range(len(plydata['face'])):
        corners = []
        color = (plydata['face'][i][1], plydata['face'][i][2], plydata['face'][i][3])
        
        #the first number in the face is the number of corners so count from 0+1 to the first number -1 
        for j in range(len(plydata['face'][i][0])):
            corners.append(plydata['face'][i][0][j])
        faces.append([corners,color])
        
    folder_name = file[0:(len(file)-4)]
    projection.render_faces(points, faces, length, folder_name)
    


startTime = datetime.now()
#----------------Use PLY files to generate renders-------------------
#open all files in parent dir
'''
for filename in os.listdir(os.getcwd()):
    #only renders .ply files
    if not filename.endswith(".ply"):
        print(filename)
    else:
        renderStart = datetime.now()
        ply_render_faces(filename, 100)
        renderStop = datetime.now()
        print(filename + " total time: "+ str(renderStop - renderStart))

#ply_render_points("tet.ply", 1000000)

voxelStartTime = datetime.now()
#ply_render_faces("voxel factory.bake.ply", 1)
ply_render_faces("square.ply", 1000)
voxelEndTime = datetime.now()'''
tetStartTime = datetime.now()
ply_render_faces("tet.ply", 10000000)
tetEndTime = datetime.now()

endTime = datetime.now()

print("Start time: " + str(startTime) + "; End time: " + str(endTime) + "; Total time: " + str(endTime - startTime))

