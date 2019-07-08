import cv2

class StructureDescriptor:
    def __init__(self, dimension):
        #尺寸
        self.dimension = dimension
    def describe(self, image):
        # resize(原图，目标尺寸，插值方法)
        image = cv2.resize(image, self.dimension, interpolation=cv2.INTER_CUBIC)
        return image
