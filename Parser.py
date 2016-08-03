from config import *
from bs4 import BeautifulSoup
from os.path import join
from nltk import word_tokenize, pos_tag
from collections import Counter
import os
import sys
from Indexer import index
import multiprocessing


def parse_all(files):
    docs = {}
    i = 0
    for file in files:
        i += 1
        docID, properties = parse(file)
        docs[docID] = properties
        print "Process %s : %s files" %(multiprocessing.current_process().name, i)
        if i % 100 == 0:
            index(docs)
            docs = {}

    return docs


def parse(file):
    file_path = join(DATASET_PATH, file)
    docID, gender, age, LIWC = extract_labels(file)
    with open(file_path, 'r') as f:
        file_content = f.read()
    soup = BeautifulSoup(file_content, 'xml')
    properties = {}
    properties['docno'] = docID
    properties['gender'] = gender
    properties['age'] = age
    properties['LIWC'] = LIWC
    all_text = ''
    posts = soup.findAll('post')
    i = 0
    for post in posts:
        i += 1
        # sys.stdout.write("\rProcessed %d / %d" %(i, len(posts)))
        # sys.stdout.flush()
        text = post.text.strip()
        all_text += text

    properties['text'] = all_text
    pronouns, prepositions, determiners = get_pos_tags(all_text)
    properties['pronouns'] = pronouns
    properties['prepositions'] = prepositions
    properties['determiners'] = determiners
    return docID, properties


def get_pos_tags(text):
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    count = Counter([j for i,j in tags if j in ['PRP', 'PRP$', 'IN', 'DT']])
    pronouns = count['PRP'] + count['PRP$']
    prepositions = count['IN']
    determiners = count['DT']
    return pronouns, prepositions, determiners


def extract_labels(filename):
    split_name = filename.split(".")
    docID = split_name[DOCID]
    gender = split_name[GENDER]
    age = split_name[AGE]
    liwc = split_name[LIWC]
    return docID, gender, age, liwc