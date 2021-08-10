import requests
from bs4 import BeautifulSoup
import re

def get_cnt_images(link):
    try:
        site = requests.get(link).text
        return len(re.findall('ImageObject', site))
    except:
        return False


def main():
    print(get_cnt_images("https://habr.com/ru/company/skillfactory/blog/570586/"))

if __name__ == '__main__':
    main()
