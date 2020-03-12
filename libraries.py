# coding: utf-8

#Acquisition
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import time
import re

#Preparation
import string
from googletrans import Translator
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer

#Reporting
import matplotlib.pyplot as plt
