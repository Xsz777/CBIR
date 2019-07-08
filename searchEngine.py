import color_descriptor
import structure_descriptor
import searcher
import cv2

limit = 3


queryImage = cv2.imread("H:/CBIR_python2/nikeset/00001.png")

cv2.namedWindow('Query', 0)
cv2.imshow("Query", queryImage)
cv2.waitKey(0)
cv2.destroyAllWindows()

image = cv2.resize(queryImage, (64,64), interpolation=cv2.INTER_CUBIC)
cv2.imshow("Query1", image)
cv2.waitKey(0)
colorIndexPath = "H:/CBIR_python2/colorindex.csv"
structureIndexPath = "H:/CBIR_python2/structindex.csv"
cannyIndexPath = "H:/CBIR_python2/cannyindex.csv"
resultPath = "H:/CBIR_python/nikeset"


colorDescriptor = color_descriptor.ColorDescriptor((8,12,3))
structureDescriptor = structure_descriptor.StructureDescriptor((64,64))

queryFeatures = colorDescriptor.describe(queryImage)
queryStructures = structureDescriptor.describe(queryImage)
#print(queryFeatures)
#print(queryStructures)

imageSearcher = searcher.Searcher(colorIndexPath, structureIndexPath,cannyIndexPath)
searchResults = imageSearcher.search(queryFeatures, queryStructures)
print(searchResults)
#print("00001，Jordan Supreme Elevation PF, ￥1199")
#print("00002，Air Jordan XXXIII PF , ￥1499")
#print("00008,  Nike Varsity Compute TR 2, ￥669")



for i in range(0, limit):
    re = cv2.imread("H:/CBIR_python2/nikeset" + "/" + searchResults[i][1] + ".png")
    cv2.namedWindow('results', 0)
    cv2.imshow("results", re)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    a = ("H:/CBIR_python2/results" + "/" + searchResults[i][1] + ".png")
    cv2.imwrite(a,re)