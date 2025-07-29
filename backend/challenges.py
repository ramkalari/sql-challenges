CHALLENGES = [
    {
        "id": 1,
        "name": "Select All Products",
        "level": "Basic",
        "question": "Write a query to select all columns from the 'products' table.",
        "schema_sql": """
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT,
  price INTEGER,
  category TEXT
);
""",
        "seed_sql": """
INSERT INTO products VALUES (1, 'Laptop', 1200, 'Electronics');
INSERT INTO products VALUES (2, 'Mouse', 25, 'Electronics');
INSERT INTO products VALUES (3, 'Keyboard', 75, 'Electronics');
INSERT INTO products VALUES (4, 'Desk Chair', 150, 'Furniture');
INSERT INTO products VALUES (5, 'Book', 15, 'Books');
""",
        "expected_column_names": ["id", "name", "price", "category"],
        "expected_output": [
            ['1', 'Laptop', '1200', 'Electronics'],
            ['2', 'Mouse', '25', 'Electronics'],
            ['3', 'Keyboard', '75', 'Electronics'],
            ['4', 'Desk Chair', '150', 'Furniture'],
            ['5', 'Book', '15', 'Books']
        ]
    },
    {
        "id": 2,
        "name": "Select Name and Price",
        "level": "Basic",
        "question": "Write a query to select only the name and price of all products.",
        "schema_sql": """
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT,
  price INTEGER,
  category TEXT
);
""",
        "seed_sql": """
INSERT INTO products VALUES (1, 'Laptop', 1200, 'Electronics');
INSERT INTO products VALUES (2, 'Mouse', 25, 'Electronics');
INSERT INTO products VALUES (3, 'Keyboard', 75, 'Electronics');
""",
        "expected_column_names": ["name", "price"],
        "expected_output": [
            ['Laptop', '1200'],
            ['Mouse', '25'],
            ['Keyboard', '75']
        ]
    },
    {
        "id": 3,
        "name": "Products in Electronics",
        "level": "Basic",
        "question": "Write a query to select all products in the 'Electronics' category.",
        "schema_sql": """
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT,
  price INTEGER,
  category TEXT
);
""",
        "seed_sql": """
INSERT INTO products VALUES (1, 'Laptop', 1200, 'Electronics');
INSERT INTO products VALUES (2, 'Desk Chair', 150, 'Furniture');
INSERT INTO products VALUES (3, 'Mouse', 25, 'Electronics');
""",
        "expected_column_names": ["id", "name", "price", "category"],
        "expected_output": [
            ['1', 'Laptop', '1200', 'Electronics'],
            ['3', 'Mouse', '25', 'Electronics']
        ]
    },
    {
        "id": 4,
        "name": "Users Older Than 30",
        "level": "Basic",
        "question": "Write a query to select all users who are older than 30.",
        "schema_sql": """
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT,
  age INTEGER
);
""",
        "seed_sql": """
INSERT INTO users VALUES (1, 'alice', 28);
INSERT INTO users VALUES (2, 'bob', 32);
INSERT INTO users VALUES (3, 'charlie', 35);
""",
        "expected_column_names": ["id", "username", "age"],
        "expected_output": [
            ['2', 'bob', '32'],
            ['3', 'charlie', '35']
        ]
    },
    {
        "id": 5,
        "name": "Laptops Order",
        "level": "Basic",
        "question": "Write a query to select orders for 'Laptop' where the quantity is greater than 1.",
        "schema_sql": """
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  product_name TEXT,
  quantity INTEGER
);
""",
        "seed_sql": """
INSERT INTO orders VALUES (1, 'Laptop', 1);
INSERT INTO orders VALUES (2, 'Mouse', 2);
INSERT INTO orders VALUES (3, 'Laptop', 3);
""",
        "expected_column_names": ["order_id", "product_name", "quantity"],
        "expected_output": [
            ['3', 'Laptop', '3']
        ]
    },
    {
        "id": 6,
        "name": "Customers from USA or Canada",
        "level": "Basic",
        "question": "Write a query to select all customers from 'USA' or 'Canada'.",
        "schema_sql": """
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT,
  country TEXT
);
""",
        "seed_sql": """
INSERT INTO customers VALUES (1, 'John Doe', 'USA');
INSERT INTO customers VALUES (2, 'Jane Smith', 'Canada');
INSERT INTO customers VALUES (3, 'Peter Jones', 'UK');
""",
        "expected_column_names": ["id", "name", "country"],
        "expected_output": [
            ['1', 'John Doe', 'USA'],
            ['2', 'Jane Smith', 'Canada']
        ]
    },
    {
        "id": 7,
        "name": "Order by Price",
        "level": "Basic",
        "question": "Write a query to select all products, ordered by price in descending order.",
        "schema_sql": """
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT,
  price INTEGER
);
""",
        "seed_sql": """
INSERT INTO products VALUES (1, 'Laptop', 1200);
INSERT INTO products VALUES (2, 'Mouse', 25);
INSERT INTO products VALUES (3, 'Keyboard', 75);
""",
        "expected_column_names": ["id", "name", "price"],
        "expected_output": [
            ['1', 'Laptop', '1200'],
            ['3', 'Keyboard', '75'],
            ['2', 'Mouse', '25']
        ]
    },
    {
        "id": 8,
        "name": "Top 2 Most Expensive Products",
        "level": "Basic",
        "question": "Write a query to select the 2 most expensive products.",
        "schema_sql": """
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT,
  price INTEGER
);
""",
        "seed_sql": """
INSERT INTO products VALUES (1, 'Laptop', 1200);
INSERT INTO products VALUES (2, 'Mouse', 25);
INSERT INTO products VALUES (3, 'Keyboard', 75);
INSERT INTO products VALUES (4, 'Monitor', 300);
""",
        "expected_column_names": ["id", "name", "price"],
        "expected_output": [
            ['1', 'Laptop', '1200'],
            ['4', 'Monitor', '300']
        ]
    },
    {
        "id": 9,
        "name": "Count Users",
        "level": "Basic",
        "question": "Write a query to count the total number of users.",
        "schema_sql": """
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT
);
""",
        "seed_sql": """
INSERT INTO users VALUES (1, 'alice');
INSERT INTO users VALUES (2, 'bob');
INSERT INTO users VALUES (3, 'charlie');
""",
        "expected_column_names": ["count"],
        "expected_output": [
            ['3']
        ]
    },
    {
        "id": 10,
        "name": "Unique Countries",
        "level": "Basic",
        "question": "Write a query to list all the unique countries where customers are from.",
        "schema_sql": """
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT,
  country TEXT
);
""",
        "seed_sql": """
INSERT INTO customers VALUES (1, 'John Doe', 'USA');
INSERT INTO customers VALUES (2, 'Jane Smith', 'Canada');
INSERT INTO customers VALUES (3, 'Peter Jones', 'UK');
INSERT INTO customers VALUES (4, 'Alice', 'USA');
""",
        "expected_column_names": ["country"],
        "expected_output": [
            ['USA'],
            ['Canada'],
            ['UK']
        ]
    },
    {
        "id": 11,
        "name": "Join Orders and Customers",
        "level": "Intermediate",
        "question": "Write a query to list all orders with the customer's name.",
        "schema_sql": """
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT,
  country TEXT
);
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  product_name TEXT,
  FOREIGN KEY(customer_id) REFERENCES customers(id)
);
""",
        "seed_sql": """
INSERT INTO customers VALUES (1, 'John Doe', 'USA');
INSERT INTO customers VALUES (2, 'Jane Smith', 'Canada');
INSERT INTO orders VALUES (1, 1, 'Laptop');
INSERT INTO orders VALUES (2, 2, 'Mouse');
""",
        "expected_column_names": ["order_id", "name"],
        "expected_output": [
            ['1', 'John Doe'],
            ['2', 'Jane Smith']
        ]
    },
    {
        "id": 12,
        "name": "Total Spent by Customer",
        "level": "Intermediate",
        "question": "Write a query to find the total amount spent by each customer.",
        "schema_sql": """
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT
);
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  amount INTEGER,
  FOREIGN KEY(customer_id) REFERENCES customers(id)
);
""",
        "seed_sql": """
INSERT INTO customers VALUES (1, 'Alice');
INSERT INTO customers VALUES (2, 'Bob');
INSERT INTO orders VALUES (1, 1, 100);
INSERT INTO orders VALUES (2, 1, 200);
INSERT INTO orders VALUES (3, 2, 150);
""",
        "expected_column_names": ["name", "total_amount"],
        "expected_output": [
            ['Alice', '300'],
            ['Bob', '150']
        ]
    },
    {
        "id": 13,
        "name": "Products Not Ordered",
        "level": "Intermediate",
        "question": "Write a query to find all products that have never been ordered.",
        "schema_sql": """
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT
);
CREATE TABLE order_items (
  id INTEGER PRIMARY KEY,
  product_id INTEGER,
  quantity INTEGER,
  FOREIGN KEY(product_id) REFERENCES products(id)
);
""",
        "seed_sql": """
INSERT INTO products VALUES (1, 'Laptop');
INSERT INTO products VALUES (2, 'Mouse');
INSERT INTO products VALUES (3, 'Keyboard');
INSERT INTO order_items VALUES (1, 1, 10);
INSERT INTO order_items VALUES (2, 2, 5);
""",
        "expected_column_names": ["name"],
        "expected_output": [
            ['Keyboard']
        ]
    },
    {
        "id": 14,
        "name": "Employees in Departments",
        "level": "Intermediate",
        "question": "Write a query to list all employees and their respective department names.",
        "schema_sql": """
CREATE TABLE departments (
  id INTEGER PRIMARY KEY,
  name TEXT
);
CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT,
  department_id INTEGER,
  FOREIGN KEY(department_id) REFERENCES departments(id)
);
""",
        "seed_sql": """
INSERT INTO departments VALUES (1, 'Engineering');
INSERT INTO departments VALUES (2, 'Sales');
INSERT INTO employees VALUES (1, 'Alice', 1);
INSERT INTO employees VALUES (2, 'Bob', 2);
INSERT INTO employees VALUES (3, 'Charlie', 1);
""",
        "expected_column_names": ["name", "department"],
        "expected_output": [
            ['Alice', 'Engineering'],
            ['Bob', 'Sales'],
            ['Charlie', 'Engineering']
        ]
    },
    {
        "id": 15,
        "name": "Departments with More Than 1 Employee",
        "level": "Intermediate",
        "question": "Write a query to find departments with more than one employee.",
        "schema_sql": """
CREATE TABLE departments (
  id INTEGER PRIMARY KEY,
  name TEXT
);
CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT,
  department_id INTEGER,
  FOREIGN KEY(department_id) REFERENCES departments(id)
);
""",
        "seed_sql": """
INSERT INTO departments VALUES (1, 'Engineering');
INSERT INTO departments VALUES (2, 'Sales');
INSERT INTO employees VALUES (1, 'Alice', 1);
INSERT INTO employees VALUES (2, 'Bob', 2);
INSERT INTO employees VALUES (3, 'Charlie', 1);
""",
        "expected_column_names": ["name"],
        "expected_output": [
            ['Engineering']
        ]
    }
]
