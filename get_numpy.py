from gensim import corpora, models, similarities
import numpy as np
import gensim 


dictionary = corpora.Dictionary.load('patents.dict')
corpus = corpora.MmCorpus('patents.mm')
tfidf = models.TfidfModel.load("model.tfidf") # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel.load("model.lsi")
corpus_lsi = lsi[corpus_tfidf]
numpy_matrix = gensim.matutils.corpus2dense(corpus_lsi, 300) 
