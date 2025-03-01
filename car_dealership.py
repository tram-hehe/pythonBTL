# File: car_dealership.py
import tkinter as tk
from tkinter import Menu
from manage_car import add_car_gui, show_cars_gui


def main_gui():
    root = tk.Tk()
    root.title("Quản lý Đại Lý Xe Hơi")

    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    car_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Quản lý Xe", menu=car_menu)
    car_menu.add_command(label="Thêm Xe", command=add_car_gui)
    car_menu.add_command(label="Xem Xe", command=show_cars_gui)

    customer_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Quản lý Khách Hàng", menu=customer_menu)

    employee_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Quản lý Nhân Viên", menu=employee_menu)

    order_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Quản lý Đơn Hàng & Hợp Đồng", menu=order_menu)

    report_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Báo Cáo & Thống Kê", menu=report_menu)

    system_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Hệ Thống", menu=system_menu)

    root.mainloop()


if __name__ == "__main__":
    main_gui()
