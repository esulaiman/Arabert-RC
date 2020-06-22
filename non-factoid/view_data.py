#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 20:10:56 2020

@author: emanalbilali
"""

import pandas as pd
import re
import string

'''
def normalize_answer(s):
    
   def remove_punctuation(answer):
    # remove . at teh end of the sentence
      if answer[-1]== '.':
        s= list(answer)
        s[-1]=''
        answer="".join(s) 
      return answer
  
   def white_space_fix(text):
        return ' '.join(text.split())
    
   return white_space_fix(remove_punctuation(s))
'''
def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

df=pd.read_json('validated_development_set.json')

data=df['data']

total_pars = 0
total_quests = 0

different_ans=[]

for index, row in data.iteritems():
    
    total_pars+=1
    title=row['title']
    context=row['context']

 # iterate through questions
    for qa in row['qas']:
        total_quests+=1
        question=qa['question']
        
        answers=list(map(lambda x: x['text'], qa['answers']))
        if normalize_answer(answers[0]) != normalize_answer(answers[1]) and normalize_answer(answers[0]) != normalize_answer(answers[2]) :
          different_ans.append(qa)   
             
        for ans in qa['answers']:
            answer_text= ans['text']
            answer_start=ans['answer_start']
            
            
print('total number of paragraph', total_pars)
print('total number of questions', total_quests)            