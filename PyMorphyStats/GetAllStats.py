import os
import json
from collections import Counter


def FindMostCommonElements(dictionary ,countWord = None):
        dict = list(dictionary.items())
        dict.sort(key=lambda t: t[0])
        dict.sort(key=lambda t: t[1], reverse=True)
        if countWord != None:
            return dict[0: int(countWord)]
        else:
            return dict

def main():
    errorFiles = 'C:\\Nivc_stats_corpus\\binary_comm'
    statsCorpusDir = 'C:\\Nivc_stats_corpus\\binary_comm\\'
    mainTree = os.walk(errorFiles)
    allStatsFilesComm = []
    allStatsFilesRus = []
    allStatsFilesEng = []
    allStatsComm = Counter()
    allStatsRus = Counter()
    allStatsEng = Counter()
    i = 0
    for d in mainTree:
        for subf in d[2]:
            print(subf)
            if "_Stat" in subf and "_comm" in subf:
                allStatsFilesComm.append(errorFiles+"\\"+subf)
            if "_Stat" in subf and "_eng" in subf:
                allStatsFilesEng.append(errorFiles+"\\"+subf)
            if "_Stat" in subf and "_rus" in subf:
                allStatsFilesRus.append(errorFiles+"\\"+subf)
        break
    contentDict = None
    for file in allStatsFilesComm:
        inputStat = open(file,"r", encoding="utf-8")
        content = inputStat.read()
        inputStat.close()
        try:
            contentDict = json.loads(content)
            contentDict =json.loads(contentDict)
        except Exception as e:
            print(file,content)
        for key in contentDict["Frequencies"]:
            allStatsComm[key] += contentDict["Frequencies"][key]
    for file in allStatsFilesEng:
        inputStat = open(file,"r", encoding="utf-8")
        content = inputStat.read()
        inputStat.close()
        try:
            contentDict = json.loads(content)
            contentDict = json.loads(contentDict)
        except Exception as e:
            print(file,content)
        for key in contentDict["Frequencies"]:
            allStatsEng[key] += contentDict["Frequencies"][key]
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
        for key in contentDict["Frequencies"]:
            allStatsRus[key] += contentDict["Frequencies"][key]

    options = [{"type":"comm","dict": allStatsComm},{"type":"eng","dict":allStatsEng},{"type":"rus","dict":allStatsRus}]

    for opt in options:
        frequencyWords = FindMostCommonElements(opt["dict"])
        bag = [item[0] for item in frequencyWords]
        #Подготовка словарей для записи в файлы
        jsonText = "{\"Domain\": \"all\",\"Frequencies\": {"
        for item in frequencyWords:
            jsonText += "\"" + item[0]+"\":"+str(item[1])+","
        jsonText = jsonText[0:-1]
        jsonText += "}}"
        # dictJson = {}
        # dictJson["Domain"] = "all"
        # dictJson["Frequencies"] = frequencyWords

        bagJson = {}
        bagJson["Domain"] = "all"
        bagJson["Frequencies"] = bag

        os.makedirs(statsCorpusDir, mode=0o777, exist_ok=True)
        output =  open(statsCorpusDir+"\\"+"full_all_Stat"+"_"+opt["type"]+".json", "w", encoding="utf-8")
        output.write(jsonText)
        output.close()

        output =  open(statsCorpusDir+"\\"+"full_all_Bag"+"_"+opt["type"]+".json", "w", encoding="utf-8")
        output.write(json.dumps(bagJson, ensure_ascii=False))
        output.close()

if __name__ == "__main__":
    main()