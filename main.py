import requests
import re
import os

from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path
import os.path


def get_string(broadcast_text, regex, regex_group=0):
    title_search = re.search(regex, broadcast_text)
    if title_search:
        title = title_search.group(regex_group)
        return title

def get_date(broadcast_text):
    r_date = r'(\d{4}-\d{2}-\d{2})'
    return get_string(broadcast_text, r_date)


def get_broadcast_title(broadcast_text):
    r_title = r'\d{4}-\d{2}-\d{2}_\d{4}\s(.*?)-'
    return get_string(broadcast_text, r_title, regex_group=1)


def get_author(broadcast_text):
    r_author = r'\d{4}-\d{2}-\d{2}_\d{4}\s(.*?)-\s(.*?)\.'
    return get_string(broadcast_text, r_author, regex_group=2)


def get_time(broadcast_text):
    r_time = r'\d{4}-\d{2}-\d{2}_(\d{4})\s'
    return get_string(broadcast_text, r_time, regex_group=1)


if __name__ == '__main__':
    #date = datetime.today().strftime('%Y-%m-%d')
    path_to_store_broadcasts = 'G:/radio_357'
    url_simx_357_fedd = 'https://www.simx.mobi/357/feed.xml'

    list_of_broadcasts_name = [
        r'Max\s357',
        r'357\sStart!'
        'Kiribati',
        'No to co teraz',
        'Co Państwo na to',
        'Lista Piosenek 357',
    ]

    list_of_authors = [r'Michniewicz',
                       r'Nied.wiecki',
                       r'Strzyczkowski']

    list_of_broadcast_regex = list_of_broadcasts_name + list_of_authors

    page = requests.get(url_simx_357_fedd)
    soup = BeautifulSoup(page.content, 'html.parser')
    results_2 = soup.find_all('guid')
    broadcasts_feed = [broadcast.text for broadcast in results_2]

    for brodcast_regex in list_of_broadcast_regex:
        r = re.compile(brodcast_regex)
        particular_broadcast_list = list(filter(r.search, broadcasts_feed))

        for broadcast in particular_broadcast_list:

            date = get_date(broadcast)
            title = get_broadcast_title(broadcast).strip().replace(' ', '_')
            author = get_author(broadcast).strip().replace(' ', '_')
            time = get_time(broadcast)

            folder_to_store_broadcast = '/'.join((path_to_store_broadcasts, title, date))
            Path(folder_to_store_broadcast).mkdir(parents=True, exist_ok=True)

            broadcast_name = f'{title}_{author}_{time}.aac'

            file_path = os.path.join(folder_to_store_broadcast, broadcast_name)
            print(os.path.isfile(file_path))
            if not os.path.isfile(file_path):
                req = requests.get(broadcast)
                with open(file_path, 'wb') as file:
                    for chunk in req.iter_content(100000):
                        file.write(chunk)
                    print(broadcast_name)
            else:
                print(f'{broadcast_name} exists in {file_path}')


