from json import JSONDecodeError
import logging
from os.path import dirname, realpath, join
from os import path
import time

from imdb_tools import *
from notion_tools import *
from private_credentials import URL

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(join(dirname(realpath(__file__)), 'debug.log')),
        logging.StreamHandler()
    ]
)


def unprocess_all(rows):
    for row in rows:
        row.processed = False


def update_movies():
    client = get_client()
    cv = get_collection_view(client, URL)
    notion_results = cv.collection.get_rows()
    total_count = 0
    for count, result in enumerate(notion_results, 1):
        total_count = count
        if result.processed:
            # skip anything that's been processed
            continue
        movie = get_movie_from_title(result.name)
        if not movie:
            # Could not find this movie
            logging.warning(f"Couldn't find '{result.name}'")
            continue
        logging.warning(f"Found {movie.get('title')} for {result.name}")
        result.year = get_year(movie)
        logging.warning(f'Added year: {result.year}')
        image_url = get_poster_url(movie)
        add_page_cover(result, image_url)
        ####### Leaving for posterity
        #try:
        #   add_gallery_embedded_image(result, image_url)
        #except JSONDecodeError:
        #    # This was happening when I used EmbedBlock rather than ImageBlock
        #    # Embedding an image with an EmbedBlock doesn't work because
        #    # of some type-based data validation that's happening
        #    logging.warning(f"Got a JSON Decode Error for {result.name}")
        ####### Leaving for posterity
        logging.warning(f'Added image for {result.name}')
        result.plot_outline = get_plot_outline(movie)
        result.processed = True
    logging.warning(f"Total count: {total_count}")

if __name__ == '__main__':
    update_movies()
