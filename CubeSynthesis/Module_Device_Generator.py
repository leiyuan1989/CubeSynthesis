# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 14:41:10 2019

@author: leiyuan
"""

import Design_Function as F


class Rect(object):
    def __init__(self,rect,layer):    
        self._layer = layer
        self._l = rect[0]
        self._r = rect[1]
        self._u = rect[2]
        self._d = rect[3]
        self._ll = (self._l,self._d)
        self._rect_w = abs(self._l - self._r)                     
        self._rect_h = abs(self._u - self._d) 
        self._rect = rect          
        self._c = (0.5*(self._l + self._r), 0.5*(self._d + self._u))
    def _Renew(self,rect):    
        self._l = rect[0]
        self._r = rect[1]
        self._u = rect[2]
        self._d = rect[3]
        self._ll = (self._l,self._d)
        self._rect_w = abs(self._l - self._r)                     
        self._rect_h = abs(self._u - self._d) 
        self._rect = rect   
        self._c = (0.5*(self._l + self._r), 0.5*(self._d + self._u))        
    def _Copy(self):
        return Rect(self._rect)
    def _Intersects(self, other):
        return F.rect_intersects(self._rect,other._rect) 
    def _Move(self,delta_x,delta_y):
        new_rect = [self._l + delta_x,self._r + delta_x,
                    self._u + delta_y,self._d + delta_y]
        self._Renew(new_rect)
        
        
        
class Mosfet:
    def __init__(self,name,loc,l,fw,nf,mtype = 'N',dr = Design_Rule):
        self.name = name
        self.loc = loc
        self.l = l
        self.fw = fw
        self.nf = nf
        self.mtype = mtype
        
       
        AA_Left_Rect = [self.loc[0] - dr.CT_s_GT - dr.CT_w - dr.AA_enc_CT,
                        self.loc[0],
                        self.loc[1] + self.fw,
                        self.loc[1]]
        self.AA_Left = Rect(AA_Left_Rect,'AA')
        
        self.GT = []
        self.AA = []
        self.GT_Top = []
        self.GT_Bottom = []
        
        temp_loc = self.loc
        for n in range(nf):
            left = temp_loc[0] 
            bottom = temp_loc[1]
            right = left + self.l
            top = bottom + self.fw
            
            GT_Rect = Rect([left,right,top,bottom],"GT")
            
            
            
        dr.POLY_ext_AA
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        