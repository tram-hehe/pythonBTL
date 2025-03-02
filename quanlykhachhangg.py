import sqlite3
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox


class CustomerManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Khách hàng")

        # 🔹 Thêm các biến StringVar để lưu dữ liệu nhập từ form
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        self.create_database()
        self.create_menu()
        self.create_widgets()

    def create_database(self):
        """Tạo cơ sở dữ liệu và bảng customers nếu chưa có"""
        self.conn = sqlite3.connect("car_dealership.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT
            )
        ''')
        self.conn.commit()

    def create_menu(self):
        """Tạo thanh menu"""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        menu_bar.add_command(label="Quản lý Xe", command=self.create_car_frame)
        menu_bar.add_command(label="Quản lý Khách hàng", command=self.create_customer_frame)
        menu_bar.add_command(label="Quản lý Đơn hàng & Hợp đồng", command=self.create_orders_frame)
        menu_bar.add_command(label="Quản lý Nhân viên & Phân quyền", command=self.create_staff_frame)
        menu_bar.add_command(label="Báo cáo & Thống kê", command=self.create_reports_frame)

    def create_car_frame(self):
        subprocess.run(["python", "manage_car.py"])

    def create_customer_frame(self):
        self.switch_frame(self.create_widgets)

    def create_orders_frame(self):
        subprocess.run(["python", "qldonhanghopdong.py"])


    def create_staff_frame(self):
        """Tạo giao diện quản lý nhân viên & phân quyền (chưa triển khai)"""
        messagebox.showinfo("Thông báo", "Chức năng Quản lý Nhân viên & Phân quyền chưa được triển khai!")

    def create_reports_frame(self):
        """Tạo giao diện báo cáo & thống kê (chưa triển khai)"""
        messagebox.showinfo("Thông báo", "Chức năng Báo cáo & Thống kê chưa được triển khai!")

    def update_customer(self):
        selected_item = self.customer_table.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn khách hàng để sửa!")
            return

        customer_id = self.customer_table.item(selected_item)['values'][0]
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip() or "N/A"  # Nếu email trống, đặt là "N/A"
        address = self.address_entry.get().strip() or "N/A"

        if not name or not phone:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        self.cursor.execute("UPDATE customers SET name=?, phone=?, email=?, address=? WHERE id=?",
                            (name, phone, email, address, customer_id))
        self.conn.commit()
        self.load_customers()
        self.clear_form()

    def select_customer(self, event):
        selected_item = self.customer_table.selection()
        if not selected_item:
            return

        item = self.customer_table.item(selected_item)
        customer_data = item['values']

        if len(customer_data) < 5:
            return

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, customer_data[1])

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, customer_data[2])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, customer_data[3])

        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, customer_data[4])

    def create_widgets(self):
        ttk.Label(self.root, text="Quản Lý Khách Hàng", font=("Arial", 16)).pack(pady=10)

        # Form nhập dữ liệu
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Họ và Tên:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Số Điện Thoại:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = ttk.Entry(form_frame)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Địa Chỉ:").grid(row=3, column=0, padx=5, pady=5)
        self.address_entry = ttk.Entry(form_frame)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)

        # Nút chức năng
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Thêm", command=self.add_customer).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Sửa", command=self.update_customer).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_customer).pack(side="left", padx=5)

        # Bảng danh sách khách hàng
        self.customer_table = ttk.Treeview(self.root, columns=("ID", "Họ Tên", "SĐT", "Email", "Địa Chỉ"),
                                           show="headings")
        self.customer_table.heading("ID", text="ID")
        self.customer_table.heading("Họ Tên", text="Họ Tên")
        self.customer_table.heading("SĐT", text="SĐT")
        self.customer_table.heading("Email", text="Email")
        self.customer_table.heading("Địa Chỉ", text="Địa Chỉ")
        self.customer_table.pack(pady=10, fill="both", expand=True)

        self.customer_table.bind("<<TreeviewSelect>>", self.select_customer)

        self.load_customers()

    def add_customer(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone or not email or not address:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return

        # Thêm khách hàng vào cơ sở dữ liệu
        self.cursor.execute("INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)",
                            (name, phone, email, address))
        self.conn.commit()
        messagebox.showinfo("Thành công", "Thêm khách hàng thành công!")
        self.load_customers()
        self.clear_form()  # Xóa form sau khi thêm khách hàng

    def delete_customer(self):
        """Xóa khách hàng"""
        selected_item = self.customer_table.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn khách hàng để xóa!")
            return

        customer_id = self.customer_table.item(selected_item)['values'][0]
        self.cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
        self.conn.commit()
        self.load_customers()
        self.clear_form()

    def clear_form(self):
        """Xóa dữ liệu trên form nhập"""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def load_customers(self):
        """Tải danh sách khách hàng"""
        self.customer_table.delete(*self.customer_table.get_children())
        self.cursor.execute("SELECT * FROM customers")
        for row in self.cursor.fetchall():
            self.customer_table.insert("", "end", values=row)


    def close_connection(self):
        """Đóng kết nối SQLite khi thoát ứng dụng"""
        self.conn.close()
        self.root.destroy()  # Đóng cửa sổ Tkinter


# Gọi sự kiện đóng kết nối khi đóng ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerManager(root)
    root.protocol("WM_DELETE_WINDOW", app.close_connection)
    root.mainloop()
