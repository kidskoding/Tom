# -*- encoding: utf-8 -*-

# Grading functions

import pandas as pd
import csv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt 
import cv2
import easyocr
from pylab import rcParams
rcParams['figure.figsize'] = 8,16
reader = easyocr.Reader(['en'])


filename = cv2.imread("agb013_student2.jpeg")
frq_test = cv2.resize(filename,(1748, 2480))
plt.imshow(frq_test)

testid = frq_test[220:340,635:880]
studentid = frq_test[220:340,1230:1550]
    
TestId_ans = reader.readtext(testid)[0][1]
StudentId_ans = reader.readtext(studentid)[0][1]

#answers
q1 = frq_test[720:850,1100:1400]
    #plt.imshow(q1)
q1_res = reader.readtext(q1)[0][1]

q2 = frq_test[1100:1200,1100:1400]
    #plt.imshow(q2)
q2_res = reader.readtext(q2)[0][1]

q3 = frq_test[1400:1550,1100:1400]
    #plt.imshow(q3)
q3_res = reader.readtext(q3)[0][1]

q4 = frq_test[1700:1870,1100:1400]
plt.imshow(q4)
q4_res = reader.readtext(q4)[0][1]
print(q4_res)