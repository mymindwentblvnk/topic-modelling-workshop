from os import listdir
from os.path import isfile, join

import pylast

import settings


DIRECTORY = 'data/raw/bios'
ARTIST_NAMES_PATH = 'data/artists.txt'
ARTISTS_WO_BIO_PATH = 'data/artists-wo-bio.txt'


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
    except pylast.MalformedResponseError:
        print(f"Bio for {artist_name} cannot be found.")


def dump_artist_bio(artist_name: str, bio: str):
    try:
        with open(f'{DIRECTORY}/{artist_name}-bio.txt', 'w') as out:
            out.write(bio)
    except FileNotFoundError:
        print(f"Bio for {artist_name} cannot be written.")
        save_artist_wo_bio(artist_name, ARTISTS_WO_BIO_PATH)


def load_artist_names(path):
    try:
        with open(path, 'r') as f:
            return [artist_name.strip() for artist_name in f.readlines()]
    except FileNotFoundError:
        return []


def save_artist_wo_bio(artist_name, path):
    with open(path, 'a') as out:
        out.write(f"{artist_name}\n")


def get_already_written_artists(path: str) -> list:
    return [f.replace('-bio.txt', '') for f in listdir(path) if isfile(join(path, f))]


if __name__ == '__main__':
    already_written_artist = set(get_already_written_artists(DIRECTORY))
    artist_names = set(load_artist_names(ARTIST_NAMES_PATH))
    artists_wo_bio = set(load_artist_names(ARTISTS_WO_BIO_PATH))

    artists_to_load = artist_names.difference(already_written_artist).difference(artists_wo_bio)

    print(f"Loading bios for {len(artists_to_load)}")
    for artist_name in artists_to_load:
        if artist_name in already_written_artist:
            continue
        print(f"Loading bio for {artist_name}")
        bio = get_artist_bio(artist_name)
        if bio:
            dump_artist_bio(artist_name, bio)
        else:
            save_artist_wo_bio(artist_name, artists_wo_bio_path)
