from random import random
from turtle import width
import numpy as np
import pygame
import math
import os

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


WIDTH,HEIGHT = 500, 500
pygame.display.set_caption("3D projection in pygame")
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#square
#"""
square_points = []
square_points.append([-1,-1,1])
square_points.append([1,-1,1])
square_points.append([1,1,1])
square_points.append([-1,1,1])
square_points.append([-1,-1,-1])
square_points.append([1,-1,-1])
square_points.append([1,1,-1])
square_points.append([-1,1,-1])
#"""
"""
[[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1],[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1]]
"""

#sphere
#"""
circle_points = []
radius = 1
sphere = 0
while sphere < 100:
    rand_x = random() * radius * 2 - radius
    rand_y = random() * radius * 2 - radius
    rand_z = math.sqrt(abs((radius * radius) - (rand_x * rand_x) - (rand_y * rand_y)))
    sphere_point = [rand_x, rand_y, rand_z]
    
    if (rand_x * rand_x) + (rand_y * rand_y) + (rand_z * rand_z)==(radius * radius):
        circle_points.append(sphere_point)
        sphere += 1
    
    rand_z *= -1
    sphere_point = [rand_x, rand_y, rand_z]  
    if (rand_x * rand_x) + (rand_y * rand_y) + (rand_z * rand_z)==(radius * radius):
        circle_points.append(sphere_point)
        sphere += 1
#"""
    
circle_pos = [WIDTH/2,HEIGHT/2]

projection_matrix = np.matrix([
    [1,0,0],
    [0,1,0],
    [0,0,0]
])

#Note: math.cos(angle) returns float while cos(angle) returns complex
def rotation_x (angle_x):
    matrix = np.matrix([
        [1,0,0],
        [0,math.cos(angle_x), -math.sin(angle_x)],
        [0,math.sin(angle_x),math.cos(angle_x)]
    ])
    return matrix
    
def rotation_y(angle_y):
    return np.matrix([
        [math.cos(angle_y),0,math.sin(angle_y)],
        [0,1,0],
        [-math.sin(angle_y),0,math.cos(angle_y)]
    ])
    
def rotation_z(angle_z):
    return np.matrix([
        [math.cos(angle_z),-math.sin(angle_z),0],
        [math.sin(angle_z),math.cos(angle_z),0],
        [0,0,1]
    ])    
            
