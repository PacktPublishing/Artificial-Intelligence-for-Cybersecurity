# Chapter 11: Cyber Threat Intelligence
# Code originally created using Google Collab
# Dataset available at: https://github.com/behzadanksu/cybertweets?tab=readme-ov-file#Dataset
# Based on: https://radimrehurek.com/gensim/auto_examples/tutorials/run_lda.html#sphx-glr-auto-examples-tutorials-run-lda-py

import bson

tweets_text = []

with open('tweets.bson', 'rb') as f:
    content = f.read()
    base = 0
    while base < len(content):
        base, d = bson.decode_document(content, base)
        tweets_text.append(d['text'])

[print(t) for i,t in enumerate(tweets_text) if i<10]

from gensim import models, corpora

from collections import defaultdict

import nltk

nltk.download()

from nltk.corpus import stopwords
s=set(stopwords.words('english'))

# remove common words
stop_words_list = set('for a of the and to in is you are I this that - = \\ ... | '.split())
# split text document
text_documents = [
    [word for word in document.lower().split() if word not in s]
    for document in tweets_text
]

text_documents = [
    [word for word in document if word not in stop_words_list]
    for document in text_documents
]

# only keep words that appear more than once
frequency = defaultdict(int)
for text in text_documents:
    for token in text:
        frequency[token] += 1

texts = [
    [token for token in text if frequency[token] > 1]
    for text in text_documents
]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

num_topics=3

model = models.LdaModel(corpus, id2word=dictionary, num_topics=num_topics)

model.print_topics(num_topics)

print(tweets_text[0])
model[corpus][0]

print(tweets_text[1])
model[corpus][1]

print(tweets_text[11])
model[corpus][11]

print(tweets_text[3])
model[corpus][3]

print(tweets_text[4])
model[corpus][4]

import pyLDAvis
import pyLDAvis.gensim_models

pyLDAvis.enable_notebook()
pyLDAvis.gensim_models.prepare(model, corpus, dictionary)

num_documents = len(tweets_text)

import numpy as np

features_list = []
for d in range(num_documents):
  features= [model[corpus][d][i][1] for i in range(num_topics)]
  features_list.append(features)

features_stacked = np.vstack(features_list)

features_stacked.shape

from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.005, min_samples=20)

predictions = dbscan.fit_predict(features_stacked)

predictions

max(predictions)

from matplotlib import pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(features_stacked[0:100,0], features_stacked[0:100,1], features_stacked[0:100,2], c=features_stacked[0:100,2], cmap='viridis')

