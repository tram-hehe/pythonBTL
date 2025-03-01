import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from manage_car import CarDealershipApp
from quanlykhachhang import CustomerManager
from qldonhanghopdong import CarDealerManagementApp


class CarDealerHome:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Quản lý Đại lý Xe hơi")
        self.root.geometry("900x600")

        # Load hình nền
        self.original_bg = Image.open("nenxee.png")  # Đảm bảo có ảnh trong thư mục
        self.bg_image = ImageTk.PhotoImage(self.original_bg)

        # Label hiển thị hình nền
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)  # Phủ kín giao diện

        # Cập nhật hình nền khi cửa sổ thay đổi kích thước
        self.root.bind("<Configure>", self.resize_background)

        self.create_widgets()

    def resize_background(self, event):
        """Tự động điều chỉnh kích thước hình nền khi thu phóng cửa sổ."""
        new_size = (event.width, event.height)
        resized_bg = self.original_bg.resize(new_size)
        self.bg_image = ImageTk.PhotoImage(resized_bg)
        self.bg_label.config(image=self.bg_image)

    def create_widgets(self):
        # Label tiêu đề, dính lên trên cùng và trải ngang
        title_label = tk.Label(self.root, text="HỆ THỐNG QUẢN LÝ ĐẠI LÝ XE HƠI", font=("Anton", 18, "bold"),
                               bg="#6E7B8B", fg="#000000", anchor="center")
        title_label.place(x=0, y=0, relwidth=1, height=50)  # Trải ngang hết màn hình

        # Frame chứa các nút để hình nền không che, dính sát bên trái và dọc theo màn hình
        self.frame = tk.Frame(self.root, bg="#363636", bd=2)
        self.frame.place(x=0, y=50, relheight=1, width=300)  # Tăng chiều rộng frame

        buttons = [
            ("Quản lý Xe", self.manage_cars),
            ("Quản lý Khách Hàng", self.manage_customers),
            ("Quản lý Nhân Viên", self.manage_employees),
            ("Quản lý Đơn hàng & Hợp đồng", self.manage_orders),
            ("Quản lý Tài Chính", self.manage_finances),
            ("Quản lý Bảo Dưỡng & Bảo Hành", self.manage_maintenance),
            ("Báo Cáo & Thống Kê", self.manage_reports),
            ("Quản lý Kho Linh Kiện & Phụ Tùng", self.manage_inventory),
            ("Hệ Thống Đăng Nhập & Phân Quyền", self.manage_auth)
        ]

        for text, command in buttons:
            btn = tk.Button(self.frame, text=text, command=command, bg="#000000", fg="white",
                            font=("Anton", 10, "bold"),
                            width=28, height=2, anchor="w", wraplength=260)
            btn.pack(pady=5, padx=10, fill=tk.X)

    def manage_cars(self):
        car_window = tk.Toplevel(self.root)
        car_window.title("Quản lý Xe")
        car_window.geometry("700x500")
        CarDealershipApp(car_window)  # Gọi form quản lý xe

    def manage_customers(self):
        car_window = tk.Toplevel(self.root)
        car_window.title("Quản lý Xe")
        car_window.geometry("700x500")
        CustomerManager(car_window)

    def manage_employees(self):
        messagebox.showinfo("Thông báo", "Chức năng Quản lý Nhân Viên đang phát triển!")

    def manage_orders(self):
        car_window = tk.Toplevel(self.root)
        car_window.title("Quản lý Đơn hàng & Hợp đồng")
        car_window.geometry("700x500")
        CarDealerManagementApp(car_window)  # Gọi form quản lý đơn hàng

    def manage_finances(self):
        messagebox.showinfo("Thông báo", "Chức năng Quản lý Tài Chính đang phát triển!")

    def manage_maintenance(self):
        messagebox.showinfo("Thông báo", "Chức năng Quản lý Bảo Dưỡng & Bảo Hành đang phát triển!")

    def manage_reports(self):
        messagebox.showinfo("Thông báo", "Chức năng Báo Cáo & Thống Kê đang phát triển!")

    def manage_inventory(self):
        messagebox.showinfo("Thông báo", "Chức năng Quản lý Kho Linh Kiện & Phụ Tùng đang phát triển!")

    def manage_auth(self):
        messagebox.showinfo("Thông báo", "Chức năng Hệ Thống Đăng Nhập & Phân Quyền đang phát triển!")


if __name__ == "__main__":
    root = tk.Tk()
    app = CarDealerHome(root)
    root.mainloop()
