# -*- coding: utf-8 -*-
"""ucgenvoleybol_withpickle.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oc5lDC20QSWfFLYoidUXrKHv1sVTMPD6
"""

import pandas as pd

data = pd.read_csv("/content/output.csv")

import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import ClassifierI
from statistics import mode
import pickle

class VoteClassifier(ClassifierI):
  def __init__(self, *classifiers):
    self.classifiers = classifiers

  def classify(self, features):
    votes = []
    for c in self.classifiers:
      v = c.classify(features)
      votes.append(v)
    return mode(votes)

  def confidence(self, features):
    votes = []
    for c in self.classifiers:
      v = c.classify(features)
      votes.append(v)

    choice_votes = votes.count(mode(votes))
    conf = choice_votes / len(votes)
    return conf

import nltk
import os
nltk.download('punkt_tab')

documents = []

for _, row in data.iterrows():
    documents.append((word_tokenize(row['Command']), row[' Label']))
print(documents)

os.makedirs("pickled_algos", exist_ok=True)

save_documents = open("pickled_algos/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

from nltk.probability import FreqDist

all_words = []
for doc, label in documents:
  for w in doc:
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)
print(all_words.most_common(15))
print(all_words["üçgen"])

word_features = list(all_words.keys())[:1000]


save_word_features = open("pickled_algos/word_features5k.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()
print(word_features)

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

new_data_ = "iç açıları toplamı 180 derece ,3 kenar 3 köşe şekline gel"
new_data = word_tokenize(new_data_)

classifier = nltk.NaiveBayesClassifier.train(training_test)
prediction = classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("Naive Bayes Algo Accuracy percent: ", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)


save_classifier = open("pickled_algos/originalnaivebayes5k.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_test)
prediction = MNB_classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("MultinomialNB Algo Accuracy percent: ", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)


save_classifier = open("pickled_algos/MNB_classifier5k.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

BernaulliNB_classifier = SklearnClassifier(BernoulliNB())
BernaulliNB_classifier.train(training_test)
prediction = BernaulliNB_classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("BernoulliNB Algo Accuracy percent: ", (nltk.classify.accuracy(BernaulliNB_classifier, testing_set))*100)


save_classifier = open("pickled_algos/BernoulliNB_classifier5k.pickle","wb")
pickle.dump(BernaulliNB_classifier, save_classifier)
save_classifier.close()

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_test)
prediction = LinearSVC_classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("BernoulliNB Algo Accuracy percent: ", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)


save_classifier = open("pickled_algos/LinearSVC_classifier5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_test)
prediction = LogisticRegression_classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("LogisticRegression Algo Accuracy percent: ", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)


save_classifier = open("pickled_algos/LogisticRegression_classifier5k.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_test)
prediction = SGDClassifier_classifier.classify(find_features(new_data))
print("Tahmin Sonucu:", prediction)
print("SGDClassifier Algo Accuracy percent: ", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)


save_classifier = open("pickled_algos/SGDC_classifier5k.pickle","wb")
pickle.dump(SGDClassifier_classifier, save_classifier)
save_classifier.close()

vote_classifier = VoteClassifier(classifier,
                                  MNB_classifier,
                                  BernaulliNB_classifier,
                                  SGDClassifier_classifier,
                                  LinearSVC_classifier,
                                  LogisticRegression_classifier)

print("vote_classifier accuracy percent:", (nltk.classify.accuracy(vote_classifier, testing_set))*100)

documents_f = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()

word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

print(len(featuresets))

testing_set = featuresets[10000:]
training_set = featuresets[:10000]

open_file = open("pickled_algos/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/BernoulliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/LogisticRegression_classifier5k.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/LinearSVC_classifier5k.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/SGDC_classifier5k.pickle", "rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()

voted_classifier = VoteClassifier(
                                  classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)

print(sentiment("iç açıları toplamı 180 derece ,3 kenar 3 köşe şekline gel"))
print(sentiment("Rica etsem ok başı şeklinde bir duruş sergiler misin?"))