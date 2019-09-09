# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 16:34:33 2019

@author: leiyuan
"""

from Module_Layout_Generator import Module_Layout_Generator as Module_LG
from Module_Layout_Generator import Gen_Layout_Database,Compile_Layout_Database 
import Module_Device_Generator as Module_DG

from Design_Rule import Design_Rule as DR

from Layout_Viewer import layout_viewer 

#main

dr = DR('hlmc_55')

n1 = Module_DG.Mosfet('n1',(0,0),280,1000,dr)
n1.gen_Layout_Dataset()

Gen_Layout_Database(n1.dict,'../layout_database/')

f = layout_viewer('../layout_database','M1_PO.ld',dr)
f = layout_viewer('../layout_database','p25.ld',dr)
f = layout_viewer('../layout_database','3to1_NAND.ld',dr)


c = Compile_Layout_Database('../layout_database','test.ld',dr)

f = layout_viewer('../layout_database','test_c.ld',dr)