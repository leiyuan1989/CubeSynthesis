# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 14:51:21 2019

@author: leiyuan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:43:00 2019

@author: leiyuan
"""

#functions
import numpy as np

def rect_intersects(rect1,rect2):
    rect1_l,rect1_r,rect1_u,rect1_d = rect1
    rect2_l,rect2_r,rect2_u,rect2_d = rect2       
    if_intersects = not (rect1_r < rect2_l or rect1_l > rect2_r 
                         or rect1_u < rect2_d or rect1_d > rect2_u)     
    rect_intersects = []
    if if_intersects:
        rect_intersects = [max(rect1_l,rect2_l), min(rect1_r,rect2_r),
                           min(rect1_u,rect2_u),max(rect1_d,rect2_d)]
    else:
        rect_intersects = []  
    return [if_intersects,rect_intersects]    

def rect_align(rect1,rect2):
    rect1_l,rect1_r,rect1_u,rect1_d = rect1
    rect2_l,rect2_r,rect2_u,rect2_d = rect2 
    t1 = (rect1_l == rect2_l)  and (rect1_r == rect2_r)
    t2 = (rect1_u == rect2_u)  and (rect1_d == rect2_d)    
    return (t1 or t2)
    
def point_in_rect(point,rect):
    return (point[0] >= rect[0] and point[0] <= rect[1] and
           point[1] <= rect[2] and point[1] >= rect[3])           

def merge_rect(rect1,rect2):
    l1,r1,u1,d1 = rect1
    l2,r2,u2,d2 = rect2
    return [min(l1,l2),max(r1,r2),max(u1,u2),min(d1,d2)]

def rect_resize(rect,l,r,u,d):
    return [rect[0] - l,rect[1] + r,rect[2] + u, rect[3] - d]

def get_rect(signle_row_df):
    return(signle_row_df[['b_l','b_r','b_u','b_d']].values.tolist()[0])

def get_square(rect,direction):
    if direction == 'l':
        return [rect[0],rect[0] + (rect[2]-rect[3]),rect[2],rect[3]]
    elif direction == 'r':
        return [rect[1] - (rect[2]-rect[3]), rect[1],rect[2],rect[3]]
    elif direction == 'u':
        return [rect[0], rect[1],rect[2],rect[2] - (rect[1] -rect[0])]
    elif direction == 'd':
        return [rect[0], rect[1],rect[3] + (rect[1] - rect[0]),rect[3]]


def dist(p1,p2):
    return np.sqrt(np.power(p1[0] - p2[0],2) + np.power(p1[1] - p2[1],2))


def rect_distance(rect1,rect2):    
    x1,x1b,y1b,y1 = rect1
    x2,x2b,y2b,y2 = rect2

    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if top and left:
        return dist((x1, y1b), (x2b, y2))
    elif left and bottom:
        return dist((x1, y1), (x2b, y2b))
    elif bottom and right:
        return dist((x1b, y1), (x2, y2b))
    elif right and top:
        return dist((x1b, y1b), (x2, y2))
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif bottom:
        return y1 - y2b
    elif top:
        return y2 - y1b
    else:             # rectangles intersect
        return 0      