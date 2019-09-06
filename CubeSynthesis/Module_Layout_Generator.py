# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 15:57:41 2019

@author: leiyuan
"""

from  python_gdsii.gdsii.library import Library
from  python_gdsii.gdsii.structure import Structure
from  python_gdsii.gdsii.elements import Boundary,ARef,Box,Path,SRef,Text
import os
import re
import pandas as pd



class Module_Layout_Generator:
    

    def __init__(self):
        print('Start generating layout')
        self.lib = 'None'
        self.structure_name_list = []
        self.structure_list = []
        self.physical_unit = 1e-9
        self.logical_unit = 0.001
        self.layer_list = []
        self.structure_dict = {}

    def Layout_Generator(self,lib_name,database_path,database,gds_file):
        lib_name_b = str.encode(lib_name+'.DB')
        lib = Library(5, lib_name_b,  self.physical_unit,self.logical_unit)   
        
        self.Database_to_Structure(database_path,database)
        
        for structure in self.structure_list:
            lib.append(structure)
        with open(gds_file, 'wb') as stream:
            lib.save(stream)
    
    def Database_to_Structure(self,database_path,database):
        file = open(database_path+database, "r")     
        structure_name = database[:-3]   
        
        self.structure_name_list.append(structure_name)
        element_dict = {}
        self.structure_dict[structure_name] = element_dict
    

        text = [t.strip() for t in file.readlines()]  
        if text[0] == '@cubism':
            structure_name = text[1].split()[1]
            structure = Structure(structure_name.encode())
            print(structure_name)
            for line in text[2:]:  
                if line == 'endlayout':
                    break
                else:
                    name,loc,para = line.split()
                    print(name,loc,para)
                    self.Database_Compiler
                    
                    
    def Database_Compiler(self,line):
        a = 'dd'
        return a
                             
                    
'''                    
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
                        if layer_map:
                            layer,datatype = map_dict[(layer,datatype)]
                        
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
                        if layer_map:
                            layer,datatype = map_dict[(layer,datatype)]                        
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
                        sname,mirror,angle = para.split(',')
                        I = SRef(sname.encode(),xy)
                        if bool(int(mirror)):
                            I.strans = pow(2,15)
                        else:
                            I.strans = 0   
                        if bool(float(angle)):
                            I.strans = I.strans + 2
                            I.angle = float(angle)
                        if save_e:#save data into element dict
                            _I = _element(name,'I')
                            _I._read_I(xy,sname)
                            element_dict[name] = _I                       
                        structure.append(I)
                        if sname in self.structure_name_list:
                            pass
                        else:
                           self.cubism_to_structure(cubism_folder,sname+'.cu') #think of location
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
                        if layer_map:
                            layer,datatype = map_dict[(layer,datatype)]
                            
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
                        if layer_map:
                            layer,datatype = map_dict[(layer,datatype)]                        
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
                           self.cubism_to_structure(cubism_folder,para+'.cu') #think of location
                    #----------------------------------------------------------
                                                              
                        
                        
                    else:
                        print(line)
                        print('-----some element unrealized------')
            self.structure_list.append(structure)   



    def cubism_to_gds(self,lib_name,cubism_folder,cubism_file,gds_file,layer_map = False,layer_map_para = []):#synthesis
        lib_name_b = str.encode(lib_name+'.DB')
        lib = Library(5, lib_name_b,  self.physical_unit,self.logical_unit)
        self.layer_map = layer_map
        self.layer_map_para = layer_map_para
        self.cubism_to_structure(cubism_folder,cubism_file)
        for structure in self.structure_list:
            lib.append(structure)
        with open(cubism_folder + gds_file, 'wb') as stream:
            lib.save(stream)
        
    def cubism_to_structure(self,cubism_folder,cubism_file):    
        file = open(cubism_folder+cubism_file, "r") 
        structure_name = cubism_file[:-3]
        self.structure_name_list.append(structure_name)
        element_dict = {}
        self.structure_dict[structure_name] = element_dict
        #
        layer_map = self.layer_map
        layer_map_para = self.layer_map_para
        #
        if layer_map:
            print(layer_map_para[0],layer_map_para[1],layer_map_para[2])
            map_dict = self.layer_mapping(layer_map_para[0],layer_map_para[1],layer_map_para[2])
        
        text = [t.strip() for t in file.readlines()]  
        if text[0] == '@cubism':
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
                        if layer_map:
                            layer,datatype = map_dict[(layer,datatype)]
                        
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
                        if layer_map:
                            layer,datatype = map_dict[(layer,datatype)]                        
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
                        sname,mirror,angle = para.split(',')
                        I = SRef(sname.encode(),xy)
                        if bool(int(mirror)):
                            I.strans = pow(2,15)
                        else:
                            I.strans = 0   
                        if bool(float(angle)):
                            I.strans = I.strans + 2
                            I.angle = float(angle)
                        if save_e:#save data into element dict
                            _I = _element(name,'I')
                            _I._read_I(xy,sname)
                            element_dict[name] = _I                       
                        structure.append(I)
                        if sname in self.structure_name_list:
                            pass
                        else:
                           self.cubism_to_structure(cubism_folder,sname+'.cu') #think of location
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
                        if layer_map:
                            layer,datatype = map_dict[(layer,datatype)]
                            
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
                        if layer_map:
                            layer,datatype = map_dict[(layer,datatype)]                        
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
                           self.cubism_to_structure(cubism_folder,para+'.cu') #think of location
                    #----------------------------------------------------------
                                                              
                        
                        
                    else:
                        print(line)
                        print('-----some element unrealized------')
            self.structure_list.append(structure)   
'''            