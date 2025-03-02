import tkinter as tk
from tkinter import ttk
import subprocess

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Đại Lý Xe Hơi")
        self.root.geometry("600x400")
        self.root.configure(bg="#FFB6C1")

        title_label = tk.Label(root, text="HỆ THỐNG QUẢN LÝ ĐẠI LÝ XE HƠI",
                               font=("Arial", 16, "bold"), bg="#FFB6C1", fg="brown")
        title_label.pack(pady=10)

        button_names = [
            "Quản lý Xe", "Quản lý Khách Hàng", "Quản lý Nhân Viên",
            "Quản lý Đơn hàng & Hợp đồng", "Quản lý Tài Chính",
            "Quản lý Bảo Dưỡng & Bảo Hành", "Báo Cáo & Thống Kê",
            "Quản lý Kho Linh Kiện & Phụ Tùng", "Hệ Thống Đăng Nhập & Phân Quyền"
        ]

        for name in button_names:
            btn = tk.Button(root, text=name, font=("Arial", 12, "bold"),
                            bg="hot pink", fg="black", width=40, height=2,
                            command=lambda n=name: self.handle_button_click(n))
            btn.pack(pady=5)

    def handle_button_click(self, button_name):
        if button_name == "Quản lý Xe":
            subprocess.run(["python", "manage_car.py"])  # Mở manage_car.py
        elif button_name == "Quản lý Khách Hàng":
            subprocess.run(["python", "customer_management.py"])
        elif button_name == "Quản lý Nhân Viên":
            subprocess.run(["python", "customer_management.py"])
        else:
            print(f"Bạn đã nhấn vào: {button_name}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
