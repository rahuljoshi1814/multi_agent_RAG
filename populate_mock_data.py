from app.db import get_connection
from faker import Faker
import random

fake = Faker()

conn = get_connection()
cur = conn.cursor()

# Store real IDs after insert
customer_ids = []
product_ids = []
employee_ids = []

# Insert Customers
for _ in range(200):
    cur.execute("INSERT INTO customers (name, email, created_at) VALUES (%s, %s, %s) RETURNING id",
                (fake.name(), fake.email(), fake.date_between(start_date='-3y', end_date='today')))
    customer_ids.append(cur.fetchone()[0])

# Insert Products
for _ in range(20):
    cur.execute("INSERT INTO products (name, category, price) VALUES (%s, %s, %s) RETURNING id",
                (fake.word().capitalize(), random.choice(["Electronics", "Books", "Clothing"]), round(random.uniform(10, 500), 2)))
    product_ids.append(cur.fetchone()[0])

# Insert Employees
for _ in range(50):
    cur.execute("INSERT INTO employees (name, role, department, hire_date) VALUES (%s, %s, %s, %s) RETURNING id",
                (fake.name(), random.choice(["Sales Rep", "Manager"]), random.choice(["Sales", "HR", "IT"]), fake.date_between(start_date='-5y', end_date='today')))
    employee_ids.append(cur.fetchone()[0])

# Insert Sales using actual IDs
for _ in range(500):
    cur.execute("INSERT INTO sales (customer_id, product_id, employee_id, amount, sale_date) VALUES (%s, %s, %s, %s, %s)",
                (random.choice(customer_ids), random.choice(product_ids), random.choice(employee_ids),
                 round(random.uniform(50, 1000), 2), fake.date_between(start_date='-2y', end_date='today')))

conn.commit()
cur.close()
conn.close()
print("Mock data inserted successfully!")