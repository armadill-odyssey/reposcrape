import datetime
import json
from multiprocessing.dummy import Pool as ThreadPool
from pprint import pprint
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import requests
from bs4 import BeautifulSoup

import store

# Github trending url
baseURL = "https://github.com/trending"

def getLanguages():
    """
    Scan all selectable languages on trending page of github
    """
    langauges = []

    trendingPage = requests.get(baseURL)
    soup = BeautifulSoup(trendingPage.content, 'lxml')

    langList = soup.select('body div.explore-pjax-container.container.explore-page > div.columns > div.column.one-fourth > div.select-menu.js-menu-container.js-select-menu > div > div > div.select-menu-list > div')[0]
    for item in langList.find_all('a', class_="select-menu-item"):
        langauges.append({
            'url': item.get('href'),
            'name': item.text.strip(),
        })
    return langauges


def scrapeTrendingList(ol):
    """
    Using a given soup of the github list (ol element),
    return formatted data of each repo
    """
    list = []

    for li in ol.find_all('li'):
        headlineEl = li.select("h3 a")[0]
        repoLink = headlineEl.get('href')
        author, repo = headlineEl.text.split('/')

        try:
            desc = li.select('.py-1 p')[0].text
        except:
            desc = ''

        try:
            lang = li.select('span[itemprop="programmingLanguage"]')[0].text
        except:
            lang = 'Unknown'

        try:
            stars = li.select('a[aria-label="Stargazers"]')[0].text.strip()
            stars = locale.atoi(stars)
        except:
            stars = 0

        try:
            forks = li.select('a[aria-label="Forks"]')[0].text
            forks = locale.atoi(forks)
        except:
            forks = 0

        starsTodayText = li.find_all('span')[-1].text.strip()
        starsToday = starsTodayText.split(' ')[0]

        try: # see if a number
            starsToday = int(starsToday)
        except:
            starsToday = 0

        list.append({
            'author': author.strip(),
            'repoLink': repoLink.strip(),
            'repo': repo.strip(),
            'desc': desc.strip(),
            'lang': lang.strip(),
            'stars': stars,
            'starsToday': starsToday,
            'forks': forks,
        })

    return list

def fetchTrending(url):
    # Fetch page
    trendingPage = requests.get(url)
    soup = BeautifulSoup(trendingPage.content, 'lxml')
    trendingOL = soup.find('ol', class_="repo-list")

    # No trending repo for lang
    if trendingOL is None:
        return []

    print(url)
    return scrapeTrendingList(trendingOL)


def scrape():
    trending = {
        'all': fetchTrending(baseURL),
    }

    languages = getLanguages()

    def assign(lang):
        trending[lang['name']] = fetchTrending(lang['url'])

    # Make the Pool of workers
    pool = ThreadPool(4)
    pool.map(assign)
    #close the pool and wait for the work to finish
    pool.close()
    pool.join()

    store.saveToFile(trending)
