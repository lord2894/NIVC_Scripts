import artm
import os
import matplotlib.pyplot as plt

def processPath(path, subd):
    batch_vectorizer = artm.BatchVectorizer(data_path=path + "\\" + subd + "\\" + "batches",
                                            data_format='batches')
    # if not os.path.isfile('kos/dictionary.dict'):
    #     dictionary.gather(data_path=batch_vectorizer.data_path)
    #     dictionary.save(dictionary_path='kos/dictionary.dict')
    # dictionary = artm.Dictionary()
    # dictionary.gather(data_path='my_collection_batches')
    if not os.path.exists(path + "\\" + subd + "\\" + "dictionary"):
        os.makedirs(path + "\\" + subd + "\\" + "dictionary", mode=0o777)
    batch_vectorizer.dictionary.save(dictionary_path=path + "\\" + subd + "\\" + "dictionary\\dictionary.dict")
    batch_vectorizer.dictionary.save_text(dictionary_path=path + "\\" + subd + "\\" + "dictionary\\dictionary.txt")

def getDictionaries(path):
    mainTree = os.walk(path)
    for d in mainTree:
        for subd in d[1][0:6]:
            processPath(path, subd)

def getTopics(path,subd):
    batch_vectorizer = artm.BatchVectorizer(data_path=path + "\\" + subd + "\\" + "batches",
                                            data_format='batches')
    model = artm.ARTM(num_topics=20, dictionary=batch_vectorizer.dictionary)
    model.scores.add(artm.PerplexityScore(name='PerplexityScore',
                                      use_unigram_document_model=False,
                                      dictionary=batch_vectorizer.dictionary))
    model.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=10)
    print "===========================PerplexityScore start===================================="
    print model.score_tracker['PerplexityScore'].value
    print "===========================PerplexityScore end======================================"
    plt.plot(xrange(model.num_phi_updates), model.score_tracker['PerplexityScore'].value, 'b--')
    plt.xlabel('Iterations count')
    plt.ylabel('PLSA perp. (blue), ARTM perp. (red)')
    plt.grid(True)
    plt.show()
    for topic_name in model.topic_names:
        print topic_name + ': ',
        print model.score_tracker['PerplexityScore'].last_tokens[topic_name]

def main():
    BigARTMCorpusDir = 'C:\\NIVC\\Nivc_BigARTM_corpus\\unary_comm\\'
    # getDictionaries(BigARTMCorpusDir)
    mainTree = os.walk(BigARTMCorpusDir)
    for d in mainTree:
        for subd in d[1][0:1]:
            getTopics(BigARTMCorpusDir,subd)

if __name__ == "__main__":
    main()
