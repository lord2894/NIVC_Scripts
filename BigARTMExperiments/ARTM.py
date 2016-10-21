import artm
import os
import matplotlib.pyplot as plt
import io

path = 'C:\\NIVC\\Nivc_BigARTM_corpus\\unary_comm\\'
subd = "golosislamacom"
batch_vectorizer = artm.BatchVectorizer(data_path=path + "\\" + subd + "\\" + "batches_pos",
                                            data_format='batches')

modelARTM = artm.ARTM(topic_names=['topic_{}'.format(i) for i in xrange(100)],
                      scores=[artm.PerplexityScore(name='PerplexityScore', use_unigram_document_model=False,
                                                   dictionary=batch_vectorizer.dictionary, class_ids=["text"]),
                              artm.SparsityPhiScore(name='SparsityPhiScore', class_id="text"),
                              artm.SparsityThetaScore(name='SparsityThetaScore'),
                              artm.TopicKernelScore(name='TopicKernelScore', probability_mass_threshold=0.3, class_id="text"),
                              artm.TopTokensScore(name='TopTokensScore', num_tokens=100, class_id="text")],
                      cache_theta=True)

modelARTM.regularizers.add(artm.SmoothSparseThetaRegularizer(name='SparseTheta', tau=-0.2))
modelARTM.regularizers.add(artm.SmoothSparsePhiRegularizer(name='SparsePhi', tau=-0.2,class_ids=["text"]))
modelARTM.regularizers.add(artm.DecorrelatorPhiRegularizer(name='DecorrelatorPhi', tau=2.5e+5, class_ids=["text"]))

modelARTM.initialize(dictionary=batch_vectorizer.dictionary)

modelARTM.num_document_passes = 3

modelARTM.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes = 30)


print "===========================ARTM PerplexityScore start===================================="
print modelARTM.score_tracker['PerplexityScore'].value
print "===========================ARTM PerplexityScore end======================================"
print "===========================PLSA PerplexityScore start===================================="


print 'Sparsity Phi: {0:.3f} (ARTM)'.format(
    modelARTM.score_tracker['SparsityPhiScore'].last_value)

print 'Sparsity Theta: {0:.3f} (ARTM)'.format(
    modelARTM.score_tracker['SparsityThetaScore'].last_value)

print 'Kernel contrast: {0:.3f} (ARTM)'.format(
    modelARTM.score_tracker['TopicKernelScore'].last_average_contrast)

print 'Kernel purity: {0:.3f} (ARTM)'.format(
    modelARTM.score_tracker['TopicKernelScore'].last_average_purity)

print 'Perplexity: {0:.3f} (ARTM)'.format(
    modelARTM.score_tracker['PerplexityScore'].last_value)


import os
if not os.path.exists(path+subd+"\\ARTM_model"):
    os.makedirs(path+subd+"\\ARTM_model", mode=0o777)
if not os.path.exists(path+subd+"\\ARTM_topics"):
    os.makedirs(path+subd+"\\ARTM_topics", mode=0o777)


print "======save ARTM========"
modelARTM.save(filename=path+subd+"\\ARTM_model\\"+subd+".model")

print "======save ARTM topics========"
with io.open(path+subd+"\\ARTM_topics"+'\\20.topics','w',encoding='utf8') as outputTopics:
    try:
        outputTopics.write(u'{\n')
        j = 0
        for topic_name in modelARTM.topic_names:
            print topic_name + "\n"
            outputTopics.write(unicode(topic_name + ': '))
            outputTopics.write(u"[")
            i = 0
            lenTopic = len(modelARTM.score_tracker['TopTokensScore'].last_tokens[topic_name])-1
            topicWords = modelARTM.score_tracker['TopTokensScore'].last_tokens[topic_name]
            for word in topicWords:
                #print word + "\n"
                outputTopics.write(unicode(word))
                if i != lenTopic:
                    outputTopics.write(u",")
                i += 1
            outputTopics.write(u"]")
            if j != len(modelARTM.topic_names)-1:
                outputTopics.write(u",\n")
            j += 1
        outputTopics.write(u"\n}")
    except Exception as e:
        print(e)
    outputTopics.close()