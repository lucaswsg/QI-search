#!/usr/bin/env python3

# Search all available QI transcripts for terms specified by the user.
# Transcripts are available on https://subslikescript.com/series/QI-380136
import requests
import bs4
import re


# send request to web page and parse using Beautiful Soup
def get_soup(page):
    res = requests.get(page)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    return soup


qiSoup = get_soup("https://subslikescript.com/series/QI-380136")

# get HTML elements with <a> tag containing episode page url
urls = qiSoup.select('.season > ul > li > a')

# get search term from user and initialize variable to keep track of
# the number of transcripts containing the search term
search_term = input("Keyword: ")
found = 0

# iterate through list of <a> tags and extract urls
for i in range(len(urls)):
    url = 'https://subslikescript.com' + urls[i].get('href')

    # get text of the episode transcript
    episodeSoup = get_soup(url)
    script = episodeSoup.select('.full-script')[0].getText()

    # search for the given search term and print URL for each
    # transcript containing the term
    result = re.search(rf'\b{search_term}\b', script, re.IGNORECASE)
    if result:
        print('Keyword {key} was found at in {url}.'.format(key=search_term, url=url))
        found += 1
    else:
        pass

print('We found {total} instances of the term "{term}".'.format(total=found, term=search_term))
