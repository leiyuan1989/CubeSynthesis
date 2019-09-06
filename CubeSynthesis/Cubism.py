# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:39:52 2019

@author: leiyuan
"""
from  python_gdsii.gdsii.library import Library
from  python_gdsii.gdsii.structure import Structure
from  python_gdsii.gdsii.elements import Boundary,ARef,Box,Path,SRef,Text
import os
import re
import pandas as pd


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
        
        
class _Box:
    def __init__(self,name):
        self.name = name
    def _load_cubism_data(self,xy,para,line):
        self.xy = list(eval(xy))
        self.layer = list(eval(para))
        self._load_data(self.xy)
        self.cubism_line = line
        
    def _load_data(self,xy):    
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
    def _to_gds(self):
        pass
        

class _Path:
    def __init__(self,name):
        self.name = name
    def _load_cubism_data(self,xy,para,line):
        self.xy = list(eval(xy))
        para =  list(eval(para))
        self.width = para[0]
        self.layer = [para[1],para[2]]
        self.cubism_line = line        
    def _to_gds(self):
        pass
    
class _SRef:
    def __init__(self,name):
        self.name = name
    def _load_cubism_data(self,xy,para,line):
        #rotation[0]: X mirror, rotation[1]: angle 
        self.xy = list(eval(xy))
        sname,mirror,angle = para.split(',')
        self.sname = sname
        self.mirror = int(mirror)
        self.angle = float(angle)
        self.cubism_line = line
    def _to_gds(self):
        pass
    
        
        
class _structure:
    def __init__(self):
        self.e_dict={}
        self.b_dict={}
        self.p_dict={}
        self.i_dict={}
        self.s_dict = {}#structure dict
#    def _get(self,ename):
#        element = self.e_dict[ename]
#        if element

        print('ss')
    def _load_structure(self,cubism_folder,cubism_file):
        file = open(cubism_folder+cubism_file, "r") 
        text = [t.strip() for t in file.readlines()]  
        if text[0] == '@cubism':
            self.name = text[1].split()[1]
            B_count = 0
            P_count = 0
            I_count = 0
            for line in text[2:]:  
                if line == 'endlayout':
                    break
                else:
                    dtype = line.split()[0]
                    rex = re.findall(r'\[(.*?)\]', line)
                    #----------------------------------------------------------    
                    if dtype == 'B':
                        name = 'B' + str(B_count)
                        B_count = B_count + 1
                        B = _Box(name)
                        B._load_cubism_data(rex[0],rex[1],line)
                        self.e_dict[name] = B
                        self.b_dict[name] = B
                    #----------------------------------------------------------
                    elif dtype == 'P':
                        name = 'P' + str(P_count)
                        P_count = P_count + 1
                        P = _Path(name)
                        P._load_cubism_data(rex[0],rex[1],line)
                        self.e_dict[name] = P
                        self.p_dict[name] = P
                    #----------------------------------------------------------       
                    elif  dtype == 'I':   
                        name = 'I' + str(I_count)
                        I_count = I_count + 1
                        I = _SRef(name)
                        I._load_cubism_data(rex[0],rex[1],line)
                        self.e_dict[name] = I
                        self.i_dict[name] = I
                        #
                        if I.sname in self.s_dict.keys():
                            pass
                        else:
                           New_S = _structure()
                           New_S.s_dict = self.s_dict
                           New_S._load_structure(cubism_folder,I.sname+'.cu') 
                           self.s_dict = New_S.s_dict
                    #----------------------------------------------------------                           
                    else:
                        print(line)
                        print('-----some element unrealized------')     
        else:
            print('Format Error!!!')      
        file.close()                     
        self.s_dict[self.name] = self    
        

#
#def read_shape(loc_data,structure):
#
#    print('-')
#def read_point():
#    if 0-9:
#        eval()
#    if b0.ss:
#        s.e_dict[b0].ss
#        
#        
def read_coord(data,struct):
    s = data
    #e.x.: "@-><B0>.l + @-><B1>.r"
    s = s.replace('@','struct')
    s = s.replace('->','._get')
    s = s.replace('<','(\'')
    s = s.replace('>','\')')
    return eval(s)
    

#->I0 t0 struc._got()    


class Cubism:
    def __init__(self):
        self.lib = 'None'
        self.structure_name_list = []
        self.structure_list = []
        self.physical_unit = 1e-9
        self.logical_unit = 0.001
        self.layer_list = []
        self.structure_dict = {}
 

    
    def cubism_to_cubismplus(self,cubism_folder,cubism_file,layer_map_para =[]):
        self.layer_map_para = layer_map_para       
        structure =  _structure()
        structure._load_structure( cubism_folder,cubism_file)
        for sname in structure.s_dict.keys():
             file = open(cubism_folder + sname + ".cup", "w") 
             temp_s= structure.s_dict[sname]
             for ename in temp_s.e_dict.keys():
                 temp_e = temp_s.e_dict[ename]
                 line = temp_e.cubism_line + ' [' + temp_e.name + ']\n'
                 file.write(line) 
             file.close()    
        return structure

    def cubismplus_to_gds(self):
        pass
        
        

       
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
        else:
            print('Format Error!!!')
       
        file.close()         
        return structure
    def layer_mapping(self,layer_file,init_pdk,target_pdk):
        layer_map = pd.read_excel(layer_file)
        layer_map = layer_map[[init_pdk+'_l',init_pdk+'_d',target_pdk+'_l',target_pdk+'_d']]
        map_dict = {}
        for i,r in layer_map.iterrows():
            map_dict[(r[init_pdk+'_l'],r[init_pdk+'_d'])] = (r[target_pdk+'_l'],r[target_pdk+'_d'])
        return map_dict
    
    def gds_to_cubism(self,gds_file,cubism_folder):
        with open(gds_file, 'rb') as stream:
            lib = Library.load(stream)
            for structure in lib:
                self.gds_convert_structure(structure,cubism_folder)                             
            self.layer_list =  list(set(self.layer_list))
            
    def gds_convert_structure(self,structure,cubism_folder):
        if isinstance(structure,Structure):         
            s_name = cubism_folder + structure.name.decode("utf-8") 
            if os.path.isfile(s_name + '.cu'):
                print(s_name + ' exist!')
                pass
            else:
                file = open(s_name + ".cu", "w") 
                file.write('@cubism\n')
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
                        mirror = 0
                        angle = 0
                        if bool(element.strans):
                           mirror = 1 
                        if bool(element.angle):
                            angle = element.angle
                        line = 'I ' + str(element.xy)
                        line = line + ' ['+ str(element.struct_name.decode("utf-8") ) + ','+ str(mirror) +',' + str(angle) + ']\n'
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



