import json
import sqlite3


def search_by_title(title):
    """
    поиск по названию
    :param title: название (str)
    :return: один фильм (dict)
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                    SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE title LIKE '%{title}%'
                    AND country != ''
                    AND type = 'Movie'
                    ORDER BY release_year DESC 
                    LIMIT 1
                    """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        results = executed_query
        one_film = {}
        for result in results:
            one_film['title'] = result[0]
            one_film['country'] = result[1]
            one_film['release_year'] = result[2]
            one_film['genre'] = result[3]
            one_film['description'] = result[4]
        return one_film

# Проверка функции
# print(search_by_title("Witness"))


def range_of_years(firs_number, second_number):
    """
    поиск по диапазону лет
    :param firs_number: первое число (int)
    :param second_number: второе число (int)
    :return: список фильмов
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE title != ''
                    AND release_year BETWEEN {firs_number} AND {second_number}
                    AND type = 'Movie'
                    GROUP BY title, release_year 
                    ORDER BY release_year DESC
                    LIMIT 100
                    """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        results = executed_query
        list_range_of_years = []
        for result in results:
            list_range_of_years.append({'title': result[0],
                                        'release_year': result[1]
                                        })

        return list_range_of_years

# Проверка функции
# print(range_of_years(2010, 2011))


def rating(group):
    """
    поиск по рейтингу
    :param group: буквенное значение рейтинга
    :return: список фильмов
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                    SELECT title, rating, release_year
                    FROM netflix
                    WHERE title != ''
                    AND release_year != ''
                    AND rating = '{group}'
                    GROUP BY title, rating, release_year 
                    """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        results = executed_query
        list_rating = []
        for result in results:
            list_rating.append({'title': result[0],
                                'rating': result[1],
                                'release_year': result[2]
                                })

        return list_rating

# Проверка функции
# print(rating('NC-17'))


def films_by_genre(listed_in):
    """
    поиск по жанру
    :param listed_in: жанр
    :return: список фльмов с этим жанром
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE title != ''
                    AND release_year != ''
                    AND description != ''
                    AND listed_in LIKE '%{listed_in}%'
                    GROUP BY title, description
                    ORDER BY release_year DESC
                    LIMIT 10
                    """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        results = executed_query
        list_by_genre = []
        for result in results:
            list_by_genre.append({'title': result[0],
                                  'description': result[1]
                                  })
        return list_by_genre

# Проверка функции
# print(films_by_genre('Comedies'))


def actors(first_actor, second_actor):
    """
    поиск актеров, с которыми они играли больше двух раз
    :param first_actor: первый актер (str)
    :param second_actor: второй актер (str)
    :return: список актеров
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                    SELECT "cast"
                    FROM netflix
                    WHERE "cast" LIKE '%{first_actor}%{second_actor}%'
                    """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        results = executed_query
        list_one = []

        for i in range(len(results)):
            one_replace = results[i][0].replace(f'{first_actor}, ', '')
            two_replace = one_replace.replace(f'{second_actor}, ', '')
            list_one.append(two_replace)

        new_str = (', ').join(list_one)
        new_list = new_str.split(', ')

        recurring_actors = []

        for i in range(len(new_list)):
            if (new_list[i] in new_list[i + 1:]) and not (new_list[i] in recurring_actors):
                recurring_actors.append(new_list[i])
        return recurring_actors

# Проверка функции
# print(actors('Jack Black', 'Dustin Hoffman'))


def total_description(type, release_year, listed_in):
    """
    поиск фильмов
    :param type: фильм или сериал
    :param release_year: когда выпущен в прокат
    :param listed_in: список жанров и подборок
    :return: загружает в JSON-файл все подходящие фильмы
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE title != ''
                    AND type = '{type}'
                    AND release_year = '{release_year}'
                    AND listed_in LIKE '%{listed_in}%'
                    """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        results = executed_query
        list_total_description = []
        for result in results:
            list_total_description.append({'type': result[0],
                                           'description': result[1]
                                           })
        with open('total_description.json', 'w') as file:
            json.dump(list_total_description, file)
        return list_total_description

# Проверка функции
# total_description('Movie', '2010', 'Comedies')
