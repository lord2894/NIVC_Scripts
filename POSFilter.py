import os
import json
import pymorphy2

errorFiles = 'C:\\NIVC\\Nivc_stats_corpus\\unary_comm\\all_Stat_rus.json'
mainTree = os.walk(errorFiles)

def FindMostCommonElements(dictionary ,countWord = None):
        dict = list(dictionary.items())
        dict.sort(key=lambda t: t[0])
        dict.sort(key=lambda t: t[1][1], reverse=True)
        if countWord != None:
            return dict[0: int(countWord)]
        else:
            return dict

contentDict = {}

inputStat = open(errorFiles, "r", encoding="utf-8-sig")
content = inputStat.read()
inputStat.close()
try:
    contentDict = json.loads(content)
    #contentDict = json.loads(contentDict)
except Exception as e:
    print(e)
    print(content)

frequencyWords = FindMostCommonElements(contentDict["Frequencies"])

# Подготовка словарей для записи в файлы
morph = pymorphy2.MorphAnalyzer()
POSOpt = ["NOUN",	#имя существительное	хомяк
"ADJF",	#имя прилагательное (полное)	хороший
"ADJS",	#имя прилагательное (краткое)	хорош
"VERB",	#глагол (личная форма)	говорю, говорит, говорил
"INFN",	#глагол (инфинитив)	говорить, сказать
"PRTF",	#причастие (полное)	прочитавший, прочитанная
"PRTS"] #причастие (краткое)	прочитана
jsonText = "{\"Domain\": \"all\",\"Frequencies\": {"
for item in frequencyWords:
    p = morph.parse(item[0])[0]
    keyPos = p.tag.POS
    if keyPos in POSOpt:
        jsonText += "\"" + item[0] + " | " + keyPos + "\": " + str(item[1]) + ",\n"
jsonText = jsonText[0:-1]
jsonText += "}}"
output = open('C:\\NIVC\\Nivc_stats_corpus\\unary_comm\\all_POS_Stat_rus.json' , "w", encoding="utf-8")
output.write(jsonText)
output.close()
