import sqlite3

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

    # def show_rating_list(self, *args):
    #     cursor = self.load_data()
    #     raiting_parametrs = {
    #         "C"
    #     }
    #     sqlite_query = f"""
    #                     select title, rating, description
    #                     FROM netflix
    #                     WHERE rating in ('%{args}%')
    #                     LIMIT 10
    #     """
    #     cursor.execute(sqlite_query)
    #     result = cursor.fetchall()
    #
    #     return result
    #

# for row in executed_query:
#         actors_row = row[0].split(", ")
#         actors_lst.extend([actor for actor in actors_row if actor not in {first_actor, second_actor}])
#
#
#

# Формат запроса:
#
# /rating/children #(включаем сюда рейтинг G)
#
# /rating/family   #(G, PG, PG-13)
#
# /rating/adult    #(R, NC-17)


# netflix_dao = NetflixDAO("netflix.db")
# films = netflix_dao.show_rating_list("R")
# print(films)