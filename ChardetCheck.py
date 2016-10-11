#from chardet.universaldetector import UniversalDetector
import chardet
#detector = UniversalDetector()
inputErr = open("C:\\ErrorFiles.log", 'r', encoding="utf-8")
outputErr = open("C:\\NewErrorFiles.log","w",encoding="utf-8")

for path in inputErr:
    filePath = path.split('|')[0]
    input = open(filePath, 'rb')
    sc = chardet.detect(input.read())
    input.close()
    print(filePath,sc)
    if sc["encoding"] != None:
        outputErr.write(path+"\n")
inputErr.close()
outputErr.close()
    # for line in input:
    #     detector.feed(line)
    #     if detector.done: break
    # detector.close()
    # print(detector.result)
    # print("====")


# import os
# import re
# from string import printable
# from w3lib.html import replace_entities
#
# def clearText(inputTextFile, outputTextFile):
#     input = open(inputTextFile, 'r', encoding="windows-1251")
#     output = open(outputTextFile, 'w', encoding="utf-8")
#     try:
#         text = input.read()
#     except Exception as e:
#         print(e)
#         outputErr = open("C:\\ErrorFiles.log", 'a', encoding="utf-8")
#         outputErr.write(inputTextFile+" | "+outputTextFile+"\n")
#         outputErr.close()
#         return
#     text = replace_entities(text)
#     PUNCTUATION = ''#u'…»«—№’'
#     RU_ALPHABET = u'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
#     final_new_text = re.sub("[^{}]+".format(printable+PUNCTUATION+RU_ALPHABET), "", text)
#     final_new_text = re.sub(r'\s+', ' ', final_new_text)
#     for c in list(PUNCTUATION):
#         final_new_text.replace(c,' '+c+' ')
#     final_new_text.replace(u'\xa0',' ')
#     output.write(final_new_text)
#     output.close()
#     input.close()
#
# def main():
#     baseCorpusDir = 'C:\\Nivc_corpus'
#     clearCorpusDir = 'C:\\Nivc_clear_corpus\\'
#     clearText("C:\\Nivc_corpus\\islamnewsru\\httpwwwislamnewsrugo_socialtopmail","C:\\Nivc_clear_corpus\\islamnewsru\\httpwwwislamnewsrugo_socialtopmail")
#
# if __name__ == "__main__":
#     main()