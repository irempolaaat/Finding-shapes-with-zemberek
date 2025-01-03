# -*- coding: utf-8 -*-
"""ucgenvoleybol_withoutzemberek.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ry4nUOoFuh-PwDP3dDTAtEzEESwASns2
"""

import pandas as pd

data = pd.read_csv("/content/output.csv")

import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import ClassifierI
from statistics import mode
import pickle

import nltk
import os
nltk.download('punkt_tab')

documents = []

for _, row in data.iterrows():
    documents.append((word_tokenize(row['Command']), row[' Label']))
print(documents)

from nltk.probability import FreqDist

all_words = []
for doc, label in documents:
  for w in doc:
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)
print(all_words.most_common(15))
print(all_words["üçgen"])

word_features = list(all_words.keys())[:1000]

def find_features(document):

  document = " ".join(document) if isinstance(document, list) else document
  words = word_tokenize(document)
  features = {}

  for w in word_features:
    features[w] = (w in words)

  return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]

train_size = int(len(featuresets) * 0.75)
training_test = featuresets[:train_size]
testing_set = featuresets[train_size:]

new_data_ = "üç kenarlı bir şekil çizer misin."
new_data = word_tokenize(new_data_)

classifier = nltk.NaiveBayesClassifier.train(training_test)
prediction = classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("Naive Bayes Algo Accuracy percent: ", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_test)

prediction = MNB_classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("MultinomialNB Algo Accuracy percent: ", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

BernaulliNB_classifier = SklearnClassifier(BernoulliNB())
BernaulliNB_classifier.train(training_test)

prediction = BernaulliNB_classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("BernoulliNB Algo Accuracy percent: ", (nltk.classify.accuracy(BernaulliNB_classifier, testing_set))*100)

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_test)

prediction = LinearSVC_classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("BernoulliNB Algo Accuracy percent: ", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_test)

prediction = LogisticRegression_classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("LogisticRegression Algo Accuracy percent: ", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

SGDClassifier = SklearnClassifier(SGDClassifier())
SGDClassifier.train(training_test)

prediction = SGDClassifier.classify(find_features(new_data))
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

prediction = vote_classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("vote_classifier accuracy percent:", (nltk.classify.accuracy(vote_classifier, testing_set))*100)