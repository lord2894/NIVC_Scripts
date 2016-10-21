import artm
import os
import matplotlib.pyplot as plt

path = 'C:\\NIVC\\Nivc_BigARTM_corpus\\unary_comm\\'
subd = "golosislamacom"
batch_vectorizer = artm.BatchVectorizer(data_path=path + "\\" + subd + "\\" + "batches_pos",
                                            data_format='batches')

modelPLSA = artm.ARTM(topic_names=['topic_{}'.format(i) for i in xrange(100)],
                      scores=[artm.PerplexityScore(name='PerplexityScore', use_unigram_document_model=False,
                                                   dictionary=batch_vectorizer.dictionary, class_ids=["text"]),
                              artm.SparsityPhiScore(name='SparsityPhiScore', class_id="text"),
                              artm.SparsityThetaScore(name='SparsityThetaScore'),
                              artm.TopicKernelScore(name='TopicKernelScore', probability_mass_threshold=0.3, class_id="text"),
                              artm.TopTokensScore(name='TopTokensScore', num_tokens=100, class_id="text")],
                      cache_theta=True)

modelPLSA.initialize(dictionary=batch_vectorizer.dictionary)

modelPLSA.num_document_passes = 5

modelPLSA.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes = 30)

print "===========================PLSA PerplexityScore start===================================="
print modelPLSA.score_tracker['PerplexityScore'].value
print "===========================PLSA PerplexityScore end======================================"


print 'Sparsity Phi: {0:.3f} (PLSA) '.format(
    modelPLSA.score_tracker['SparsityPhiScore'].last_value)

print 'Sparsity Theta: {0:.3f} (PLSA)'.format(
    modelPLSA.score_tracker['SparsityThetaScore'].last_value)

print 'Kernel contrast: {0:.3f} (PLSA)'.format(
    modelPLSA.score_tracker['TopicKernelScore'].last_average_contrast)

print 'Kernel purity: {0:.3f} (PLSA)'.format(
    modelPLSA.score_tracker['TopicKernelScore'].last_average_purity)

print 'Perplexity: {0:.3f} (PLSA)'.format(
    modelPLSA.score_tracker['PerplexityScore'].last_value)


import os
if not os.path.exists(path+subd+"\\PLSA_model"):
    os.makedirs(path+subd+"\\PLSA_model", mode=0o777)
if not os.path.exists(path+subd+"\\PLSA_topics"):
    os.makedirs(path+subd+"\\PLSA_topics", mode=0o777)


print "======save PLSA========"
modelPLSA.save(filename=path+subd+"\\PLSA_model\\"+subd+".model")

print "======save PLSA topics========"
import io
with io.open(path+subd+"\\PLSA_topics"+'\\20.topics','w',encoding='utf8') as outputTopics:
    try:
        outputTopics.write(u'{\n')
        j = 0
        for topic_name in modelPLSA.topic_names:
            print topic_name + "\n"
            outputTopics.write(unicode(topic_name + ': '))
            outputTopics.write(u"[")
            i = 0
            for word in modelPLSA.score_tracker['TopTokensScore'].last_tokens[topic_name]:
                #print word + "\n"
                outputTopics.write(unicode(word))
                if i != len(modelPLSA.score_tracker['TopTokensScore'].last_tokens[topic_name])-1:
                    outputTopics.write(u",")
                i += 1
            outputTopics.write(u"]")
            if j != len(modelPLSA.topic_names)-1:
                outputTopics.write(u",\n")
            j += 1
        outputTopics.write(u"\n}")
    except Exception as e:
        print(e)
    outputTopics.close()
