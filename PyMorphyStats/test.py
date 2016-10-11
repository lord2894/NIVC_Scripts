# -*- coding: utf-8 -*-
from nltk.tokenize import TweetTokenizer
from PyMorphyStats import FrequencyDict
import json
import os
import operator

import unicodedata

def main():
    options = [{"type":"eng","language":["eng"], "dict": FrequencyDict("C:\\WordNet\\dict", 'C:\\PymorphyDicts')},
                {"type":"rus","language":["rus"], "dict": FrequencyDict("C:\\WordNet\\dict", "C:\\PymorphyDicts")},
                {"type":"comm","language":["eng","rus"], "dict": FrequencyDict("C:\\WordNet\\dict", "C:\\PymorphyDicts")}]

    clearCorpusDir = 'C:\\Nivc_clear_corpus\\'
    statsCorpusDir = 'C:\\Nivc_stats_corpus\\unary_comm\\'
    stastsErr = open("C:\\Nivc_stats_corpus\\StatsErr.log","a", encoding="utf-8")
    mainTree = os.walk(clearCorpusDir)
    count = 1
    domain = 1
    for d in mainTree:
        for subd in d[1]:
            newPath = d[0]+"\\"+subd
            subTree = os.walk(newPath)
            i = 1
            print("domain: ", domain)

            for f in subTree:
                for subf in f[2]:
                    if subf != "httpgolosislamacomnewsphpid10724":
                        continue
                    filePath = f[0]+"\\"+subf
                    input = open(filePath,"r",encoding="utf-8")
                    try:
                        text = input.read()
                    except Exception as e:
                        stastsErr.write(filePath + "\n")
                        continue
                    input.close()
                    #Включаем документ в общую статистику + Получаем статистику по конкретному тексту
                    for opt in options:
                        try:
                            frequencyWords = opt["dict"].ParseTweet(text, opt["language"])
                        except Exception as e:
                            stastsErr.write(filePath+"\n")
                            break

                        if opt["type"] == "comm" and len(frequencyWords) == 0:
                            stastsErr.write(filePath + "\n")
                            break
                        bag = [item[0] for item in frequencyWords]
                        #frequencyWords = {a:b for a,b in frequencyWords}#dict(frequencyWords)
                        #frequencyWords = dict(frequencyWords)


                        #Подготовка словарей для записи в файлы
                        jsonText = "{\"Domain\": \""+subd+"\",\"Source\": \""+subf+"\", \"Frequencies\": {"
                        for item in frequencyWords:
                            jsonText += "\"" + item[0]+"\":"+str(item[1])+","
                        jsonText = jsonText[0:-1]
                        jsonText += "}}"
                        # dictJson = {}
                        # dictJson["Domain"] = subd
                        # dictJson["Source"] = subf
                        # dictJson["Frequencies"] = frequencyWords

                        bagJson = {}
                        bagJson["Domain"] = subd
                        bagJson["Source"] = subf
                        bagJson["Frequencies"] = bag

                        os.makedirs(statsCorpusDir+subd, mode=0o777, exist_ok=True)
                        output = open(statsCorpusDir+subd+"\\"+str(i)+"_Stat"+"_"+opt["type"]+".json", "w", encoding="utf-8")
                        #jsonText = json.dumps(dictJson,ensure_ascii=False)
                        output.write(jsonText)
                        output.close()

                        output = open(statsCorpusDir+subd+"\\"+str(i)+"_Bag"+"_"+opt["type"]+".json", "w", encoding="utf-8")
                        jsonText = json.dumps(bagJson,ensure_ascii=False)
                        output.write(jsonText)
                        output.close()
                    print(i)
                    i+=1
                    count += 1
            for opt in options:
                frequencyWords = opt["dict"].FindMostCommonElementsDomain()
                bag = [item[0] for item in frequencyWords]
                #Подготовка словарей для записи в файлы
                jsonText = "{\"Domain\": \""+subd+"\", \"Frequencies\": {"
                for item in frequencyWords:
                    jsonText += "\"" + item[0]+"\":"+str(item[1])+","
                jsonText = jsonText[0:-1]
                jsonText += "}}"
                # dictJson = {}
                # dictJson["Domain"] = subd
                # dictJson["Frequencies"] = frequencyWords

                bagJson = {}
                bagJson["Domain"] = subd
                bagJson["Frequencies"] = bag

                os.makedirs(statsCorpusDir, mode=0o777, exist_ok=True)
                output =  open(statsCorpusDir+"\\"+subd+"_Stat"+"_"+opt["type"]+".json", "w", encoding="utf-8")
                output.write(jsonText)
                output.close()

                output =  open(statsCorpusDir+"\\"+subd+"_Bag"+"_"+opt["type"]+".json", "w", encoding="utf-8")
                output.write(json.dumps(bagJson))
                output.close()
    for opt in options:
        frequencyWords = opt["dict"].FindMostCommonElements()
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
        output =  open(statsCorpusDir+"\\"+"all_Stat"+"_"+opt["type"]+".json", "w", encoding="utf-8")
        output.write(json.dumps(jsonText))
        output.close()

        output =  open(statsCorpusDir+"\\"+"all_Bag"+"_"+opt["type"]+".json", "w", encoding="utf-8")
        output.write(json.dumps(bagJson))
        output.close()
    stastsErr.close()
    print("Documets count: ",count)


if __name__ == "__main__":
    main()