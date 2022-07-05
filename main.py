"""
This program scrapes Google's top results to extract mainly title tags of top results
Inputs: a dictionary of the main keywords we want to do a Google search for, with Keywords as keys and empty
arrays as values. named (kws)

Output: the title tags are exported into a txt file that can be imported into a Google sheet for more processing

Source: https://practicaldatascience.co.uk/data-science/how-to-scrape-google-search-results-using-python
"""

import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import csv

def get_source(url):
    """Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_results(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.de/search?q=" + query)

    return response


def parse_results(response):
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"

    results = response.html.find(css_identifier_result)

    output = []

    for result in results:
        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            #'text': result.find(css_identifier_text, first=True).text
        }

        output.append(item)

    return output

def google_search(query):
    response = get_results(query)
    return parse_results(response)

titles = {}
kws = {"elastische spitze":[],"mahagoni braun haarfarbe":[],"kurzhaar perücken damen":[],
       "Perücken für Frauen":[],"blonde perücke kurz":[],"haarfarbe mahagoni braun":[],
       "synthetische perücken":[],"afro perücke frauen":[],"haarfarbe braun schwarz":[],
       "echthaar perücken damen":[],"synthetik haare kaufen":[],"weißblond farbe":[],
       "beste braune haarfarbe":[],"elastischer spitzenstoff":[],"haarfarbe braun gold":[],
       "haarfarbe braun mahagoni":[],"kastanienbraun ombre":[],"natürliche braune haarfarbe":[],
       "natürliches braun haarfarbe":[],"natürliches hellbraun":[],"synthetische perücken kaufen":[],
       "synthetik perücke waschen":[],"alle haartypen":[],"haartypen":[],"damen perücken kurzhaar":[]}
for kw in kws:
    results = google_search(kw)
    for i in list(range(8)):
        kws[kw].append(results[i]["title"])
    print (kws)
    #print (results)

fields = kws.keys()
print (kws)
file_name = "competitors_titles.txt"
with open(file_name,"w", encoding='utf-8') as file:
    for keyword in kws:
        file.write("***"+keyword+"\n")
        for title in kws[keyword]:
            file.write(title + "\n")

