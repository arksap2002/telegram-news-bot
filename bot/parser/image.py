import requests
from bs4 import BeautifulSoup

def get_cnt_images(link):
    try:
        site = requests.get(link).text
        block = BeautifulSoup(site, "lxml").find('div', attrs={'class':
            'au av aw ax ay gn ba v'})
        return len(block.find_all('figure'))
    except:
        return False


def main():
    print(get_cnt_images("https://towardsdatascience.com/using-dotenv-to-hide-sensitive-information-in-python-77ab9dfdaac8"))

if __name__ == '__main__':
    main()
