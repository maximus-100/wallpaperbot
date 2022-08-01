import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import re
from database import WallpapersDB
import time

load_dotenv()

URL = os.getenv('URL')
HOST = os.getenv('HOST')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36'
}

class CategoryParser:
    def __init__(self, url, name, category_id, pages: int = 3, download=False):
        self.url = url
        self.name = name
        self.category_id = category_id
        self.pages = pages
        self.download = download

    def get_html(self, i):
        try:
            html = requests.get(self.url + f'/page{i}', headers=HEADERS).text
            return html
        except:
            print('Не удалось получить страницу')

    def get_soup(self, i):
        html = self.get_html(i)
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def get_data(self):
        for i in range(1, self.pages + 1):
            soup = self.get_soup(i)
            images_blocks = soup.find_all('a', class_='wallpapers__link')
            for block in images_blocks:
                try:
                    page_link = HOST + block['href']

                    page_html = requests.get(page_link, headers=HEADERS).text
                    del page_link
                    page_soup = BeautifulSoup(page_html, 'html.parser')
                    resolution = page_soup.find_all('span', class_='wallpaper-table__cell')[1].get_text(strip=True)

                    image_link = block.find('img', class_='wallpapers__image').get('src')
                    image_link = image_link.replace('300x168', resolution)


                    WallpapersDB.insert_into_images(image_link, self.category_id)

                    if self.download:
                        if self.name not in os.listdir():
                            os.mkdir(str(self.name))
                        responceImage = requests.get(image_link, headers=HEADERS).content
                        image_name = image_link.replace('https://images.wallpaperscraft.ru/image/single/', '')
                        with open(file=f'{self.name}/{image_name}', mode='wb') as file:
                            file.write(responceImage)

                except Exception as e:
                    pass



def parser():
    html = requests.get(URL, headers=HEADERS).text
    soup = BeautifulSoup(html, 'html.parser')
    block = soup.find('ul', class_='filters__list')
    filters = block.find_all('a', class_='filter__link')
    for f in filters:
        link = HOST + f.get('href')

        name = f.get_text(strip=True)

        true_name = re.findall(r'[3]*[Da-яА-Я]+', name)[0]

        pages = int(re.findall(r'[0-9][0-9]+', name)[0]) // 15

        WallpapersDB.insert_category(true_name)
        category_id = WallpapersDB.get_category_id(true_name)
        parser = CategoryParser(url=link,
                                name=true_name,
                                category_id=category_id)  # download=True
        parser.get_data()




parser()
