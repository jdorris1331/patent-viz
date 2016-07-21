from gensim import corpora, models, similarities


dictionary = corpora.Dictionary.load('patents20k.dict')
corpus = corpora.MmCorpus('patents20k.mm')
tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus]
#tfidf.save('model.tfidf')

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
corpus_lsi = lsi[corpus_tfidf]
#lsi.save('model.lsi')
#lsi.print_topics(300)

