# coding=utf-8
import os
import json
from collections import Counter
import copy
import math


def FindMostCommonElements(dictionary ,countWord = None):
        dict = list(dictionary.items())
        dict.sort(key=lambda t: t[0])
        dict.sort(key=lambda t: t[1], reverse=True)
        if countWord != None:
            return dict[0: int(countWord)]
        else:
            return dict

def getContrastCorpus():
    contrastStats = Counter()
    contrastFile = 'C:\\NIVC\\Nivc_contrast_corpus\\contrast_stats_comm.tsv'
    inputStat = open(contrastFile,"r", encoding="windows-1251")
    statLine = inputStat.readline()
    start = True
    while statLine != None and statLine != '':
        if start:
            start = False
            statLine = inputStat.readline()
            continue
        statLine = statLine.split("\t")
        try:
            contrastStats[statLine[0]] = int(statLine[1][:-1])
        except Exception as e:
            print(statLine)
        statLine = inputStat.readline()
    return contrastStats


def main():
    contrastStats = getContrastCorpus()
    errorFiles = 'C:\\NIVC\\Nivc_stats_corpus\\binary_comm'
    statsCorpusDir = 'C:\\NIVC\\Nivc_stats_corpus\\binary_comm\\'
    mainTree = os.walk(errorFiles)
    deleteWords = [ "БЫЛЬ",
                    "ВТОРА",
                    "ИЗА",
                    "ЕЩЕ",
                    "МЕРЯ",
                    "МИРО",
                    "ПРЯ",
                    "ТОГО",
                    "УЖЕ"]
    allStatsFilesRus = []
    allStatsFilesEng = []
    i = 0
    for d in mainTree:
        for subf in d[2]:
            print(subf)
            if "_Stat" in subf and "_rus" in subf:
                allStatsFilesRus.append(statsCorpusDir+subf)
        break
    contentDict = None
    newContentDict = {}
    for file in allStatsFilesRus:
        print(file)
        inputStat = open(file,"r", encoding="utf-8-sig")
        content = inputStat.read()
        inputStat.close()
        try:
            contentDict = json.loads(content)
            newContentDict = copy.deepcopy(contentDict["Frequencies"])
            #contentDict =json.loads(contentDict)
        except Exception as e:
            print(e)
            print(file,content)
        for key in contentDict["Frequencies"]:
            splitedKey = key.split()
            err = False
            for word in splitedKey:
                if word in deleteWords:
                    err = True
                    break
            if err:
                newContentDict.pop(key,None)
        frequencyWords = FindMostCommonElements(newContentDict)
        bag = [item[0] for item in frequencyWords]
        # Подготовка словарей для записи в файлы
        jsonText = "{\"Domain\": \""+contentDict["Domain"]+"\" ,\"Frequencies\": {\n"
        for item in frequencyWords:
            jsonText += "\"" + item[0] + "\": " + str(item[1]) + ",\n"
        jsonText = jsonText[0:-2]
        jsonText += "}}"
        output = open(file, "w", encoding="utf-8")
        output.write(jsonText)
        output.close()


if __name__ == "__main__":
    main()