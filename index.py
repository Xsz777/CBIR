import color_descriptor
import structure_descriptor
import glob
import cv2


#色彩特征
colorDesriptor = color_descriptor.ColorDescriptor((8, 12, 3))

output = open("H:/CBIR_python2/colorindex.csv","w")
for imagePath in glob.glob("H:/CBIR_python2/nikeset/*.png"):
    #文件名字
    imageName = imagePath[24:29]
    image = cv2.imread(imagePath)
    features = colorDesriptor.describe(image)
    #读入特征
    features = [str(feature).replace("\n", "") for feature in features]
    output.write("%s,%s\n" % (imageName, ",".join(features)))

output.close()

#空间构图特征
structureDescriptor = structure_descriptor.StructureDescriptor((64, 64))

output = open("H:/CBIR_python2/structindex.csv","w")

for imagePath in glob.glob("H:/CBIR_python2/nikeset/*.png"):
    #读取文件名字
    imageName = imagePath[24:29]
    image = cv2.imread(imagePath)
    structures = structureDescriptor.describe(image)
    structures = [str(structure).replace("\n", "") for structure in structures]
    output.write("%s,%s\n" % (imageName, ",".join(structures)))

output.close()

output = open("H:/CBIR_python2/cannyindex.csv","w")
for imagePath in glob.glob("H:/CBIR_python2/canny/*.png"):
    #文件名字
    imageName = imagePath[22:27]
    #print(imageName)
    image = cv2.imread(imagePath)
    features = colorDesriptor.describe(image)
    #读入特征
    features = [str(feature).replace("\n", "") for feature in features]
    output.write("%s,%s\n" % (imageName, ",".join(features)))

output.close()

