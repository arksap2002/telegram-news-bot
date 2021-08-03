import requests
from bs4 import BeautifulSoup

site = "https://medium.com"

def get_topics(theme):
    link = site + "/topic/" + theme
    response = requests.get(link).text
    soup = BeautifulSoup(response, "lxml")

    blocs = soup.find_all("section")

    res = []
    for i in range(3):
        res.append(blocs[2 * i].find("a"))

    return res


def get_link(bloc):
    print(bloc)
    return site + bloc.get("href")

def get_href(bloc):
    return '<a href="' + get_link(bloc) + '">' + bloc.text + "</a>"

def main():
    print(get_link(get_topics("self")[0]))

if __name__ == '__main__':
    main()