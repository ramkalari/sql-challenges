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
        "question": "Write a query to select all products in the 'Electronics' category.\n\nReturn columns: id, name, price, category",
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
        "question": "Write a query to select all users who are older than 30.\n\nReturn columns: id, username, age",
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
        "question": "Write a query to list all the unique countries where customers are from.\n\nReturn columns: country",
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
        "question": "Write a query to list all orders with the customer's name.\n\nReturn columns: order_id, customer_name, amount",
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
        "question": "Write a query to find the total amount spent by each customer.\n\nReturn columns: name, total_amount",
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
        "question": "Write a query to find all products that have never been ordered.\n\nReturn columns: name",
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
        "question": "Write a query to list all employees and their respective department names.\n\nReturn columns: employee_name, department_name",
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
        "question": "Write a query to find departments with more than one employee.\n\nReturn columns: department_name",
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
    },
    {
        "id": 16,
        "name": "Running Total with Window Functions",
        "level": "Advanced",
        "question": "Write a query to calculate the running total of sales for each month using window functions.",
        "schema_sql": """
CREATE TABLE sales (
  id INTEGER PRIMARY KEY,
  month TEXT,
  amount INTEGER
);
""",
        "seed_sql": """
INSERT INTO sales VALUES (1, 'Jan', 1000);
INSERT INTO sales VALUES (2, 'Feb', 1500);
INSERT INTO sales VALUES (3, 'Mar', 1200);
INSERT INTO sales VALUES (4, 'Apr', 1800);
""",
        "expected_column_names": ["month", "amount", "running_total"],
        "expected_output": [
            ['Jan', '1000', '1000'],
            ['Feb', '1500', '2500'],
            ['Mar', '1200', '3700'],
            ['Apr', '1800', '5500']
        ]
    },
    {
        "id": 17,
        "name": "Rank Employees by Salary",
        "level": "Advanced",
        "question": "Write a query to rank employees by salary within their department using window functions.\n\nReturn columns: name, department_id, salary, rank",
        "schema_sql": """
CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT,
  department TEXT,
  salary INTEGER
);
""",
        "seed_sql": """
INSERT INTO employees VALUES (1, 'Alice', 'Engineering', 80000);
INSERT INTO employees VALUES (2, 'Bob', 'Engineering', 90000);
INSERT INTO employees VALUES (3, 'Charlie', 'Sales', 70000);
INSERT INTO employees VALUES (4, 'Diana', 'Sales', 75000);
INSERT INTO employees VALUES (5, 'Eve', 'Engineering', 85000);
""",
        "expected_column_names": ["name", "department", "salary", "rank"],
        "expected_output": [
            ['Bob', 'Engineering', '90000', '1'],
            ['Eve', 'Engineering', '85000', '2'],
            ['Alice', 'Engineering', '80000', '3'],
            ['Diana', 'Sales', '75000', '1'],
            ['Charlie', 'Sales', '70000', '2']
        ]
    },
    {
        "id": 18,
        "name": "Recursive CTE - Employee Hierarchy",
        "level": "Advanced",
        "question": "Write a query using a recursive CTE to find all employees and their managers in a hierarchical structure.",
        "schema_sql": """
CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT,
  manager_id INTEGER,
  FOREIGN KEY(manager_id) REFERENCES employees(id)
);
""",
        "seed_sql": """
INSERT INTO employees VALUES (1, 'CEO', NULL);
INSERT INTO employees VALUES (2, 'Manager A', 1);
INSERT INTO employees VALUES (3, 'Manager B', 1);
INSERT INTO employees VALUES (4, 'Employee 1', 2);
INSERT INTO employees VALUES (5, 'Employee 2', 2);
INSERT INTO employees VALUES (6, 'Employee 3', 3);
""",
        "expected_column_names": ["employee_name", "manager_name", "level"],
        "expected_output": [
            ['CEO', '', '0'],
            ['Manager A', 'CEO', '1'],
            ['Manager B', 'CEO', '1'],
            ['Employee 1', 'Manager A', '2'],
            ['Employee 2', 'Manager A', '2'],
            ['Employee 3', 'Manager B', '2']
        ]
    },
    {
        "id": 19,
        "name": "Pivot Table - Sales by Product and Region",
        "level": "Advanced",
        "question": "Write a query to create a pivot table showing sales amounts by product and region using conditional aggregation.",
        "schema_sql": """
CREATE TABLE sales (
  id INTEGER PRIMARY KEY,
  product TEXT,
  region TEXT,
  amount INTEGER
);
""",
        "seed_sql": """
INSERT INTO sales VALUES (1, 'Laptop', 'North', 1000);
INSERT INTO sales VALUES (2, 'Laptop', 'South', 1200);
INSERT INTO sales VALUES (3, 'Mouse', 'North', 500);
INSERT INTO sales VALUES (4, 'Mouse', 'South', 600);
INSERT INTO sales VALUES (5, 'Keyboard', 'North', 300);
INSERT INTO sales VALUES (6, 'Keyboard', 'South', 400);
""",
        "expected_column_names": ["product", "north", "south"],
        "expected_output": [
            ['Laptop', '1000', '1200'],
            ['Mouse', '500', '600'],
            ['Keyboard', '300', '400']
        ]
    },
    {
        "id": 20,
        "name": "Complex Subquery - Products Above Average Price",
        "level": "Advanced",
        "question": "Write a query to find all products with prices above the average price of all products in their category.",
        "schema_sql": """
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT,
  category TEXT,
  price INTEGER
);
""",
        "seed_sql": """
INSERT INTO products VALUES (1, 'Laptop A', 'Electronics', 1200);
INSERT INTO products VALUES (2, 'Laptop B', 'Electronics', 1000);
INSERT INTO products VALUES (3, 'Mouse A', 'Electronics', 50);
INSERT INTO products VALUES (4, 'Mouse B', 'Electronics', 30);
INSERT INTO products VALUES (5, 'Book A', 'Books', 20);
INSERT INTO products VALUES (6, 'Book B', 'Books', 25);
""",
        "expected_column_names": ["name", "category", "price"],
        "expected_output": [
            ['Laptop A', 'Electronics', '1200'],
            ['Mouse A', 'Electronics', '50'],
            ['Book B', 'Books', '25']
        ]
    },
    {
        "id": 21,
        "name": "Self-Join - Employee Pairs",
        "level": "Advanced",
        "question": "Write a query to find all pairs of employees who work in the same department and have the same salary.",
        "schema_sql": """
CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT,
  department TEXT,
  salary INTEGER
);
""",
        "seed_sql": """
INSERT INTO employees VALUES (1, 'Alice', 'Engineering', 80000);
INSERT INTO employees VALUES (2, 'Bob', 'Engineering', 80000);
INSERT INTO employees VALUES (3, 'Charlie', 'Sales', 70000);
INSERT INTO employees VALUES (4, 'Diana', 'Sales', 70000);
INSERT INTO employees VALUES (5, 'Eve', 'Engineering', 90000);
""",
        "expected_column_names": ["employee1", "employee2", "department", "salary"],
        "expected_output": [
            ['Alice', 'Bob', 'Engineering', '80000'],
            ['Charlie', 'Diana', 'Sales', '70000']
        ]
    },
    {
        "id": 22,
        "name": "Multiple Window Functions",
        "level": "Advanced",
        "question": "Write a query to calculate both the running total and the percentage of total sales for each month using multiple window functions.",
        "schema_sql": """
CREATE TABLE sales (
  id INTEGER PRIMARY KEY,
  month TEXT,
  amount INTEGER
);
""",
        "seed_sql": """
INSERT INTO sales VALUES (1, 'Jan', 1000);
INSERT INTO sales VALUES (2, 'Feb', 1500);
INSERT INTO sales VALUES (3, 'Mar', 1200);
INSERT INTO sales VALUES (4, 'Apr', 1800);
""",
        "expected_column_names": ["month", "amount", "running_total", "percentage"],
        "expected_output": [
            ['Jan', '1000', '1000', '18.18'],
            ['Feb', '1500', '2500', '27.27'],
            ['Mar', '1200', '3700', '21.82'],
            ['Apr', '1800', '5500', '32.73']
        ]
    },
    {
        "id": 23,
        "name": "Correlated Subquery - Top Performers",
        "level": "Advanced",
        "question": "Write a query to find employees who earn more than the average salary in their department using a correlated subquery.",
        "schema_sql": """
CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT,
  department TEXT,
  salary INTEGER
);
""",
        "seed_sql": """
INSERT INTO employees VALUES (1, 'Alice', 'Engineering', 80000);
INSERT INTO employees VALUES (2, 'Bob', 'Engineering', 90000);
INSERT INTO employees VALUES (3, 'Charlie', 'Engineering', 70000);
INSERT INTO employees VALUES (4, 'Diana', 'Sales', 75000);
INSERT INTO employees VALUES (5, 'Eve', 'Sales', 65000);
INSERT INTO employees VALUES (6, 'Frank', 'Sales', 85000);
""",
        "expected_column_names": ["name", "department", "salary"],
        "expected_output": [
            ['Bob', 'Engineering', '90000'],
            ['Frank', 'Sales', '85000']
        ]
    },
    {
        "id": 24,
        "name": "Date Functions and Intervals",
        "level": "Advanced",
        "question": "Write a query to find all orders placed in the last 30 days and calculate the days since each order was placed.",
        "schema_sql": """
CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_name TEXT,
  order_date DATE,
  amount INTEGER
);
""",
        "seed_sql": """
INSERT INTO orders VALUES (1, 'Alice', '2024-01-15', 100);
INSERT INTO orders VALUES (2, 'Bob', '2024-01-20', 200);
INSERT INTO orders VALUES (3, 'Charlie', '2024-01-25', 150);
INSERT INTO orders VALUES (4, 'Diana', '2023-12-01', 300);
INSERT INTO orders VALUES (5, 'Eve', '2024-01-30', 250);
""",
        "expected_column_names": ["customer_name", "order_date", "amount", "days_ago"],
        "expected_output": [
            ['Alice', '2024-01-15', '100', '15'],
            ['Bob', '2024-01-20', '200', '10'],
            ['Charlie', '2024-01-25', '150', '5'],
            ['Eve', '2024-01-30', '250', '0']
        ]
    },
    {
        "id": 25,
        "name": "Complex Aggregation with CASE",
        "level": "Advanced",
        "question": "Write a query to categorize sales by amount ranges and count the number of sales in each range.",
        "schema_sql": """
CREATE TABLE sales (
  id INTEGER PRIMARY KEY,
  amount INTEGER
);
""",
        "seed_sql": """
INSERT INTO sales VALUES (1, 100);
INSERT INTO sales VALUES (2, 250);
INSERT INTO sales VALUES (3, 500);
INSERT INTO sales VALUES (4, 750);
INSERT INTO sales VALUES (5, 1200);
INSERT INTO sales VALUES (6, 150);
INSERT INTO sales VALUES (7, 300);
INSERT INTO sales VALUES (8, 800);
""",
        "expected_column_names": ["range", "count"],
        "expected_output": [
            ['0-200', '2'],
            ['201-500', '3'],
            ['501-1000', '2'],
            ['1000+', '1']
        ]
    }
]
