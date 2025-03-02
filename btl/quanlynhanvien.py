import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def connect_db():
    conn = sqlite3.connect("car_dealership.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            position TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Nhân Viên - Đại lý Xe hơi")
        self.root.geometry("1000x600")
        connect_db()
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Quản lý Nhân Viên", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=10, fill=tk.X)

        btn_texts = ["Thêm nhân viên", "Sửa thông tin nhân viên", "Xóa nhân viên"]
        btn_commands = [self.open_add_window, self.open_update_window, self.open_delete_window]

        for i, (text, command) in enumerate(zip(btn_texts, btn_commands)):
            tk.Button(frame_buttons, text=text, command=command).pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(frame_buttons)
        self.search_entry.pack(side=tk.RIGHT, padx=5)

        self.search_option = ttk.Combobox(frame_buttons, values=["Mã nhân viên", "Chức vụ", "Phòng ban"])
        self.search_option.current(0)
        self.search_option.pack(side=tk.RIGHT, padx=5)

        tk.Button(frame_buttons, text="Tìm kiếm", command=self.search_employee).pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=(
        "Mã nhân viên", "Họ và tên", "Giới tính", "Địa chỉ", "Số điện thoại", "Chức vụ"), show='headings')
        for label in self.tree['columns']:
            self.tree.heading(label, text=label)
            self.tree.column(label, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.load_employees()

    def open_add_window(self):
        self.open_employee_window("Thêm Nhân Viên", self.add_employee)

    def open_update_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên để sửa!")
            return
        self.open_employee_window("Sửa Nhân Viên", self.update_employee, self.tree.item(selected_item, 'values'))

    def open_delete_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên để xóa!")
            return
        employee_id = self.tree.item(selected_item, 'values')[0]
        self.execute_db("DELETE FROM employees WHERE employee_id=?", (employee_id,))
        self.load_employees()

    def open_employee_window(self, title, save_command, values=None):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("400x400")
        labels = ["Mã nhân viên", "Họ và tên", "Giới tính", "Địa chỉ", "Số điện thoại", "Chức vụ"]
        self.entries = {}

        for i, text in enumerate(labels):
            tk.Label(window, text=text + ":").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            if values:
                entry.insert(0, values[i])
            self.entries[text] = entry

        tk.Button(window, text="Lưu", command=lambda: [save_command(), window.destroy()]).grid(pady=10)

    def execute_db(self, query, params=()):
        conn = sqlite3.connect("car_dealership.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def load_employees(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect("car_dealership.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row[1:])
        conn.close()

    def add_employee(self):
        data = [entry.get() for entry in self.entries.values()]
        if any(not field for field in data):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return
        self.execute_db("INSERT INTO employees VALUES (NULL, ?, ?, ?, ?, ?, ?)", data)
        self.load_employees()

    def update_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên để sửa!")
            return
        values = [entry.get() for entry in self.entries.values()]
        self.execute_db(
            "UPDATE employees SET employee_id=?, name=?, gender=?, address=?, phone=?, position=? WHERE employee_id=?",
            values + [self.tree.item(selected_item, 'values')[0]])
        self.load_employees()

    def search_employee(self):
        search_text = self.search_entry.get()
        search_field = self.search_option.get()
        field_mapping = {"Mã nhân viên": "employee_id", "Chức vụ": "position", "Phòng ban": "department"}
        query = f"SELECT * FROM employees WHERE {field_mapping[search_field]} LIKE ?"
        conn = sqlite3.connect("car_dealership.db")
        cursor = conn.cursor()
        cursor.execute(query, (f"%{search_text}%",))
        rows = cursor.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())
        if rows:
            for row in rows:
                self.tree.insert("", tk.END, values=row[1:])
        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy nhân viên!")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
