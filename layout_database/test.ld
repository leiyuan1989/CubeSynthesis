@LayoutDatabase
layout new_NAND
I1 [(335, 6290)] [p25,0,0]
I2 [(335, 290)] [n25,0,0]
I3 [T,(CommonSD,I1,r)] [p25,0,0]
I4 [T,(CommonSD,I3,r)] [p25,0,0]
I5 [T,(CommonSD,I2,r)] [n25,0,0]
I6 [T,(CommonSD,I5,r)] [n25,0,0]
I7 [T,(CommonCentre,I2,u)] [M1_PO,0,0]
I8 [T,(CommonCentre,I5,u)] [M1_PO,0,0]
I9 [T,(CommonCentre,I6,u)] [M1_PO,0,0]
I10 [T,(CommonCentre,I1,d)] [M1_PO,0,0]
I11 [T,(CommonCentre,I3,d)] [M1_PO,0,0]
I12 [T,(CommonCentre,I4,d)] [M1_PO,0,0]
P1 [(-220, -520), (2250, -520)] [1000,101,1]
P2 [(-220, 8100), (2250, 8100)] [1000,101,1]

P3 [T,(CommonCentre,I3,d)] [1000,101,1]
P4 [T,(CommonCentre,I4,d)] [1000,101,1]
P5 [T,(CommonCentre,I3,d)] [1000,101,1]
P6 [T,(CommonCentre,I4,d)] [1000,101,1]
P7 [T,(CommonCentre,I3,d)] [1000,101,1]
P8 [T,(CommonCentre,I4,d)] [1000,101,1]#strait line

P8 [T,(CommonCentre,I4,d)] [1000,101,1]#z line
P8 [T,(CommonCentre,I4,d)] [1000,101,1]#strait line

endlayout
