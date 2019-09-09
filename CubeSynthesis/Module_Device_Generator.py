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
        self._boundary = [(self._l,self._d),(self._r,self._d),
                          (self._r,self._u),(self._l,self._u),(self._l,self._d)]         
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
        self._boundary = [(self._l,self._d),(self._r,self._d),
                          (self._r,self._u),(self._l,self._u),(self._l,self._d)]                
        self._c = (0.5*(self._l + self._r), 0.5*(self._d + self._u))        
    def _Copy(self):
        return Rect(self._rect)
    def _Intersects(self, other):
        return F.rect_intersects(self._rect,other._rect) 
    def _Move(self,delta_x,delta_y):
        new_rect = [self._l + delta_x,self._r + delta_x,
                    self._u + delta_y,self._d + delta_y]
        self._Renew(new_rect)
        
        
        
class Mosfet:#single gate: this is a demo device, and it need to add finger number function
    def __init__(self,name,loc,l,fw,dr,nf = 1,mtype = 'N'):
        self.name = name
        self.loc = loc
        self.l = l
        self.fw = fw
        self.nf = nf
        self.mtype = mtype
        self.dr = dr
       
        self.gen_mos()
        
       
        
    def gen_mos(self):
        dr = self.dr    
        AA_Left_Rect = [self.loc[0] - dr._('CT_s_GT') - dr._('CT_w') - dr._('AA_enc_CT'),
                        self.loc[0],
                        self.loc[1] + self.fw,
                        self.loc[1]]
        AA_Right_Rect = [self.loc[0]  + self.l,
                        self.loc[0] + self.l + dr._('CT_s_GT') + dr._('CT_w') + dr._('AA_enc_CT'),
                        self.loc[1] + self.fw,
                        self.loc[1]]        
        
        PO_Rect = [self.loc[0],self.loc[0] + self.l, 
                   self.loc[1] + self.fw,self.loc[1]]
        
        self.CT_Left_Rect = [self.loc[0] - dr._('CT_s_GT') - dr._('CT_w'),
                        self.loc[0] - dr._('CT_s_GT'),
                        self.loc[1] + self.fw,
                        self.loc[1]]
        self.CT_Right_Rect = [self.loc[0]  + self.l + dr._('CT_s_GT'),
                        self.loc[0] + self.l + dr._('CT_s_GT') + dr._('CT_w'),
                        self.loc[1] + self.fw,
                        self.loc[1]]        
        
        CT_Left =  self.gen_Via(self.CT_Left_Rect,dr._('CT_w'),dr._('CT_s'),dr._('AA_enc_CT'),axis = 1)
        CT_Right =  self.gen_Via(self.CT_Right_Rect,dr._('CT_w'),dr._('CT_s'),dr._('AA_enc_CT'),axis = 1)        
        
        self.AA_Left = Rect(AA_Left_Rect,dr.AA)
        self.AA_Right = Rect(AA_Right_Rect,dr.AA)        
        self.PO = Rect(PO_Rect,dr.PO)
        self.AA = Rect(PO_Rect,dr.AA)        
        
        self.CT_Left = []
        for rect in CT_Left:
            self.CT_Left.append(Rect(rect,dr.CT))
        self.CT_Right = []
        for rect in CT_Right:
            self.CT_Right.append(Rect(rect,dr.CT))         

     
    def gen_Via(self,V_rect,V_w,V_s,Rect_ext_V,axis = 1): #need add axis = 0(horization direction)    
        l,r,t,d = V_rect
        Vias = []
        if (r-l) == V_w:#width of V_rect equal to V_w
            t1 = t - d - 2*Rect_ext_V - V_w
            n_V = int(t1/float(V_w + V_s))
            merge = (t1 - n_V*(V_w + V_s))/2
            
            t_t = t - Rect_ext_V - merge
            for i in range(n_V + 1):
                Vias.append([l,r,t_t,t_t-V_w])
                t_t = t_t - V_w - V_s
        else:
            print('V_rect error')
        return Vias
    def gen_Layout_Dataset(self):
        self.dict = {}
        self.dict['name'] = self.name
        self.dict['db'] = []
        self.dict['db'].append(self.gen_line_rect(self.AA_Left))
        self.dict['db'].append(self.gen_line_rect(self.AA_Right))
        self.dict['db'].append(self.gen_line_rect(self.PO))
        self.dict['db'].append(self.gen_line_rect(self.AA))
        
        for rect in self.CT_Left:
            self.dict['db'].append(self.gen_line_rect(rect))            
        for rect in self.CT_Right:
            self.dict['db'].append(self.gen_line_rect(rect))          
       
        
    def gen_line_rect(self,rect):
        line = 'B ' + str(rect._boundary)+ ' [' + self.dr.get_layer_num(rect._layer) + ']\n'
        return line

        
    def gen_I_rect(self,name):
        line = 'I [' + str(self.loc)+ '] [' + name + ',0,0]\n'
        return line        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        