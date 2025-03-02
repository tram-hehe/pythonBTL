import sqlite3
import matplotlib.pyplot as plt
import numpy as np


def get_sales_data():
    conn = sqlite3.connect("car_dealership.db")
    cursor = conn.cursor()

    # Đảm bảo bảng sales tồn tại
    cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        car_brand TEXT,
        amount REAL,
        date TEXT,
        car_id INTEGER,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )""")
    conn.commit()

    # Truy vấn dữ liệu
    cursor.execute("""
        SELECT employees.name, SUM(sales.amount) 
        FROM sales 
        JOIN employees ON sales.employee_id = employees.id 
        GROUP BY employees.name
    """)
    sales_by_employee = cursor.fetchall()

    cursor.execute("""
        SELECT cars.brand, SUM(sales.amount)
        FROM sales
        JOIN cars ON sales.car_id = cars.car_id  -- Đổi từ cars.id -> cars.car_id
        GROUP BY cars.brand
    """)
    sales_by_brand = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("""
        SELECT cars.model, COUNT(sales.id) 
        FROM sales 
        JOIN cars ON sales.car_id = cars.car_id  -- Đổi từ cars.id -> cars.car_id
        GROUP BY cars.model
    """)
    top_selling_cars = cursor.fetchall()

    conn.close()

    return sales_by_employee, sales_by_brand, total_customers, top_selling_cars



def plot_sales_by_employee(sales_by_employee):
    if not sales_by_employee:
        print("Không có dữ liệu doanh thu theo nhân viên.")
        return
    names, sales = zip(*sales_by_employee)
    plt.figure(figsize=(8, 5))
    plt.bar(names, sales, color='blue')
    plt.xlabel("Nhân viên")
    plt.ylabel("Doanh thu")
    plt.title("Doanh thu theo nhân viên")
    plt.xticks(rotation=45)
    plt.show()


def plot_sales_by_brand(sales_by_brand):
    if not sales_by_brand:
        print("Không có dữ liệu doanh thu theo hãng xe.")
        return
    brands, sales = zip(*sales_by_brand)
    plt.figure(figsize=(8, 5))
    plt.pie(sales, labels=brands, autopct='%1.1f%%', startangle=140)
    plt.title("Doanh thu theo hãng xe")
    plt.show()


def plot_top_selling_cars(top_selling_cars):
    if not top_selling_cars:
        print("Không có dữ liệu xe bán chạy.")
        return
    models, counts = zip(*top_selling_cars)
    plt.figure(figsize=(8, 5))
    plt.plot(models, counts, marker='o', linestyle='-', color='red')
    plt.xlabel("Mẫu xe")
    plt.ylabel("Số lượng bán")
    plt.title("Xe bán chạy nhất")
    plt.xticks(rotation=45)
    plt.show()


def main():
    sales_by_employee, sales_by_brand, total_customers, top_selling_cars = get_sales_data()
    print(f"Tổng số khách hàng: {total_customers}")
    plot_sales_by_employee(sales_by_employee)
    plot_sales_by_brand(sales_by_brand)
    plot_top_selling_cars(top_selling_cars)


if __name__ == "__main__":
    main()
