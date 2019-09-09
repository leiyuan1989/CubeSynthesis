# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 14:59:32 2019

@author: leiyuan
"""
import pandas as pd

#design rule

class Design_Rule:
    def __init__(self,techname,
                     layer_map_file = '../design_rule/layer_mapping.csv',
                     design_rule_file = '../design_rule/design_rule.csv'):
        self.AA = "AA"
        self.PO = "PO"
        self.SDN = "SDN"
        self.SDP = "SDP"
        self.NW = "NW"
        self.CT = "CT"
        self.M1 = "M1"
        self.V1 = "V1"
        self.M2 = "M2"
        
        self.techname = techname
        self.layer_map = pd.read_csv(layer_map_file)
        self.design_rule = pd.read_csv(design_rule_file)        
        #self.
    
    def _(self,name):
       dr = self.design_rule
       return int(dr[dr.name == name][self.techname].tolist()[0])
    def get_layer_num(self,name):
       lm = self.layer_map
       return str(lm[lm.layer == name][self.techname].tolist()[0])       

    def get_plot_para(self,layer_num):
       lm = self.layer_map
       row = lm[lm[self.techname] == layer_num]
       color = row['color'].tolist()[0]
       hatch = row['hatch'].tolist()[0][1:-1]
       line = row['line'].tolist()[0][1:-1]
       alpha = row['alpha'].tolist()[0]    
       return (color,hatch,line,alpha)
        
dr = Design_Rule('hlmc_55')
#class Rule:
    
    