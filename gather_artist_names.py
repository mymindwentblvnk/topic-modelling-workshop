import time

import requests

from bs4 import BeautifulSoup


def get_artist_names_from_lastfm_user(user_name: str) -> list:
    artist_names = []

    page = 1
    while True:
        time.sleep(0.5)
        url = f'https://www.last.fm/user/{user_name}/library/artists?date_preset=ALL&page={page}'
        r = requests.get(url)
        print(f"Calling {url}")
        if not r.url.endswith(str(page)):
            break
        soup = BeautifulSoup(r.text, "html.parser")
        names = [e.text for e in soup.find_all('a', class_='link-block-target')]
        artist_names.extend(names)
        page += 1
    return artist_names


def dump_artist_names(artist_names: list, user_name: str):
    file_name = f'data/artists/artist_names-{user_name}.txt'
    with open(file_name, 'w') as f:
        for artist_name in artist_names:
            f.write(f"{artist_name}\n")


if __name__ == '__main__':
    # List of LastFM user names
    user_names = []
    for user_name in user_names:
        print(f"Scraping artists of {user_name}")
        artist_names = get_artist_names_from_lastfm_user(user_name)
        dump_artist_names(artist_names, user_name)
