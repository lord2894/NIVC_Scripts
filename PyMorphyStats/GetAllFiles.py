import os
import json

errorFiles = 'C:\\NIVC\\Nivc_stats_corpus\\binary_comm\\islamcivilru'
mainTree = os.walk(errorFiles)

listFile = "C:\\ListFile.txt"
output = open(listFile , "w", encoding="utf-8")
contentDict = {}
counter = 0
for d in mainTree:
    for subf in d[2]:
        print(subf)
        if "_Stat" in subf and "_rus" in subf:
            inputStat = open(errorFiles+"\\"+subf,"r", encoding="utf-8-sig")
            content = inputStat.read()
            inputStat.close()
            try:
                contentDict = json.loads(content)
                #contentDict = json.loads(contentDict)
            except Exception as e:
                print(e)
                print(errorFiles+"\\"+subf,content)
            if "ПЛОХОЕ ЛЮДОЕДСТВО | A N" in contentDict["Frequencies"]:
                output.write(contentDict["Source"]+'\t ПЛОХОЕ ЛЮДОЕДСТВО | A N \t'+str(contentDict["Frequencies"]["ПЛОХОЕ ЛЮДОЕДСТВО | A N"])+"\n")
                counter += 1

output.write("Document count: "+str(counter)+"\n")
output.close()