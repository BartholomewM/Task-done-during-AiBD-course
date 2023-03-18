import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb',
                        password='adb2020')


def film_in_category(category_id: int) -> Union[pd.DataFrame, None]:
    """ Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego id kategorii.
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|

    Tabela wynikowa ma być posortowana po tylule filmu i języku.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania

    """

    if isinstance(category_id, int):
        return pd.read_sql(f"""
            select
            f.title as title,
            l.name as languge,
            c.name as category    
            
            from
            film f
            
            inner join language l
            on f.language_id = l.language_id 
            
            inner join film_category fc
            on fc.film_id = f.film_id
            
            inner join category c
            on fc.category_id = c.category_id
            
            
            where c.category_id = {category_id}
            
            order by f.title ASC
            
            """,
                           connection)

    return None


def number_films_in_category(category_id: int) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów w zadanej kategori przez id kategorii.
    Przykład wynikowej tabeli:
    |   |category   |count|
    |0	|Action 	|64	  |

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if isinstance(category_id, int):
        return pd.read_sql(f"""
            SELECT
            c.name as category,
            COUNT(f.title) as "count"
            
            FROM
            film f

            INNER JOIN film_category fc
            ON fc.film_id = f.film_id

            INNER JOIN category c
            ON c.category_id = fc.category_id  

            WHERE c.category_id = {category_id}

            GROUP BY c.name

            """,
                           connection)

    return None


def number_film_by_length(min_length: Union[int, float] = 0, max_length: Union[int, float] = 1e6):
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów o dla poszczegulnych długości
    pomiędzy wartościami min_length a max_length.
    Przykład wynikowej tabeli:
    |   |length     |count|
    |0	|46 	    |64	  |

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    min_length (int,float): wartość minimalnej długości filmu
    max_length (int,float): wartość maksymalnej długości filmu

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if (isinstance(min_length, int) or isinstance(min_length, float)) \
            and (isinstance(max_length, int) or isinstance(max_length, float))\
            and max_length > min_length:
        return pd.read_sql(f"""
            SELECT
            f.length,
            count(*) as "count"

            FROM
            film f

            GROUP BY f.length
            having ({min_length} <= f.length
            and f.length <= {max_length})
            """, connection)
    return None


def client_from_city(city: str) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o listę klientów z zadanego miasta przez wartość city.
    Przykład wynikowej tabeli:
    |   |city	    |first_name	|last_name
    |0	|Athenai	|Linda	    |Williams
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    city (str): nazwa miaste dla którego mamy sporządzić listę klientów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if isinstance(city, str):
        return pd.read_sql(f"""
            SELECT
            c.city as city,
            cu.first_name,
            cu.last_name

            FROM
            city c

            inner join address a 
            on c.city_id = a.city_id
            
            inner join customer cu
            on a.address_id = cu.address_id
            
            where (c.city = '{city}')
            
            group by cu.last_name, cu.first_name, city
                        
            """, connection)
    return None


def avg_amount_by_length(length: Union[int, float]) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o średnią wartość wypożyczenia filmów dla zadanej długości length.
    Przykład wynikowej tabeli:
    |   |length |avg
    |0	|48	    |4.295389
    
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    length (int,float): długość filmu dla którego mamy pożyczyć średnią wartość wypożyczonych filmów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(length, int) or isinstance(length, float):
        return pd.read_sql(f"""
                select
                f.length,
                AVG(p.amount) as "avg" 
                
                from
                film f

                inner join inventory i 
                on f.film_id = i.film_id
                
                inner join rental r
                on i.inventory_id = r.inventory_id               

                inner join payment p
                on p.rental_id = r.rental_id

                where (f.length = {length} )
                
                group by f.length

                """, connection)
    return None


def client_by_sum_length(sum_min: Union[int, float]) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o sumaryczny czas wypożyczonych filmów przez klientów powyżej zadanej wartości .
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |sum
    |0  |Brian	    |Wyman  	|1265
    
    Tabela wynikowa powinna być posortowane według sumy, imienia i nazwiska klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    sum_min (int,float): minimalna wartość sumy długości wypożyczonych filmów którą musi spełniać klient
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(sum_min, int) or isinstance(sum_min, float):
        return pd.read_sql(f"""
                select distinct 
                cus.first_name,
                cus.last_name ,               
                sum(f.length)

                from
                film f

                inner join inventory i 
                on f.film_id = i.film_id

                inner join rental r
                on i.inventory_id = r.inventory_id               

                inner join customer cus
                on cus.customer_id = r.customer_id
                                
                group by cus.first_name, cus.last_name
                
                having sum(f.length) >= {sum_min}
                
                order by sum(f.length), cus.last_name
                
                """, connection)
    return None


def category_statistic_length(name: str) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o statystykę długości filmów w kategorii o zadanej nazwie.
    Przykład wynikowej tabeli:
    |   |category   |avg    |sum    |min    |max
    |0	|Action 	|111.60 |7143   |47 	|185
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    name (str): Nazwa kategorii dla której ma zostać wypisana statystyka
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if isinstance(name, str):
        return pd.read_sql(f"""
            SELECT
            c.name as category,
            AVG(f.length) as "avg",
            SUM(f.length) as "sum",
            MIN(f.length) as "min",
            MAX(f.length) as "max"
                        
            FROM
            film f

            INNER JOIN film_category fc
            ON fc.film_id = f.film_id

            INNER JOIN category c
            ON c.category_id = fc.category_id  

            WHERE c.name = '{name}'

            GROUP BY c.name

                """, connection)
    return None
