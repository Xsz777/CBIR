import cv2
import glob


for imagePath in glob.glob("H:/CBIR_python2/nikeset/*.png"):
    img = cv2.imread(imagePath)
    #彩色
    blurred = cv2.GaussianBlur(img, (3, 3), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
    edge_output = cv2.Canny(gray,50,150)
    dst = cv2.bitwise_and(img, img, mask= edge_output)

    a = imagePath[23:29]
    b = ("H:/CBIR_python2/canny" + "/" + a + ".png")
    c = ("H:/CBIR_python2/canny_black" + "/" + a + ".png")
    #黑白
    cv2.imwrite(c,cv2.Canny(img, 200, 300))
    cv2.imwrite(b,dst)
