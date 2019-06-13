# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:39:52 2019

@author: leiyuan
"""

#CubeSynthesis 1st editon

from  python_gdsii.gdsii.library import Library
from  python_gdsii.gdsii.structure import Structure
from  python_gdsii.gdsii.elements import Boundary,ARef,Box,Path,SRef,Text
import os
import re



class _element:
    def __init__(self,name,dtype):
        self.name = name    
        self.dtype = dtype
    def _read_B(self,xy,layer,layer_dt):
        self.xy = xy
        self.layer = layer
        self.layer_dt = layer_dt         
        self.box = _box()
        self.box._B_box(xy)
        self.location = self.box.ld
    def _read_BR(self,r_location,r_init,xy_init,layer,layer_dt):  
        self.r_location = r_location
        self.r_init = r_init
        self.xy = xy_init
        self.layer = layer
        self.layer_dt = layer_dt           
        vector_x = r_location[0] - r_init[0]
        vector_y = r_location[1] - r_init[1]
        self.abs_xy = [(t[0] + vector_x,t[1] + vector_y) for t in xy_init]
    def _read_P(self,xy,layer,layer_dt,width):
        self.xy = xy
        self.layer = layer
        self.layer_dt = layer_dt   
        self.width = width        
        
    def _read_I(self,xy,address,structlist = False):
        self.xy = xy
        self.address = address
        self.box = _box()
        self.box._I_box(xy,address)#temporary
        self.location = xy[0]

    def _read_IR(self,r_location,r_init,xy_init,address):  
        self.r_location = r_location
        self.r_init = r_init
        self.xy = xy_init
        self.address = address
        vector_x = r_location[0] - r_init[0]
        vector_y = r_location[1] - r_init[1]
        self.abs_xy = [(xy_init[0] + vector_x,xy_init[1] + vector_y)]

        
    def _read_PR(self,r_location,r_init,xy_init,layer,layer_dt,width):
        self.r_location = r_location
        self.r_init = r_init        
        self.xy = xy_init
        self.layer = layer
        self.layer_dt = layer_dt   
        self.width = width 
        vector_x = r_location[0] - r_init[0]
        vector_y = r_location[1] - r_init[1]
        self.abs_xy = [(t[0] + vector_x,t[1] + vector_y) for t in xy_init]          
        
        
class _box:
    def __init__(self):
        pass
    def _B_box(self,xy):
        x = [t[0] for t in xy]
        y = [t[1] for t in xy]        
        self.l = min(x)
        self.r = max(x)
        self.u = max(y)
        self.d = min(y)
        self.ld = (self.l,self.d)
        self.lu = (self.l,self.u)
        self.rd = (self.r,self.d)
        self.ru = (self.r,self.u)
        self.width = self.r - self.l
        self.height = self.u - self.d
        self.centre = ((self.l + self.r)/2,(self.u + self.d)/2)  
    def _I_box(self,xy,structure_dict):
        #future
        pass
        
        



class CubeSynthesis:
    def __init__(self):
        self.lib = 'None'
        self.structure_name_list = []
        self.structure_list = []
        self.physical_unit = 1e-9
        self.logical_unit = 0.001
        self.layer_list = []
        self.structure_dict = {}
        
    def cube_to_gds(self,lib_name,cube_folder,cube_file,gds_file):#synthesis
        lib_name_b = str.encode(lib_name+'.DB')
        lib = Library(5, lib_name_b,  self.physical_unit,self.logical_unit)
        self.cube_to_structure(cube_folder,cube_file)
        for structure in self.structure_list:
            lib.append(structure)
        with open(cube_folder + gds_file, 'wb') as stream:
            lib.save(stream)
        
    def cube_to_structure(self,cube_folder,cube_file):    
        file = open(cube_folder+cube_file, "r") 
        structure_name = cube_file[:-4]
        self.structure_name_list.append(structure_name)
        element_dict = {}
        self.structure_dict[structure_name] = element_dict
        
        text = [t.strip() for t in file.readlines()]  
        if text[0] == '@cube':
            structure_name = text[1].split()[1]
            structure = Structure(structure_name.encode())
            print(structure_name)
            for line in text[2:]:  
                if line == 'endlayout':
                    break
                else:
                    dtype = line.split()[0]
                    rex = re.findall(r'\[(.*?)\]', line)
                    xy_s = rex[0]
                    para = rex[1]
                    save_e = False
                    if len(rex) == 3:
                        save_e = True
                        name = rex[2]
                    else:
                        name = 'None'
                    
                    #----------------------------------------------------------    
                    if dtype == 'B':
                        xy_s = re.findall(r'\((.*?)\)', xy_s)
                        xy =[]
                        for p in xy_s:
                            x,y = p.split(',')
                            xy.append((int(x),int(y)))
                        layer,datatype = para.split(',')
                        layer = int(layer)
                        datatype = int(datatype)
                        B = Boundary(layer, datatype, xy)
                        if save_e:#save data into element dict
                            _B = _element(name,'B')
                            _B._read_B(xy,layer,datatype)
                            element_dict[name] = _B
                        structure.append(B)
                    #----------------------------------------------------------
                    elif dtype == 'P':
                        xy_s = re.findall(r'\((.*?)\)', xy_s)
                        xy =[]
                        for p in xy_s:
                            x,y = p.split(',')
                            xy.append((int(x),int(y)))
                        width,layer,datatype = para.split(',')
                        width = int(width)
                        layer = int(layer)
                        datatype = int(datatype)
                        if save_e:#save data into element dict
                            _P = _element(name,'P')
                            _P._read_P(xy,layer,datatype,width)
                            element_dict[name] = _P         
                            
                        P = Path(layer, datatype,xy)
                        P.width = width
                        structure.append(P)
                    #----------------------------------------------------------       
                    elif  dtype == 'I':   
                        xy_s = re.findall(r'\((.*?)\)', xy_s)
                        xy =[]
                        for p in xy_s:
                            x,y = p.split(',')
                            xy.append((int(x),int(y)))
                        
                        I = SRef(para.encode(),xy)
                        if save_e:#save data into element dict
                            _I = _element(name,'I')
                            _I._read_I(xy,para)
                            element_dict[name] = _I                       
                        structure.append(I)
                        if para in self.structure_name_list:
                            pass
                        else:
                           self.cube_to_structure(cube_folder,para+'.txt') #think of location
                    #----------------------------------------------------------   
                    elif dtype == 'BR':
                        xy_s = re.findall(r'\((.*?)\)', xy_s)
                        xy =[]
                        R_name = xy_s[0]
                        R_location = element_dict[R_name].location
                        for p in xy_s[1:]:
                            x,y = p.split(',')
                            xy.append((int(x),int(y)))
                        layer,datatype = para.split(',')
                        layer = int(layer)
                        datatype = int(datatype)
                        if save_e:#save data into element dict
                            _BR = _element(name,'BR')
                            _BR._read_BR(R_location,xy[0],xy[1:],layer,datatype)
                            element_dict[name] = _BR
                        B = Boundary(layer, datatype, _BR.abs_xy)                            
                        structure.append(B)
                    #----------------------------------------------------------
                    elif dtype == 'PR':
                        xy_s = re.findall(r'\((.*?)\)', xy_s)
                        xy =[]
                        R_name = xy_s[0]
                        R_location = element_dict[R_name].location                        
                        for p in xy_s[1:]:
                            x,y = p.split(',')
                            xy.append((int(x),int(y)))
                        width,layer,datatype = para.split(',')
                        width = int(width)
                        layer = int(layer)
                        datatype = int(datatype)
                        if save_e:#save data into element dict
                            _PR = _element(name,'PR')
                            _PR._read_PR(R_location,xy[0],xy[1:],layer,datatype,width)
                            element_dict[name] = _PR                          
                                   
                        P = Path(layer, datatype,_PR.abs_xy)
                        P.width = width
                        structure.append(P)
                    #----------------------------------------------------------                       
                    elif dtype == 'IR':
                        xy_s = re.findall(r'\((.*?)\)', xy_s)
                        xy =[]
                        R_name = xy_s[0]
                        R_location = element_dict[R_name].location                        
                        for p in xy_s[1:]:
                            x,y = p.split(',')
                            xy.append((int(x),int(y)))
                        if save_e:#save data into element dict
                            _IR = _element(name,'IR')
                            _IR._read_IR(R_location,xy[0],xy[1],para)
                            element_dict[name] = _IR                               
                        I = SRef(para.encode(),_IR.abs_xy)                            
                        structure.append(I)
                        if para in self.structure_name_list:
                            pass
                        else:
                           self.cube_to_structure(cube_folder,para+'.txt') #think of location
                    #----------------------------------------------------------
                                                
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                    else:
                        print(line)
                        print('-----some element unrealized------')
            self.structure_list.append(structure)         
        else:
            print('Format Error!!!')
       
        file.close()         
        return structure
    
    
    def gds_to_cube(self,gds_file,cube_folder):
        with open(gds_file, 'rb') as stream:
            lib = Library.load(stream)
            for structure in lib:
                self.convert_structure(structure,cube_folder)                             
            self.layer_list =  list(set(self.layer_list))
            
    def convert_structure(self,structure,cube_folder):
        if isinstance(structure,Structure):         
            s_name = cube_folder + structure.name.decode("utf-8") 
            if os.path.isfile(s_name + '.txt'):
                print(s_name + ' exist!')
                pass
            else:
                file = open(s_name + ".txt", "w") 
                file.write('@cube\n')
                file.write('layout ' + structure.name.decode("utf-8") + '\n')
                                    
                for element in structure:
                    if isinstance(element,Boundary):
                        line = 'B ' + str(element.xy)
                        line = line + ' [' + str(element.layer) + \
                                ',' + str(element.data_type) + ']\n'
                        file.write(line) 
                        self.layer_list.append((element.layer,element.data_type))
                    elif isinstance(element,Path):
                        line = 'P ' + str(element.xy)
                        line = line + ' ['+ str(element.width) + ',' +\
                                str(element.layer) + ',' + str(element.data_type) + ']\n'
                        file.write(line)  
                        self.layer_list.append((element.layer,element.data_type))                        
                    elif  isinstance(element,SRef):   
                        line = 'I ' + str(element.xy)
                        line = line + ' ['+ str(element.struct_name.decode("utf-8") ) + ']\n'
                        file.write(line)                    
                    else:
                        print(element)
                        print('-----some element unconverted------')
                file.write('endlayout')                 
                file.close()    
                        
        
#test 
#  para2_s = re.findall(r'\{(.*)\}', line)
with open('../gds/inv.gds', 'rb') as stream:
    lib = Library.load(stream)        


file = open("copy.txt", "w") 
file.write("Your text goes here") 
file.close() 

os.path.isfile('copy2.txt')




c = CubeSynthesis()
#c.gds_to_cube('../gds/inv.gds','cubefile/inv/')

test = c.cube_to_gds("smic14ff_lei_test","cubefile/inv2/","inv_test.txt","cube.gds")








