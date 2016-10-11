# -*- coding: utf-8 -*-
import os
import re
from string import printable
from w3lib.html import replace_entities
import chardet
import sys


def clearText(inputTextFile, outputTextFile,outputErr):
    input = open(inputTextFile, 'rb')
    sc = chardet.detect(input.read())
    input.close()
    #print(inputTextFile,sc)
    # if sc["encoding"] != None:
    #     outputErr.write(path+"\n")
    if sc["encoding"] != None and sc["confidence"] > 0.5:
        input = open(inputTextFile, 'r', encoding=sc["encoding"])
        output = open(outputTextFile, 'w', encoding="utf-8")
        try:
            text = input.read()
        except Exception as e:
            print(e)
            outputErr = open("C:\\ErrorFiles.log", 'a', encoding="utf-8")
            outputErr.write(inputTextFile+" | "+outputTextFile+"\n")
            outputErr.close()
            return
        text = replace_entities(text)
        PUNCTUATION = ''#u'…»«—№’'
        RU_ALPHABET = u'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        final_new_text = re.sub("[^{}]+".format(printable+PUNCTUATION+RU_ALPHABET), "", text)
        final_new_text = re.sub(r'\s+', ' ', final_new_text)
        for c in list(PUNCTUATION):
            final_new_text.replace(c,' '+c+' ')
        final_new_text.replace(u'\xa0',' ')
        output.write(final_new_text)
        output.close()
        input.close()
    else:
        outputErr.write(inputTextFile+"\n")
def main(domain):
    outputErr = open("C:\\NewErrorFiles.log","w",encoding="utf-8")
    baseCorpusDir = 'C:\\Nivc_corpus'
    clearCorpusDir = 'C:\\Nivc_clear_corpus\\'
    mainTree = os.walk(baseCorpusDir)
    for d in mainTree:
        for subd in d[1][domain:domain+1]:
            if subd in ["islamnewsru","rosmuslimru"]:
                continue
            newPath = d[0]+"\\"+subd
            subTree = os.walk(newPath)
            for f in subTree:
                for subf in f[2]:
                    filePath = f[0]+"\\"+subf
                    outputFilePath = clearCorpusDir+subd+"\\"+subf
                    os.makedirs(clearCorpusDir+subd, mode=0o777, exist_ok=True)
                    clearText(filePath,outputFilePath,outputErr)
    outputErr.close()

if __name__ == "__main__":
    main(int(sys.argv[1]))
