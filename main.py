from flask import Flask, jsonify
import utils

app = Flask(__name__)


@app.route('/movie/<title>')  # вьюшка, которая выводит один фильм
def movie(title):
    one_film = utils.search_by_title(title)
    return jsonify(one_film)


@app.route('/movie/<int:firs_number>/to/<int:second_number>')  # вьюшка, которая выводит несколько фильмов
def range_year(firs_number, second_number):                    # в зависимости от диапазона лет
    list_range_of_years = utils.range_of_years(firs_number, second_number)
    return jsonify(list_range_of_years)


@app.route('/rating/<group>')  # вьюшка, которая выводит один фильмы по соответствующей категории
def rating(group):
    if group == 'children':
        list_rating = utils.rating('G')
        return jsonify(list_rating)
    elif group == 'family':
        list_rating_1 = utils.rating('G')
        list_rating_2 = utils.rating('PG')
        list_rating_3 = utils.rating('PG-13')
        return jsonify(list_rating_1 + list_rating_2 + list_rating_3)
    else:
        list_rating_1 = utils.rating('R')
        list_rating_2 = utils.rating('NC-17')
        return jsonify(list_rating_1 + list_rating_2)


@app.route('/genre/<genre>')  # вьюшка, которая выводит один фильмы в зависимости от жанра
def films_genre(genre):
    list_by_genre = utils.films_by_genre(genre)
    return jsonify(list_by_genre)


if __name__ == '__main__':
    app.run(debug=True)
# Структура таблицы
# -----------------------
# show_id — id тайтла
# type — фильм или сериал
# title — название
# director — режиссер
# cast — основные актеры
# country — страна производства
# date_added — когда добавлен на Нетфликс
# release_year — когда выпущен в прокат
# rating — возрастной рейтинг
# duration — длительность
# duration_type — минуты или сезоны
# listed_in — список жанров и подборок
# description — краткое описание
# -----------------------
