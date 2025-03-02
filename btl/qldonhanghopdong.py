import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
from docx import Document

class CarDealerManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Đại lý Xe hơi")
        self.root.geometry("600x400")

        self.create_database()
        self.create_main_menu()

    def create_database(self):
        self.conn = sqlite3.connect("car_dealership.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                customer TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                car_model TEXT NOT NULL,
                invoice TEXT NOT NULL,
                staff TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contracts (
                contract_id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                order_date TEXT NOT NULL,
                delivery_date TEXT NOT NULL,
                warranty TEXT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        ''')

        self.conn.commit()

    def create_main_menu(self):
        title_label = tk.Label(self.root, text="Quản lý Đại lý Xe hơi", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        btn_orders = tk.Button(self.root, text="Quản lý Đơn hàng", command=self.open_order_management, width=30)
        btn_orders.pack(pady=10)

        btn_contracts = tk.Button(self.root, text="Quản lý Hợp đồng", command=self.open_contract_management, width=30)
        btn_contracts.pack(pady=10)

    def open_order_management(self):
        OrderManagement(self.root)

    def open_contract_management(self):
        ContractManagement(self.root)

class OrderManagement:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Quản lý Đơn hàng")
        self.window.geometry("1000x500")
        self.create_widgets()
        self.load_orders()

    def create_widgets(self):
        frame_input = tk.Frame(self.window)
        frame_input.pack(pady=10)

        labels = ["Mã Đơn Hàng", "Khách Hàng", "Địa Chỉ", "Số Điện Thoại", "Mẫu Xe", "Hóa Đơn Giao Dịch",
                  "Nhân viên phụ trách", "Trạng thái"]
        self.entries = {}

        for i, text in enumerate(labels):
            tk.Label(frame_input, text=text + ":").grid(row=i // 4, column=(i % 4) * 2, padx=5, pady=5)
            entry = tk.Entry(frame_input)
            entry.grid(row=i // 4, column=(i % 4) * 2 + 1, padx=5, pady=5)
            self.entries[text] = entry

        frame_search = tk.Frame(self.window)
        frame_search.pack(pady=10)
        tk.Label(frame_search, text="Tìm kiếm Mã Đơn Hàng:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(frame_search)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        btn_search = tk.Button(frame_search, text="Tìm", command=self.search_order)
        btn_search.pack(side=tk.LEFT, padx=5)

        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(pady=10)

        btn_add = tk.Button(frame_buttons, text="Thêm", command=self.add_order)
        btn_add.grid(row=0, column=0, padx=5)

        btn_update = tk.Button(frame_buttons, text="Sửa", command=self.update_order)
        btn_update.grid(row=0, column=1, padx=5)

        btn_delete = tk.Button(frame_buttons, text="Xóa", command=self.delete_order)
        btn_delete.grid(row=0, column=2, padx=5)

        self.tree = ttk.Treeview(self.window, columns=labels, show='headings')
        for label in labels:
            self.tree.heading(label, text=label)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def search_order(self):
        search_query = self.search_entry.get()

        if not search_query:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã đơn hàng để tìm kiếm!")
            return

        conn = sqlite3.connect("car_dealership.db")
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM orders WHERE order_id LIKE ?''', ('%' + search_query + '%',))
        orders = cursor.fetchall()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for order in orders:
            self.tree.insert("", "end", values=order)

        conn.close()

    def add_order(self):
        order_id = self.entries["Mã Đơn Hàng"].get()
        customer = self.entries["Khách Hàng"].get()
        address = self.entries["Địa Chỉ"].get()
        phone = self.entries["Số Điện Thoại"].get()
        car_model = self.entries["Mẫu Xe"].get()
        invoice = self.entries["Hóa Đơn Giao Dịch"].get()
        staff = self.entries["Nhân viên phụ trách"].get()
        status = self.entries["Trạng thái"].get()

        if not order_id or not customer or not address or not phone or not car_model or not invoice or not staff or not status:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            conn = sqlite3.connect("car_dealership.db")
            cursor = conn.cursor()

            cursor.execute('''INSERT INTO orders (order_id, customer, address, phone, car_model, invoice, staff, status)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (order_id, customer, address, phone, car_model, invoice, staff, status))

            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Đơn hàng đã được thêm!")
            self.load_orders()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm đơn hàng: {e}")
    def update_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn một đơn hàng để sửa!")
            return

        order_id = self.entries["Mã Đơn Hàng"].get()
        customer = self.entries["Khách Hàng"].get()
        address = self.entries["Địa Chỉ"].get()
        phone = self.entries["Số Điện Thoại"].get()
        car_model = self.entries["Mẫu Xe"].get()
        invoice = self.entries["Hóa Đơn Giao Dịch"].get()
        staff = self.entries["Nhân viên phụ trách"].get()
        status = self.entries["Trạng thái"].get()

        if not order_id or not customer or not address or not phone or not car_model or not invoice or not staff or not status:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            conn = sqlite3.connect("car_dealership.db")
            cursor = conn.cursor()

            cursor.execute('''UPDATE orders SET customer = ?, address = ?, phone = ?, car_model = ?, invoice = ?, staff = ?, status = ?
                                  WHERE order_id = ?''',
                           (customer, address, phone, car_model, invoice, staff, status, order_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Đơn hàng đã được cập nhật!")
            self.load_orders()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể sửa đơn hàng: {e}")
    def delete_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn một đơn hàng để xóa!")
            return

        order_id = self.tree.item(selected_item[0], "values")[0]

        try:
            conn = sqlite3.connect("car_dealership.db")
            cursor = conn.cursor()

            cursor.execute('''DELETE FROM orders WHERE order_id = ?''', (order_id,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Đơn hàng đã được xóa!")
            self.load_orders()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa đơn hàng: {e}")

    def load_orders(self):
        conn = sqlite3.connect("car_dealership.db")
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM orders''')
        orders = cursor.fetchall()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for order in orders:
            self.tree.insert("", "end", values=order)

        conn.close()

class ContractManagement:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Quản lý Hợp đồng")
        self.window.geometry("1000x600")
        self.create_widgets()
        self.load_contracts()

    def create_widgets(self):
        frame_input = tk.Frame(self.window)
        frame_input.pack(pady=10)

        labels = ["Mã Hợp Đồng", "Mã Đơn Hàng", "Ngày Đặt Hàng", "Ngày Bàn Giao", "Phiếu Bảo Hành"]
        self.entries = {}

        # Tạo các ô nhập liệu
        for i, text in enumerate(labels):
            tk.Label(frame_input, text=text + ":").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(frame_input)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[text] = entry

        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(pady=10)

        # Thêm các nút điều khiển
        btn_add = tk.Button(frame_buttons, text="Thêm", command=self.add_contract)
        btn_add.grid(row=0, column=0, padx=5)

        btn_update = tk.Button(frame_buttons, text="Sửa", command=self.update_contract)
        btn_update.grid(row=0, column=1, padx=5)

        btn_delete = tk.Button(frame_buttons, text="Xóa", command=self.delete_contract)
        btn_delete.grid(row=0, column=2, padx=5)


        # Tạo bảng Treeview để hiển thị hợp đồng
        self.tree = ttk.Treeview(self.window, columns=(
        "Mã Hợp Đồng", "Mã Đơn Hàng", "Ngày Đặt Hàng", "Ngày Bàn Giao", "Phiếu Bảo Hành"), show='headings')
        for label in ["Mã Hợp Đồng", "Mã Đơn Hàng", "Ngày Đặt Hàng", "Ngày Bàn Giao", "Phiếu Bảo Hành"]:
            self.tree.heading(label, text=label)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def add_contract(self):
        # Lấy giá trị từ các ô nhập liệu
        contract_id = self.entries["Mã Hợp Đồng"].get()
        order_id = self.entries["Mã Đơn Hàng"].get()
        order_date = self.entries["Ngày Đặt Hàng"].get()
        delivery_date = self.entries["Ngày Bàn Giao"].get()
        warranty = self.selected_warranty_file if hasattr(self, 'selected_warranty_file') else None

        # Kiểm tra xem các ô nhập liệu có trống không
        if not contract_id or not order_id or not order_date or not delivery_date or not warranty:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin và chọn phiếu bảo hành!")
            return

        try:
            # Thêm hợp đồng vào cơ sở dữ liệu
            conn = sqlite3.connect("car_dealership.db")
            cursor = conn.cursor()

            cursor.execute('''INSERT INTO contracts (contract_id, order_id, order_date, delivery_date, warranty)
                              VALUES (?, ?, ?, ?, ?)''',
                           (contract_id, order_id, order_date, delivery_date, warranty))

            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Hợp đồng đã được thêm!")
            self.load_contracts()  # Làm mới bảng sau khi thêm hợp đồng

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm hợp đồng: {e}")

    def update_contract(self):
        # Lấy giá trị từ các ô nhập liệu
        contract_id = self.entries["Mã Hợp Đồng"].get()
        order_id = self.entries["Mã Đơn Hàng"].get()
        order_date = self.entries["Ngày Đặt Hàng"].get()
        delivery_date = self.entries["Ngày Bàn Giao"].get()
        warranty = self.entries["Phiếu Bảo Hành"].get()

        # Kiểm tra xem các ô nhập liệu có trống không
        if not contract_id or not order_id or not order_date or not delivery_date or not warranty:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            # Cập nhật hợp đồng trong cơ sở dữ liệu
            conn = sqlite3.connect("car_dealership.db")
            cursor = conn.cursor()

            cursor.execute('''UPDATE contracts SET order_id = ?, order_date = ?, delivery_date = ?, warranty = ?
                              WHERE contract_id = ?''',
                           (order_id, order_date, delivery_date, warranty, contract_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Hợp đồng đã được cập nhật!")
            self.load_contracts()  # Làm mới bảng sau khi cập nhật hợp đồng

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật hợp đồng: {e}")

    def delete_contract(self):
        # Lấy Mã Hợp Đồng từ ô nhập liệu
        contract_id = self.entries["Mã Hợp Đồng"].get()

        if not contract_id:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã Hợp Đồng để xóa!")
            return

        try:
            # Xóa hợp đồng khỏi cơ sở dữ liệu
            conn = sqlite3.connect("car_dealership.db")
            cursor = conn.cursor()

            cursor.execute('''DELETE FROM contracts WHERE contract_id = ?''', (contract_id,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Hợp đồng đã được xóa!")
            self.load_contracts()  # Làm mới bảng sau khi xóa hợp đồng

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa hợp đồng: {e}")

    def import_contracts(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            # Đọc dữ liệu từ file
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            # Xóa dữ liệu cũ trong bảng Treeview trước khi hiển thị dữ liệu mới
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Hiển thị dữ liệu từ file lên Treeview
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=(row["Mã Hợp Đồng"], row["Mã Đơn Hàng"], row["Ngày Đặt Hàng"],
                                                    row["Ngày Bàn Giao"], row["Phiếu Bảo Hành"]))

            # Để dữ liệu đã hiển thị lên bảng Treeview, bây giờ mới tiến hành lưu vào cơ sở dữ liệu
            conn = sqlite3.connect("car_dealership.db")
            cursor = conn.cursor()

            # Nhập dữ liệu vào cơ sở dữ liệu
            for _, row in df.iterrows():
                cursor.execute('''INSERT INTO contracts (contract_id, order_id, order_date, delivery_date, warranty)
                                  VALUES (?, ?, ?, ?, ?)''',
                               (row["Mã Hợp Đồng"], row["Mã Đơn Hàng"], row["Ngày Đặt Hàng"], row["Ngày Bàn Giao"],
                                row["Phiếu Bảo Hành"]))

            conn.commit()
            conn.close()
            messagebox.showinfo("Nhập dữ liệu", "Nhập hợp đồng từ file thành công!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể nhập dữ liệu: {e}")

    def create_widgets(self):
        frame_input = tk.Frame(self.window)
        frame_input.pack(pady=10)

        labels = ["Mã Hợp Đồng", "Mã Đơn Hàng", "Ngày Đặt Hàng", "Ngày Bàn Giao", "Phiếu Bảo Hành"]
        self.entries = {}

        # Tạo các ô nhập liệu
        for i, text in enumerate(labels[:-1]):  # Loại bỏ Phiếu Bảo Hành khỏi các entry thông thường
            tk.Label(frame_input, text=text + ":").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(frame_input)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[text] = entry

        # Thêm phần chọn file cho Phiếu Bảo Hành
        tk.Label(frame_input, text="Phiếu Bảo Hành:").grid(row=len(labels) - 1, column=0, padx=5, pady=5)
        self.warranty_file_button = tk.Button(frame_input, text="Chọn File", command=self.select_warranty_file)
        self.warranty_file_button.grid(row=len(labels) - 1, column=1, padx=5, pady=5)
        self.warranty_file_label = tk.Label(frame_input, text="Chưa chọn file")
        self.warranty_file_label.grid(row=len(labels) - 1, column=2, padx=5, pady=5)

        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(pady=10)

        btn_add = tk.Button(frame_buttons, text="Thêm", command=self.add_contract)
        btn_add.grid(row=0, column=0, padx=5)

        btn_update = tk.Button(frame_buttons, text="Sửa", command=self.update_contract)
        btn_update.grid(row=0, column=1, padx=5)

        btn_delete = tk.Button(frame_buttons, text="Xóa", command=self.delete_contract)
        btn_delete.grid(row=0, column=2, padx=5)

        # Tạo bảng Treeview để hiển thị hợp đồng
        self.tree = ttk.Treeview(self.window, columns=(
        "Mã Hợp Đồng", "Mã Đơn Hàng", "Ngày Đặt Hàng", "Ngày Bàn Giao", "Phiếu Bảo Hành"), show='headings')
        for label in ["Mã Hợp Đồng", "Mã Đơn Hàng", "Ngày Đặt Hàng", "Ngày Bàn Giao", "Phiếu Bảo Hành"]:
            self.tree.heading(label, text=label)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def select_warranty_file(self):
        # Mở hộp thoại chọn file
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
        if file_path:
            self.selected_warranty_file = file_path
            self.warranty_file_label.config(text=file_path.split("/")[-1])  # Hiển thị tên file trên giao diện

    def load_contracts(self):
        conn = sqlite3.connect("car_dealership.db")
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM contracts''')
        contracts = cursor.fetchall()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for contract in contracts:
            # Hiển thị đường dẫn file phiếu bảo hành hoặc tên file
            warranty = contract[4] if contract[4] else "Chưa có file"
            self.tree.insert("", "end", values=(contract[0], contract[1], contract[2], contract[3], warranty))

        conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = CarDealerManagementApp(root)
    root.mainloop()

