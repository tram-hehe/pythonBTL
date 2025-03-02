import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class CarDealerManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Đơn hàng & Hợp đồng - Đại lý Xe hơi")
        self.root.geometry("800x500")

        self.create_database()
        self.create_widgets()
        self.load_data()
        self.create_menu()

    def create_database(self):
        self.conn = sqlite3.connect("car_dealership.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                customer TEXT NOT NULL,
                car_model TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        menu_bar.add_command(label="Quản lý Xe", command=self.create_car_frame)
        search_var = tk.StringVar()  # Biến lưu từ khóa tìm kiếm

        menu_bar.add_command(label="Quản lý Khách hàng", command=self.create_customer_frame)
        menu_bar.add_command(label="Quản lý Đơn hàng & Hợp đồng", command=self.create_orders_frame)
        menu_bar.add_command(label="Quản lý Nhân viên & Phân quyền", command=self.create_staff_frame)
        menu_bar.add_command(label="Báo cáo & Thống kê", command=self.create_reports_frame)

    def create_car_frame(self):
        subprocess.run(["python", "manage_car.py"])

    def create_customer_frame(self):
        subprocess.run(["python", "customer_management.py"])

    def create_orders_frame(self):
        subprocess.run(["python", "qldonhanghopdong.py"])

    def create_staff_frame(self):
        """Tạo giao diện quản lý nhân viên & phân quyền (chưa triển khai)"""
        messagebox.showinfo("Thông báo", "Chức năng Quản lý Nhân viên & Phân quyền chưa được triển khai!")

    def create_reports_frame(self):
        """Tạo giao diện báo cáo & thống kê (chưa triển khai)"""
        messagebox.showinfo("Thông báo", "Chức năng Báo cáo & Thống kê chưa được triển khai!")

    def create_widgets(self):
        # Label title
        title_label = tk.Label(self.root, text="Quản lý Đơn hàng & Hợp đồng", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Frame nhập dữ liệu
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Mã Đơn Hàng:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_order_id = tk.Entry(frame_input)
        self.entry_order_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Khách Hàng:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_customer = tk.Entry(frame_input)
        self.entry_customer.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Mẫu Xe:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_car_model = tk.Entry(frame_input)
        self.entry_car_model.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Ngày Ký Hợp Đồng:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=10)

        self.btn_add = tk.Button(frame_buttons, text="Thêm", command=self.add_order)
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_update = tk.Button(frame_buttons, text="Sửa", command=self.update_order)
        self.btn_update.grid(row=0, column=1, padx=5)

        self.btn_delete = tk.Button(frame_buttons, text="Xóa", command=self.delete_order)
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.btn_search = tk.Button(frame_buttons, text="Tìm kiếm", command=self.search_order)
        self.btn_search.grid(row=0, column=3, padx=5)

        # Bảng hiển thị dữ liệu
        self.tree = ttk.Treeview(self.root, columns=("order_id", "customer", "car_model", "date"), show='headings')
        self.tree.heading("order_id", text="Mã Đơn Hàng")
        self.tree.heading("customer", text="Khách Hàng")
        self.tree.heading("car_model", text="Mẫu Xe")
        self.tree.heading("date", text="Ngày Ký")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def add_order(self):
        data = (self.entry_order_id.get(), self.entry_customer.get(), self.entry_car_model.get(), self.entry_date.get())
        if any(not field for field in data):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            self.cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?)", data)
            self.conn.commit()
            self.tree.insert("", tk.END, values=data)
            self.clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Mã đơn hàng đã tồn tại!")

    def update_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một đơn hàng để sửa!")
            return

        data = (self.entry_customer.get(), self.entry_car_model.get(), self.entry_date.get(), self.entry_order_id.get())
        self.cursor.execute("UPDATE orders SET customer=?, car_model=?, date=? WHERE order_id=?", data)
        self.conn.commit()
        self.load_data()
        self.clear_entries()

    def delete_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một đơn hàng để xóa!")
            return

        order_id = self.tree.item(selected_item)['values'][0]
        self.cursor.execute("DELETE FROM orders WHERE order_id=?", (order_id,))
        self.conn.commit()
        self.tree.delete(selected_item)

    def search_order(self):
        search_id = self.entry_order_id.get()
        for row in self.tree.get_children():
            if self.tree.item(row)['values'][0] == search_id:
                self.tree.selection_set(row)
                self.tree.focus(row)
                return
        messagebox.showinfo("Thông báo", "Không tìm thấy đơn hàng!")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT * FROM orders")
        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def clear_entries(self):
        self.entry_order_id.delete(0, tk.END)
        self.entry_customer.delete(0, tk.END)
        self.entry_car_model.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CarDealerManagementApp(root)
    root.mainloop()