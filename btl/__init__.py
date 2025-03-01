class CarDealershipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Đại lý Xe hơi")
        self.root.geometry("900x600")  # Đặt kích thước cửa sổ

        self.create_sidebar()  # Gọi hàm tạo menu bên trái
        self.current_frame = None
        self.create_car_frame()  # Hiển thị giao diện quản lý xe ban đầu

    def create_sidebar(self):
        sidebar = tk.Frame(self.root, width=200, bg="#333", relief="raised")
        sidebar.pack(side="left", fill="y")

        menu_buttons = [
            ("Quản lý Xe", self.create_car_frame),
            ("Quản lý Khách hàng", self.create_customer_frame),
            ("Quản lý Đơn hàng & Hợp đồng", self.create_orders_frame),
            ("Quản lý Nhân viên & Phân quyền", self.create_staff_frame),
            ("Báo cáo & Thống kê", self.create_reports_frame)
        ]

        for text, command in menu_buttons:
            btn = tk.Button(sidebar, text=text, command=command, bg="#555", fg="white",
                            font=("Arial", 12), bd=0, padx=10, pady=5, anchor="w")
            btn.pack(fill="x", padx=10, pady=5)

    def switch_frame(self, new_frame_creator):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        new_frame_creator()
