import os

def main():
    errorFiles = 'C:\\Nivc_stats_corpus'
    baseCorpusDir = 'C:\\Nivc_corpus'
    clearCorpusDir = 'C:\\Nivc_clear_corpus\\'
    mainTree = os.walk(errorFiles)
    for d in mainTree:
        for subf in d[2]:
            errorFilePath = d[0]+"\\"+subf
            input = open(errorFilePath,"r", encoding="utf-8")
            for file in input:
                normalErrorFilePath = file.replace("\\","\\\\")
                normalErrorFilePath = normalErrorFilePath.replace("\\\\\\\\","\\\\")
                normalErrorFilePath = normalErrorFilePath.replace("\\\\","\\")
                #os.remove(normalErrorFilePath[:-1])
                print(normalErrorFilePath)
            input.close()

if __name__ == "__main__":
    main()