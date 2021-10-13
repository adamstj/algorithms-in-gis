#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'qt')


# In[ ]:


#Opens the Coord.txt file and the Polygons.txt file and creates each a nested list for each row in the file.
with open(r"C:\Users\adams\Documents\Lund_Master\GISN07\4_Point-in-polygon\data\Coord.txt") as f:
    coords = []
    for line in f: 
        coords.append([int(x) for x in line.split()])
print(coords)

with open(r"C:\Users\adams\Documents\Lund_Master\GISN07\4_Point-in-polygon\data\Polygons.txt") as f:
    polygons = []
    for line in f: 
        polygons.append([int(x) for x in line.split()])
print(polygons)


# In[ ]:


#Iterates over the polygons list and appends each polygon vertex x,y (indexed from the coords list) to two new lists separately
# one containing all the x values and the other the y values, nested in a list for each polygon.
x_values = []
y_values = []
for index, polygon in enumerate(polygons):
    temp_x = []
    temp_y = []
    for vertex in polygon:
        if vertex != 0:
            temp_x.append(coords[vertex-1][0])
            temp_y.append(coords[vertex-1][1])
    x_values.append(temp_x)
    y_values.append(temp_y)
    
print("X Values: ", x_values)
print("Y Values: ",y_values)


# In[ ]:


#Creates a function called AreaCalc which takes three arguments, an x-list, a y-list and a index value
def AreaCalc(x_list, y_list, ind):
    #Test if the first and last vertex has the same position
    if x_list[ind][0] == x_list[ind][-1] and y_list[ind][0] == y_list[ind][-1]:
        #Creates a Variable "n" which holds the number of line segments
        n = len(x_list[ind]) - 1
    else:
        #Creates another last vertex which holds the same position as the first vertex
        x_list[ind].append(x_list[ind][0])
        y_list[ind].append(y_list[ind][0])
        n = len(x_list[ind]) - 1
    
    #Creates a Variable "area" and sets it to 0
    area = 0

    # Iterates for each line segment (which is 1 less than number of
    # vertexes) to ensure it does not perform the formula on the last
    # vertex as "i", as there will be no "i+1" for that one.
    for index, i in enumerate(range(n)):
        #Computes the determinant of current and nextcoming vertex, then
        #adds that with the current "area" value and assigns it as a new
        #value to "area".
        area += (x_list[ind][i]*y_list[ind][i+1] - y_list[ind][i]*x_list[ind][i+1])
    
    #The absolute value (Not negative) is divided by half and assigned to "area"
    area = 1/2*abs(area)
    return area


# In[ ]:


#Creates a function called IntersectOne which takes six arguments, two x-values, two y-values and two point values
#Where xa_val == the first vertex x-value and ya_val == the first vertex y-value (vertex a)
#and xb_val == the second vertex x-value and yb_val == the second vertex y-value (vertex b)
#and poiA == the "point of interest" value (vertex c) and poiB == the generated point where x == 0 (vertex d) (These two represents a line object for the clicked point)
def IntersectOne(xa_val, xb_val, ya_val, yb_val, poiA, poiB):

    #Calculates the area of vertex a, b and c
    area_valA = (ya_val * (xb_val - poiA[0]) + 
                yb_val * (poiA[0] - xa_val) + 
                poiA[1] * (xa_val - xb_val)) / 2
    #Sets a side measure value depending on if the area is positive, negative or 0
    if area_valA > 0:
        side_valA = 1
    elif area_valA == 0:
        side_valA = 0
    else:
        side_valA = -1

    #Calculates the area of vertex a, b and d
    area_valB = (ya_val * (xb_val - poiB[0]) + 
                yb_val * (poiB[0] - xa_val) + 
                poiB[1] * (xa_val - xb_val)) / 2
    #Sets a side measure value depending on if the area is positive, negative or 0
    if area_valB > 0:
        side_valB = 1
    elif area_valB == 0:
        side_valB = 0
    else:
        side_valB = -1


    # Checks if vertex c and d are on the same side of a,b-line
    if side_valA != side_valB:
        FirstMatch = 1
    else:
        FirstMatch = 0
        
    return FirstMatch


# In[ ]:


#Creates a function called IntersectTwo which takes six arguments, two x-values, two y-values and two point values
#Calculates the same thing as function IntersectOne except this time with line object composed of vertex c and d in focus
def IntersectTwo(poiA, poiB, xa_val, xb_val, ya_val, yb_val):

    #Calculates the area of vertex c, d and a
    area_valA = (poiA[1] * (poiB[0] - xa_val) + 
                poiB[1] * (xa_val - poiA[0]) + 
                ya_val * (poiA[0] - poiB[0])) / 2
    #Sets a side measure value depending on if the area is positive, negative or 0
    if area_valA > 0:
        side_valA = 1
    elif area_valA == 0:
        side_valA = 0
    else:
        side_valA = -1

    #Calculates the area of vertex c, d and b
    area_valB = (poiA[1] * (poiB[0] - xb_val) + 
                poiB[1] * (xb_val - poiA[0]) + 
                yb_val * (poiA[0] - poiB[0])) / 2
    #Sets a side measure value depending on if the area is positive, negative or 0
    if area_valB > 0:
        side_valB = 1
    elif area_valB == 0:
        side_valB = 0
    else:
        side_valB = -1

    #Checks if vertex a and b are on the same side of c,d-line
    if side_valA != side_valB:
        SecondMatch = 1
    else:
        SecondMatch = 0

    return SecondMatch


