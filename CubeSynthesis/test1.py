# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 02:14:06 2019

@author: leiyu
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

#https://xkcd.com/color/rgb/
plt.rcdefaults()

def path_segment_to_boundary(start_p,end_p,width):
    x1,y1 = start_p
    x2,y2 = end_p
    w = 0.5*width
    if (x1 == x2)&(y1!=y2):
        return [[x1-w,y1],[x1+w,y1],[x2+w,y2],[x2-w,y2],[x1-w,y1]]
    elif (x1 != x2)&(y1==y2):
        return [[x1,y1-w],[x1,y1+w],[x2,y2+w],[x2,y2-w],[x1,y1-w]]
    else:
        return ['error points']
    

def path_to_polygon(path_point,path_w):
    start_point = path_point[0]
    end_point = path_point[-1]
    polygons = []
    if len(path_point) <= 2:
        polygons.append(path_segment_to_boundary(start_point,end_point,path_w))
    else:
        for point in path_point[1:-1]:
            segment = path_segment_to_boundary(start_point,point,path_w)
            polygons.append(segment)
            polygons.append([[point[0] - 0.5*path_w,point[1] - 0.5*path_w],
                            [point[0] - 0.5*path_w,point[1] + 0.5*path_w],
                            [point[0] + 0.5*path_w,point[1] + 0.5*path_w],
                            [point[0] + 0.5*path_w,point[1] - 0.5*path_w],
                            [point[0] - 0.5*path_w,point[1] - 0.5*path_w]])

            start_point = point
            
    polygons.append(path_segment_to_boundary(start_point,end_point,path_w))    
    return polygons

        

    
    

fig, ax = plt.subplots()


x = np.array([0,2,2])
y = np.array([1,1,2])

#line = mlines.Line2D(x, y, lw=5., alpha=0.3,color = '#15b01a')
#ax.add_line(line)

points = tuple(zip(x, y))                   

polygons = path_to_polygon(points,0.2)                     
                     
for po in  polygons:
                       
                     
    ax.add_patch(mpatches.Polygon(po, closed=True,color = '#15b01a',
                      fill=False,alpha = 0.3,hatch=None))



#ax.add_patch(mpatches.Polygon(po, closed=True,color = '#15b01a',
                     # fill=False, hatch='/'))




plt.axis('equal')
#plt.axis('off')
plt.tight_layout()

plt.show()