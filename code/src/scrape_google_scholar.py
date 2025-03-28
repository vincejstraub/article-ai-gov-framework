#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The scrape_google_scholar.py module uses Serpapi to retrieve the search results.
Source: https://gist.github.com/dimitryzub/7bac71d4443f208ee0c79f04de230958
"""


from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd
import os, json


def scrape_organic_results():
    params = {
      "api_key": "", # your serpapi api key
      "engine": "google_scholar",
      "q": '"data science" OR "artificial intelligence" OR "machine learning" OR "cognitive intelligence" AND "public policy" OR "government" OR "policy" OR "public sector" OR "public digital services" OR "government innovation" OR "digital government" OR "artificial for government" AND "framework" OR "typology" OR "mapping" OR "classification" OR "taxonomy" OR "ontology" OR "concept" OR theory"',
      "hl": "en", # language
      "as_ylo": "2018",
      "as_yhi": "2023",
      "num": "100"
    }

    search = GoogleSearch(params)

    organic_results_data = []

    while True:
        results = search.get_dict()

        print(f"Extracting publications from page #{results.get('serpapi_pagination', {}).get('current')}.")

        for result in results.get("organic_results", {}):
            position = result.get("position")
            title = result.get("title")
            publication_info_summary = result.get("publication_info", {}).get("summary")
            result_id = result["result_id"]
            link = result.get("link")
            result_type = result.get("type")
            snippet = result.get("snippet")

            try:
                file_title = result["resources"][0]["title"]
            except: file_title = None

            try:
                file_link = result["resources"][0]["link"]
            except: file_link = None

            try:
                file_format = result["resources"][0]["file_format"]
            except: file_format = None

            try:
                cited_by_count = int(result["inline_links"]["cited_by"]["total"])
            except: cited_by_count = None

            cited_by_id = result.get("inline_links", {}).get("cited_by", {}).get("cites_id", {})
            cited_by_link = result.get("inline_links", {}).get("cited_by", {}).get("link", {})

            try:
                total_versions = int(result["inline_links"]["versions"]["total"])
            except: total_versions = None

            all_versions_link = result.get("inline_links", {}).get("versions", {}).get("link", {})
            all_versions_id = result.get("inline_links", {}).get("versions", {}).get("cluster_id", {})

            organic_results_data.append({
                "page_number": results.get("serpapi_pagination", {}).get("current"),
                "position": position + 1,
                "result_type": result_type,
                "title": title,
                "link": link,
                "result_id": result_id,
                "publication_info_summary": publication_info_summary,
                "snippet": snippet,
                "cited_by_count": cited_by_count,
                "cited_by_link": cited_by_link,
                "cited_by_id": cited_by_id,
                "total_versions": total_versions,
                "all_versions_link": all_versions_link,
                "all_versions_id": all_versions_id,
                "file_format": file_format,
                "file_title": file_title,
                "file_link": file_link,
            })

        if "next" in results.get("serpapi_pagination", {}):
            search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
        else:
            break

    return organic_results_data


def save_organic_results_to_csv():
    print("waiting for organic results to save..")
    organic_df = pd.DataFrame(data=scrape_organic_results())
    organic_df.to_csv("google_scholar_organic_results.csv", encoding="utf-8")

    
save_organic_results_to_csv()
