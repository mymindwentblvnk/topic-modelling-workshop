from os import listdir
from os.path import isfile, join

import pylast

import settings


client = pylast.LastFMNetwork(api_key=settings.API_KEY,
                              api_secret=settings.API_SECRET,
                              username=settings.USER,
                              password_hash=pylast.md5(settings.PASSWORD))


def get_artist_bio(artist_name: str):
    try:
        artist = client.get_artist(artist_name)
        bio = artist.get_bio_content()

        if bio and 'There are at least' not in bio:  # No perfect match found
            return bio
    except pylast.WSError:
        print(f"Bio for {artist_name} cannot be found.")


def dump_artist_bio(bio: str, path: str):
    try:
        with open(path, 'w') as out:
            out.write(bio)
    except FileNotFoundError:
        print(f"Bio for {artist_name} cannot be written.")


def load_artist_names(path):
    with open(path, 'r') as f:
        return [artist_name.strip() for artist_name in f.readlines()]


def get_already_written_artists(path: str) -> list:
    return [f.replace('-bio.txt', '') for f in listdir(path) if isfile(join(path, f))]


if __name__ == '__main__':
    directory = 'data/raw/bios'
    already_written_artist = set(get_already_written_artists(directory))
    artist_names = set(load_artist_names('data/artists.txt'))

    for artist_name in artist_names.difference(already_written_artist):
        if artist_name in already_written_artist:
            continue
        print(f"Loading bio for {artist_name}")
        path = f'{directory}/{artist_name}-bio.txt'
        bio = get_artist_bio(artist_name)

        if bio:
            dump_artist_bio(bio, path)
