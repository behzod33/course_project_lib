-- вьюшка: детали заказов
create view order_details as
select 
    o.order_id,
    o.order_date,
    o.required_date,
    c.first_name || ' ' || c.last_name as customer_name,
    s.store_name,
    p.product_name,
    cat.category_name,
    oi.quantity,
    oi.list_price,
    oi.discount,
    (oi.quantity * oi.list_price * (1 - oi.discount)) as total_price
from orders o
join customers c on o.customer_id = c.customer_id
join order_items oi on o.order_id = oi.order_id
join products p on oi.product_id = p.product_id
join stores s on o.store_id = s.store_id
join categories cat on p.category_id = cat.category_id;


-- вьюшка: остатки товаров по магазинам
create view stock_summary as
select 
    s.store_name,
    p.product_name,
    st.quantity
from stocks st
join stores s on st.store_id = s.store_id
join products p on st.product_id = p.product_id;

-- вьюшка: продажи по категориям
create view sales_by_category as
select 
    cat.category_name,
    sum(oi.quantity * oi.list_price * (1 - oi.discount)) as total_sales
from order_items oi
join products p on oi.product_id = p.product_id
join categories cat on p.category_id = cat.category_id
group by cat.category_name;

-- вьюшка: активные сотрудники по магазинам
create view active_staffs as
select 
    s.store_name,
    st.first_name || ' ' || st.last_name as staff_name,
    st.email,
    st.phone,
    st.active
from staffs st
join stores s on st.store_id = s.store_id
where st.active = 1;

-- вьюшка: заказы за последние 30 дней
create view recent_orders as
select 
    o.order_id,
    o.order_date,
    c.first_name || ' ' || c.last_name as customer_name,
    p.product_name,
    oi.quantity,
    oi.list_price,
    (oi.quantity * oi.list_price * (1 - oi.discount)) as total_price
from orders o
join customers c on o.customer_id = c.customer_id
join order_items oi on o.order_id = oi.order_id
join products p on oi.product_id = p.product_id
where o.order_date >= current_date - interval '30 days';
