#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 00:25:00 2020

@author: emanalbilali
"""

import pandas as pd 
import uuid
import json


# creating JSON file structure
def create_json(df):
    
    dataset={'data':[], 'version':str}
    paragraph={'title':str, 'context':str, 'qas':[]}
    question={'id':str, 'question':str, 'answer':{}}
    answer={'answer_start':int, 'text':str}

    seen_titles=[]
    
    dataset['version']='1.1'

    for index, row in df.iterrows():
    
        paragraph={'title':str, 'context':str, 'qas':[]}
        answer={'answer_start':int, 'text':str}
        answer['answer_start']= row['answer_start']
        answer['text']= row['answer']
             
     # question dictionary
        question['id']= str(row['id'])
        question['question']=row['question']
        question['answer']=answer
    
        if row['title'] in seen_titles:
        
          pas=next((item for item in dataset['data'] if item["title"] == row['title']), None)
       # append question to list of questions for this paragraph
          pas['qas'].append(question.copy())
          question.clear()
                 
        
        else:
   # create new text 
            paragraph['title']= row['title']
            seen_titles.append(row['title'])
            paragraph['context']=row['article']
            paragraph['qas'].append(question.copy())
            dataset['data'].append(paragraph.copy())
            question.clear()
    return dataset

# load dataset
val_development= pd.read_csv('validated_development.csv')
val_test= pd.read_csv('validated_test.csv')

# assign id to each row
val_development['id'] = [uuid.uuid4().int for _ in range(len(val_development.index))]
val_test['id'] = [uuid.uuid4().int for _ in range(len(val_test.index))]

del val_development['Unnamed: 0']
del val_development['in']
del val_test['Unnamed: 0']
del val_test['in']

#create & save JSON file
val_dev_json=create_json(val_development)
val_test_json=create_json(val_test)

with open("validated_development.json", 'w') as fp:
        json.dump(val_dev_json, fp)

with open("validated_test.json", 'w') as fp:
        json.dump(val_test_json, fp) 
        
# create json file for train, validation and test
train= pd.read_csv('training_wikidata_79,048.csv')
development= pd.read_csv('validation_wikidata_9,806.csv')
test=pd.read_csv('test_wikidata_9789.csv')      

# assign id to each row
train['id'] = [uuid.uuid4().int for _ in range(len(train.index))]
development['id'] = [uuid.uuid4().int for _ in range(len(development.index))]
test['id'] = [uuid.uuid4().int for _ in range(len(test.index))]

#create & save JSON file
train_json=create_json(train)
development_json=create_json(development)
test_json=create_json(test)
        
with open("trin.json", 'w') as fp:
        json.dump(train_json, fp)

with open("development.json", 'w') as fp:
        json.dump(development_json, fp)
        
with open("test.json", 'w') as fp:
        json.dump(test_json, fp)