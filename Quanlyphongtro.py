import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ====================================================================
# PHẦN 1: THÔNG TIN KẾT NỐI VÀ HÀM CƠ BẢN
# ====================================================================

DB_CONFIG = {
    'host': 'localhost',
    'database': 'Quan_ly_phong_tro',
    'user': 'root',
    'password': '2205'
}

# Sử dụng một vai trò bất kỳ để khởi động giao diện đầy đủ (Form 1-6)
CURRENT_USER_ROLE = 'Administrator' 


def create_db_connection():
    """Tạo và trả về đối tượng kết nối database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        messagebox.showerror("Lỗi Kết Nối", f"Không thể kết nối đến cơ sở dữ liệu:\n{e}\nVui lòng kiểm tra MySQL server, tên database, user và password.")
        return None

def print_invoice(ma_hdon):
    """Mô phỏng chức năng in hóa đơn/hợp đồng."""
    messagebox.showinfo("In Tài Liệu", f"Đang tiến hành in tài liệu có Mã: {ma_hdon}")

def print_list(list_name):
    """Mô phỏng chức năng in danh sách."""
    messagebox.showinfo("In Danh Sách", f"Đang tiến hành in danh sách: {list_name}")


# ====================================================================
# PHẦN 2: CÁC LỚP FORM (CÓ CHỨC NĂNG CSDL THỰC TẾ)
# ====================================================================

## 2.1. Form 1: Hóa Đơn
class InvoiceForm(ttk.Frame):
    def __init__(self, parent, db_connector):
        super().__init__(parent, padding="10")
        self.conn = db_connector
        ttk.Label(self, text="1. QUẢN LÝ HÓA ĐƠN", font=('Arial', 14, 'bold')).pack(pady=10)
        
        filter_frame = ttk.LabelFrame(self, text="Bộ Lọc Hóa Đơn"); filter_frame.pack(fill='x', pady=5, padx=5)
        self.combo_phong = self.create_filter_combo(filter_frame, "Phòng:"); self.combo_hd = self.create_filter_combo(filter_frame, "Hợp Đồng:")
        self.combo_thangnam = self.create_filter_combo(filter_frame, "Tháng/Năm:"); self.combo_tinhtrang = self.create_filter_combo(filter_frame, "Trạng Thái:", ['Tất cả', 'Đã Thanh Toán', 'Chưa Thanh Toán'])
        ttk.Button(filter_frame, text="Áp Dụng Lọc", command=self.load_invoice_data).pack(side=tk.LEFT, padx=10)
        self.load_filters()

        toolbar = ttk.Frame(self); toolbar.pack(fill='x', pady=5)
        ttk.Button(toolbar, text="In Hóa Đơn", command=lambda: self.print_selected_invoice()).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Tải lại", command=self.load_invoice_data).pack(side=tk.LEFT, padx=5)

        columns = ("MaHD", "NgayTao", "MaHDong", "MaPhong", "TinhTrang")
        self.invoice_tree = ttk.Treeview(self, columns=columns, show='headings', height=8)
        self.invoice_tree.heading("MaHD", text="Mã HĐ"); self.invoice_tree.heading("NgayTao", text="Ngày Tạo")
        self.invoice_tree.heading("MaHDong", text="Mã HĐ"); self.invoice_tree.heading("MaPhong", text="Phòng")
        self.invoice_tree.heading("TinhTrang", text="Tình Trạng"); self.invoice_tree.pack(fill='x', pady=(5, 10))
        self.invoice_tree.bind('<<TreeviewSelect>>', self.show_invoice_details)

        self.detail_frame = ttk.LabelFrame(self, text="Chi Tiết Dịch Vụ và Tính Tổng Tiền"); self.detail_frame.pack(fill='both', expand=True, padx=5)
        self.create_detail_treeview()
        self.total_label = ttk.Label(self.detail_frame, text="TỔNG CỘNG: 0 VNĐ", font=('Arial', 12, 'bold')); self.total_label.pack(fill='x', padx=5, pady=5)
        self.load_invoice_data()

    def create_filter_combo(self, parent, label_text, values=['Tất cả']):
        frame = ttk.Frame(parent); frame.pack(side=tk.LEFT, padx=10, pady=5); ttk.Label(frame, text=label_text).pack(side=tk.LEFT)
        combo = ttk.Combobox(frame, values=values, state="readonly", width=15); combo.set('Tất cả'); combo.pack(side=tk.LEFT); return combo

    def create_detail_treeview(self):
        columns = ("TenDV", "MaDV", "SoLuong", "DonGia", "ThanhTien"); self.detail_tree = ttk.Treeview(self.detail_frame, columns=columns, show='headings', height=5)
        self.detail_tree.heading("TenDV", text="Tên Dịch Vụ"); self.detail_tree.heading("MaDV", text="Mã DV"); self.detail_tree.heading("SoLuong", text="Số Lượng"); self.detail_tree.heading("DonGia", text="Đơn Giá (VNĐ)"); self.detail_tree.heading("ThanhTien", text="Thành Tiền (VNĐ)")
        self.detail_tree.column("TenDV", width=150, anchor=tk.W); self.detail_tree.column("MaDV", width=80, anchor=tk.CENTER); self.detail_tree.column("SoLuong", width=80, anchor=tk.CENTER); self.detail_tree.column("DonGia", width=120, anchor=tk.E); self.detail_tree.column("ThanhTien", width=120, anchor=tk.E)
        self.detail_tree.pack(fill='both', expand=True)

    def load_filters(self):
        if not self.conn or not self.conn.is_connected(): return
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT MaPhong FROM Phong ORDER BY MaPhong;"); phong_list = ['Tất cả'] + [r[0] for r in cursor.fetchall()]; self.combo_phong['values'] = phong_list
            cursor.execute("SELECT DISTINCT MaHDong FROM HopDong ORDER BY MaHDong;"); hd_list = ['Tất cả'] + [r[0] for r in cursor.fetchall()]; self.combo_hd['values'] = hd_list
            cursor.execute("SELECT DISTINCT YEAR(NgayTao), MONTH(NgayTao) FROM HoaDon ORDER BY 1 DESC, 2 DESC;"); thangnam_list = ['Tất cả'] + [f"T{r[1]}/{r[0]}" for r in cursor.fetchall()]; self.combo_thangnam['values'] = thangnam_list
            cursor.close()
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi tải bộ lọc:\n{e}")

    def load_invoice_data(self):
        if not self.conn or not self.conn.is_connected(): return
        for item in self.invoice_tree.get_children(): self.invoice_tree.delete(item)
        query = "SELECT HDN.MaHDon, HDN.NgayTao, H.MaHDong, H.MaPhong, HDN.TinhTrang FROM HoaDon HDN JOIN HopDong H ON HDN.MaHDong = H.MaHDong WHERE 1=1"
        params = []
        if self.combo_phong.get() != 'Tất cả': query += " AND H.MaPhong = %s"; params.append(self.combo_phong.get())
        if self.combo_hd.get() != 'Tất cả': query += " AND H.MaHDong = %s"; params.append(self.combo_hd.get())
        if self.combo_tinhtrang.get() != 'Tất cả': query += " AND HDN.TinhTrang = %s"; params.append(self.combo_tinhtrang.get())
        if self.combo_thangnam.get() != 'Tất cả':
            month = int(self.combo_thangnam.get().split('/')[0][1:]); year = int(self.combo_thangnam.get().split('/')[1])
            query += " AND MONTH(HDN.NgayTao) = %s AND YEAR(HDN.NgayTao) = %s"; params.append(month); params.append(year)
        query += " ORDER BY HDN.NgayTao DESC;"

        try:
            cursor = self.conn.cursor(); cursor.execute(query, params); records = cursor.fetchall(); cursor.close()
            for row in records:
                ngay_tao_str = row[1].strftime('%d/%m/%Y') if row[1] else ''; self.invoice_tree.insert("", tk.END, values=(row[0], ngay_tao_str, row[2], row[3], row[4]))
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Hóa Đơn:\n{e}")
            
    def show_invoice_details(self, event):
        selected_item = self.invoice_tree.focus();
        if not selected_item:
            for item in self.detail_tree.get_children(): self.detail_tree.delete(item); self.total_label.config(text="TỔNG CỘNG: 0 VNĐ"); return
        ma_hdon = self.invoice_tree.item(selected_item, 'values')[0];
        if not self.conn or not self.conn.is_connected(): return
        for item in self.detail_tree.get_children(): self.detail_tree.delete(item)
        query_details = "SELECT DV.TenDV, CT.MaDV, CT.SoLuong, DV.DonGia, (CT.SoLuong * DV.DonGia) AS ThanhTien FROM ChiTietHoaDon CT JOIN DichVu DV ON CT.MaDV = DV.MaDV WHERE CT.MaHDon = %s;"
        query_gia_phong = "SELECT H.GiaPhong FROM HoaDon HDN JOIN HopDong H ON HDN.MaHDong = H.MaHDong WHERE HDN.MaHDon = %s;"
        tong_tien = 0

        try:
            cursor = self.conn.cursor(); cursor.execute(query_gia_phong, (ma_hdon,))
            gia_phong_row = cursor.fetchone(); gia_phong = gia_phong_row[0] if gia_phong_row else 0; tong_tien += gia_phong
            self.detail_tree.insert("", tk.END, values=("Tiền thuê phòng", "PHONG", 1, f"{gia_phong:,}", f"{gia_phong:,}"))
            cursor.execute(query_details, (ma_hdon,)); dich_vu_records = cursor.fetchall(); cursor.close()
            for row in dich_vu_records:
                ten_dv, ma_dv, so_luong, don_gia, thanh_tien = row; tong_tien += thanh_tien if thanh_tien is not None else 0
                self.detail_tree.insert("", tk.END, values=(ten_dv, ma_dv, so_luong, f"{don_gia:,}", f"{thanh_tien:,}"))
            self.total_label.config(text=f"TỔNG CỘNG HÓA ĐƠN: {tong_tien:,} VNĐ")
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi tải chi tiết hóa đơn:\n{e}")

    def print_selected_invoice(self):
        selected_item = self.invoice_tree.focus();
        if selected_item: print_invoice(self.invoice_tree.item(selected_item, 'values')[0])
        else: messagebox.showwarning("In Hóa Đơn", "Vui lòng chọn một hóa đơn từ danh sách.")

## 2.2. Form 2: Hợp Đồng (Lọc theo Khu, Phòng)
class ContractForm(ttk.Frame):
    def __init__(self, parent, db_connector):
        super().__init__(parent, padding="10"); self.conn = db_connector
        ttk.Label(self, text="2. QUẢN LÝ HỢP ĐỒNG", font=('Arial', 14, 'bold')).pack(pady=10)
        
        filter_frame = ttk.LabelFrame(self, text="Bộ Lọc Hợp Đồng"); filter_frame.pack(fill='x', pady=5, padx=5)
        frame_khu = ttk.Frame(filter_frame); frame_khu.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(frame_khu, text="Khu Trọ:").pack(side=tk.LEFT)
        self.combo_khu = ttk.Combobox(frame_khu, state="readonly", width=20); self.combo_khu.pack(side=tk.LEFT)
        self.combo_khu.bind("<<ComboboxSelected>>", self.filter_rooms)
        frame_phong = ttk.Frame(filter_frame); frame_phong.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(frame_phong, text="Phòng:").pack(side=tk.LEFT)
        self.combo_phong = ttk.Combobox(frame_phong, state="readonly", width=15); self.combo_phong.pack(side=tk.LEFT)
        ttk.Button(filter_frame, text="Áp Dụng Lọc", command=self.load_contract_data).pack(side=tk.LEFT, padx=10)
        self.load_khu_data()

        toolbar = ttk.Frame(self); toolbar.pack(fill='x', pady=5)
        ttk.Button(toolbar, text="In Hợp Đồng", command=lambda: print_invoice("HD_SAMPLE")).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Tải lại", command=self.load_contract_data).pack(side=tk.LEFT, padx=5)
        
        columns = ("MaHDong", "MaPhong", "GiaPhong", "NgayBD", "NgayKT", "TenNguoiThue")
        self.contract_tree = ttk.Treeview(self, columns=columns, show='headings', height=8)
        self.contract_tree.heading("MaHDong", text="Mã HĐ"); self.contract_tree.heading("MaPhong", text="Phòng"); self.contract_tree.heading("GiaPhong", text="Giá Phòng (VNĐ)")
        self.contract_tree.heading("NgayBD", text="Ngày BĐ"); self.contract_tree.heading("NgayKT", text="Ngày KT"); self.contract_tree.heading("TenNguoiThue", text="Người Thuê Chính")
        self.contract_tree.column("MaHDong", width=80, anchor=tk.W); self.contract_tree.column("MaPhong", width=80, anchor=tk.CENTER); self.contract_tree.column("GiaPhong", width=120, anchor=tk.E)
        self.contract_tree.column("NgayBD", width=100, anchor=tk.CENTER); self.contract_tree.column("NgayKT", width=100, anchor=tk.CENTER); self.contract_tree.column("TenNguoiThue", width=180, anchor=tk.W)
        self.contract_tree.pack(fill='x', pady=(5, 10))
        self.load_contract_data()
    
    def load_khu_data(self):
        if not self.conn or not self.conn.is_connected(): return
        query = "SELECT MaKhu, Ten FROM KhuTro ORDER BY Ten;"
        try:
            cursor = self.conn.cursor(); cursor.execute(query); khu_records = cursor.fetchall(); cursor.close()
            self.khu_map = {f"{r[0]} - {r[1]}": r[0] for r in khu_records}
            khu_list = ['Tất cả'] + list(self.khu_map.keys())
            self.combo_khu['values'] = khu_list; self.combo_khu.set('Tất cả')
            self.combo_phong['values'] = ['Tất cả']; self.combo_phong.set('Tất cả')
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Khu Trọ:\n{e}")

    def filter_rooms(self, event=None):
        if not self.conn or not self.conn.is_connected(): return
        selected_khu_display = self.combo_khu.get(); self.combo_phong.set('Tất cả'); self.combo_phong['values'] = ['Tất cả']
        if selected_khu_display == 'Tất cả': return
        ma_khu = self.khu_map.get(selected_khu_display)
        if not ma_khu: return
        query = "SELECT MaPhong FROM Phong WHERE MaKhu = %s ORDER BY MaPhong;"
        try:
            cursor = self.conn.cursor(); cursor.execute(query, (ma_khu,)); room_records = cursor.fetchall(); cursor.close()
            room_list = ['Tất cả'] + [r[0] for r in room_records]; self.combo_phong['values'] = room_list; self.combo_phong.set('Tất cả')
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi lọc Phòng:\n{e}")

    def load_contract_data(self):
        if not self.conn or not self.conn.is_connected(): return
        for item in self.contract_tree.get_children(): self.contract_tree.delete(item)
        selected_khu_display = self.combo_khu.get(); selected_phong = self.combo_phong.get()
        query = """
        SELECT HD.MaHDong, HD.MaPhong, HD.GiaPhong, HD.NgayBD, HD.NgayKT, NT.HoTen
        FROM HopDong HD JOIN KiKet KK ON HD.MaHDong = KK.MaHDong JOIN NguoiThue NT ON KK.CCCD = NT.CCCD
        JOIN Phong P ON HD.MaPhong = P.MaPhong WHERE 1=1"""
        params = []
        if selected_khu_display != 'Tất cả' and selected_khu_display in self.khu_map:
            ma_khu = self.khu_map[selected_khu_display]; query += " AND P.MaKhu = %s"; params.append(ma_khu)
        if selected_phong != 'Tất cả': query += " AND HD.MaPhong = %s"; params.append(selected_phong)
        query += " ORDER BY HD.NgayBD DESC;"
        try:
            cursor = self.conn.cursor(); cursor.execute(query, params); records = cursor.fetchall(); cursor.close()
            for row in records:
                ma_hdong, ma_phong, gia_phong, ngay_bd, ngay_kt, ho_ten = row
                ngay_bd_str = ngay_bd.strftime('%d/%m/%Y') if ngay_bd else 'N/A'; ngay_kt_str = ngay_kt.strftime('%d/%m/%Y') if ngay_kt else 'N/A'
                self.contract_tree.insert("", tk.END, values=(ma_hdong, ma_phong, f"{gia_phong:,}", ngay_bd_str, ngay_kt_str, ho_ten))
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Hợp Đồng:\n{e}")

## 2.3. Form 3: Danh sách Phòng (Lọc theo Khu, Trạng thái)
class RoomForm(ttk.Frame):
    def __init__(self, parent, db_connector):
        super().__init__(parent, padding="10"); self.conn = db_connector
        ttk.Label(self, text="3. DANH SÁCH PHÒNG", font=('Arial', 14, 'bold')).pack(pady=10)
        filter_frame = ttk.LabelFrame(self, text="Bộ Lọc Phòng"); filter_frame.pack(fill='x', pady=5, padx=5)
        frame_khu = ttk.Frame(filter_frame); frame_khu.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(frame_khu, text="Khu Trọ:").pack(side=tk.LEFT); self.combo_khu = ttk.Combobox(frame_khu, state="readonly", width=20); self.combo_khu.pack(side=tk.LEFT)
        frame_trang_thai = ttk.Frame(filter_frame); frame_trang_thai.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(frame_trang_thai, text="Trạng Thái:").pack(side=tk.LEFT); self.combo_trang_thai = ttk.Combobox(frame_trang_thai, state="readonly", width=15, values=['Tất cả', 'Trong', 'DaThue']); self.combo_trang_thai.set('Tất cả'); self.combo_trang_thai.pack(side=tk.LEFT)
        ttk.Button(filter_frame, text="Áp Dụng Lọc", command=self.load_room_data).pack(side=tk.LEFT, padx=10)
        self.load_khu_data()
        toolbar = ttk.Frame(self); toolbar.pack(fill='x', pady=5)
        ttk.Button(toolbar, text="In Danh Sách Phòng", command=lambda: print_list("DanhSachPhong")).pack(side=tk.LEFT, padx=5); ttk.Button(toolbar, text="Tải lại", command=self.load_room_data).pack(side=tk.LEFT, padx=5)
        columns = ("MaPhong", "TrangThai", "MaKhu", "TenKhuTro", "GiaPhong"); self.room_tree = ttk.Treeview(self, columns=columns, show='headings')
        self.room_tree.heading("MaPhong", text="Mã Phòng"); self.room_tree.heading("TrangThai", text="Trạng Thái"); self.room_tree.heading("MaKhu", text="Mã Khu"); self.room_tree.heading("TenKhuTro", text="Tên Khu Trọ")
        self.room_tree.heading("GiaPhong", text="Giá Thuê (VNĐ)"); self.room_tree.column("MaPhong", width=100, anchor=tk.W); self.room_tree.column("TrangThai", width=120, anchor=tk.CENTER)
        self.room_tree.column("MaKhu", width=80, anchor=tk.CENTER); self.room_tree.column("TenKhuTro", width=180, anchor=tk.W); self.room_tree.column("GiaPhong", width=120, anchor=tk.E)
        self.room_tree.pack(fill='both', expand=True); self.room_tree.tag_configure('Trong', background='lightgreen'); self.load_room_data()
    
    def load_khu_data(self):
        if not self.conn or not self.conn.is_connected(): return
        query = "SELECT MaKhu, Ten FROM KhuTro ORDER BY Ten;"
        try:
            cursor = self.conn.cursor(); cursor.execute(query); khu_records = cursor.fetchall(); cursor.close()
            self.khu_map = {f"{r[0]} - {r[1]}": r[0] for r in khu_records}
            khu_list = ['Tất cả'] + list(self.khu_map.keys()); self.combo_khu['values'] = khu_list; self.combo_khu.set('Tất cả')
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Khu Trọ:\n{e}")

    def load_room_data(self):
        if not self.conn or not self.conn.is_connected(): return
        for item in self.room_tree.get_children(): self.room_tree.delete(item)
        selected_khu_display = self.combo_khu.get(); selected_trang_thai = self.combo_trang_thai.get()
        query = """
        SELECT P.MaPhong, P.TrangThai, P.MaKhu, KT.Ten, HD.GiaPhong 
        FROM Phong P JOIN KhuTro KT ON P.MaKhu = KT.MaKhu LEFT JOIN HopDong HD ON P.MaPhong = HD.MaPhong AND P.TrangThai = 'DaThue' WHERE 1=1"""
        params = []
        if selected_khu_display != 'Tất cả' and selected_khu_display in self.khu_map:
            ma_khu = self.khu_map[selected_khu_display]; query += " AND P.MaKhu = %s"; params.append(ma_khu)
        if selected_trang_thai != 'Tất cả': query += " AND P.TrangThai = %s"; params.append(selected_trang_thai)
        query += " ORDER BY P.MaKhu, P.MaPhong;"
        try:
            cursor = self.conn.cursor(); cursor.execute(query, params); records = cursor.fetchall(); cursor.close()
            for row in records:
                gia_phong = f"{row[4]:,}" if row[4] else "N/A"
                if row[1] == 'Trong':
                    self.room_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], gia_phong), tags=('Trong',))
                else:
                    self.room_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], gia_phong))
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Phòng:\n{e}")


## 2.4. Form 4: Danh sách Người Thuê (Lọc theo Khu)
class TenantForm(ttk.Frame):
    def __init__(self, parent, db_connector):
        super().__init__(parent, padding="10"); self.conn = db_connector
        ttk.Label(self, text="4. DANH SÁCH NGƯỜI THUÊ", font=('Arial', 14, 'bold')).pack(pady=10)
        filter_frame = ttk.LabelFrame(self, text="Bộ Lọc Khu Trọ"); filter_frame.pack(fill='x', pady=5, padx=5)
        frame_khu = ttk.Frame(filter_frame); frame_khu.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(frame_khu, text="Khu Trọ:").pack(side=tk.LEFT); self.combo_khu = ttk.Combobox(frame_khu, state="readonly", width=20); self.combo_khu.pack(side=tk.LEFT)
        ttk.Button(filter_frame, text="Áp Dụng Lọc", command=self.load_tenant_data).pack(side=tk.LEFT, padx=10)
        self.load_khu_data()
        toolbar = ttk.Frame(self); toolbar.pack(fill='x', pady=5)
        ttk.Button(toolbar, text="In Danh Sách Người Thuê", command=lambda: print_list("DanhSachNguoiThue")).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Tải lại", command=self.load_tenant_data).pack(side=tk.LEFT, padx=5)
        columns = ("CCCD", "HoTen", "SDT", "MaPhong", "TenKhu"); self.tenant_tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tenant_tree.heading("CCCD", text="CCCD"); self.tenant_tree.heading("HoTen", text="Họ Tên"); self.tenant_tree.heading("SDT", text="SĐT"); self.tenant_tree.heading("MaPhong", text="Phòng"); self.tenant_tree.heading("TenKhu", text="Khu Trọ");
        self.tenant_tree.column("CCCD", width=120, anchor=tk.W); self.tenant_tree.column("HoTen", width=180, anchor=tk.W); self.tenant_tree.column("SDT", width=120, anchor=tk.CENTER); self.tenant_tree.column("MaPhong", width=80, anchor=tk.CENTER); self.tenant_tree.column("TenKhu", width=150, anchor=tk.W);
        self.tenant_tree.pack(fill='both', expand=True); self.load_tenant_data()

    def load_khu_data(self):
        if not self.conn or not self.conn.is_connected(): return
        query = "SELECT MaKhu, Ten FROM KhuTro ORDER BY Ten;"
        try:
            cursor = self.conn.cursor(); cursor.execute(query); khu_records = cursor.fetchall(); cursor.close()
            self.khu_map = {f"{r[0]} - {r[1]}": r[0] for r in khu_records}
            khu_list = ['Tất cả'] + list(self.khu_map.keys()); self.combo_khu['values'] = khu_list; self.combo_khu.set('Tất cả')
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Khu Trọ:\n{e}")

    def load_tenant_data(self):
        if not self.conn or not self.conn.is_connected(): return
        for item in self.tenant_tree.get_children(): self.tenant_tree.delete(item)
        selected_khu_display = self.combo_khu.get()
        query = """
        SELECT NT.CCCD, NT.HoTen, NT.SDT, P.MaPhong, KT.Ten FROM NguoiThue NT
        JOIN KiKet KK ON NT.CCCD = KK.CCCD JOIN HopDong HD ON KK.MaHDong = HD.MaHDong
        JOIN Phong P ON HD.MaPhong = P.MaPhong JOIN KhuTro KT ON P.MaKhu = KT.MaKhu WHERE 1=1"""
        params = []
        if selected_khu_display != 'Tất cả' and selected_khu_display in self.khu_map:
            ma_khu = self.khu_map[selected_khu_display]; query += " AND P.MaKhu = %s"; params.append(ma_khu)
        query += " ORDER BY KT.Ten, P.MaPhong, NT.HoTen;"
        try:
            cursor = self.conn.cursor(); cursor.execute(query, params); records = cursor.fetchall(); cursor.close()
            for row in records: self.tenant_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4]))
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Người Thuê:\n{e}")

## 2.5. Form 5: Danh sách Quản Lý (Kèm Khu Phụ Trách)
class ManagerForm(ttk.Frame):
    def __init__(self, parent, db_connector):
        super().__init__(parent, padding="10"); self.conn = db_connector
        ttk.Label(self, text="5. DANH SÁCH NGƯỜI QUẢN LÝ", font=('Arial', 14, 'bold')).pack(pady=10)
        toolbar = ttk.Frame(self); toolbar.pack(fill='x', pady=5)
        ttk.Button(toolbar, text="In Danh Sách Quản Lý", command=lambda: print_list("DanhSachQuanLy")).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Tải lại", command=self.load_manager_data).pack(side=tk.LEFT, padx=5)
        columns = ("CCCD", "HoTen", "SDT", "KhuTroPhuTrach"); self.manager_tree = ttk.Treeview(self, columns=columns, show='headings')
        self.manager_tree.heading("CCCD", text="CCCD"); self.manager_tree.heading("HoTen", text="Họ Tên"); self.manager_tree.heading("SDT", text="SĐT"); self.manager_tree.heading("KhuTroPhuTrach", text="Khu Trọ Phụ Trách");
        self.manager_tree.column("CCCD", width=120, anchor=tk.W); self.manager_tree.column("HoTen", width=180, anchor=tk.W); self.manager_tree.column("SDT", width=100, anchor=tk.CENTER); self.manager_tree.column("KhuTroPhuTrach", width=300, anchor=tk.W);
        self.manager_tree.pack(fill='both', expand=True, pady=(5, 10)); self.load_manager_data()

    def load_manager_data(self):
        if not self.conn or not self.conn.is_connected(): return
        for item in self.manager_tree.get_children(): self.manager_tree.delete(item)
        query = """
        SELECT NQL.CCCD, NQL.HoTen, NQL.SDT, GROUP_CONCAT(KT.Ten SEPARATOR ' | ') AS Khu_Phu_Trach
        FROM NguoiQuanLy NQL LEFT JOIN KhuTro KT ON NQL.CCCD = KT.CCCD
        GROUP BY NQL.CCCD, NQL.HoTen, NQL.SDT ORDER BY NQL.HoTen;"""
        try:
            cursor = self.conn.cursor(); cursor.execute(query); records = cursor.fetchall(); cursor.close()
            for row in records: 
                cccd, ho_ten, sdt, khu_phu_trach = row
                khu_display = khu_phu_trach if khu_phu_trach else "Chưa phân công"
                self.manager_tree.insert("", tk.END, values=(cccd, ho_ten, sdt, khu_display))
        except Error as e: messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Quản Lý:\n{e}")

## 2.6. Form 6: Báo Cáo & Thống Kê (Tính Tổng Doanh Thu Tháng)
## 2.6. Form 6: Báo Cáo & Thống Kê (Báo cáo theo Khu Trọ)
class ReportForm(ttk.Frame):
    def __init__(self, parent, db_connector):
        super().__init__(parent, padding="10"); 
        self.conn = db_connector
        
        ttk.Label(self, text="6. BÁO CÁO DOANH THU THEO KHU", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # --- KHUNG LỌC THEO THÁNG ---
        filter_frame = ttk.LabelFrame(self, text="Bộ Lọc Thời Gian")
        filter_frame.pack(fill='x', pady=5, padx=5)
        
        frame_thangnam = ttk.Frame(filter_frame); frame_thangnam.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(frame_thangnam, text="Tháng/Năm:").pack(side=tk.LEFT)
        self.combo_thangnam = ttk.Combobox(frame_thangnam, state="readonly", width=15); self.combo_thangnam.pack(side=tk.LEFT)
        self.load_month_filter()
        
        ttk.Button(filter_frame, text="Tạo Báo Cáo", command=self.load_report_data).pack(side=tk.LEFT, padx=10)
        
        # --- KẾT QUẢ TỔNG HỢP ---
        self.tong_doanh_thu_var = tk.StringVar(value="Tổng Doanh Thu Chung: 0 VNĐ")
        ttk.Label(self, textvariable=self.tong_doanh_thu_var, font=('Arial', 12, 'bold')).pack(pady=10)
        
        columns = ("TenKhu", "TongGiaPhong", "TongDichVu", "TongDoanhThu")
        self.report_tree = ttk.Treeview(self, columns=columns, show='headings', height=10)
        self.report_tree.heading("TenKhu", text="Tên Khu Trọ"); 
        self.report_tree.heading("TongGiaPhong", text="Tổng Tiền Phòng (VNĐ)");
        self.report_tree.heading("TongDichVu", text="Tổng Tiền Dịch Vụ (VNĐ)");
        self.report_tree.heading("TongDoanhThu", text="TỔNG DOANH THU (VNĐ)");

        self.report_tree.column("TenKhu", width=150, anchor=tk.W); 
        self.report_tree.column("TongGiaPhong", width=150, anchor=tk.E); 
        self.report_tree.column("TongDichVu", width=150, anchor=tk.E);
        self.report_tree.column("TongDoanhThu", width=180, anchor=tk.E);
        self.report_tree.pack(fill='both', expand=True, pady=(5, 10))
        
        # --- Nút In ---
        toolbar = ttk.Frame(self); toolbar.pack(fill='x', pady=5)
        ttk.Button(toolbar, text="In Báo Cáo Chi Tiết", command=lambda: print_list("BaoCaoDoanhThuTheoKhu")).pack(side=tk.LEFT, padx=5)
        
        self.load_report_data() # Tải báo cáo ban đầu

    def load_month_filter(self):
        """Tải danh sách Tháng/Năm từ bảng HoaDon."""
        if not self.conn or not self.conn.is_connected(): return
        
        query = "SELECT DISTINCT YEAR(NgayTao), MONTH(NgayTao) FROM HoaDon ORDER BY 1 DESC, 2 DESC;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            thangnam_list = [f"T{r[1]}/{r[0]}" for r in cursor.fetchall()]
            cursor.close()
            
            current_month = datetime.now().strftime("T%#m/%Y")
            if current_month not in thangnam_list: thangnam_list.insert(0, current_month)
                
            self.combo_thangnam['values'] = thangnam_list
            if thangnam_list: self.combo_thangnam.set(thangnam_list[0])

        except Error as e:
            messagebox.showerror("Lỗi DB", f"Lỗi khi tải bộ lọc Tháng/Năm:\n{e}")

    def load_report_data(self):
        """Tính Tổng Tiền Phòng và Tổng Tiền Dịch Vụ theo từng Khu Trọ."""
        if not self.conn or not self.conn.is_connected(): return
        
        for item in self.report_tree.get_children(): self.report_tree.delete(item)

        selected_thangnam = self.combo_thangnam.get()
        if not selected_thangnam or selected_thangnam.lower() == 'tất cả':
            messagebox.showwarning("Lỗi Báo Cáo", "Vui lòng chọn một Tháng/Năm cụ thể."); return
        
        try:
            month = int(selected_thangnam.split('/')[0][1:])
            year = int(selected_thangnam.split('/')[1])
        except (ValueError, IndexError):
            messagebox.showerror("Lỗi Định Dạng", "Định dạng Tháng/Năm không hợp lệ."); return

        # Truy vấn phức hợp: Lấy tên khu, tổng tiền phòng, tổng tiền dịch vụ theo từng khu trọ
        query = """
        SELECT
            KT.Ten AS TenKhu,
            SUM(H.GiaPhong) AS TongGiaPhong,
            SUM(T.TongDichVu) AS TongTienDichVu
        FROM
            HoaDon HDN
        JOIN
            HopDong H ON HDN.MaHDong = H.MaHDong
        JOIN
            Phong P ON H.MaPhong = P.MaPhong
        JOIN
            KhuTro KT ON P.MaKhu = KT.MaKhu
        JOIN
            (SELECT 
                CT.MaHDon, SUM(CT.SoLuong * DV.DonGia) AS TongDichVu
             FROM 
                ChiTietHoaDon CT JOIN DichVu DV ON CT.MaDV = DV.MaDV
             GROUP BY CT.MaHDon) AS T ON HDN.MaHDon = T.MaHDon
        WHERE
            MONTH(HDN.NgayTao) = %s AND YEAR(HDN.NgayTao) = %s
        GROUP BY
            KT.Ten
        ORDER BY
            TongGiaPhong DESC;
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (month, year))
            records = cursor.fetchall()
            cursor.close()

            tong_doanh_thu_chung = 0
            
            for row in records:
                ten_khu, tong_gia_phong, tong_tien_dich_vu = row
                
                # Xử lý NULL và tính tổng cộng cho khu đó
                tong_gia_phong = tong_gia_phong if tong_gia_phong is not None else 0
                tong_tien_dich_vu = tong_tien_dich_vu if tong_tien_dich_vu is not None else 0
                tong_khu = tong_gia_phong + tong_tien_dich_vu
                
                tong_doanh_thu_chung += tong_khu
                
                # Chèn dữ liệu vào Treeview
                self.report_tree.insert("", tk.END, values=(
                    ten_khu, 
                    f"{tong_gia_phong:,}", 
                    f"{tong_tien_dich_vu:,}", 
                    f"{tong_khu:,}"
                ))
            
            # Cập nhật label tổng doanh thu chung
            self.tong_doanh_thu_var.set(f"TỔNG DOANH THU CHUNG THÁNG {selected_thangnam}: {tong_doanh_thu_chung:,} VNĐ")

        except Error as e:
            messagebox.showerror("Lỗi DB", f"Lỗi khi tính toán doanh thu theo khu:\n{e}")
