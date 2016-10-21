import io
import json

def FindMostCommonElements(dictionary ,countWord = None):
        dict = list(dictionary.items())
        dict.sort(key=lambda t: t[0])
        dict.sort(key=lambda t: t[1], reverse=True)
        if countWord != None:
            return dict[0: int(countWord)]
        else:
            return dict

path = 'C:\\NIVC\\Nivc_BigARTM_corpus\\unary_comm\\'
subd = "islamcivilru"
content = ""
with io.open(path+subd+"\\ARTM_topics"+'\\100.topics','r', encoding='utf-8') as inputStat:
    try:
        content = inputStat.read()
    except Exception as e:
        print("Error",e)
    inputStat.close()
contentDict = {}
try:
    contentDict = json.loads(content)
except Exception as e:
    print(content)

with io.open(path+subd+"\\ARTM_topics"+'\\100.topics','w',encoding='utf8') as outputTopics:
    try:
        outputTopics.write(u'{\n')
        j = 0
        topic_names = [key for key in contentDict]
        topic_names.sort()
        for topic_name in topic_names:
            wordStats = FindMostCommonElements(contentDict[topic_name])
            #print topic_name + "\n"
            outputTopics.write(u"\""+unicode(topic_name + u'\": '))
            outputTopics.write(u"{")
            i = 0
            for word in wordStats:
                #print word + "\n"
                outputTopics.write(u"\""+unicode(word[0])+u"\": "+unicode(str(word[1])))
                if i != len(wordStats):
                    outputTopics.write(u",\n")
                i += 1
            outputTopics.write(u"}")
            if j != len(topic_names)-1:
                outputTopics.write(u",\n")
            j += 1
        outputTopics.write(u"\n}")
    except Exception as e:
        print(e)
    outputTopics.close()