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

        self.selected_order_id = None  # Lưu ID đơn hàng đang chọn
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

        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(pady=10)

        btn_add = tk.Button(frame_buttons, text="Thêm", command=self.add_order)
        btn_add.grid(row=0, column=0, padx=5)

        btn_update = tk.Button(frame_buttons, text="Sửa", command=self.update_order)
        btn_update.grid(row=0, column=1, padx=5)

        btn_delete = tk.Button(frame_buttons, text="Xóa", command=self.delete_order)
        btn_delete.grid(row=0, column=2, padx=5)

        self.tree = ttk.Treeview(self.window, columns=labels, show='headings', selectmode="browse")
        for label in labels:
            self.tree.heading(label, text=label)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    def on_item_selected(self, event):
        """ Điền thông tin đơn hàng vào ô nhập khi chọn một dòng trong bảng """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        order_data = self.tree.item(selected_item[0], "values")

        self.selected_order_id = order_data[0]  # Lưu mã đơn hàng để cập nhật
        for i, key in enumerate(self.entries.keys()):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, order_data[i])

    def add_order(self):
        """ Thêm đơn hàng mới vào database """
        order_data = [entry.get() for entry in self.entries.values()]

        if not all(order_data):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            with sqlite3.connect("car_dealership.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', order_data)
                conn.commit()

            messagebox.showinfo("Thành công", "Đơn hàng đã được thêm!")
            self.clear_entries()
            self.load_orders()

        except sqlite3.DatabaseError as e:
            messagebox.showerror("Lỗi", f"Không thể thêm đơn hàng: {e}")

    def update_order(self):
        """ Cập nhật đơn hàng đã chọn """
        if not self.selected_order_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn đơn hàng cần sửa!")
            return

        order_data = [entry.get() for entry in self.entries.values()]
        if not all(order_data):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            with sqlite3.connect("car_dealership.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''UPDATE orders 
                                  SET customer = ?, address = ?, phone = ?, car_model = ?, invoice = ?, staff = ?, status = ?
                                  WHERE order_id = ?''',
                               (order_data[1], order_data[2], order_data[3], order_data[4], order_data[5], order_data[6], order_data[7], self.selected_order_id))
                conn.commit()

            messagebox.showinfo("Thành công", "Đơn hàng đã được cập nhật!")
            self.clear_entries()
            self.load_orders()

        except sqlite3.DatabaseError as e:
            messagebox.showerror("Lỗi", f"Không thể sửa đơn hàng: {e}")

    def delete_order(self):
        """ Xóa đơn hàng được chọn """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn một đơn hàng để xóa!")
            return

        order_id = self.tree.item(selected_item[0], "values")[0]

        try:
            with sqlite3.connect("car_dealership.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''DELETE FROM orders WHERE order_id = ?''', (order_id,))
                conn.commit()

            messagebox.showinfo("Thành công", "Đơn hàng đã được xóa!")
            self.clear_entries()
            self.load_orders()

        except sqlite3.DatabaseError as e:
            messagebox.showerror("Lỗi", f"Không thể xóa đơn hàng: {e}")

    def load_orders(self):
        """ Load danh sách đơn hàng lên bảng """
        self.tree.delete(*self.tree.get_children())  # Xóa bảng cũ

        with sqlite3.connect("car_dealership.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders")
            orders = cursor.fetchall()

        for order in orders:
            self.tree.insert("", "end", values=order)

    def clear_entries(self):
        """ Xóa dữ liệu trong ô nhập """
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_order_id = None  # Xóa ID đơn hàng đang chọn


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

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item = self.tree.item(selected_item)
        values = item['values']

        # Gán dữ liệu vào ô nhập
        self.entries["Mã Hợp Đồng"].delete(0, tk.END)
        self.entries["Mã Hợp Đồng"].insert(0, values[0])

        self.entries["Mã Đơn Hàng"].delete(0, tk.END)
        self.entries["Mã Đơn Hàng"].insert(0, values[1])

        self.entries["Ngày Đặt Hàng"].delete(0, tk.END)
        self.entries["Ngày Đặt Hàng"].insert(0, values[2])

        self.entries["Ngày Bàn Giao"].delete(0, tk.END)
        self.entries["Ngày Bàn Giao"].insert(0, values[3])

        self.selected_warranty_file = values[4]  # Lưu phiếu bảo hành
        self.warranty_file_label.config(text=values[4])

    def update_contract(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn hợp đồng để sửa!")
            return

        item = self.tree.item(selected_item)
        contract_id = item['values'][0]  # Lấy Mã Hợp Đồng từ bảng

        order_id = self.entries["Mã Đơn Hàng"].get()
        order_date = self.entries["Ngày Đặt Hàng"].get()
        delivery_date = self.entries["Ngày Bàn Giao"].get()
        warranty = self.selected_warranty_file if hasattr(self, 'selected_warranty_file') else item['values'][4]

        if not order_id or not order_date or not delivery_date:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            conn = sqlite3.connect("car_dealership.db")
            cursor = conn.cursor()

            cursor.execute('''UPDATE contracts 
                              SET order_id = ?, order_date = ?, delivery_date = ?, warranty = ?
                              WHERE contract_id = ?''',
                           (order_id, order_date, delivery_date, warranty, contract_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Hợp đồng đã được cập nhật!")
            self.load_contracts()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật hợp đồng: {e}")

    def delete_contract(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn hợp đồng để xóa!")
            return

        item = self.tree.item(selected_item)
        contract_id = item['values'][0]

        # Hiện hộp thoại xác nhận
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa hợp đồng {contract_id} không?")
        if not confirm:
            return

        try:
            conn = sqlite3.connect("car_dealership.db")
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contracts WHERE contract_id = ?', (contract_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Hợp đồng đã được xóa!")
            self.load_contracts()  # Cập nhật lại danh sách
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa hợp đồng: {e}")

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
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

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

