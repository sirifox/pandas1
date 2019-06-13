import pandas as pd
import numpy as np


# **Задание 1**

# Используем файл keywords.csv.

# Необходимо написать гео-классификатор, который каждой строке сможет выставить географическую принадлежность определенному региону. Т. е. если поисковый запрос содержит название города региона, то в столбце 'region' пишется название этого региона. Если поисковый запрос не содержит названия города, то ставим 'undefined'.

# Правила распределения по регионам Центр, Северо-Запад и Дальний Восток:

# Результат классификации запишите в отдельный столбец region.

geo_data = {

    'Центр': ['москва', 'тула', 'ярославль'],

    'Северо-Запад': ['петербург', 'псков', 'мурманск'],

    'Дальний Восток': ['владивосток', 'сахалин', 'хабаровск']

}

def geo_search(phrase):
  for word in phrase.split():
    wor = word.lower() 
    for reg in geo_data:
      if word in geo_data[reg]:
        return reg
  return 'undefined'
  
keywords = pd.read_csv('keywords.csv')

keywords['region'] = [geo_search(phrase) for phrase in keywords['keyword']]

keywords.to_csv('k2.csv')
print(keywords)


# **Задание 2**

# Напишите функцию, которая классифицирует фильмы из материалов занятия по следующим правилам:
#     - оценка 2 и меньше - низкий рейтинг
#     - оценка 4 и меньше - средний рейтинг
#     - оценка 4.5 и 5 - высокий рейтинг

# Результат классификации запишите в столбец class

movies = pd.read_csv('movies.csv', usecols=[0, 1])
ratings = pd.read_csv('ratings.csv', usecols=[1, 2])
movies.head()
ratings.head()
# ratings = ratings.groupby(movieId).agg({'rating': 'mean'}).head()
mov_rat = pd.merge(ratings.groupby('movieId').agg({'rating': 'mean'}), movies, 'left' ,on='movieId')


def rate_class(rate):
  if rate >= 4.5:
    return 'высокий рейтинг'
  elif rate <= 2:
    return 'низкий рейтинг'
  else:
    return 'средний рейтинг'


mov_rat['class'] = [rate_class(rate) for rate in mov_rat['rating']]

print(mov_rat)

# **Задание 3**

# Посчитайте среднее значение Lifetime киноманов (пользователи, которые поставили 100 и более рейтингов). Под Lifetime понимается разница между максимальным и минимальным значением timestamp для каждого пользователя. Ответ дайте в днях.

ratings = pd.read_csv('ratings.csv', usecols=[0, 3])

uniq_users = [us for us in pd.unique(ratings.userId) if ratings['userId'].value_counts()[us]>=100]

lifetime = int(np.mean([ratings[ratings['userId'] == us]['timestamp'].max() - ratings[ratings['userId'] == us]['timestamp'].min() for us in uniq_users ]) / 86400)


print(lifetime)

# **Задание 4**

# Есть мнение, что "раньше снимали настоящее кино, не то что сейчас". Ваша задача проверить это утверждение, используя файлы с рейтингами фильмов из материалов занятия. Т. е. проверить верно ли, что с ростом года выпуска фильма его средний рейтинг становится ниже.

# При этом мы не будем затрагивать субьективные факторы выставления этих рейтингов, а пройдемся по следующему алгоритму:

# 1. В переменную years запишите список из всех годов с 1950 по 2010.

# 2. Напишите функцию production_year, которая каждой строке из названия фильма выставляет год выпуска. Не все названия фильмов содержат год выпуска в одинаковом формате, поэтому используйте следующий алгоритм:
#     - для каждой строки пройдите по всем годам списка years
#     - если номер года присутствует в названии фильма, то функция возвращает этот год как год выпуска
#     - если ни один из номеров года списка years не встретился в названии фильма, то возвращается 1900 год

# 3. Запишите год выпуска фильма по алгоритму пункта 2 в новый столбец 'year'

# 4. Посчитайте средний рейтинг всех фильмов для каждого значения столбца 'year' и отсортируйте результат по убыванию рейтинга


def production_year(name, year_list):
  for year in year_list:
    if str(year) in name:
      return year
  return 1900

movies = pd.read_csv('movies.csv', usecols=[0, 1])
ratings = pd.read_csv('ratings.csv', usecols=[1, 2])
movies.head()
ratings.head()

mov_rat = pd.merge(ratings.groupby('movieId').agg({'rating': 'mean'}), movies, 'left' ,on='movieId')

years = list(range(1950,2011))

mov_rat['year'] = [production_year(film, years) for film in mov_rat['title']]
mov_rat = mov_rat.groupby('year').agg({'rating': 'mean'}).sort_values(by='rating',ascending =False)

print(mov_rat)
