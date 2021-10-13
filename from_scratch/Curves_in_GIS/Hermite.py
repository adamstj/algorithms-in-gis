#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseButton

get_ipython().run_line_magic('matplotlib', 'qt')


# In[ ]:


#Sets parameters for the plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0,5)
ax.set_ylim(0,5)

#Creates empty lists to store vertex x,y data
points = []
selectedx = []
selectedy = []

#Creates a function called 'onclick' which instantiates on left/right click of the mouse
def onclick(event):
    button = 1

    #Retrieve the clicked vertex
    clicked_x, clicked_y = event.xdata, event.ydata
    clicked_vertex = [clicked_x, clicked_y]

    #Check if left or right click
    if button == 1:
        if event.button is MouseButton.LEFT:
            button = 1
        else:
            button = 3

    #If left click, plot the point and then collect the vertexes clicked
    if button == 1:
        ax.plot(clicked_x,clicked_y, marker='*', markersize=8, color='b')
        selectedx.append(clicked_x)
        selectedy.append(clicked_y)
        points.append(clicked_vertex)
        print("Left click to add another vertex, Right click to finish the input")

    #If right click, Calculate and plot vertexes, line segments and Curves
    else:
        print("\nYou finished the input!")
        #Plot points and line segments
        for index, i in enumerate(range(len(points))):
            ax.plot(selectedx,selectedy, color='green', lw=1)
            ax.plot(selectedx[index],selectedy[index], marker='*', markersize=8, color='blue')
            
        rows = int(len(points))
        Xmatrix = np.ones((rows,rows), dtype=float)

        for row in range(len(Xmatrix)):
            for index, item in enumerate(range(len(Xmatrix[row])-1)):
                Xmatrix[row][item+1] = np.power(points[row][0], index +1)
        selectedy_np = np.array(selectedy)
        #Unsure if the np.linalg.solve() was okay to use in this exercise but it was the only 
        # equivalent solution I found in Python for the Matlab "Xmatrix\Y"
        parameters = np.linalg.solve(Xmatrix, selectedy_np)


        xPlotVal = np.linspace(selectedx[0], selectedx[-1], 100)
        yPlotVal = []

        for index, i in enumerate(range(len(xPlotVal))):
            tmp = 0
            tmp = parameters[0]
            for p in range(rows-1):
                tmp += parameters[p+1] * np.power(xPlotVal[i], p+1)
            yPlotVal.append(tmp)

        #Plot the 3rd polynominal curve
        plt.plot(xPlotVal,yPlotVal)

#######################################! HERMITE ALGORITHM2 START! #####################################
        #Create two list variables to store the x,y values of the Hermite algorithm for plotting
        xPlotValh = []
        yPlotValh = [[] for x in range(len(points)-1)]
        
        #Calculate k
        k_list = []
        for index, item in enumerate(range(len(points))):
            if index == 0:
                k = (points[item+1][1]-points[item][1])/(points[item+1][0]-points[item][0])
                k_list.append(k)
            elif index == len(points)-1:
                k = (points[item][1]-points[item-1][1])/(points[item][0]-points[item-1][0])
                k_list.append(k)
            else:
                k = (points[item+1][1]-points[item-1][1])/(points[item+1][0]-points[item-1][0])
                k_list.append(k)

        #Iterate for each polynom in the Hermite algorithm (each segment)
        for index, item in enumerate(range(len(points)-1)):
            #Set up each variable h,d,t,k1,k2 for each segment
            h = points[item+1][0] - points[item][0]
            d = points[item+1][1] - points[item][1]
            t = np.linspace(0, 1, 100)
            k1 = k_list[index]
            k2 = k_list[index+1]
            
            #Create an x-value for each t
            x = np.linspace(selectedx[index], selectedx[index+1], 100)
            xPlotValh.append(x)

            #Iterate each of the 100 created vertexes
            for jindex, j in enumerate(range(len(xPlotValh[index]))):
                tmp2 = 0
                #Calculate the Hermite for each vertex
                tmp2 = points[index][1] + t[jindex]*d + t[jindex]*(t[jindex]-1)*(d-h*k1) + t[jindex]**2 * (t[jindex]-1) * (h*(k1 + k2)-2*d)

                #Assign the calculated Hermite value to yPlotValh
                yPlotValh[index].append(tmp2)

#######################################! HERMITE ALGORITHM2 END! #######################################


        #Iterate each segment and plot the Hermite curve in color red
        for i in range(len(points)-1):
            plt.plot(xPlotValh[i],yPlotValh[i], color='red')

        print("The 3rd polynomial curve is colored blue\nThe Hermite is colored red")
        event.canvas.mpl_disconnect(cid)
    plt.draw()


print("left click to add a vertex, then right click to finish the input")
cid = fig.canvas.mpl_connect('button_press_event', onclick)

