# -*- coding: utf-8 -*-
#  coding=utf-8
import re
import os
from collections import Counter
from Lemmatizer import Lemmatizer
import pymorphy2
from nltk.tokenize import TweetTokenizer
import xlwt as xlwt
from nltk.corpus import stopwords
class FrequencyDict:
    def __init__(self, pathToWordNetDict, pathToPymprphyDict):

        # Определяем регулярное выражение для поиска английских слов
        #self.wordPatternEng = re.compile(u"^((?:[a-zA-Z]+)(?:[-']([?:[a-zA-Z]+))*)$")
        #self.wordPatternRus = re.compile(u"^((?:[а-яА-яЁё]+)(?:[-]([?:[а-яА-яЁё]+))*)$")
        # Частотный словарь(использум класс collections.Counter для поддержки подсчёта уникальных элементов в последовательностях)
        self.frequencyDict = Counter()
        self.frequencyDictDomain = Counter()
        self.RuLemmatizer = pymorphy2.MorphAnalyzer()#RuLemmatizer = get_morph(pathToPymprphyDict)
        self.EngLemmatizer = Lemmatizer(pathToWordNetDict)
        self.tokenizer = TweetTokenizer(reduce_len=True, preserve_case=True)

    def wordPatternEng(self, word):
        engLetter = re.compile(u"([a-zA-Z])")
        q = False
        start = True
        i = 1
        end = len(word)
        for letter in word:
            if start:
                if not engLetter.match(letter):
                    return False
                else:
                    start = False
                    continue
            if not (engLetter.match(letter) or letter in ["-", "'"]):
                return False
            if letter == "'" and q:
                return False
            elif letter == "'":
                q = True
            if i == end and letter in ["-","'"]:
                return False
            i+=1
        return True

    def wordPatternRus(self, word):
        rusLetter = re.compile(u"([а-яА-яЁё])")
        start = True
        i = 1
        end = len(word)
        for letter in word:
            if start:
                if not rusLetter.match(letter):
                    return False
                else:
                    start = False
                    continue
            if not (rusLetter.match(letter) or letter == "-"):
                return False
            if i == end and letter == "-":
                return False
            i+=1
        return True

     # Метод находит в строке слова согласно своим правилам и затем добавляет в частотный словарь
    def FindWordsFromContent(self, content, language):
        frequencyDictText = Counter()
        PUNCTUATION = [u';', u':', u',', u'.',
               u'!', u'?', u'...', u'…',
               u'»', u'«', u'\\', u'-',
               u'{', u'..', u'|', u'—',
               u'&', u'*', u'@', u'#',
               u'^', u'(', u')', u'_'
               u'/', u'%', u'$', u'№',
               u'\'', u'\"', u'~', u'[',
               u']', u'+', u'=', u'’',
               u'>', u'<', u'a', u'the', u'в']
        tokens = self.tokenizer.tokenize(content)
        stopwords_eng = set(stopwords.words('english'))
        stopwords_rus = set(stopwords.words('russian'))
        #tokens = [token for token in tokens if not [pun for pun in PUNCTUATION if pun == token]]
        tokens = [token for token in tokens if (not token in PUNCTUATION) and (not token in stopwords_eng) and (not token in stopwords_rus)]
        if "eng" in language:
            result = [token for token in tokens if self.wordPatternEng(token)]
            # result = []
            # i = 1
            # for token in tokens:
            #     print(i, token)
            #     if self.wordPatternEng.match(token):
            #         result.append(token)
            #     i+=1
            #result = self.wordPatternEng.findall(content)  # В строке найдем список английских слов
            for word in result:
                word = word.upper()#.lower()#.encode('utf-8')  # Приводим слово к нижнему регистру
                lemma = self.EngLemmatizer.GetLemma(word).upper() 	# Нормализуем слово
                if (lemma != ""):
                    self.frequencyDict[lemma] += 1		# Добавляем в счетчик частотного словаря нормализованное слово
                    frequencyDictText[lemma] += 1
                    self.frequencyDictDomain[lemma] += 1
                else:
                    self.frequencyDict[word] += 1		# Добавляем в счетчик частотного словаря не нормализованное слово
                    frequencyDictText[word] += 1
                    self.frequencyDictDomain[lemma] += 1
        if "rus" in language:
            #result = self.wordPatternRus.findall(content)  # В строке найдем список английских слов
            result = [token for token in tokens if self.wordPatternRus(token)]
            for word in result:
                word = word.upper()#.encode('utf-8')  # Приводим слово к нижнему регистру
                lemma = list(self.RuLemmatizer.normal_forms(word))[0].upper()#.encode("utf-8") 	# Нормализуем слово
                if (lemma != ""):
                    self.frequencyDict[lemma] += 1		# Добавляем в счетчик частотного словаря нормализованное слово
                    frequencyDictText[lemma] += 1
                else:
                    self.frequencyDict[word] += 1		# Добавляем в счетчик частотного словаря не нормализованное слово
                    frequencyDictText[lemma] += 1
        dict = list(frequencyDictText.items())
        dict.sort(key=lambda t: t[0])
        dict.sort(key=lambda t: t[1], reverse=True)
        return dict

    # Метод парсит файл в формате txt
    def ParseTweet(self, tweetText, language):
        try:
            return self.FindWordsFromContent(tweetText, language)  # Для каждой строки вызываем обработчик контента
        except Exception as e:
            print(e)

    # Метод отдает первые countWord слов частотного словаря, отсортированные по ключу и значению
    def FindMostCommonElements(self, countWord = None):
        dict = list(self.frequencyDict.items())
        dict.sort(key=lambda t: t[0])
        dict.sort(key=lambda t: t[1], reverse=True)
        if countWord != None:
            return dict[0: int(countWord)]
        else:
            return dict

    def FindMostCommonElementsDomain(self, countWord = None):
        dict = list(self.frequencyDictDomain.items())
        dict.sort(key=lambda t: t[0])
        dict.sort(key=lambda t: t[1], reverse=True)
        if countWord != None:
            return dict[0: int(countWord)]
        else:
            return dict

    def ClearDomainFrequencies(self):
        self.frequencyDictDomain = Counter()


    def SaveResultToExcel(self, language):
        try:
            # if not os.path.exists("C:\\"):
            #     raise Exception('No such directory: "%s"' % self.pathResult)
            dict = list(self.frequencyDict.items())
            dict.sort(key=lambda t: t[0])
            dict.sort(key=lambda t: t[1], reverse=True)
            if dict:
                description = "MostPopular"+language
                style = xlwt.easyxf('font: name Times New Roman')
                wb = xlwt.Workbook()
                ws = wb.add_sheet(description)
                nRow = 0
                for item in dict:
                    ws.write(nRow, 0, item[0].decode("utf-8"), style)
                    ws.write(nRow, 1, item[1], style)
                    nRow += 1
                wb.save(os.path.join("C:\\", description + '.xls'))
        except Exception as e:
            print(e)

    def GetSpecifiedWords(self, text, countWords=0):
        tokens = self.tokenizer.tokenize(text)
        lemmas = []
        result = [token for token in tokens if self.wordPatternEng(token)]
        for word in result:
            word = word.lower()  # Приводим слово к нижнему регистру
            lemma = self.EngLemmatizer.GetLemma(word).upper() 	# Нормализуем слово
            if (lemma != ""):
                lemmas.append(lemma)
            else:
                lemmas.append(word)
        #result = self.wordPatternRus.findall(content)  # В строке найдем список английских слов
        result = [token for token in tokens if self.wordPatternRus(token)]
        for word in result:
            word = word.upper()  # Приводим слово к нижнему регистру
            lemma = list(self.RuLemmatizer.normal_forms(word))[0].upper() 	# Нормализуем слово
            if (lemma != ""):
                lemmas.append(lemma)
            else:
                lemmas.append(word)
        if countWords == 0:
            specifiedWords = [lemma for lemma in lemmas if lemma in self.frequencyDict.keys()]
        else:
            dict = list(self.frequencyDict.items())
            dict.sort(key=lambda t: t[0])
            dict.sort(key=lambda t: t[1], reverse=True)
            dict = dict[0: int(countWords)]
            dict = [dict_item[0] for dict_item in dict]
            specifiedWords = [lemma for lemma in lemmas if lemma in dict]
        return list(set(specifiedWords))