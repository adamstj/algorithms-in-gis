#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'qt')


# In[3]:


#Opens the Coord.txt file and the Polygons.txt file and creates each a nested list for each row in the file.
with open(r"C:\Users\adams\Documents\Lund_Master\GISN07\6_Affine_transformation\data\commonPoints.txt") as f:
    coords = []
    for line in f: 
        coords.append([int(x) for x in line.split()])
print(coords)


# In[4]:


#Create two separate lists consisting of the x,y and X,Y respectively
primaryC = [[] for x in range(len(coords))]
secondaryC = [[] for x in range(len(coords))]
for index, coord in enumerate(coords):
    primaryC[index].extend((coord[3], coord[4]))
    secondaryC[index].extend((coord[1], coord[2]))


print(primaryC)
print(secondaryC)


# In[5]:


#Create the Y vector
Y = np.zeros((6, 1))
for index, i in enumerate(secondaryC):
    Y[index] = i[0]
    Y[index+len(secondaryC)] = i[1]
print(Y)


# In[6]:


#Create the A matrix
A = np.zeros((6,6))
for index, i in enumerate(primaryC):
    A[index][0] = 1
    A[index][1] = i[0]
    A[index][2] = i[1]

    A[index+len(primaryC)][len(primaryC)] = 1
    A[index+len(primaryC)][len(primaryC)+1] = i[0]
    A[index+len(primaryC)][len(primaryC)+2] = i[1]
print(A)


# In[7]:


#Create the B vector consisting of a1,a2,a3,b1,b2,b3
B = np.linalg.solve(A,Y)
print(B)


# In[8]:


# Extracting the unknown parameters from the B vector and its corresponding computations
X0 = B[0]
Y0 = B[3]
mx = np.sqrt((B[1]**2 + B[4]**2))
my = np.sqrt((B[2]**2 + B[5]**2))
a = np.arctan((B[4]/B[1]))
b = np.arctan((-B[5]/B[2])) - np.arctan((B[4]/B[1]))

print("this is the unknown parameters: \n\nX0: {}\nY0: {} \nmx: {} \nmy: {} \na: {} \nb: {}".format(X0[0], Y0[0], mx[0], my[0], a[0], b[0]))


# In[9]:


#Plots the two sets of points in separate subplots
fig, axes = plt.subplots(nrows=1, ncols=2)
axes[0].set_title('Original System')
axes[1].set_title('Destination System')

for index, i in enumerate(primaryC):
    axes[0].plot(primaryC[index][0], primaryC[index][1], color ='red', marker = 'o', label='Control Point' if index == 0 else "")
    axes[1].plot(secondaryC[index][0], secondaryC[index][1], color ='blue', marker = 'o', label='Control Point' if index == 0 else "")

axes[0].legend()
axes[1].legend()

