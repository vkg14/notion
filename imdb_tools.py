import logging
from operator import itemgetter
import string

from imdb import IMDb

from utils import levenshtein


def _format_title(title: str):
    """
    Formatting the movie title for comparisons with other titles. Currently,
    this just entails simply lowercasing the string and removing punctuation.
    """
    return title.lower().translate(str.maketrans('', '', string.punctuation))

def get_movie_from_title(title: str):
    imdb_client = IMDb()
    choices = [movie for movie in imdb_client.search_movie(title) \
            if movie.get('kind', '').lower() == 'movie']
    if not choices:
        # No valid choices
        return None
    # Find the closest movie by title name levenshtein distance
    scores = [levenshtein(_format_title(movie.get('title', '')),
                          _format_title(title)) for movie in choices]
    logging.warning(f'Choices:\n{choices}')
    logging.warning(f'Scores:\n{scores}')
    best_choice = choices[scores.index(min(scores))]
    logging.warning(f'Best Choice: {best_choice}')
    # The search above yields a truncated form of the movie class
    # To get the full form, we need to get_movie using movieID
    return imdb_client.get_movie(best_choice.movieID)


def get_year(movie) -> int:
    return movie.get('year')


def get_poster_url(movie):
    return movie.get('full-size cover url') or movie.get('cover url')


def get_plot_outline(movie) -> str:
    return movie.get('plot outline')
