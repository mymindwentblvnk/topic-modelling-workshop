import csv
from os import listdir

BIOS_DIRECTORY = 'data/raw/bios'


def load_artist_names(path: str) -> list:
    return [f.replace('-bio.txt', '') for f in listdir(path) if f.endswith('-bio.txt')]


def read_bio(artist_name: str) -> str:
    with open(f'data/raw/bios/{artist_name}-bio.txt', 'r') as bio:
        return bio.read().replace("\n", " ")


if __name__ == '__main__':
    with open('data/data.csv', 'w', newline='') as out:
        writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        artist_names = load_artist_names(BIOS_DIRECTORY)
        for index, artist_name in enumerate(artist_names, 1):
            print(f"{index}/{len(artist_names)}")
            bio = read_bio(artist_name)
            writer.writerow((artist_name, bio))
