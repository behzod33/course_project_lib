# etl.py
"""
Модуль etl.py
Отвечает за получение данных из базы данных DuckDB для создания pandas DataFrame.
"""

import duckdb

def fetch_data(query, database_path='my.db'):
    """
    Выполняет SQL-запрос к базе данных и возвращает результат в виде pandas DataFrame.

    Параметры:
    - query (str): SQL-запрос для выполнения.
    - database_path (str): Путь к файлу базы данных DuckDB.

    Возвращает:
    - DataFrame: Результат выполнения запроса.
    """
    con = duckdb.connect(database=database_path)
    
    df = con.execute(query).fetchdf()
    
    con.close()
    
    return df
