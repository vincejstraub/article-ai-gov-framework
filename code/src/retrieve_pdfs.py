#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The retrieve_pfds.py contains functions to retrieve the file of 
a search result and extract article keywords from the first page.
"""


import io
import re
import sys
import requests
import numpy as np
import pandas as pd

import pdfquery
import PyPDF2

def run_automatic_extraction():
    database = load_database()
    database['keywords'] = database.apply(store_keywords, axis=1)
    
    return database


def load_database(filepath='../data/processed/search_results_processed.xlsx'):
    database_df = pd.read_excel(filepath)

    return database_df


def store_keywords(row):
    url = row['file_link']
    return extract_keywords(url)
    

def extract_keywords(url):  
    try:
        contents = get_keywords(url)
    except IndexError: 
        print(url)
        return contents

    try:   
        keywords = contents.split(':')[1].strip()
        keywords = ' '.join(word for word in keywords.split() if len(word)>2)
        keywords = re.sub('[!@#$:0-9]', '', keywords).split(',')
        keywords = list(map(str.strip, keywords))
        keywords = remove_terms(keywords)
        keywords = [i.replace('\n',' ') for i in keywords]
    
        if 'intro' in str(keywords):
            keywords = remove_introduction(keywords)
        
        if 'and' in str(keywords):
            keywords = remove_and(keywords)
    
        return keywords
    
    except:
        return contents
    
    
def get_keywords(url):
    text = get_pdf_text(url)
    if text is not np.nan:
        for i in ['keywords', 'key words', 'index terms']:
            if i in text.lower():
                try: 
                    keywords = text.lower().split(i)[1].split('.')[0]
                    return keywords
                except IndexError:
                    return np.nan
    else:
        return np.nan
    

def get_pdf_text(url):
    r = requests.get(url, verify=False)
    f = io.BytesIO(r.content)
   
    try:
        reader = PyPDF2.PdfReader(f)
        pages = len(reader.pages)
        return str(reader.pages.extract_text())
    except:
        return np.nan
    
    
def get_pdf_main_text(url):
    r = requests.get(url, verify=False)
    f = io.BytesIO(r.content)

    try:
        reader = PyPDF2.PdfReader(f)
        pages = len(reader.pages)
        
        pages_text = []
        for i in range(0, pages): 
            pages_text.append((reader.pages[i].extract_text()))
        
        main_text = ' '.join(
            pages_text).replace('\n', '').strip().lower()
                
        return main_text
        
    except:
        return np.nan


def remove_terms(keywords, terms=[
    'artificial intelligence', 'artiﬁcial intelligence']): 
    for term in terms:
        keywords = [i.replace(term,'') for i in keywords]

    return list(map(str.strip, keywords))
    

def remove_introduction(keywords, term='intro'):
    counter = 0
    for i in keywords:
        if term in i:
            keywords[counter] = i.split(term)[0].strip()
        else:
            pass
        counter += 1
    
    return keywords


def remove_and(keywords, term='and'):
    counter = 0
    for i in keywords:
        if term in i:
            new_keywords = i.split('and')
            keywords.remove(i)
        else:
            pass
        counter += 1

    keywords += new_keywords
    keywords = [i.strip(' ') for i in keywords]
    
    return keywords
