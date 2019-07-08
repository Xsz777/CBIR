import numpy
import csv
import re


class Searcher:
    def __init__(self, colorIndexPath, structureIndexPath,cannyIndexPath):
        self.colorIndexPath, self.structureIndexPath ,self.cannyIndexPath= colorIndexPath, structureIndexPath, cannyIndexPath
    #计算卡方
    def solveColorDistance(self, features, queryFeatures, eps = 1e-5):
        distance = 0.5 * numpy.sum([((a - b) ** 2) / (a + b + eps) for a, b in zip(features, queryFeatures)])
        return distance
    #空间特征相似度
    def solveStructureDistance(self, structures, queryStructures, eps = 1e-5):
        distance = 0
        normalizeRatio = 5e3#正则化
        for index in range(len(queryStructures)):
            for subIndex in range(len(queryStructures[index])):
                a = structures[index][subIndex]
                b = queryStructures[index][subIndex]
                distance += (a - b) ** 2 / (a + b + eps)
        return distance / normalizeRatio
    #颜色特征寻找
    def searchByColor(self, queryFeatures):
        searchResults = {}
        with open(self.colorIndexPath) as indexFile:
            reader = csv.reader(indexFile)
            for line in reader:
                features = []
                for feature in line[1:]:
                    feature = feature.replace("[", "").replace("]", "")
                    findStartPosition = 0
                    feature = re.split("\s+", feature)
                    rmlist = []
                    for index, strValue in enumerate(feature):
                        if strValue == "":
                            rmlist.append(index)
                    for _ in range(len(rmlist)):
                        currentIndex = rmlist[-1]
                        rmlist.pop()
                        del feature[currentIndex]
                    feature = [float(eachValue) for eachValue in feature]
                    features.append(feature)
                distance = self.solveColorDistance(features, queryFeatures)
                searchResults[line[0]] = distance
            indexFile.close()

        return searchResults
    def searchByCanny(self, queryFeatures):
        cannyResults = {}
        with open(self.cannyIndexPath) as indexFile:
            reader = csv.reader(indexFile)
            for line in reader:
                features = []
                for feature in line[1:]:
                    feature = feature.replace("[", "").replace("]", "")
                    findStartPosition = 0
                    feature = re.split("\s+", feature)
                    rmlist = []
                    for index, strValue in enumerate(feature):
                        if strValue == "":
                            rmlist.append(index)
                    for _ in range(len(rmlist)):
                        currentIndex = rmlist[-1]
                        rmlist.pop()
                        del feature[currentIndex]
                    feature = [float(eachValue) for eachValue in feature]
                    features.append(feature)
                distance = self.solveColorDistance(features, queryFeatures)
                cannyResults[line[0]] = distance
            indexFile.close()

        return cannyResults
    #将未处理的query图像矩阵转为用于匹配的特征向量形式
    def transformRawQuery(self, rawQueryStructures):
        queryStructures = []
        for substructure in rawQueryStructures:
            structure = []
            for line in substructure:
                for tripleColor in line:
                    structure.append(float(tripleColor))
            queryStructures.append(structure)
        return queryStructures

    # 空间特征寻找
    def searchByStructure(self, rawQueryStructures):
        searchResults = {}
        queryStructures = self.transformRawQuery(rawQueryStructures)
        #print(queryStructures)
        with open(self.structureIndexPath) as indexFile:
            reader = csv.reader(indexFile)
            for line in reader:
                structures = []
                for structure in line[1:]:
                    structure = structure.replace("[", "").replace("]", "")
                    structure = re.split("\s+", structure)
                    if structure[0] == "":
                        structure = structure[1:]
                    structure = [float(eachValue) for eachValue in structure]
                    structures.append(structure)
                distance = self.solveStructureDistance(structures, queryStructures)
                searchResults[line[0]] = distance
            indexFile.close()
        #print(searchResults)
        return searchResults

    #两种评价汇总得到最终结果
    def search(self, queryFeatures, rawQueryStructures, limit = 3):
        structweight = 0.1
        cannyweight = 0.1
        featureweight = 0.5
        featureResults = self.searchByColor(queryFeatures)
        structureResults = self.searchByStructure(rawQueryStructures)
        cannyResults = self.searchByCanny(queryFeatures)
        results = {}
        for key, value in featureResults.items():
            results[key] = featureweight * value + structweight * structureResults[key] + cannyweight * cannyResults[key]
        #results = sorted(results.items(), key = lambda item: item[1], reverse = False)
        results = sorted([(v, k) for (k, v) in results.items()])
        return results[ : limit]