# -*- coding: utf-8 -*-
import os
import io
import json
import artm
import pymorphy2
from collections import Counter

POSOpt = ["NOUN",	#имя существительное	хомяк
    "ADJF",	#имя прилагательное (полное)	хороший
    "ADJS",	#имя прилагательное (краткое)	хорош
    "VERB",	#глагол (личная форма)	говорю, говорит, говорил
    "INFN",	#глагол (инфинитив)	говорить, сказать
    "PRTF",	#причастие (полное)	прочитавший, прочитанная
    "PRTS"] #причастие (краткое)	прочитана

morph = pymorphy2.MorphAnalyzer()

def POSFilter(word):
    p = morph.parse(word)
    keyPos = p[0].tag.POS
    if keyPos in POSOpt:
        return True;
    return False

def main():
    statsCorpusDir = 'C:\\NIVC\\Nivc_stats_corpus\\unary_comm'
    BigARTMCorpusDir = 'C:\\NIVC\\Nivc_BigARTM_corpus\\unary_comm\\'
    mainTree = os.walk(statsCorpusDir)
    allStatsFilesRus = []
    i = 0
    for d in mainTree:
        for subd in d[1][1:6]:
            print(subd)
            newPath = d[0] + "\\" + subd
            subTree = os.walk(newPath)
            i = 1
            for f in subTree:
                for subf in f[2]:
                    filePath = f[0] + "\\" + subf
                    print(subf)
                    if "_Stat" in subf and "_rus" in subf:
                        allStatsFilesRus.append([filePath,subf])

            if not os.path.exists(BigARTMCorpusDir+subd+"\\"+"vowpal_wabbit_pos"):
                os.makedirs(BigARTMCorpusDir+subd+"\\"+"vowpal_wabbit_pos", mode=0o777)
            if not os.path.exists(BigARTMCorpusDir+subd+"\\"+"batches_pos"):
                os.makedirs(BigARTMCorpusDir+subd+"\\"+"batches_pos", mode=0o777)
            with io.open(BigARTMCorpusDir+subd+"\\"+"vowpal_wabbit_pos\\"+"stats.vwwbbbt",'w',encoding='utf8') as output:
                #i = 1
                for file in allStatsFilesRus:
                    content = ""
                    output.write(unicode(file[1] + " |text "))
                    with io.open(file[0],'r',encoding='utf8') as inputStat:
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
                    vowpalWabbitStr = ""
                    # if i == 17009:
                    #     print "here"
                    for key in contentDict["Frequencies"]:
                        if (unicode(key) != unicode("") and unicode(key) != unicode(" ")):
                            if POSFilter(key):
                                output.write(unicode(key + ":"+str(contentDict["Frequencies"][key])+" "))
                    output.write(unicode("\n"))
                    #print(i)
                    #i+=1
                output.close()
            batch_vectorizer = artm.BatchVectorizer(data_path=BigARTMCorpusDir+subd+"\\"+"vowpal_wabbit_pos\\"+"stats.vwwbbbt",
                                                    data_format='vowpal_wabbit',
                                                    target_folder=BigARTMCorpusDir+subd+"\\"+"batches_pos")

        break

if __name__ == "__main__":
    main()