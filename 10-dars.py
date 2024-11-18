import psycopg2

connection = psycopg2.connect("""
dbname='',
user='',
password='',
host=''
""")

with connection.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(50) NOT NULL,
            category VARCHAR(50) NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id SERIAL PRIMARY KEY,
            product_name VARCHAR(50) NOT NULL,
            quantity INTEGER NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            inventory_id SERIAL PRIMARY KEY,
            product_name VARCHAR(50) NOT NULL,
            stock INTEGER NOT NULL
        );
    """)
    connection.commit()

with connection.cursor() as cursor:
    cursor.executemany("""
        INSERT INTO products (product_name, category) VALUES (%s, %s)
    """, [
        ('Laptop', 'device'),
        ('Phone', 'device'),
        ('Table', 'Furniture'),
        ('Chair', 'Furniture'),
        ('Notebook', 'device')
    ])
    
    cursor.executemany("""
        INSERT INTO sales (product_name, quantity) VALUES (%s, %s)
    """, [
        ('Laptop', 10),
        ('Phone', 5),
        ('Table', 2),
        ('Pen', 50)
    ])
    
    cursor.executemany("""
        INSERT INTO inventory (product_name, stock) VALUES (%s, %s)
    """, [
        ('Laptop', 20),
        ('Phone', 10),
        ('Chair', 15),
        ('Notebook', 100)
    ])
    connection.commit()

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT product_name FROM sales
        UNION
        SELECT product_name FROM inventory;
    """)
    unique_product_names = cursor.fetchall()

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT product_name FROM products
        INTERSECT
        SELECT product_name FROM inventory;
    """)
    common_product_names = cursor.fetchall()

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT product_name FROM products
        EXCEPT
        SELECT product_name FROM inventory;
    """)
    missing_in_inventory = cursor.fetchall()

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT DISTINCT product_name FROM sales;
    """)
    distinct_sold_products = cursor.fetchall()
