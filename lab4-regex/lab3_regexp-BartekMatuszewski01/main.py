import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb',
                        password='adb2020');


def film_in_category(category: Union[int, str]) -> Union[pd.DataFrame, None]:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str, dokładnie taki jak podana wartość
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)
    dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(category, int):
        category_id = category

        df = pd.read_sql(f"""
            select f.title as "title", l.name as "languge", c.name as "category"
            from film f
            inner join language l on f.language_id = l.language_id
            inner join film_category fc on f.film_id = fc.film_id
            inner join category c on fc.category_id = c.category_id
            where c.category_id = {category_id}
            order by f.title, l.name
            
        """, connection)

        return df

    elif isinstance(category, str):
        df = pd.read_sql(f"""
                    select f.title as "title", l.name as "languge", c.name as "category"
                    from film f
                    inner join language l on f.language_id = l.language_id
                    inner join film_category fc on f.film_id = fc.film_id
                    inner join category c on fc.category_id = c.category_id
                    where c.name = '{category}'
                    order by f.title, l.name

        """, connection)
        return df

    return None


def film_in_category_case_insensitive(category: Union[int, str]) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli category jest int
        - name: jeżeli category jest str
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(category, int):
        category_id = category

        df = pd.read_sql(f"""
            select f.title as "title", l.name as "languge", c.name as "category"
            from film f
            inner join language l on f.language_id = l.language_id
            inner join film_category fc on f.film_id = fc.film_id
            inner join category c on fc.category_id = c.category_id
            where c.category_id = {category_id}
            order by f.title, l.name

        """, connection)

        return df

    elif isinstance(category, str):
        df = pd.read_sql(f"""
                    select f.title as "title", l.name as "languge", c.name as "category"
                    from film f
                    inner join language l on f.language_id = l.language_id
                    inner join film_category fc on f.film_id = fc.film_id
                    inner join category c on fc.category_id = c.category_id
                    where lower(c.name) = lower('{category}')
                    order by f.title, l.name

        """, connection)
        return df

    return None


def film_cast(title: str) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o obsadę filmu o dokładnie zadanym tytule.
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |
    |0	|Greg       |Chaplin    | 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    title (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(title, str):
        df = pd.read_sql(f"""
            select a.first_name, a.last_name
            from film f
            inner join film_actor fa on f.film_id = fa.film_id
            inner join actor a on a.actor_id = fa.actor_id 
            where f.title = '{title}'
            order by a.last_name, a.first_name
        """, connection)
        return df

    return None

def film_title_case_insensitive(words: list):
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuły filmów zawierających conajmniej jedno z podanych słów z listy words.
    Przykład wynikowej tabeli:
    |   |title              |
    |0	|Crystal Breaking 	| 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    words(list): wartość minimalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if not isinstance(words, list):
        return None

    words_str = '|'.join(words)

    df = pd.read_sql(f"""
    SELECT film.title 
    FROM film 
    WHERE title ~* '(^| )({words_str})""" + """{1,}($| )' 
    ORDER BY title""", con=connection)

    return df