# ====================================================================
# PHẦN 3: ỨNG DỤNG CHÍNH (THÊM CÁC FORM THEO THỨ TỰ MỚI)
# ====================================================================

class QuanLyApp:
    def __init__(self, master):
        self.master = master
        master.title("Hệ Thống Quản Lý Phòng Trọ (6 Forms Đầy Đủ)")
        master.geometry("1000x700")

        self.conn = self.create_db_connection()
        if not self.conn:
            master.destroy(); return

        self.notebook = ttk.Notebook(master); self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # THÊM CÁC FORM THEO THỨ TỰ YÊU CẦU MỚI NHẤT
        self.add_tab("1. Hóa Đơn", InvoiceForm)
        self.add_tab("2. Hợp Đồng", ContractForm)
        self.add_tab("3. Danh sách Phòng", RoomForm)
        self.add_tab("4. Danh sách Người Thuê", TenantForm)
        self.add_tab("5. Danh sách Quản Lý", ManagerForm)
        self.add_tab("6. Báo Cáo & Thống Kê", ReportForm)

    def create_db_connection(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG); print("✅ Kết nối database thành công."); return conn
        except Error as e: return None

    def add_tab(self, title, form_class):
        frame = form_class(self.notebook, self.conn)
        self.notebook.add(frame, text=title)

    def on_closing(self):
        if self.conn and self.conn.is_connected():
            self.conn.close(); print("Đã đóng kết nối MySQL khi thoát ứng dụng.")
        self.master.destroy()

# ====================================================================
# PHẦN 4: CHẠY ỨNG DỤNG
# ====================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = QuanLyApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()