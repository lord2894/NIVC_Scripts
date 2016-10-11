import artm
import os
import matplotlib.pyplot as plt

path = 'C:\\NIVC\\Nivc_BigARTM_corpus\\unary_comm\\'
subd = "golosislamacom"
batch_vectorizer = artm.BatchVectorizer(data_path=path + "\\" + subd + "\\" + "batches",
                                            data_format='batches')

modelARTM = artm.ARTM(topic_names=['topic_{}'.format(i) for i in xrange(2)],
                      scores=[artm.PerplexityScore(name='PerplexityScore', use_unigram_document_model=False, dictionary=batch_vectorizer.dictionary),
                              artm.SparsityPhiScore(name='SparsityPhiScore'),
                              #artm.SparsityThetaScore(name='SparsityThetaScore'),
                              #artm.TopicKernelScore(name='TopicKernelScore', probability_mass_threshold=0.3),
                              artm.TopTokensScore(name='TopTokensScore', num_tokens=6)],
                      cache_theta=True)

#modelARTM.regularizers.add(artm.SmoothSparseThetaRegularizer(name='SparseTheta', tau=-0.15))
modelARTM.regularizers.add(artm.SmoothSparsePhiRegularizer(name='SparsePhi', tau=-0.51))
#modelARTM.regularizers.add(artm.DecorrelatorPhiRegularizer(name='DecorrelatorPhi', tau=1.5e+5))

modelARTM.initialize(dictionary=batch_vectorizer.dictionary)

modelARTM.num_document_passes = 1

modelARTM.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes = 1)

print "===========================ARTM PerplexityScore start===================================="
print modelARTM.score_tracker['PerplexityScore'].value
print "===========================ARTM PerplexityScore end======================================"


print 'Sparsity Phi: {0:.3f} (ARTM)'.format(
    modelARTM.score_tracker['SparsityPhiScore'].last_value)

# print 'Sparsity Theta: {0:.3f} (ARTM)'.format(
#     modelARTM.score_tracker['SparsityThetaScore'].last_value)
#
# print 'Kernel contrast: {0:.3f} (ARTM)'.format(
#     modelARTM.score_tracker['TopicKernelScore'].last_average_contrast)
#
# print 'Kernel purity: {0:.3f} (ARTM)'.format(
#     modelARTM.score_tracker['TopicKernelScore'].last_average_purity)

print 'Perplexity: {0:.3f} (ARTM)'.format(
    modelARTM.score_tracker['PerplexityScore'].last_value)


for topic_name in modelARTM.topic_names:
    print topic_name + ': ',
    print modelARTM.score_tracker['TopTokensScore'].last_tokens[topic_name]