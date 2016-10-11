# -*- coding: utf-8 -*-
import os
import json
from collections import Counter
import math


def FindMostCommonElements(dictionary ,countWord = None):
        dict = list(dictionary.items())
        dict.sort(key=lambda t: t[0])
        dict.sort(key=lambda t: t[1][1], reverse=True)
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
    errorFiles = 'C:\\NIVC\\Nivc_stats_corpus\\unary_comm'
    statsCorpusDir = 'C:\\NIVC\\Nivc_stats_corpus\\unary_comm\\'
    mainTree = os.walk(errorFiles)
    allStatsFilesComm = []
    allStatsFilesRus = []
    allStatsFilesEng = []
    i = 0
    for d in mainTree:
        for subf in d[2]:
            print(subf)
            if "_Stat" in subf and "_comm" in subf:
                allStatsFilesComm.append(statsCorpusDir+subf)
            if "_Stat" in subf and "_eng" in subf:
                allStatsFilesEng.append(statsCorpusDir+subf)
            if "_Stat" in subf and "_rus" in subf:
                allStatsFilesRus.append(statsCorpusDir+subf)
        break
    contentDict = None
    for file in allStatsFilesRus:
        inputStat = open(file,"r", encoding="utf-8-sig")
        content = inputStat.read()
        inputStat.close()
        try:
            contentDict = json.loads(content)
            #contentDict =json.loads(contentDict)
        except Exception as e:
            print(e)
            print(file,content)
        for key in contentDict["Frequencies"]:
            tf = 10
            if key in contrastStats:
                tf = contrastStats[key]
            print(key,tf)
            contentDict["Frequencies"][key] = [contentDict["Frequencies"][key],contentDict["Frequencies"][key]*math.log10(1000000.0/tf)]
        frequencyWords = FindMostCommonElements(contentDict["Frequencies"])
        bag = [item[0] for item in frequencyWords]
        # Подготовка словарей для записи в файлы
        jsonText = "{\"Domain\": \"all\",\"Frequencies\": {"
        for item in frequencyWords:
            jsonText += "\"" + item[0] + "\": " + str(item[1]) + ",\n"
        jsonText = jsonText[0:-1]
        jsonText += "}}"
        output = open(file, "w", encoding="utf-8")
        output.write(jsonText)
        output.close()

    for file in allStatsFilesRus:
        inputStat = open(file,"r", encoding="utf-8-sig")
        content = inputStat.read()
        inputStat.close()
        try:
            contentDict = json.loads(content)
            #contentDict = json.loads(contentDict)
        except Exception as e:
            print(e)
            print(file,content)
        newFileNameSplited = file.replace(statsCorpusDir,"").split("_")[1:]
        newFileName = '_'.join(newFileNameSplited)
        frequencyWords = FindMostCommonElements(contentDict["Frequencies"])
        #Подготовка словарей для записи в файлы
        jsonText = "{\"Domain\": \""+newFileNameSplited[0]+"\",\"Frequencies\": {"
        for item in frequencyWords:
            if (item[1] >= 100):
                jsonText += "\"" + item[0]+"\":"+str(item[1])+","
        jsonText = jsonText[0:-1]
        jsonText += "}}"

        output = open(file, "w", encoding="utf-8")
        output.write(jsonText)
        output.close()


if __name__ == "__main__":
    main()