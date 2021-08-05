import requests
from bs4 import BeautifulSoup

site = "https://medium.com"


def get_topics(theme):
    link = site + "/search?q=" + theme
    try:
        response = requests.get(link).text
        print(link)
        soup = BeautifulSoup(response, "lxml")

        blocks = soup.find_all("div", attrs={"class": "postArticle-content"})
        if len(blocks) == 0:
            return " "
        print(blocks)
        print(blocks[1].text, '\n')
        res = []
        for i in range(0, min(3, len(blocks))):
            res.append(blocks[i].find("a"))

        print(res)
        return res
    except:
        return False


def get_link(bloc):
    # print(bloc)
    lk = bloc.get("href")
    return (site if lk[0] == '/' else '') \
           + bloc.get("href")


def get_href(bloc):
    print(bloc, '\n')
    return '<a href="' + get_link(bloc) + '">' + bloc.text + "</a>"
