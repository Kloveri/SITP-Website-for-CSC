# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 20:22:34 2025

@author: DELL
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
h_lower,h_upper = 35,104
s_lower,s_upper = 15,255
v_lower,v_upper = 15,255
zone_we_have = 22
for num in range(22,zone_we_have + 1):
    url = r"C:\Users\DELL\Desktop\Green\Zone" + str(num) + ".png"
    image = cv2.imread(url)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([h_lower, s_lower, v_lower])
    upper_green = np.array([h_upper, s_upper, v_upper])
    mask = cv2.inRange(hsv_image, lower_green, upper_green)
    green_p = cv2.bitwise_and(image, image, mask=mask)
    green_part = cv2.cvtColor(green_p, cv2.COLOR_BGR2HSV)
    #green_part = green_p
    '''cv2.imshow('Image', green_part)
    cv2.waitKey()
    cv2.destroyAllWindows()
    '''
    url_new = r"C:\Users\DELL\Desktop\Green\Zone" + str(num) + "_New.png"
    cv2.imwrite(url_new, green_part)

    height = green_part.shape[0]
    length = green_part.shape[1]
    green = 0
    total = 0
    def Valid(h,s,v):
        if h_lower <= h <= h_upper:
            if s_lower <= s <= s_upper:
                if v_lower <= v <= v_upper:
                    return True
        else: return False
    for i in range(0,height):
        for j in range(0,length):
            h,s,v= green_part[i,j]
            if  Valid(h,s,v):
                green += 1
            h1,s1,v1 = image[i,j]
            if not (h1,s1,v1) == (255,255,255):
                total += 1
    with open(r"C:\Users\DELL\Desktop\Green\Green_Ratio.doc","a") as f:
        f.write("ratio_green of Zone")
        f.write(str(num))
        f.write(":")
        f.write(str(green/total))
        f.write("\n")
    print(total)
    print(green)
    print("ratio_green: ", green/total)
