#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The extract_keywords.py module uses Yake! to extract keywords from each article
Source: https://github.com/LIAAD/yake
"""


def extract_keywords(text):
    language = "en"
    max_ngram_size = 1
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 10

    kw_extractor = yake.KeywordExtractor(lan=language, 
                                         n=max_ngram_size, 
                                         dedupLim=deduplication_thresold, 
                                         dedupFunc=deduplication_algo, 
                                         windowsSize=windowSize, 
                                         top=numOfKeywords)

    keywords = kw_extractor.extract_keywords(text)
    
    return list(dict(keywords).keys())
