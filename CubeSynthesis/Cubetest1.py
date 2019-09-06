# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 11:02:09 2019

@author: leiyuan
"""

import Cubism



cs = Cubism.Cubism()

cs.gds_to_cubism('../gds/3to1_NAND.gds','../cubefolder/3to1_NAND/')

#cs.gds_to_cubism('../gds/lvsft_nor_lv.gds','../cubefolder/lvsft_nor_lv/')
#test = cs.cubism_to_gds("smic14ff_lei_test","../cubefolder/lvsft_nor_lv/","lvsft_nor_lv.txt","cube.gds",layer_map = False)
#test = cs.cube_to_gds("auto_csmc011_test","cubefile/inv2/","inv.txt","cube.gds",layer_map = True,layer_map_para=map_para)
#struc = cs.cubism_to_cubismplus("../cubefolder/lvsft_nor_lv/","lvsft_nor_lv.txt")



#with open('../gds/cube.gds', 'rb') as stream:
#    lib = Library.load(stream)
#
#for s in  lib[-1]:
#    if isinstance(s,SRef):
#        print(bool(s.strans),bool(s.angle),s.xy)
#        print(s.strans,s.angle,s.xy)        
#        print('---------------------------')
#        
#
#        
#with open('../gds/lei_test2.gds', 'rb') as stream:
#    lib = Library.load(stream)
#
#new_lib = Library(5, b'NEWLIB.DB', 1e-9, 0.001)
#struc = lib[1] # libraries and structures are derived from list class
#struc2 = Structure('struc1'.encode())
#new_lib.append(struc)
#new_lib.append(lib[0])
#
#struc[4].angle = 180.0
#
#
#new_lib.append(struc2)
#struc2.append(Boundary(45, 0, [(-1000, -1000), (-1000, 0), (0,0), (0, -1000), (-1000, -1000)]))
#struc2.append(Boundary(46, 0, [(-2000, -2000), (-2000, 0), (0,0), (0, -2000), (-2000, -2000)]))
#s = SRef('struc1'.encode(),[(0,0)])
#
#
#s.strans = 2
#
#
#s.angle = 270.0
#struc.append(s )
#
#with open('../gds/new_lib.gds', 'wb') as stream:
#    new_lib.save(stream)        
#    
#with open('../gds/new_lib.gds', 'rb') as stream:
#    lib = Library.load(stream)
#
#for i in lib[0]:
#    if isinstance(i,SRef):
#        #print(i.struct_name)
#        print(i.xy,i.strans,i.angle)    
#    
#    