def render_faces(points, faces, folder_size, name):
    pygame.display.set_caption("Projection of " + name)
    
    folder_name = name +"_Projection"

    parent_dir = os.getcwd()

    found = True

    count = 0
    while found:
        try: 
            path = folder_name + str(count)
            os.mkdir(os.path.join(parent_dir, path))
            found = False
        except:
            count += 1
        

    angle_x, angle_y, angle_z = 0, 0, 0

    translate_x, translate_y, translate_z = .25 , 0, 0

    tSwitch_x, tSwitch_y, tSwitch_z = 1, 1, 1

    tMax_x, tMax_y, tMax_z = 5, 5, 5

    max_x, max_y, max_z = -100000000, -100000000, -100000000
    min_x, min_y, min_z = 100000000, 100000000, 100000000
    for point in points:
        if point[0] > max_x: max_x = point[0]
        if point[1] > max_y: max_y = point[1]
        if point[2] > max_z: max_z = point[2]
        if point[0] < min_x: min_x = point[0]
        if point[1] < min_y: min_y = point[1]
        if point[2] < min_z: min_z = point[2]
    
    x_diff = max_x - min_x
    y_diff = max_y - min_y
    z_diff = max_z - min_z
    
    xyz_maxDiff = 0
    if x_diff > y_diff and x_diff > z_diff :
        xyz_maxDiff = x_diff
    elif y_diff > x_diff and y_diff > z_diff:
        xyz_maxDiff = y_diff
    elif z_diff > y_diff and x_diff < z_diff:
        xyz_maxDiff = z_diff
    else:
        xyz_maxDiff = x_diff
    
    sizeMin = 0
    if WIDTH < HEIGHT:
        sizeMin = WIDTH
    else:
        sizeMin = HEIGHT
        
    scale = (xyz_maxDiff) * (.30 * sizeMin)
    
    print(scale)
    

    projected_points = [
        [n,n] for n in range(len(points))
    ]

    translated_points = [
        [n,n,n] for n in range(len(points))
    ]



    clock = pygame.time.Clock()
    image_count = 0
    while image_count < folder_size:
        clock.tick(30)
        
        #setup closing the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        
        #-------------------DRAWING----------------
        #clear screen
        screen.fill(WHITE)
        
        for p in range(len(points)):
            translated_points[p-1][0] = translate_x + points[p-1][0]
            translated_points[p-1][1] = translate_y + points[p-1][1]
            translated_points[p-1][2] = translate_z + points[p-1][2]
            
        #print(translated_points)
        
        i = 0
        for point in translated_points:
            #use dot product to project x,y,z of 3d shape to x,y of screen
            #reshape forces each point to be a 2D array to be multiplied by the projection matrix
            rotated2d = np.dot(rotation_x(angle_x), np.matrix(point).reshape(3,1))
            rotated2d = np.dot(rotation_y(angle_y), rotated2d)
            rotated2d = np.dot(rotation_z(angle_z), rotated2d)
            projected2d = np.dot(projection_matrix, rotated2d)
            
            x = float(projected2d[0][0]*scale) + circle_pos[0]
            y = float(projected2d[1][0]*scale) + circle_pos[1]
            
            projected_points[i] = [x,y]
            #pygame.draw.circle(screen,RED,projected_points[i], 5)
            i += 1    
            
        for face in faces:
            #print(face)
            corners = []
            for i in face[0]:
                corners.append(projected_points[i])
            corners.append(corners[0])
            #print(corners)
            pygame.draw.polygon(screen,pygame.Color(face[1]),corners)
                
        #generate average point - for noticing translations
        x_sum = 0
        y_sum = 0
        z_sum = 0
        for p in range(len(translated_points)):
            x_sum += translated_points[p-1][0]
            y_sum += translated_points[p-1][1]
            z_sum += translated_points[p-1][2]
        
        average_point = [x_sum/len(translated_points), y_sum/len(translated_points), z_sum/len(translated_points)]
        rotated_average2d = np.dot(rotation_x(angle_x), np.matrix(average_point).reshape(3,1))
        rotated_average2d = np.dot(rotation_y(angle_y), rotated_average2d)
        rotated_average2d = np.dot(rotation_z(angle_z), rotated_average2d)
        projected_average2D = np.dot(projection_matrix, rotated_average2d)
        
        aX = float(projected_average2D[0][0] * scale) + circle_pos[0]
        aY = float(projected_average2D[1][0] * scale) + circle_pos[1]
            
        projected_average = [aX,aY]
        
                
        angle_x += .125
        angle_y += .015
        angle_z += .025
        
        if (translate_x * tSwitch_x) >= (tMax_x * tSwitch_x):
            tSwitch_x = tSwitch_x * -1
        
        if (translate_y * tSwitch_y) >= (tMax_y * tSwitch_y):
            tSwitch_y = tSwitch_y * -1
        
        if (translate_z * tSwitch_z) >= (tMax_z * tSwitch_z):
            tSwitch_z = tSwitch_z * -1
            
        #translate_x += random() * .005 * tSwitch_x
        #translate_y += random() * .0025 * tSwitch_y
        #translate_z += random() * .00125 * tSwitch_z
        
        
        #pygame.draw.circle(screen,BLACK,(30,30),5)
        
        image_label =  path + "/"+ name +"_projection" + str(image_count) + ".jpg"
        
        #update the screen and save image if and only if projection is on screen
        if(projected_average[0] > WIDTH *.9 or projected_average[0] < WIDTH * .1 or projected_average[1] > HEIGHT * .9 or projected_average[1] < HEIGHT * .1):
            tSwitch_x = tSwitch_x * -1
            tSwitch_y = tSwitch_y * -1
            tSwitch_z = tSwitch_z * -1
            screen.fill(RED)
            #pygame.display.update()
        else:
            pygame.display.update()
            pygame.image.save(screen, image_label)
            image_count += 1