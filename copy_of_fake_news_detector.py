# -*- coding: utf-8 -*-
"""Copy of fake-news-detector.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cpX1AdWUMa2tFQqyjNasAbltIyNFezda
Please go there and see the code in action!!

Hello and welcome to the fake news detector!
"""

import pandas as pd
import numpy as np
import re

true = pd.read_csv('True.csv')

fake = pd.read_csv('Fake.csv')

true['label'] = 1

fake['label'] = 0

news = pd.concat([fake, true], axis = 0)

news.isnull().sum()

news = news.drop(['title', 'subject', 'date'], axis = 1)

news = news.sample(frac=1) #reshuffle

news.reset_index(inplace=True)

news = news.drop(['index'], axis = 1)

def wordopt(text):
  text = text.lower() #convert to lowercase
  text = re.sub(r'https?://\S+|www\.\S+', '', text) #remove URLs
  text = re.sub(r'<.*?>', '', text) # remove HTML tags
  text = re.sub(r'[^\w\s]', '', text) #remove punctuation
  text = re.sub(r'\d', '', text) #remove digits
  text = re.sub(r'\n', '', text) #remove newline characters
  return text

news['text'] = news['text'].apply(wordopt)

news.head()

news['text']

x = news['text']
y = news['label']

x

y

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

x_train.shape

x_test.shape

from sklearn.feature_extraction.text import TfidfVectorizer

vectorization = TfidfVectorizer()

xv_train = vectorization.fit_transform(x_train)

xv_test = vectorization.transform(x_test)

xv_train

xv_test

from sklearn.linear_model import LogisticRegression

LR = LogisticRegression()

LR.fit(xv_train, y_train)

pred_lr = LR.predict(xv_test)

print(LR.score(xv_test, y_test))

from sklearn.metrics import classification_report

print(classification_report(y_test, pred_lr))

from sklearn.tree import DecisionTreeClassifier

DTC = DecisionTreeClassifier()

DTC.fit(xv_train, y_train)

pred_dtc = DTC.predict(xv_test)

DTC.score(xv_test, y_test)

print(classification_report(y_test, pred_dtc))

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier()

rfc.fit(xv_train, y_train)

predict_rfc = rfc.predict(xv_test)

rfc.score(xv_test, y_test)

print(classification_report(y_test, predict_rfc))

from sklearn.ensemble import GradientBoostingClassifier

gbc = GradientBoostingClassifier()

gbc.fit(xv_train, y_train)

pred_gbc = gbc.predict(xv_test)

gbc.score(xv_test, y_test)

print(classification_report(y_test, pred_gbc))

def output_label(n):
  if n == 0:
    return "This is fake."
  elif n ==1:
    return "This is true."

def manual_testing(news):
  testing_news = {"text": [news]} #correct syntax
  new_def_test = pd.DataFrame(testing_news)
  new_def_test["text"] = new_def_test["text"].apply(wordopt)
  new_x_test = new_def_test["text"]
  new_xv_test = vectorization.transform(new_x_test)
  pred_lr = LR.predict(new_xv_test)
  pred_dtc = DTC.predict(new_xv_test)
  predict_rfc = rfc.predict(new_xv_test)
  return "\n\nLR Prediction: {} \nRFC Prediction: {}".format(
      output_label(pred_lr[0]), output_label(predict_rfc[0]))

news_article = str(input())

manual_testing(news_article)
