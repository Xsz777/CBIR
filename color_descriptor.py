import cv2
import numpy

class ColorDescriptor:
    #属性bin
    def __init__(self, bins):
        self.bins = bins
    #颜色特征对比用的卡方函数（比较离散概率）
    #比较两个直方图。可选的eps值用来预防除零错误。
    #histA 特征库   histB待检测图片
    def getHistogram(self, image, mask, isCenter):
        imageHistogram = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])
        imageHistogram = cv2.normalize(imageHistogram, imageHistogram).flatten()
        #添加中心权重
        if isCenter:
            weight = 5.0
            for index in range(len(imageHistogram)):
                imageHistogram[index] *= weight
        return imageHistogram
    def describe(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []
        #长宽中心
        height, width = image.shape[0], image.shape[1]
        centerX, centerY = int(width * 0.5), int(height * 0.5)
        #为每个需要提取特征的区域构建掩模
        segments = [(0, centerX, 0, centerY), (0, centerX, centerY, height), (centerX, width, 0, centerY), (centerX, width, centerY, height)]
        #中心区域
        axesX, axesY = int(width * 0.75) / 2, int (height * 0.75) / 2
        ellipseMask = numpy.zeros([height, width], dtype="uint8")
        #绘制中心椭圆
        cv2.ellipse(ellipseMask, (int(centerX), int(centerY)), (int(axesX), int(axesY)), 0, 0, 360, 255, -1)
        #五个区域依次提取颜色直方图
        for startX, endX, startY, endY in segments:
            cornerMask = numpy.zeros([height, width], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipseMask)
            #卡方
            imageHistogram = self.getHistogram(image, cornerMask, False)
            features.append(imageHistogram)
        # 中心区域
        imageHistogram = self.getHistogram(image, ellipseMask, True)
        features.append(imageHistogram)
        return features