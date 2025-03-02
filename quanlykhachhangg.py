import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class CustomerManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Khách hàng")
        self.root.geometry("900x500")

        # Các biến lưu giá trị
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        self.create_database()
        self.create_widgets()

    def create_database(self):
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

    def create_widgets(self):
        search_frame = ttk.LabelFrame(self.root, text="Tìm kiếm & Lọc khách hàng")
        search_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(search_frame, text="Họ tên:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(search_frame, textvariable=self.name_var, width=20).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Số điện thoại:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(search_frame, textvariable=self.phone_var, width=15).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(search_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(search_frame, textvariable=self.email_var, width=20).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Địa chỉ:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(search_frame, textvariable=self.address_var, width=30).grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(search_frame, text="Tìm kiếm", command=self.search_customer).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(search_frame, text="Làm mới", command=self.load_customers).grid(row=1, column=4, padx=5, pady=5)

        self.customer_table = ttk.Treeview(self.root, columns=("ID", "Họ Tên", "SĐT", "Email", "Địa Chỉ"), show="headings")
        self.customer_table.heading("ID", text="ID")
        self.customer_table.heading("Họ Tên", text="Họ Tên")
        self.customer_table.heading("SĐT", text="SĐT")
        self.customer_table.heading("Email", text="Email")
        self.customer_table.heading("Địa Chỉ", text="Địa Chỉ")
        self.customer_table.pack(pady=10, fill="both", expand=True)

        self.customer_table.bind("<ButtonRelease-1>", self.select_customer)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Thêm", command=self.add_customer).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Sửa", command=self.update_customer).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_customer).pack(side="left", padx=5)

        self.load_customers()

    def select_customer(self, event):
        selected_item = self.customer_table.focus()
        if selected_item:
            values = self.customer_table.item(selected_item, 'values')
            self.name_var.set(values[1])
            self.phone_var.set(values[2])
            self.email_var.set(values[3])
            self.address_var.set(values[4])

    def add_customer(self):
        name, phone, email, address = self.name_var.get(), self.phone_var.get(), self.email_var.get(), self.address_var.get()
        if not name or not phone:
            messagebox.showwarning("Lỗi", "Họ tên và SĐT không được để trống!")
            return
        self.cursor.execute("INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)", (name, phone, email, address))
        self.conn.commit()
        self.load_customers()
        messagebox.showinfo("Thành công", "Thêm khách hàng thành công!")

    def update_customer(self):
        selected_item = self.customer_table.focus()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn khách hàng để sửa!")
            return
        values = self.customer_table.item(selected_item, 'values')
        customer_id = values[0]
        self.cursor.execute("UPDATE customers SET name=?, phone=?, email=?, address=? WHERE id=?",
                            (self.name_var.get(), self.phone_var.get(), self.email_var.get(), self.address_var.get(),
                             customer_id))

        self.conn.commit()
        self.load_customers()
        messagebox.showinfo("Thành công", "Cập nhật khách hàng thành công!")

    def delete_customer(self):
        selected_item = self.customer_table.focus()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn khách hàng để xóa!")
            return
        values = self.customer_table.item(selected_item, 'values')
        customer_id = values[0]
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa khách hàng này?")
        if confirm:
            self.cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
            self.conn.commit()
            self.load_customers()
            messagebox.showinfo("Thành công", "Xóa khách hàng thành công!")

    def search_customer(self):
        query = "SELECT * FROM customers WHERE 1=1"
        params = []

        if self.name_var.get():
            query += " AND name LIKE ?"
            params.append(f"%{self.name_var.get()}%")

        if self.phone_var.get():
            query += " AND phone LIKE ?"
            params.append(f"%{self.phone_var.get()}%")

        if self.email_var.get():
            query += " AND email LIKE ?"
            params.append(f"%{self.email_var.get()}%")

        if self.address_var.get():
            query += " AND address LIKE ?"
            params.append(f"%{self.address_var.get()}%")

        self.cursor.execute(query, params)
        results = self.cursor.fetchall()

        self.customer_table.delete(*self.customer_table.get_children())
        for row in results:
            self.customer_table.insert("", "end", values=row)

    def load_customers(self):
        self.customer_table.delete(*self.customer_table.get_children())
        self.cursor.execute("SELECT * FROM customers")
        for row in self.cursor.fetchall():
            self.customer_table.insert("", "end", values=row)

    def close_connection(self):
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerManager(root)
    root.protocol("WM_DELETE_WINDOW", app.close_connection)
    root.mainloop()
