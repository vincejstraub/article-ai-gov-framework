#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The preprocess_results.py cleans the retrieved search results.
"""


import numpy as np
import pandas as pd


def main():
    database = load_database()
    database_df = remove_books(database)
    database_df['publication'] = database_df['publication_info_summary'].apply(
        get_publication
    )
    database_df['match_title'] = database_df['title'].apply(
        match_title
    )
    
    database_df.to_excel(
        '../data/processed/search_esults_processed.xlsx'
    )


def load_database(filepath='../data/raw/raw_search_results.csv'):
    database = pd.read_csv(filepath)

    return database


def remove_books(df):
    database = df.loc[df['file_link'].notnull()].sort_values(
        by=['cited_by_count'], ascending=False
    )
    database_df = database.drop_duplicates(
        subset=['title', 'link'], keep='first')
    database_df = database_df.loc[~database_df['result_type'].isin(
        ['Book', 'Citation']
    )]
    database_df.reset_index(inplace=True)
    
    return database_df


def get_publication(s):
    return s.split(' - ')[1].split(',')[0].replace('…', '').strip()


def match_title(s, terms=[
    'government', 'public', 'administration', 'policy', 'service'
]):
    if any([x in s for x in terms]):
        return 1
    else:
        return 0
