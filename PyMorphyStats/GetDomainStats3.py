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
    errorFiles = 'C:\\Nivc_stats_corpus\\unary_comm'
    statsCorpusDir = 'C:\\Nivc_stats_corpus\\unary_comm\\'
    mainTree = os.walk(errorFiles)
    allStatsFilesComm = []
    allStatsFilesRus = []
    allStatsFilesEng = []
    allStatsComm = Counter()
    allStatsRus = Counter()
    allStatsEng = Counter()
    i = 0
    for d in mainTree:
        for subd in d[1][2:3]:
            newPath = d[0] + "\\" + subd
            subTree = os.walk(newPath)
            i = 1
            for f in subTree:
                for subf in f[2]:
                    filePath = f[0] + "\\" + subf
                    print(subf)
                    if "_Stat" in subf and "_comm" in subf:
                        allStatsFilesComm.append(filePath)
                    if "_Stat" in subf and "_eng" in subf:
                        allStatsFilesEng.append(filePath)
                    if "_Stat" in subf and "_rus" in subf:
                        allStatsFilesRus.append(filePath)
            for file in allStatsFilesComm:
                inputStat = open(file,"r", encoding="utf-8")
                try:
                    content = inputStat.read()
                except Exception as e:
                    print("Error",file)
                    continue
                inputStat.close()
                try:
                    contentDict = json.loads(content)
                except Exception as e:
                    print(file,content)
                for key in contentDict["Frequencies"]:
                    allStatsComm[key] += contentDict["Frequencies"][key]
            for file in allStatsFilesEng:
                inputStat = open(file,"r", encoding="utf-8")
                try:
                    content = inputStat.read()
                except Exception as e:
                    print("Error",file)
                    continue
                inputStat.close()
                try:
                    contentDict = json.loads(content)
                except Exception as e:
                    print(file,content)
                for key in contentDict["Frequencies"]:
                    allStatsEng[key] += contentDict["Frequencies"][key]
            for file in allStatsFilesRus:
                inputStat = open(file,"r", encoding="utf-8")
                try:
                    content = inputStat.read()
                except Exception as e:
                    print("Error",file)
                    continue
                inputStat.close()
                try:
                    contentDict = json.loads(content)
                except Exception as e:
                    print(file,content)
                for key in contentDict["Frequencies"]:
                    allStatsRus[key] += contentDict["Frequencies"][key]

            options = [{"type":"comm","dict": allStatsComm},{"type":"eng","dict":allStatsEng},{"type":"rus","dict":allStatsRus}]

            for opt in options:
                frequencyWords = FindMostCommonElements(opt["dict"])
                bag = [item[0] for item in frequencyWords]
                # Подготовка словарей для записи в файлы
                jsonText = "{\"Domain\": \"" + subd + "\",\"Frequencies\": {"
                for item in frequencyWords:
                    jsonText += "\"" + item[0] + "\":" + str(item[1]) + ","
                jsonText = jsonText[0:-1]
                jsonText += "}}"
                # dictJson = {}
                # dictJson["Domain"] = "all"
                # dictJson["Frequencies"] = frequencyWords

                bagJson = {}
                bagJson["Domain"] = "all"
                bagJson["Frequencies"] = bag

                os.makedirs(statsCorpusDir, mode=0o777, exist_ok=True)
                output = open(statsCorpusDir + "\\" + subd + "_Stat" + "_" + opt["type"] + ".json", "w",
                              encoding="utf-8")
                output.write(jsonText)
                output.close()

                output = open(statsCorpusDir + "\\" + subd + "_Bag" + "_" + opt["type"] + ".json", "w",
                              encoding="utf-8")
                output.write(json.dumps(bagJson,ensure_ascii=False))
                output.close()
            break
        break

if __name__ == "__main__":
    main()