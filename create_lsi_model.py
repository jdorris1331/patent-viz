from gensim import corpora, models, similarities


dictionary = corpora.Dictionary.load('patents.dict')
corpus = corpora.MmCorpus('patents.mm')
#tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
#corpus_tfidf = tfidf[corpus]
#tfidf.save('model.tfidf')

#lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
#corpus_lsi = lsi[corpus_tfidf]
#lsi.save('model.lsi')
#lsi.print_topics(300)

tfidf = models.TfidfModel.load("model.tfidf") # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel.load("model.lsi")
corpus_lsi = lsi[corpus_tfidf]
index = similarities.MatrixSimilarity(lsi[corpus])
index.save('patents.index')
