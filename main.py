import streamlit as st
import pandas as pd
import plotly.express as px
from etl import fetch_data
import re

# Функция для защиты от SQL инъекций
def escape_sql(value):
    return re.sub(r"'", "''", value)

@st.cache_data
def load_data(query):
    """
    Кеширование и загрузка данных с использованием запроса SQL.
    """
    try:
        orders_df = fetch_data(query)
        return orders_df
    except Exception as e:
        st.error(f"Ошибка при загрузке данных: {e}")
        return pd.DataFrame()

def main():
    st.set_page_config(page_title='Дашборд Продаж', layout='wide')
    st.title('Интерактивный Дашборд Продаж')
    
    st.sidebar.header('Фильтры')
    
    date_range = st.sidebar.date_input('Период заказа', [])
    
    customer_name = st.sidebar.text_input('Имя клиента')
    
    store_query = "select distinct store_name from order_details;"
    store_list = fetch_data(store_query)['store_name'].dropna().tolist()
    store_name = st.sidebar.selectbox('Название магазина', options=['Все'] + store_list)
    
    product_query = "select distinct product_name from order_details;"
    product_list = fetch_data(product_query)['product_name'].dropna().tolist()
    product_name = st.sidebar.multiselect('Название продукта', options=product_list)
    
    category_query = "select distinct category_name from order_details;"
    category_list = fetch_data(category_query)['category_name'].dropna().tolist()
    category_name = st.sidebar.multiselect('Категория продукта', options=category_list)
    
    # Формирование условий фильтрации
    conditions = []
    if date_range and len(date_range) == 2:
        start_date = date_range[0].strftime('%Y-%m-%d')
        end_date = date_range[1].strftime('%Y-%m-%d')
        conditions.append(f"order_date between '{start_date}' and '{end_date}'")
    elif date_range and len(date_range) == 1:
        single_date = date_range[0].strftime('%Y-%m-%d')
        conditions.append(f"order_date = '{single_date}'")
    
    if customer_name:
        safe_customer_name = escape_sql(customer_name)
        conditions.append(f"customer_name ilike '%{safe_customer_name}%'")
    
    if store_name and store_name != 'Все':
        safe_store_name = escape_sql(store_name)
        conditions.append(f"store_name = '{safe_store_name}'")
    
    if product_name:
        safe_product_names = [escape_sql(name) for name in product_name]
        product_names = "', '".join(safe_product_names)
        conditions.append(f"product_name in ('{product_names}')")
    
    if category_name:
        safe_category_names = [escape_sql(name) for name in category_name]
        category_names = "', '".join(safe_category_names)
        conditions.append(f"category_name in ('{category_names}')")
    
    where_clause = ''
    if conditions:
        where_clause = 'where ' + ' and '.join(conditions)
    
    query_orders = f'''
    select *
    from order_details
    {where_clause}
    order by order_date desc
    '''
    
    st.write("Условия фильтрации:", conditions)
    st.write("SQL-запрос для получения данных:", query_orders)
    
    orders_df = load_data(query_orders)
    
    st.subheader('Детали заказов')
    st.dataframe(orders_df)
    
    if not orders_df.empty:
        # Оконные функции и дополнительные метрики
        orders_df['product_sales_rank'] = orders_df.groupby('product_name')['total_price'].transform('sum')
        orders_df['product_sales_rank'] = orders_df['product_sales_rank'].rank(method='dense', ascending=False)

        # Скользящее среднее по продажам
        orders_df['moving_avg_sales'] = orders_df.groupby('order_date')['total_price'].transform(lambda x: x.rolling(3).mean())

        orders_df['store_sales_rank'] = orders_df.groupby('store_name')['total_price'].transform('sum')
        orders_df['store_sales_rank'] = orders_df['store_sales_rank'].rank(method='dense', ascending=False)

        orders_df['avg_discount'] = orders_df.groupby('product_name')['discount'].transform('mean')
        
        # График: Объем продаж по продуктам
        sales_by_product = orders_df.groupby('product_name')['total_price'].sum().reset_index()
        fig1 = px.bar(sales_by_product, x='product_name', y='total_price', title='Общий объем продаж по продуктам')
        st.plotly_chart(fig1, use_container_width=True)
        
        # График: Объем продаж по клиентам
        sales_by_customer = orders_df.groupby('customer_name')['total_price'].sum().reset_index()
        fig2 = px.bar(sales_by_customer, x='customer_name', y='total_price', title='Общий объем продаж по клиентам')
        st.plotly_chart(fig2, use_container_width=True)
        
        # График: Количество заказов по датам
        orders_over_time = orders_df.groupby('order_date')['order_id'].nunique().reset_index()
        fig3 = px.line(orders_over_time, x='order_date', y='order_id', title='Количество заказов по датам')
        st.plotly_chart(fig3, use_container_width=True)
        
        # График: Средняя скидка по продуктам
        discount_by_product = orders_df.groupby('product_name')['avg_discount'].mean().reset_index()
        fig4 = px.bar(discount_by_product, x='product_name', y='avg_discount', title='Средняя скидка по продуктам')
        st.plotly_chart(fig4, use_container_width=True)
        
        # График: Объем продаж по магазинам
        sales_by_store = orders_df.groupby('store_name')['total_price'].sum().reset_index()
        fig5 = px.bar(sales_by_store, x='store_name', y='total_price', title='Общий объем продаж по магазинам')
        st.plotly_chart(fig5, use_container_width=True)
        
        # График: Объем продаж по категориям
        sales_by_category = orders_df.groupby('category_name')['total_price'].sum().reset_index()
        fig6 = px.bar(sales_by_category, x='category_name', y='total_price', title='Общий объем продаж по категориям')
        st.plotly_chart(fig6, use_container_width=True)

        # Таблица рангов продуктов
        st.subheader("Ранг продуктов по объему продаж")
        st.write(orders_df[['product_name', 'product_sales_rank']].drop_duplicates().sort_values(by='product_sales_rank'))

        # Таблица рангов магазинов
        st.subheader("Ранг магазинов по объему продаж")
        st.write(orders_df[['store_name', 'store_sales_rank']].drop_duplicates().sort_values(by='store_sales_rank'))

    else:
        st.write('Нет данных для отображения с выбранными фильтрами.')

if __name__ == '__main__':
    main()
