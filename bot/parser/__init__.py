import requests
import re
import time
from bs4 import BeautifulSoup
from joblib import Parallel, delayed

site_medium = "https://medium.com"
site_habr = "https://habr.com/en"


def dow_all(links, results):
    results.append(Parallel(n_jobs=9)(map(delayed(download), links)))


def download(link):
    print(link)
    res = requests.get(link).text
    return res


def get_medium(res, theme):
    link_medium = site_medium + "/search?q=" + theme
    # try:
    response = requests.get(link_medium).text
    soup = BeautifulSoup(response, "lxml")

    blocks = soup.find_all("div", attrs={
        "class": "postArticle postArticle--short js-postArticle js-trackPostPresentation"})
    timer = time.time()

    links_author = []
    links_articles = []
    for i in range(0, len(blocks)):
        links_author.append(get_link(blocks[i].find("a", attrs={
            "class": "link u-baseColor--link avatar"})))
        links_articles.append(get_link(blocks[i].find("div", attrs={"class": "postArticle-content"}).find("a")))
    results_author = []
    results_articles = []
    dow_all(links_author, results_author)
    dow_all(links_articles, results_articles)
    print(len(results_author[0]))

    for i in range(0, len(blocks)):
        newlist = []
        zalupa = blocks[i].find("button", attrs={
            "class": "button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents"}).text
        numlikes = re.findall(r"[-+]?\d*\.\d+|\d+", zalupa)[0]
        numlikes = float(numlikes)
        if zalupa[len(zalupa) - 1] == 'K':
            numlikes *= 1000
        if zalupa[len(zalupa) - 1] == 'M':
            numlikes *= 1000000
        # print(numlikes)
        zalupa = blocks[i].find("a", attrs={"class": "button button--chromeless u-baseColor--buttonNormal"}).text
        numcomments = re.findall(r"[-+]?\d*\.\d+|\d+", zalupa)[0]
        numcomments = float(numcomments)
        if zalupa[len(zalupa) - 1] == 'K':
            numcomments *= 1000
        if zalupa[len(zalupa) - 1] == 'M':
            numcomments *= 1000000
        # print(numcomments)

        newlist.append(blocks[i].find("a").text)
        authorlink = get_link(blocks[i].find("a", attrs={
            "class": "link u-baseColor--link avatar"}))

        headers = {"Range": "bytes=10"}
        # response = requests.get(authorlink, headers=headers).text
        # print(response)
        soup = BeautifulSoup(results_author[0][i], "lxml")
        # print(soup)
        zalupa = soup.find_all("div", attrs={"class": "dq dr t"})
        numfollowers = float(0)
        if len(zalupa) != 0:
            numfollowers = zalupa[0].find("a").text
            numfollowers = numfollowers[0: len(numfollowers) - 9]
            crunch = re.findall(r"[-+]?\d*\.\d+|\d+", numfollowers)[0]
            realnum = float(crunch)
            if numfollowers[len(crunch)] == 'K':
                realnum *= 1000
            if numfollowers[len(crunch)] == 'M':
                realnum *= 1000000
            numfollowers = realnum
        print(numfollowers)
        # print(newlist, '\n')
        # print(blocks[i], '\n')
        soup = BeautifulSoup(results_articles[0][i], "lxml")
        numpictures = len(soup.find_all("figure"))
        res.append(blocks[i].find("div", attrs={"class": "postArticle-content"}).find("a"))
    print(timer - time.time())


def get_habr(res, theme):
    link_habr = site_habr + "/search/?q=" + theme + "&target_type=posts&order=relevance"
    response = requests.get(link_habr).text
    soup = BeautifulSoup(response, "lxml")
    # print(link_habr)
    blocks = soup.find_all("article")
    for i in blocks:
        print(i.find("a"))
    for i in blocks:
        numcomments = float(re.findall(r"[-+]?\d*\.\d+|\d+", i.find("div", attrs={"title": "Read comments"}).text)[0])
        numlikes = i.find("div", attrs={"class": "tm-votes-meter tm-data-icons__item"}).text
        zalupa = (re.findall(r"[-+]?\d*\.\d+|\d+", numlikes))
        numlikes = float(zalupa[1]) - float(zalupa[2])
        # print(numlikes)


def get_topics(theme):
    res = []
    get_medium(res, theme)
    # get_habr(res, theme)
    return res


# except:
#     return False


def get_link(bloc):
    # print(bloc)
    lk = bloc.get("href")
    return (site_medium if lk[0] == '/' else '') \
           + bloc.get("href")


def get_href(bloc):
    print(bloc, '\n')
    return '<a href="' + get_link(bloc) + '">' + bloc.text + "</a>"
