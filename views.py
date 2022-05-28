import logging

from flask import Blueprint, render_template, request, abort, jsonify

from netflix_dao import NetflixDAO

# Создаем блупринт
api_netflix_blueprint = Blueprint('api_netflix_blueprint', __name__)

# Создаем DAO
netflix_dao = NetflixDAO("netflix.db")

logger = logging.getLogger("basic")

# Создаем вьюшку с выводом данных про фильм
@api_netflix_blueprint.route('/movie/<title>')
def netflix_title(title):
    logger.debug(f"Запрошен фильм c названием {title} через API")
    film = netflix_dao.search_film(title)
    return jsonify(film)

# Создаем вьюшку с выводом фильмов в заданном диапазоне
@api_netflix_blueprint.route('/movie/<int:min_release_year>/to/<int:max_release_year>')
def netflix_range_of_release(min_release_year, max_release_year):
    logger.debug(f"Запрошен вывод фильмов в диапазоне от {min_release_year} года до {max_release_year}")
    range_of_films = netflix_dao.range_of_release(min_release_year, max_release_year)
    return jsonify(range_of_films)

# Создаем вьюшку с выводом фильмов по категории
@api_netflix_blueprint.route('/rating/<category>')
def get_movies_by_rating(category):
    logger.debug(f"Запрошен вывод фильмов категории {category}")
    movies_by_rating = netflix_dao.show_rating_list(category)
    return jsonify(movies_by_rating)


# Создаем вьюшку с выводом фильмов по заданному жанру
@api_netflix_blueprint.route('/genre/<genre>')
def get_movies_by_genre(genre):
    logger.debug(f"Запрошен вывод фильмов жанра {genre}")
    movies_by_genre = netflix_dao.show_listed_in(genre)
    return jsonify(movies_by_genre)

