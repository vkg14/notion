from os.path import dirname, realpath, join

from lib.imdb_tools import *
from lib.notion_tools import *
from private_credentials import URL

logging.basicConfig(
    level=logging.INFO,
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
    cv = client.get_collection_view(URL)
    # We must supply a limit here as per: https://github.com/jamalex/notion-py/pull/294#pullrequestreview-607510490
    notion_results = cv.collection.get_rows(limit=-1)
    for count, result in enumerate(notion_results, 1):
        if result.processed:
            # skip anything that's been processed
            continue
        movie = get_movie_from_title(result.name)
        if not movie:
            # Could not find this movie
            logging.warning(f"Couldn't find '{result.name}'")
            continue
        logging.info(f"Found {movie.get('title')} for {result.name}")
        result.year = get_year(movie)
        logging.info(f'Added year: {result.year}')
        image_url = get_poster_url(movie)
        add_page_cover(result, image_url)
        logging.info(f'Added image for {result.name}')
        result.plot_outline = get_plot_outline(movie)
        result.processed = True
    logging.info(f'Total count: {count}')

if __name__ == '__main__':
    update_movies()
