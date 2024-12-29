# -*- coding: utf-8 -*-
"""ucgenvoleybol_withzemberek.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10w34jMkgS3A9VYUEzXbvBodrMVeWASPO
"""

import pandas as pd

data = open("/content/output.csv","r", encoding='utf-8').read()
#print(data[:500])

import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import ClassifierI
from statistics import mode
import pickle

!pip install TurkishStemmer
!pip install zemberek-python
from nltk.corpus import stopwords
nltk.download('stopwords')
import random
import re
from TurkishStemmer import TurkishStemmer
from zemberek import (
    TurkishSentenceNormalizer,
    TurkishMorphology,
    TurkishTokenizer,
)

tokenizer = TurkishTokenizer.DEFAULT
turkish_stopwords = stopwords.words("turkish")
stemmer = TurkishStemmer()
morphology = TurkishMorphology.create_with_defaults()
normalizer = TurkishSentenceNormalizer(morphology)

import nltk
import os
nltk.download('punkt_tab')

pattern = r"\s+[^\sa-zA-Z0-9ğüşöçıĞÜŞİÖÇ,]"
document = re.sub(pattern, "", data)
print(document[:100])
lines = document.split("\n")
document = document.replace(lines[0] + '\n', '', 1)
#print(document)

documents = []
all_words = []
for r in document.split("\n"):
  #print(r)
  if "," in r:
    command_part, label = r.rsplit(",", 1)
    #print(command_part, label)
    pattern_new = r"[^\sa-zA-Z0-9ğüşöçıĞÜŞİÖÇ]"
    command_part = re.sub(pattern_new, "", command_part)
    #print(command_part)
    command_part = normalizer.normalize(command_part)
    #print(command_part)
    command_part = command_part.lower()
    documents.append((command_part, label))
    #print(documents)
    tokens = tokenizer.tokenize(command_part)
    words = [
        stemmer.stem(token.content)
        for token in tokens
        if token.content not in turkish_stopwords
    ]
    #print(words)
    all_words.extend(words)
    #print(all_words)
    #break

random.shuffle(documents)

from nltk.probability import FreqDist

all_words = FreqDist(all_words)
print(all_words)
word_features = list(all_words.keys())[:400]
print(word_features)

def find_features(command):

  command = normalizer.normalize(command)
  tokens = tokenizer.tokenize(command)
  words = [
      stemmer.stem(token.content)
      for token in tokens
      if token.content not in turkish_stopwords
  ]
  features = {}

  for w in word_features:
    features[w] = (w in words)

  return features

featuresets = [(find_features(command_part), label) for (command_part, label) in documents]
command_with_label = [(command_part, label) for (command_part, label) in documents]

train_size = int(len(featuresets) * 0.80)
training_test = featuresets[:train_size]
testing_set = featuresets[train_size:]
testing_set_special = command_with_label[train_size:]
classifier = nltk.NaiveBayesClassifier.train(training_test)
classifier.train(training_test)

i = 0
for test_command in testing_set_special:
  testing_state = [testing_set[i]]
  accuracy = (nltk.classify.accuracy(classifier, testing_state)) * 100

  if accuracy < 50:
        print(
            f"command: {test_command[0]} predict label: {classifier.classify(find_features(test_command[0]))}  real label: {test_command[1]}"
        )
  i += 1

new_data_ = "üç kenarlı bir şekil çizer misin."
new_data = word_tokenize(new_data_)

classifier = nltk.NaiveBayesClassifier.train(training_test)
prediction = classifier.classify(find_features(new_data_))
print("Tahmin Sonucu:", prediction)
print("Naive Bayes Algo Accuracy percent: ", (nltk.classify.accuracy(classifier, testing_set))*100)
#classifier.show_most_informative_features(15)

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_test)

prediction = MNB_classifier.classify(find_features(new_data_))
print("Tahmin Sonucu:", prediction)
print("MultinomialNB Algo Accuracy percent: ", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

BernaulliNB_classifier = SklearnClassifier(BernoulliNB())
BernaulliNB_classifier.train(training_test)

prediction = BernaulliNB_classifier.classify(find_features(new_data_))
print("Tahmin Sonucu:", prediction)
print("BernoulliNB Algo Accuracy percent: ", (nltk.classify.accuracy(BernaulliNB_classifier, testing_set))*100)

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_test)

prediction = LinearSVC_classifier.classify(find_features(new_data_))
print("Tahmin Sonucu:", prediction)
print("BernoulliNB Algo Accuracy percent: ", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_test)

prediction = LogisticRegression_classifier.classify(find_features(new_data_))
print("Tahmin Sonucu:", prediction)
print("LogisticRegression Algo Accuracy percent: ", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

SGDClassifier = SklearnClassifier(SGDClassifier())
SGDClassifier.train(training_test)

prediction = SGDClassifier.classify(find_features(new_data_))
print("Tahmin Sonucu:", prediction)
print("SGDClassifier Algo Accuracy percent: ", (nltk.classify.accuracy(SGDClassifier, testing_set))*100)

class VoteClassifier(ClassifierI):
  def __init__(self, *classifiers):
    self.classifiers = classifiers

  def classify(self, features):
    votes = []
    for c in self.classifiers:
      v = c.classify(features)
      votes.append(v)
    return mode(votes)

vote_classifier = VoteClassifier(classifier,
                                  MNB_classifier,
                                  BernaulliNB_classifier,
                                  SGDClassifier,
                                  LinearSVC_classifier,
                                  LogisticRegression_classifier)

prediction = vote_classifier.classify(find_features(new_data_))
print("Tahmin Sonucu:", prediction)
print("vote_classifier accuracy percent:", (nltk.classify.accuracy(vote_classifier, testing_set))*100)