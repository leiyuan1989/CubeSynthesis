# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 02:01:41 2019

@author: leiyu
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


#
def layout_viewer(folder,file,dr):
    fig, ax = plt.subplots(figsize = (10,10))    
    file = open(folder + '/' + file, "r") 
    text = [t.strip() for t in file.readlines()]    
    if text[0] == '@LayoutDatabase':
        name = text[1].split()[1]
        for line in text[2:-1]:
            l_type,t1,t2 = line.split(' [')
            loc = eval('[' + t1)
            layer = t2[:-1]
            if l_type == 'B':          
                plot_para = dr.get_plot_para(layer)
                ax.add_patch(mpatches.Polygon(loc, closed=True,fill=False,
                            color = plot_para[0],hatch = plot_para[1],
                            linestyle =  plot_para[2],alpha = plot_para[3]))
            elif l_type == 'P':
                path_w,layer0,layer1 = layer.split(',')
                plot_para = dr.get_plot_para(layer0+','+layer1)                
                polygons = path_to_polygon(loc,int(path_w))
                for polygon in polygons:
                    ax.add_patch(mpatches.Polygon(polygon, closed=True,fill=True,
                                color = plot_para[0],alpha = 0.5))                                    
            elif l_type == 'I':
                I_loc = loc[0]
                name,para1,para2 = layer.split(',')#maybe more hiearchy here, need more improvement
                file = open(folder + '/' + name + '.ld', "r") 
                text = [t.strip() for t in file.readlines()] 

                if text[0] == '@LayoutDatabase':
                    name = text[1].split()[1]
                    for line in text[2:-1]:
                        l_type,t1,t2 = line.split(' [')
                        orig_loc = eval('[' + t1)
                        loc = []
                        for p in orig_loc:
                            loc.append([p[0] + I_loc[0],p[1] + I_loc[1]])                       
                        layer = t2[:-1]
                        if l_type == 'B':          
                            plot_para = dr.get_plot_para(layer)
                            ax.add_patch(mpatches.Polygon(loc, closed=True,fill=False,
                                        color = plot_para[0],hatch = plot_para[1],
                                        linestyle =  plot_para[2],alpha = plot_para[3]))
                        elif l_type == 'P':
                            path_w,layer0,layer1 = layer.split(',')
                            plot_para = dr.get_plot_para(layer0+','+layer1)                
                            polygons = path_to_polygon(loc,int(path_w))
                            for polygon in polygons:
                                ax.add_patch(mpatches.Polygon(polygon, closed=True,fill=True,
                                            color = plot_para[0],alpha = 0.5))      
    plt.axis('equal')
    #plt.axis('off')
    plt.tight_layout()
    plt.show()        
    return (l_type,loc,layer)
    
    
    
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