# In[ ]:


#Creates a function called IntersectFunc which takes three arguments a list of x, a list of y and the point of interest
def IntersectFunc(x_values, y_values, poi):
    #Creates a line by appending another vertex with x == 0 and y == to the y of first vertex
    poi_line = list([poi])
    poi_line.append([0, poi[1]])

    #Creates a nested lists with the number of sub-lists set to the number of polygons
    # to store potential intersections at certain lines
    intersect_list = [[] for x in range(len(x_values))]

    # Iterates each polygon
    for polygon in range(len(x_values)):
        #Iterates each vertex except the last one
        for vertex in range(len(x_values[polygon])-1):
            #Calls the 'IntersectOne' function on the present vertex (a), next vertex (b) poi (c) and poi with x==0 (d)
            First_measure = IntersectOne(x_values[polygon][vertex], x_values[polygon][vertex+1], 
                                        y_values[polygon][vertex], y_values[polygon][vertex+1], 
                                        poi_line[0], poi_line[1])

            #Calls the 'IntersectTwo' function on the poi(c), poi with x==0 (d), present vertex (a) and next vertex (b)
            Second_measure = IntersectTwo(poi_line[0], poi_line[1], 
                                        x_values[polygon][vertex], x_values[polygon][vertex+1], 
                                        y_values[polygon][vertex], y_values[polygon][vertex+1])

            #Check if the two values returned from the two functions 'IntersectOne' and 'IntersectTwo'
            #both returns 1, if so, classify it as an intersection and store the information in the intersect_list.
            if First_measure == 1 and Second_measure == 1:
                intersect_list[polygon].append(1)
            else:
                intersect_list[polygon].append(0)

    return intersect_list


# In[ ]:


#Creates a function called PointInPolygonFunc which takes one argument, a list of 1/0 values,
# where 1 == intersection
def PointInPolygonFunc(list_of_intersections):
    
    #Iterates each polygon
    for index, i in enumerate(range(len(list_of_intersections))):
        #Initiate an intersect counter which resets for each new polygon
        IntersectCounter = 0

        #Iterate each line segment in the polygon
        for jndex, j in enumerate(range(len(list_of_intersections[i]))):
            #accumulate the intersect values for the current polygon
            IntersectCounter += list_of_intersections[i][j]

        #If the remainder of the number of intersects divided by two is not 0 then it is an odd number
        # and the polygon by which the point is within have been found
        if (IntersectCounter % 2) != 0:
            #print("Point is in polygon index:", index)
            return index
        else:
            continue


# In[ ]:


# Plot the figure
fig = plt.figure()
ax = fig.add_subplot(111)

#Iterate over each polygon and plot its border black
# and fill its area blue
for index, i in enumerate(range(len(polygons))):
    ax.plot(x_values[i],y_values[i], color='black', lw=2)
    ax.fill_between(x_values[i],y_values[i], color='blue', y2=0) #y2=0, lw=2)


#Create an empty list for storing the input coordinates when clicking the map
clicked_vertex = []

#Create a function called onclick which takes one argument, event
def onclick(event):

    #Store the x,y coordinates generated from clicking the map in a list
    clicked_x, clicked_y = event.xdata, event.ydata
    clicked_vertex = [clicked_x, clicked_y]
    print("You clicked at X: {:.2f} Y: {:.2f}".format(clicked_vertex[0], clicked_vertex[1]))

    #Calls the function InterSectFunc to calculate if the clicked point and its fictive line going to X = 0 
    # intersects with each line segment in each polygon and returns a list containing information of whether it intersected to each line segment.
    intersectionslist = IntersectFunc(x_values, y_values, clicked_vertex)

    #Calls the function PointInPolygonFunc to calculate the number of intersections to each polygon and returns which polygon has 
    # an odd number of intersections i.e. the polygon which the clicked point is within.
    selectedpoly = PointInPolygonFunc(intersectionslist)

    #Calls the function AreaCalc to calculate the area of the selected polygon
    area_of_selected = AreaCalc(x_values,y_values,selectedpoly)


    print("\nyou selected polygon with index:", selectedpoly)
    print("\nThe area of the polygon you selected is:",area_of_selected)
    
    #Iterate over each polygon to plot them again
    for index, i in enumerate(range(len(polygons))):

        #If the polygon is the currently selected one it plot its border and fill it red
        if index == selectedpoly:
            ax.plot(x_values[i],y_values[i], color='red', lw=2)
            ax.fill_between(x_values[i],y_values[i], color='red')

        #All other polygons gets plotted its border black and fill in blue
        else:
            ax.plot(x_values[i],y_values[i], color='black', lw=2)
            ax.fill_between(x_values[i],y_values[i], color='blue')
    plt.draw()

    print("\nDo you want to choose another polygon?")
    print("----------------------------------------------------\n")


cid = fig.canvas.mpl_connect('button_press_event', onclick)


plt.show()

