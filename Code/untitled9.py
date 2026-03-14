import cv2
import numpy as np

# 读取图像
image = cv2.imread(r"C:\Users\DELL\Desktop\road.png")


blurred_image = cv2.blur(image, (5, 5))

# 显示滤波前后的图像
cv2.imshow('Original Image', image)
cv2.imshow('Blurred Image', blurred_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
