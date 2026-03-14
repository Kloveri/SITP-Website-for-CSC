import cv2
image = cv2.imread(r"C:\Users\DELL\Desktop\Zone1.png")
b,g,r=cv2.split(image)
cive = 0.441*r -0.811*g +0.415*b +18.78745
gray = cive.astype("uint8")
ret , th =cv2.threshold(gray, 0, 1, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
B=b*th
G=g*th
R=r*th
image_new = cv2.merge([B,G,R])
cv2.imshow('Image', image_new)
cv2.waitKey()
cv2.destroyAllWindows()
cv2.imwrite(r"C:\Users\DELL\Desktop\Zone1_New.png", image_new)
