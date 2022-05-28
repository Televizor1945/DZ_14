import sqlite3
from collections import Counter


class NetflixDAO:

    def __init__(self, path_netflix):
        """ При создании экземпляра DAO нужно указать путь к файлу с данными"""
        self.path_netflix = path_netflix

    def load_data(self):
        """ Создаём подключение к базе данных netflix"""
        with sqlite3.connect(self.path_netflix) as connection:
            cursor = connection.cursor()
        return cursor

    def search_film(self, film_name):
        """  функция, которая принимает название фильма и возвращет его описание"""
        cursor = self.load_data()
        sqlite_query = f"""
                        select title, country, MAX(release_year), listed_in, description, MAX(date_added)
                        FROM netflix
                        WHERE title LIKE '%{film_name}%'
        """
        cursor.execute(sqlite_query)
        result = cursor.fetchall()

        result_search = {
        		"title": result[0][0],
        		"country": result[0][1],
        		"release_year": result[0][2],
        		"genre": result[0][3],
        		"description": result[0][3]
        }

        return result_search

    def range_of_release(self, min_release_year, max_release_year):
        """  функция, которая принимает два года (период от и по) и возвращет название фильмов в этот период"""
        cursor = self.load_data()
        sqlite_query = f"""
                        select title, release_year
                        FROM netflix
                        WHERE release_year BETWEEN {min_release_year} AND {max_release_year}
                        LIMIT 100
        """
        cursor.execute(sqlite_query)

        result = []
        for item in cursor.fetchall():
            result.append(
                {
                    "title": item[0],
                    "release_year": item[1]
                }
            )

        return result

    def show_rating_list(self, rating):
        """  функция, которая принимает список рейтингов и возвращала данные по ним (название фильма, рейтинг, описание)"""
        cursor = self.load_data()
        rating_parameters = {
            "children": "'G'",
            "family": "'G', 'PG', 'PG-13'",
            "adult": "'G', 'NC-17'",
        }
        if rating not in rating_parameters:
            return "Переданной группы не существует"
        sqlite_query = f"""
                        select title, rating, description
                        FROM netflix
                        WHERE rating in ({rating_parameters[rating]})
                        LIMIT 100
        """
        cursor.execute(sqlite_query)
        result = cursor.fetchall()
        result_list = []
        for movie in result:
            result_list.append({
                "title": movie[0],
                "rating": movie[1],
                "description": movie[2],
            })

        return result_list

    def show_listed_in(self, genre):
        """  функция, которая принимает название жанра и возвращет список 10 самых свежих фильмов данного жанра"""
        cursor = self.load_data()
        sqlite_query = f"""select title, description, listed_in
                        FROM netflix
                        WHERE listed_in LIKE '%{genre}%'
        """
        cursor.execute(sqlite_query)
        result = cursor.fetchall()
        result_list_genre = []
        for item in result:
            result_list_genre.append(
                {
                    "title": item[0],
                    "description": item[1]
                }
            )

        return result

    def cast_partners(self, actor1, actor2):
        """  функция, которая принимает в качестве аргумента имена двух актеров, сохраняет
        всех актеров из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз"""
        cursor = self.load_data()
        sqlite_query = f"""select `cast`
                        FROM netflix
                        WHERE `cast` LIKE '%{actor1}%' and `cast` LIKE '%{actor2}%'
        """
        cursor.execute(sqlite_query)
        result = cursor.fetchall()
        actors_list = []
        for cast in result:
            actors_list.extend(cast[0].split(', '))
        counter = Counter(actors_list)
        result_list = []
        for actor, count in counter.items():
            if actor not in [actor1, actor2] and count > 2:
                result_list.append(actor)

        return result_list


    def search_movie_by_param(self, movie_type, release_year, genre):
        """  функция, которая принимает в качестве аргумента тип картины, год выпуска и жанр - затем выдаёт список подходящих фильмов в JSON"""
        cursor = self.load_data()
        sqlite_query = f"""select title, description
                        FROM netflix
                        WHERE netflix.type = '{movie_type}'
                        and release_year = '{release_year}'
                        and listed_in LIKE '%{genre}%'
        """
        cursor.execute(sqlite_query)
        result = cursor.fetchall()
        result_list = []
        for movie in result:
            result_list.append({"title": movie[0],
                    "description": movie[1]})

        return result_list

