import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class CustomerManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Khách Hàng")
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

    def create_widgets(self):
        """Tạo giao diện người dùng"""
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
        """Thêm khách hàng mới vào cơ sở dữ liệu"""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin bắt buộc!")
            return

        self.cursor.execute("INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)",
                            (name, phone, email, address))
        self.conn.commit()
        self.load_customers()
        self.clear_form()

    def load_customers(self):
        """Tải danh sách khách hàng lên bảng"""
        self.customer_table.delete(*self.customer_table.get_children())
        self.cursor.execute("SELECT * FROM customers")
        for row in self.cursor.fetchall():
            self.customer_table.insert("", "end", values=row)

    def create_car_frame(self):
        messagebox.showinfo("Thông báo", "Chức năng Quản lý Xe chưa được triển khai!")

    def create_orders_frame(self):
        messagebox.showinfo("Thông báo", "Chức năng Quản lý Đơn hàng & Hợp đồng chưa được triển khai!")

    def create_staff_frame(self):
        messagebox.showinfo("Thông báo", "Chức năng Quản lý Nhân viên & Phân quyền chưa được triển khai!")

    def create_reports_frame(self):
        messagebox.showinfo("Thông báo", "Chức năng Báo cáo & Thống kê chưa được triển khai!")

    def create_customer_frame(self):
        self.create_widgets()  # Gọi lại hàm tạo giao diện quản lý khách hàng

    def update_customer(self):
        """Cập nhật thông tin khách hàng"""
        selected_item = self.customer_table.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn khách hàng để sửa!")
            return

        customer_id = self.customer_table.item(selected_item)['values'][0]
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        self.cursor.execute("UPDATE customers SET name=?, phone=?, email=?, address=? WHERE id=?",
                            (name, phone, email, address, customer_id))
        self.conn.commit()
        self.load_customers()
        self.clear_form()

    def delete_customer(self):
        """Xóa khách hàng khỏi cơ sở dữ liệu"""
        selected_item = self.customer_table.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn khách hàng để xóa!")
            return

        customer_id = self.customer_table.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa khách hàng này?")
        if confirm:
            self.cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
            self.conn.commit()
            self.load_customers()
            self.clear_form()

    def select_customer(self, event):
        """Lấy thông tin khách hàng khi chọn dòng trong bảng"""
        selected_item = self.customer_table.selection()
        if not selected_item:
            return

        customer = self.customer_table.item(selected_item)['values']
        self.clear_form()

        self.name_entry.insert(0, customer[1])
        self.phone_entry.insert(0, customer[2])
        self.email_entry.insert(0, customer[3])
        self.address_entry.insert(0, customer[4])


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerManager(root)
    root.mainloop()
