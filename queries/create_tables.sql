-- создание таблицы брендов
create table brands (
    brand_id integer primary key,
    brand_name varchar not null
);

-- создание таблицы категорий
create table categories (
    category_id integer primary key,
    category_name varchar not null
);

-- создание таблицы магазинов (stores)
create table stores (
    store_id integer primary key,
    store_name varchar not null,
    phone varchar,
    email varchar,
    street varchar,
    city varchar,
    state varchar,
    zip_code varchar
);

-- создание таблицы сотрудников (staffs)
create table staffs (
    staff_id integer primary key,
    first_name varchar not null,
    last_name varchar not null,
    email varchar,
    phone varchar,
    active integer default 1,
    store_id integer,
    manager_id integer,
    foreign key (store_id) references stores(store_id)
);

-- создание таблицы клиентов (customers)
create table customers (
    customer_id integer primary key,
    first_name varchar not null,
    last_name varchar not null,
    phone varchar,
    email varchar,
    street varchar,
    city varchar,
    state varchar,
    zip_code varchar
);

-- создание таблицы продуктов (products)
create table products (
    product_id integer primary key,
    product_name varchar not null,
    brand_id integer,
    category_id integer,
    model_year integer,
    list_price decimal(10, 2),
    foreign key (brand_id) references brands(brand_id),
    foreign key (category_id) references categories(category_id)
);

-- создание таблицы заказов (orders)
create table orders (
    order_id integer primary key,
    customer_id integer not null,
    order_status integer,
    order_date date,
    required_date date,
    shipped_date date,
    store_id integer,
    staff_id integer,
    foreign key (customer_id) references customers(customer_id),
    foreign key (store_id) references stores(store_id),
    foreign key (staff_id) references staffs(staff_id)
);

-- создание таблицы позиций заказов (order_items)
create table order_items (
    order_id integer not null,
    item_id integer not null,
    product_id integer not null,
    quantity integer not null,
    list_price decimal(10, 2) not null,
    discount decimal(4, 2) default 0,
    primary key (order_id, item_id),
    foreign key (order_id) references orders(order_id),
    foreign key (product_id) references products(product_id)
);

-- создание таблицы запасов (stocks)
create table stocks (
    store_id integer not null,
    product_id integer not null,
    quantity integer not null,
    primary key (store_id, product_id),
    foreign key (store_id) references stores(store_id),
    foreign key (product_id) references products(product_id)
);
