# ddl.py
"""
Модуль ddl.py
Отвечает за создание таблиц в базе данных DuckDB и заполнение их данными из файлов источников.
"""

import duckdb
import pandas as pd
import os

def create_tables(database_path='my.db', tables_sql_path='queries/create_tables.sql'):
    """
    Создает таблицы в базе данных DuckDB, выполняя SQL-скрипт.

    Параметры:
    - database_path (str): Путь к файлу базы данных DuckDB.
    - tables_sql_path (str): Путь к SQL-скрипту, создающему таблицы.
    """
    con = duckdb.connect(database=database_path)

    with open(tables_sql_path, 'r') as f:
        create_tables_sql = f.read()

    con.execute(create_tables_sql)

    con.close()

def load_data(database_path='my.db', source_folder='source'):
    """
    Загружает данные из CSV-файлов в папке источника в соответствующие таблицы базы данных.

    Параметры:
    - database_path (str): Путь к файлу базы данных DuckDB.
    - source_folder (str): Путь к папке, содержащей исходные CSV-файлы.
    """
    con = duckdb.connect(database=database_path)

    data_files = {
        'brands': 'brands.csv',
        'categories': 'categories.csv',
        'stores': 'stores.csv',
        'staffs': 'staffs.csv',
        'customers': 'customers.csv',
        'products': 'products.csv',
        'orders': 'orders.csv',
        'order_items': 'order_items.csv',
        'stocks': 'stocks.csv'
    }

    for table_name, file_name in data_files.items():
        file_path = os.path.join(source_folder, file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            con.execute(f"delete from {table_name};")
            con.execute(f"insert into {table_name} select * from df;")
            print(f"Данные загружены в таблицу '{table_name}' из файла '{file_name}'.")
            
        else:
            print(f"Файл '{file_name}' не найден в папке источника '{source_folder}'.")

    con.close()

def create_views(database_path='my.db', views_sql_path='queries/create_views.sql'):
    """
    Создает представления (вьюшки) в базе данных DuckDB, выполняя SQL-скрипт.

    Параметры:
    - database_path (str): Путь к файлу базы данных DuckDB.
    - views_sql_path (str): Путь к SQL-скрипту, создающему представления.
    """
    con = duckdb.connect(database=database_path)

    with open(views_sql_path, 'r') as f:
        create_views_sql = f.read()

    con.execute(create_views_sql)

    con.close()

if __name__ == '__main__':
    print("Создание таблиц...")
    create_tables()
    print("Таблицы успешно созданы.")

    print("Загрузка данных в таблицы...")
    load_data()
    print("Данные успешно загружены.")

    print("Создание представлений...")
    create_views()
    print("Представления успешно созданы.")
