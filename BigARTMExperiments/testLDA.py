import artm
import os
import matplotlib.pyplot as plt

path = 'C:\\NIVC\\Nivc_BigARTM_corpus\\unary_comm\\'
subd = "golosislamacom"
batch_vectorizer = artm.BatchVectorizer(data_path=path + "\\" + subd + "\\" + "batches",
                                            data_format='batches')

lda = artm.LDA(num_topics=15, alpha=0.2, beta=0.02,
               num_document_passes=5, dictionary=batch_vectorizer.dictionary,
               cache_theta=True)

lda.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=10)

print lda.sparsity_phi_last_value
print lda.sparsity_theta_last_value
print lda.perplexity_value

top_tokens = lda.get_top_tokens(num_tokens=10)
for i, token_list in enumerate(top_tokens):
    print 'Topic #{0}: {1}'.format(i, token_list)

print lda.phi_
print lda.get_theta()