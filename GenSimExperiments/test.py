# # -*- coding: utf-8 -*-
#
# from gensim import corpora
# import os
# import pymorphy2
# import io
# import json
#
# POSOpt = ["NOUN",	#имя существительное	хомяк
#     "ADJF",	#имя прилагательное (полное)	хороший
#     "ADJS",	#имя прилагательное (краткое)	хорош
#     "VERB",	#глагол (личная форма)	говорю, говорит, говорил
#     "INFN",	#глагол (инфинитив)	говорить, сказать
#     "PRTF",	#причастие (полное)	прочитавший, прочитанная
#     "PRTS"] #причастие (краткое)	прочитана
#
# morph = pymorphy2.MorphAnalyzer()
#
# def POSFilter(word):
#     p = morph.parse(word)
#     keyPos = p[0].tag.POS
#     if keyPos in POSOpt:
#         return True;
#     return False
#
# dictionary = corpora.Dictionary.load('C:\\NIVC\\Nivc_GenSim_corpus\\unary_comm\\islamcivilru\\mm_pos\\islamcivilru.dict')
# print(dictionary)
# statsCorpusDir = 'C:\\NIVC\\Nivc_stats_corpus\\unary_comm'
# BigARTMCorpusDir = 'C:\\NIVC\\Nivc_GenSim_corpus\\unary_comm\\'
# mainTree = os.walk(statsCorpusDir)
# allStatsFilesRus = []
# texts = []
# corpus = []
# for d in mainTree:
#     for subd in d[1][2:3]:
#         i = 0
#         corpus = [dictionary.doc2bow(text) for text in texts]
#         mainTree = os.walk(statsCorpusDir)
#         for file in allStatsFilesRus:
#             content = ""
#             contentDict = {}
#             with io.open(file[0], 'r', encoding='utf8') as inputStat:
#                 try:
#                     content = inputStat.read()
#                 except Exception as e:
#                     print("Error",file)
#                     continue
#                 inputStat.close()
#             try:
#                 contentDict = json.loads(content)
#             except Exception as e:
#                 print(file,content)
#             for key in contentDict["Frequencies"]:
#                 if (unicode(key) != unicode("") and unicode(key) != unicode(" ")) and POSFilter(key):
#                     id =  dictionary.token2id[unicode(key)]
#                     corpus[i][id] = contentDict["Frequencies"][key]
#      corpora.MmCorpus.serialize(BigARTMCorpusDir+subd+"\\"+"mm_pos\\"+subd+'.mm', corpus)