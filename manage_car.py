import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk
import os
from tkinter import Entry, Button

# Kết nối SQLite
def connect_db():
    conn = sqlite3.connect("car_dealership.db")
    return conn


def execute_query(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def fetch_data(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def create_tables():
    execute_query("""
        CREATE TABLE IF NOT EXISTS cars (
            car_id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            color TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            image_path TEXT
        )
    """)

    execute_query("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)


# Gọi hàm tạo bảng trước khi chạy ứng dụng
create_tables()


class CarDealershipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Đại lý Xe hơi")
        self.search_var = tk.StringVar()  # Biến tìm kiếm
        self.create_menu()
        self.current_frame = None
        self.create_car_frame()


    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        menu_bar.add_command(label="Quản lý Xe", command=self.create_car_frame)
        search_var = tk.StringVar()  # Biến lưu từ khóa tìm kiếm

        menu_bar.add_command(label="Quản lý Khách hàng", command=self.create_customer_frame)
        menu_bar.add_command(label="Quản lý Đơn hàng & Hợp đồng", command=self.create_orders_frame)
        menu_bar.add_command(label="Quản lý Nhân viên & Phân quyền", command=self.create_staff_frame)
        menu_bar.add_command(label="Báo cáo & Thống kê", command=self.create_reports_frame)

    def switch_frame(self, new_frame_creator):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.LabelFrame(self.root)
        self.current_frame.pack(padx=10, pady=10, fill="both", expand=True)
        new_frame_creator()

    def create_car_frame(self):
        self.switch_frame(self.build_car_frame)

    def create_reports_frame(self):
        self.switch_frame(self.build_reports_frame)

    def build_reports_frame(self):
        ttk.Label(self.current_frame, text="Báo cáo & Thống kê", font=("Arial", 14)).pack(pady=10)

    def create_staff_frame(self):
        self.switch_frame(self.build_staff_frame)

    def build_staff_frame(self):
        ttk.Label(self.current_frame, text="Quản lý Nhân viên & Phân quyền", font=("Arial", 14)).pack(pady=10)

    def build_car_frame(self):
        ttk.Label(self.current_frame, text="Quản lý Xe", font=("Arial", 14)).pack(pady=10)

        search_frame = ttk.LabelFrame(self.current_frame, text="Tìm kiếm & Lọc xe")
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Hãng xe:").grid(row=0, column=0, padx=5, pady=5)
        self.brand_entry = ttk.Entry(search_frame)
        self.brand_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Khoảng giá:").grid(row=0, column=2, padx=5, pady=5)
        self.min_price_entry = ttk.Entry(search_frame, width=10)
        self.min_price_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(search_frame, text="đến").grid(row=0, column=4, padx=5, pady=5)
        self.max_price_entry = ttk.Entry(search_frame, width=10)
        self.max_price_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(search_frame, text="Năm sản xuất:").grid(row=1, column=0, padx=5, pady=5)
        self.year_entry = ttk.Entry(search_frame)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Màu sắc:").grid(row=1, column=2, padx=5, pady=5)
        self.color_entry = ttk.Entry(search_frame)
        self.color_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(search_frame, text="Tìm kiếm", command=self.search_car).grid(row=1, column=6, padx=10, pady=5)

        # Bảng hiển thị danh sách xe
        columns = ("ID", "Hãng", "Mẫu", "Năm", "Màu", "Giá", "Số lượng")
        self.car_table = ttk.Treeview(self.current_frame, columns=columns, show="headings")
        for col in columns:
            self.car_table.heading(col, text=col)
            self.car_table.column(col, width=100)
        self.car_table.pack(fill="both", expand=True)

        self.car_table.bind("<<TreeviewSelect>>", self.display_car_image)

        # Hiển thị ảnh xe
        self.car_image_label = tk.Label(self.current_frame)
        self.car_image_label.pack(pady=10)

        btn_frame = ttk.Frame(self.current_frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Thêm xe", command=self.show_add_car_form).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Sửa xe", command=self.show_edit_car_form).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Xóa xe", command=self.delete_car).grid(row=0, column=2, padx=5)

        self.car_table.bind("<<TreeviewSelect>>", self.display_car_image)

        # Thêm Label để hiển thị ảnh
        self.car_image_label = tk.Label(self.current_frame)
        self.car_image_label.pack(pady=10)

        self.load_cars()

    def display_car_image(self, event):
        selected_item = self.car_table.selection()
        if not selected_item:
            return

        car_id = self.car_table.item(selected_item)['values'][0]
        car_data = fetch_data("SELECT image_path FROM cars WHERE car_id = ?", (car_id,))

        if car_data and car_data[0][0]:
            image_path = car_data[0][0]

            if not os.path.exists(image_path):
                messagebox.showerror("Lỗi", f"Ảnh không tồn tại: {image_path}")
                return

            try:
                img = Image.open(image_path)
                img = img.resize((200, 150))  # Điều chỉnh kích thước ảnh
                img = ImageTk.PhotoImage(img)

                self.car_image_label.config(image=img)
                self.car_image_label.image = img  # Giữ tham chiếu tránh bị garbage collector xóa

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở ảnh: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Không có ảnh nào được lưu cho xe này.")

    def create_orders_frame(self):
        self.switch_frame(self.build_orders_frame)

    def build_orders_frame(self):
        ttk.Label(self.current_frame, text="Quản lý Đơn hàng & Hợp đồng", font=("Arial", 14)).pack(pady=10)

    def load_cars(self):
        for row in self.car_table.get_children():
            self.car_table.delete(row)
        cars = fetch_data("SELECT * FROM cars")
        for car in cars:
            self.car_table.insert("", "end", values=car)

    def delete_car(self):
        selected_item = self.car_table.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một xe để xóa!")
            return
        car_id = self.car_table.item(selected_item)['values'][0]
        execute_query("DELETE FROM cars WHERE car_id = ?", (car_id,))
        self.load_cars()
        messagebox.showinfo("Thông báo", "Đã xóa xe thành công!")

    def show_add_car_form(self):
        self.show_car_form("Thêm xe mới", None)

    def show_edit_car_form(self):
        selected_item = self.car_table.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một xe để sửa!")
            return
        car_id = self.car_table.item(selected_item)['values'][0]
        car_data = fetch_data("SELECT * FROM cars WHERE car_id = ?", (car_id,))[0]
        self.show_car_form("Sửa xe", car_data)

    def show_car_form(self, title, car_data):
        form_window = tk.Toplevel(self.root)
        form_window.title(title)

        fields = ["Hãng", "Mẫu", "Năm", "Màu", "Giá", "Số lượng"]
        entries = {}
        image_path = tk.StringVar()

        for i, field in enumerate(fields):
            ttk.Label(form_window, text=field).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(form_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            if car_data:
                entry.insert(0, car_data[i + 1])
            entries[field] = entry

        ttk.Label(form_window, text="Ảnh").grid(row=len(fields), column=0, padx=5, pady=5)
        ttk.Entry(form_window, textvariable=image_path).grid(row=len(fields), column=1, padx=5, pady=5)

        def select_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                image_path.set(file_path)
                print("Ảnh đã chọn:", file_path)  # Kiểm tra đường dẫn ảnh


        ttk.Button(form_window, text="Chọn ảnh", command=select_image).grid(row=len(fields), column=2, padx=5, pady=5)

        def save_car():
            data = [entries[field].get() for field in fields] + [image_path.get()]
            print("Dữ liệu trước khi lưu:", data)  # Debug in dữ liệu trước khi lưu
            try:
                data[2] = int(data[2])  # Năm sản xuất
                data[4] = float(data[4])  # Giá
                data[5] = int(data[5])  # Số lượng

                if car_data:
                    execute_query(
                        "UPDATE cars SET brand=?, model=?, year=?, color=?, price=?, quantity=?, image_path=? WHERE car_id=?",
                        tuple(data) + (car_data[0],)
                    )
                    messagebox.showinfo("Thành công", "Đã cập nhật xe!")
                else:
                    execute_query(
                        "INSERT INTO cars (brand, model, year, color, price, quantity, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        tuple(data)
                    )
                    messagebox.showinfo("Thành công", "Đã thêm xe mới!")

                form_window.destroy()
                self.load_cars()
            except ValueError:
                messagebox.showerror("Lỗi", "Dữ liệu nhập vào không hợp lệ!")

        ttk.Button(form_window, text="Lưu", command=save_car).grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

    def create_customer_frame(self):
        self.switch_frame(self.build_customer_frame)

    def build_customer_frame(self):
        ttk.Label(self.current_frame, text="Quản lý Khách hàng", font=("Arial", 14)).pack(pady=10)

        btn_frame = ttk.Frame(self.current_frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Thêm khách hàng", command=self.show_add_customer_form).grid(row=0, column=0,
                                                                                                    padx=5)
        ttk.Button(btn_frame, text="Sửa khách hàng", command=self.show_edit_customer_form).grid(row=0, column=1,
                                                                                                    padx=5)
        ttk.Button(btn_frame, text="Xóa khách hàng", command=self.delete_customer).grid(row=0, column=2, padx=5)

        columns = ("ID", "Tên", "SĐT", "Email", "Địa chỉ")
        self.customer_table = ttk.Treeview(self.current_frame, columns=columns, show="headings")
        for col in columns:
            self.customer_table.heading(col, text=col)
            self.customer_table.column(col, width=120)
        self.customer_table.pack(fill="both", expand=True)

        self.load_customers()

    def load_customers(self):
        for row in self.customer_table.get_children():
            self.customer_table.delete(row)
        customers = fetch_data("SELECT * FROM customers")
        for customer in customers:
            self.customer_table.insert("", "end", values=customer)

    def search_car(self):
        brand = self.brand_entry.get().strip()
        min_price = self.min_price_entry.get().strip()
        max_price = self.max_price_entry.get().strip()
        year = self.year_entry.get().strip()
        color = self.color_entry.get().strip()

        query = "SELECT * FROM cars WHERE 1=1"
        params = []

        if brand:
            query += " AND brand LIKE ?"
            params.append(f"%{brand}%")

        if min_price.isdigit():
            query += " AND price >= ?"
            params.append(float(min_price))

        if max_price.isdigit():
            query += " AND price <= ?"
            params.append(float(max_price))

        if year.isdigit():
            query += " AND year = ?"
            params.append(int(year))

        if color:
            query += " AND color LIKE ?"
            params.append(f"%{color}%")

        # Xóa dữ liệu cũ
        for row in self.car_table.get_children():
            self.car_table.delete(row)

        # Lấy dữ liệu mới
        search_results = fetch_data(query, params)

        for row in search_results:
            self.car_table.insert("", "end", values=row)

        if not search_results:
            messagebox.showinfo("Kết quả", "Không tìm thấy xe nào!")


if __name__ == "__main__":
    root = tk.Tk()
    app = CarDealershipApp(root)
    root.mainloop()
