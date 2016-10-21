# -*- coding: utf-8 -*-
import os
import io
import json
import pymorphy2
from gensim import corpora
from collections import Counter


statsCorpusDir = 'C:\\NIVC\\Nivc_stats_corpus\\binary_comm'
BigARTMCorpusDir = 'C:\\NIVC\\Nivc_GenSim_corpus\\binary_comm\\'
mainTree = os.walk(statsCorpusDir)
allStatsFilesRus = []
texts = []
i = 0

err = False
for d in mainTree:
    deleteWords = [ u"БЫЛЬ",
                    u"ВТОРА",
                    u"ИЗА",
                    u"ЕЩЕ",
                    u"МЕРЯ",
                    u"МИРО",
                    u"ПРЯ",
                    u"ТОГО",
                    u"УЖЕ"]
    for subd in d[1][1:5]:
        corpus = []
        dictionary = corpora.Dictionary()
        print(subd)
        newPath = d[0] + "\\" + subd
        subTree = os.walk(newPath)
        i = 1
        for f in subTree:
            for subf in f[2]:
                filePath = f[0] + "\\" + subf
                #print(subf)
                if "_Stat" in subf and "_rus" in subf:
                    allStatsFilesRus.append([filePath,subf])

        if not os.path.exists(BigARTMCorpusDir+subd+"\\"+"mm_pos"):
            os.makedirs(BigARTMCorpusDir+subd+"\\"+"mm_pos", mode=0o777)

        for file in allStatsFilesRus:
            content = ""
            contentDict = {}
            with io.open(file[0],'r',encoding='utf-8-sig') as inputStat:
                try:
                    content = inputStat.read()
                except Exception as e:
                    print("Error",file)
                    continue
                inputStat.close()
            try:
                contentDict = json.loads(content)
            except Exception as e:
                print e
                print(file,content)
            textWords = [unicode(key) for key in contentDict["Frequencies"] if (unicode(key) != unicode("") and unicode(key) != unicode(" "))]
            newBow = dictionary.doc2bow(textWords,True)
            for key in textWords:
                splitedKey = key.split()
                errWord = False
                for word in splitedKey:
                    if word in deleteWords:
                        errWord = True
                    break
                if not errWord:
                    id = dictionary.token2id[unicode(key)]
                    ind = [i for i, x in enumerate(newBow) if isinstance(x, tuple) and x[0] == id]
                    if ind != []:
                        newBowList = list(newBow[ind[0]])
                        newBowList[1] = contentDict["Frequencies"][key]
                        newBow[ind[0]] = tuple(newBowList)
                    else:
                        err = True
                        print "Error"
                        break

            if err: break
            corpus.append(newBow)
        if err:
            print subd
            break
        dictionary.save(BigARTMCorpusDir+subd+"\\"+"mm_pos\\"+subd+".dict")
        corpora.MmCorpus.serialize(BigARTMCorpusDir+subd+"\\"+"mm_pos\\"+subd+'.mm', corpus)