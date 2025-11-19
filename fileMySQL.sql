CREATE SCHEMA `Quan_ly_phong_tro`;
USE `Quan_ly_phong_tro`;
CREATE TABLE `NguoiQuanLy` (
    `CCCD` VARCHAR(12) PRIMARY KEY,
    `HoTen` VARCHAR(100) NOT NULL,
    `SDT` CHAR(10) UNIQUE
);
INSERT INTO `NguoiQuanLy` (`CCCD`, `HoTen`, `SDT`)
VALUES 
    ('002234567891', 'Nguyễn Ngọc Anh', '0987654321'),
    ('003234567892', 'Nguyễn Kiều Linh', '0905111222');
CREATE TABLE `KhuTro` (
    `MaKhu` VARCHAR(50) PRIMARY KEY, 
    `Ten` VARCHAR(255) NOT NULL,
    `DiaChi` VARCHAR(255) NOT NULL,
    `SoLuongPhong` INT DEFAULT 0,
    `CCCD` VARCHAR(12),
    FOREIGN KEY (`CCCD`) REFERENCES `NguoiQuanLy`(`CCCD`)
);
INSERT INTO `KhuTro` (`MaKhu`, `Ten`, `DiaChi`, `SoLuongPhong`, `CCCD`)
VALUES 
    ('KHU_001', 'Khu trọ Hạnh Phúc', '789 Đường Mỹ Đình, Hà Nội', 12, '002234567891'),
    ('KHU_002', 'Nhà trọ Mặt Trời', '101 Đường Xuân Thủy, Hà Nội', 5, '003234567892'),
    ('KHU_003', 'Khu trọ Xanh', '22 Ngõ Hàng Bột, Hà Nội', 7, '002234567891'),
    ('KHU_004', 'Nhà trọ Hoa Sữa', '33 Phố Cổ, Hà Nội', 4, '003234567892'),
    ('KHU_005', 'Khu trọ Vạn An', '55 Đường Giải Phóng, Hà Nội', 10, '002234567891');
  
CREATE TABLE `Phong` (
    `MaPhong` VARCHAR(50) PRIMARY KEY,
    `TrangThai` VARCHAR(50) DEFAULT 'Trong',
    `MaKhu` VARCHAR(50) NOT NULL,
    FOREIGN KEY (`MaKhu`) REFERENCES `KhuTro`(`MaKhu`)
);
INSERT INTO `Phong` (`MaPhong`, `TrangThai`, `MaKhu`)
VALUES 
    -- 12 phòng cho KHU_001
    ('P101_KHU001', 'DaThue', 'KHU_001'),
    ('P102_KHU001', 'Trong', 'KHU_001'),
    ('P103_KHU001', 'DaThue', 'KHU_001'),
    ('P104_KHU001', 'Trong', 'KHU_001'),
    ('P105_KHU001', 'DaThue', 'KHU_001'),
    ('P106_KHU001', 'DaThue', 'KHU_001'),
    ('P201_KHU001', 'Trong', 'KHU_001'),
    ('P202_KHU001', 'DaThue', 'KHU_001'),
    ('P203_KHU001', 'Trong', 'KHU_001'),
    ('P204_KHU001', 'DaThue', 'KHU_001'),
    ('P301_KHU001', 'Trong', 'KHU_001'),
    ('P302_KHU001', 'Trong', 'KHU_001'),
    -- 5 phòng cho KHU_002
    ('P101_KHU002', 'DaThue', 'KHU_002'),
    ('P102_KHU002', 'DaThue', 'KHU_002'),
    ('P103_KHU002', 'Trong', 'KHU_002'),
    ('P201_KHU002', 'DaThue', 'KHU_002'),
    ('P202_KHU002', 'Trong', 'KHU_002'),
    -- 7 phòng cho KHU_003
    ('P101_KHU003', 'Trong', 'KHU_003'),
    ('P102_KHU003', 'DaThue', 'KHU_003'),
    ('P103_KHU003', 'Trong', 'KHU_003'),
    ('P201_KHU003', 'DaThue', 'KHU_003'),
    ('P202_KHU003', 'Trong', 'KHU_003'),
    ('P203_KHU003', 'DaThue', 'KHU_003'),
    ('P301_KHU003', 'Trong', 'KHU_003'),
    -- 4 phòng cho KHU_004
    ('P101_KHU004', 'DaThue', 'KHU_004'),
    ('P102_KHU004', 'DaThue', 'KHU_004'),
    ('P103_KHU004', 'DaThue', 'KHU_004'),
    ('P104_KHU004', 'Trong', 'KHU_004'),
    -- 10 phòng cho KHU_005
    ('P101_KHU005', 'Trong', 'KHU_005'),
    ('P102_KHU005', 'DaThue', 'KHU_005'),
    ('P103_KHU005', 'Trong', 'KHU_005'),
    ('P104_KHU005', 'DaThue', 'KHU_005'),
    ('P105_KHU005', 'Trong', 'KHU_005'),
    ('P201_KHU005', 'DaThue', 'KHU_005'),
    ('P202_KHU005', 'Trong', 'KHU_005'),
    ('P203_KHU005', 'DaThue', 'KHU_005'),
    ('P204_KHU005', 'Trong', 'KHU_005'),
    ('P205_KHU005', 'DaThue', 'KHU_005');

CREATE TABLE `NguoiThue` (
    `CCCD` VARCHAR(12) PRIMARY KEY,
    `HoTen` VARCHAR(100) NOT NULL,
    `SDT` VARCHAR(15)
);
INSERT INTO `NguoiThue` (`CCCD`, `HoTen`, `SDT`)
VALUES
    ('080123456001', 'Nguyễn Văn An', '0901111001'),
    ('080123456002', 'Trần Thị Bình', '0901111002'),
    ('080123456003', 'Lê Minh Cường', '0901111003'),
    ('080123456004', 'Phạm Thị Dung', '0901111004'),
    ('080123456005', 'Vũ Văn Hùng', '0901111005'),
    ('080123456006', 'Đỗ Thị Lan', '0901111006'),
    ('080123456007', 'Hoàng Minh Long', '0901111007'),
    ('080123456008', 'Bùi Thị Mai', '0901111008'),
    ('080123456009', 'Đặng Văn Nam', '0901111009'),
    ('080123456010', 'Hồ Thị Oanh', '0901111010'),
    ('080123456011', 'Lý Văn Phúc', '0901111011'),
    ('080123456012', 'Võ Thị Quyên', '0901111012'),
    ('080123456013', 'Ngô Minh Sơn', '0901111013'),
    ('080123456014', 'Phan Thị Tâm', '0901111014'),
    ('080123456015', 'Trịnh Văn Tùng', '0901111015'),
    ('080123456016', 'Lâm Thị Uyên', '0901111016'),
    ('080123456017', 'Châu Minh Vỹ', '0901111017'),
    ('080123456018', 'Mai Thị Xuân', '0901111018'),
    ('080123456019', 'Tô Văn Yến', '0901111019'),
    ('080123456020', 'Huỳnh Đức Toàn', '0901111020');

CREATE TABLE `DichVu` (
    `MaDV` VARCHAR(50) PRIMARY KEY, 
    `TenDV` VARCHAR(100) NOT NULL,
    `DonGia` BIGINT DEFAULT 0
);
INSERT INTO `DichVu` (`MaDV`, `TenDV`, `DonGia`)
VALUES 
    ('DV001', 'Tiền điện', 4000),
    ('DV002', 'Tiền nước', 30000),
    ('DV003', 'Tiền vệ sinh chung', 200000),
    ('DV004', 'Tiền Internet', 100000),
    ('DV005', 'Phí gửi xe (nếu có)', 100000);

CREATE TABLE `HopDong` (
    `MaHDong` VARCHAR(50) PRIMARY KEY, 
    `GiaPhong` BIGINT NOT NULL,
    `TienCoc` BIGINT DEFAULT 0,
    `NgayBD` DATE,
    `NgayKT` DATE,
    `MaPhong` VARCHAR(50) NOT NULL,
    FOREIGN KEY (`MaPhong`) REFERENCES `Phong`(`MaPhong`)
);
INSERT INTO `HopDong` (`MaHDong`, `GiaPhong`, `TienCoc`, `NgayBD`, `NgayKT`, `MaPhong`)
VALUES
    -- 6 phòng 'DaThue' của KHU_001
    ('HD001', 3000000, 3000000, '2025-01-01', '2026-01-01', 'P101_KHU001'),
    ('HD002', 3200000, 3200000, '2025-02-15', '2026-02-15', 'P103_KHU001'),
    ('HD003', 3000000, 3000000, '2025-03-01', '2026-03-01', 'P105_KHU001'),
    ('HD004', 3000000, 3000000, '2025-03-10', '2026-03-10', 'P106_KHU001'),
    ('HD005', 3500000, 3500000, '2025-04-05', '2026-04-05', 'P202_KHU001'),
    ('HD006', 3500000, 3500000, '2025-05-01', '2026-05-01', 'P204_KHU001'),
    
    -- 3 phòng 'DaThue' của KHU_002
    ('HD007', 2500000, 2500000, '2025-01-10', '2026-01-10', 'P101_KHU002'),
    ('HD008', 2500000, 2500000, '2025-02-20', '2026-02-20', 'P102_KHU002'),
    ('HD009', 2700000, 2700000, '2025-06-01', '2026-06-01', 'P201_KHU002'),
    
    -- 3 phòng 'DaThue' của KHU_003
    ('HD010', 2800000, 2800000, '2025-01-05', '2026-01-05', 'P102_KHU003'),
    ('HD011', 3000000, 3000000, '2025-03-15', '2026-03-15', 'P201_KHU003'),
    ('HD012', 3000000, 3000000, '2025-07-01', '2026-07-01', 'P203_KHU003'),
    
    -- 3 phòng 'DaThue' của KHU_004
    ('HD013', 4000000, 4000000, '2025-01-20', '2026-01-20', 'P101_KHU004'),
    ('HD014', 4000000, 4000000, '2025-04-10', '2026-04-10', 'P102_KHU004'),
    ('HD015', 4200000, 4200000, '2025-08-01', '2026-08-01', 'P103_KHU004'),
    
    -- 5 phòng 'DaThue' của KHU_005
    ('HD016', 2200000, 2200000, '2025-02-01', '2026-02-01', 'P102_KHU005'),
    ('HD017', 2200000, 2200000, '2025-05-15', '2026-05-15', 'P104_KHU005'),
    ('HD018', 2400000, 2400000, '2025-06-10', '2026-06-10', 'P201_KHU005'),
    ('HD019', 2400000, 2400000, '2025-07-07', '2026-07-07', 'P203_KHU005'),
    ('HD020', 2500000, 2500000, '2025-09-01', '2026-09-01', 'P205_KHU005');

CREATE TABLE `KiKet` (
    `MaHDong` VARCHAR(50) NOT NULL,
    `CCCD` VARCHAR(12) NOT NULL,
    `NgayLap` DATE,
    PRIMARY KEY (`MaHDong`, `CCCD`),
    FOREIGN KEY (`MaHDong`) REFERENCES `HopDong`(`MaHDong`),
    FOREIGN KEY (`CCCD`) REFERENCES `NguoiThue`(`CCCD`)
);
INSERT INTO `KiKet` (`MaHDong`, `CCCD`, `NgayLap`)
VALUES
    ('HD001', '080123456001', '2025-01-01'),
    ('HD002', '080123456002', '2025-02-15'),
    ('HD003', '080123456003', '2025-03-01'),
    ('HD004', '080123456004', '2025-03-10'),
    ('HD005', '080123456005', '2025-04-05'),
    ('HD006', '080123456006', '2025-05-01'),
    ('HD007', '080123456007', '2025-01-10'),
    ('HD008', '080123456008', '2025-02-20'),
    ('HD009', '080123456009', '2025-06-01'),
    ('HD010', '080123456010', '2025-01-05'),
    ('HD011', '080123456011', '2025-03-15'),
    ('HD012', '080123456012', '2025-07-01'),
    ('HD013', '080123456013', '2025-01-20'),
    ('HD014', '080123456014', '2025-04-10'),
    ('HD015', '080123456015', '2025-08-01'),
    ('HD016', '080123456016', '2025-02-01'),
    ('HD017', '080123456017', '2025-05-15'),
    ('HD018', '080123456018', '2025-06-10'),
    ('HD019', '080123456019', '2025-07-07'),
    ('HD020', '080123456020', '2025-09-01');

CREATE TABLE `HoaDon` (
    `MaHDon` VARCHAR(50) PRIMARY KEY,
    `TinhTrang` VARCHAR(50) DEFAULT 'ChuaThanhToan',
    `NgayTao` DATE,
    `MaHDong` VARCHAR(50) NOT NULL,
    FOREIGN KEY (`MaHDong`) REFERENCES `HopDong`(`MaHDong`)
);
INSERT INTO `HoaDon` (`MaHDon`, `TinhTrang`, `NgayTao`, `MaHDong`)
VALUES 
    ('HDN_T11_001', 'DaThanhToan', '2025-11-05', 'HD001'),
    ('HDN_T11_002', 'DaThanhToan', '2025-11-05', 'HD002'),
    ('HDN_T11_003', 'ChuaThanhToan', '2025-11-05', 'HD003'),
    ('HDN_T11_004', 'DaThanhToan', '2025-11-05', 'HD004'),
    ('HDN_T11_005', 'DaThanhToan', '2025-11-05', 'HD005'),
    ('HDN_T11_006', 'ChuaThanhToan', '2025-11-05', 'HD006'),
    ('HDN_T11_007', 'DaThanhToan', '2025-11-05', 'HD007'),
    ('HDN_T11_008', 'ChuaThanhToan', '2025-11-05', 'HD008'),
    ('HDN_T11_009', 'DaThanhToan', '2025-11-05', 'HD009'),
    ('HDN_T11_010', 'DaThanhToan', '2025-11-05', 'HD010'),
    ('HDN_T11_011', 'ChuaThanhToan', '2025-11-05', 'HD011'),
    ('HDN_T11_012', 'DaThanhToan', '2025-11-05', 'HD012'),
    ('HDN_T11_013', 'DaThanhToan', '2025-11-05', 'HD013'),
    ('HDN_T11_014', 'DaThanhToan', '2025-11-05', 'HD014'),
    ('HDN_T11_015', 'ChuaThanhToan', '2025-11-05', 'HD015'),
    ('HDN_T11_016', 'DaThanhToan', '2025-11-05', 'HD016'),
    ('HDN_T11_017', 'DaThanhToan', '2025-11-05', 'HD017'),
    ('HDN_T11_018', 'ChuaThanhToan', '2025-11-05', 'HD018'),
    ('HDN_T11_019', 'DaThanhToan', '2025-11-05', 'HD019'),
    ('HDN_T11_020', 'ChuaThanhToan', '2025-11-05', 'HD020');

CREATE TABLE `ChiTietHoaDon` (
    `MaHDon` VARCHAR(50) NOT NULL,
    `MaDV` VARCHAR(50) NOT NULL,
    `SoLuong` INT DEFAULT 0,
    PRIMARY KEY (`MaHDon`, `MaDV`),
    FOREIGN KEY (`MaHDon`) REFERENCES `HoaDon`(`MaHDon`),
    FOREIGN KEY (`MaDV`) REFERENCES `DichVu`(`MaDV`)
);
INSERT INTO `ChiTietHoaDon` (`MaHDon`, `MaDV`, `SoLuong`)
VALUES 
    -- Hóa đơn 001
    ('HDN_T11_001', 'DV001', 120),
    ('HDN_T11_001', 'DV002', 10),
    ('HDN_T11_001', 'DV003', 1),
    ('HDN_T11_001', 'DV004', 1),
    ('HDN_T11_001', 'DV005', 2), -- Có 2 xe

    -- Hóa đơn 002
    ('HDN_T11_002', 'DV001', 90),
    ('HDN_T11_002', 'DV002', 8),
    ('HDN_T11_002', 'DV003', 1),
    ('HDN_T11_002', 'DV004', 1),
    ('HDN_T11_002', 'DV005', 1), -- Có 1 xe

    -- Hóa đơn 003
    ('HDN_T11_003', 'DV001', 150),
    ('HDN_T11_003', 'DV002', 12),
    ('HDN_T11_003', 'DV003', 1),
    ('HDN_T11_003', 'DV004', 1),
    ('HDN_T11_003', 'DV005', 0), -- Không gửi xe

    -- Hóa đơn 004
    ('HDN_T11_004', 'DV001', 110),
    ('HDN_T11_004', 'DV002', 7),
    ('HDN_T11_004', 'DV003', 1),
    ('HDN_T11_004', 'DV004', 1),
    ('HDN_T11_004', 'DV005', 1),

    -- Hóa đơn 005
    ('HDN_T11_005', 'DV001', 200),
    ('HDN_T11_005', 'DV002', 15),
    ('HDN_T11_005', 'DV003', 1),
    ('HDN_T11_005', 'DV004', 1),
    ('HDN_T11_005', 'DV005', 2),

    -- Hóa đơn 006
    ('HDN_T11_006', 'DV001', 85),
    ('HDN_T11_006', 'DV002', 6),
    ('HDN_T11_006', 'DV003', 1),
    ('HDN_T11_006', 'DV004', 1),
    ('HDN_T11_006', 'DV005', 0),

    -- Hóa đơn 007
    ('HDN_T11_007', 'DV001', 130),
    ('HDN_T11_007', 'DV002', 9),
    ('HDN_T11_007', 'DV003', 1),
    ('HDN_T11_007', 'DV004', 1),
    ('HDN_T11_007', 'DV005', 1),

    -- Hóa đơn 008
    ('HDN_T11_008', 'DV001', 100),
    ('HDN_T11_008', 'DV002', 10),
    ('HDN_T11_008', 'DV003', 1),
    ('HDN_T11_008', 'DV004', 1),
    ('HDN_T11_008', 'DV005', 1),

    -- Hóa đơn 009
    ('HDN_T11_009', 'DV001', 125),
    ('HDN_T11_009', 'DV002', 11),
    ('HDN_T11_009', 'DV003', 1),
    ('HDN_T11_009', 'DV004', 1),
    ('HDN_T11_009', 'DV005', 2),

    -- Hóa đơn 010
    ('HDN_T11_010', 'DV001', 70),
    ('HDN_T11_010', 'DV002', 5),
    ('HDN_T11_010', 'DV003', 1),
    ('HDN_T11_010', 'DV004', 1),
    ('HDN_T11_010', 'DV005', 1),

    -- Hóa đơn 011
    ('HDN_T11_011', 'DV001', 115),
    ('HDN_T11_011', 'DV002', 8),
    ('HDN_T11_011', 'DV003', 1),
    ('HDN_T11_011', 'DV004', 1),
    ('HDN_T11_011', 'DV005', 0),

    -- Hóa đơn 012
    ('HDN_T11_012', 'DV001', 140),
    ('HDN_T11_012', 'DV002', 12),
    ('HDN_T11_012', 'DV003', 1),
    ('HDN_T11_012', 'DV004', 1),
    ('HDN_T11_012', 'DV005', 1),

    -- Hóa đơn 013
    ('HDN_T11_013', 'DV001', 160),
    ('HDN_T11_013', 'DV002', 14),
    ('HDN_T11_013', 'DV003', 1),
    ('HDN_T11_013', 'DV004', 1),
    ('HDN_T11_013', 'DV005', 2),

    -- Hóa đơn 014
    ('HDN_T11_014', 'DV001', 110),
    ('HDN_T11_014', 'DV002', 9),
    ('HDN_T11_014', 'DV003', 1),
    ('HDN_T11_014', 'DV004', 1),
    ('HDN_T11_014', 'DV005', 0),

    -- Hóa đơn 015
    ('HDN_T11_015', 'DV001', 135),
    ('HDN_T11_015', 'DV002', 10),
    ('HDN_T11_015', 'DV003', 1),
    ('HDN_T11_015', 'DV004', 1),
    ('HDN_T11_015', 'DV005', 1),

    -- Hóa đơn 016
    ('HDN_T11_016', 'DV001', 95),
    ('HDN_T11_016', 'DV002', 7),
    ('HDN_T11_016', 'DV003', 1),
    ('HDN_T11_016', 'DV004', 1),
    ('HDN_T11_016', 'DV005', 1),

    -- Hóa đơn 017
    ('HDN_T11_017', 'DV001', 105),
    ('HDN_T11_017', 'DV002', 8),
    ('HDN_T11_017', 'DV003', 1),
    ('HDN_T11_017', 'DV004', 1),
    ('HDN_T11_017', 'DV005', 2),

    -- Hóa đơn 018
    ('HDN_T11_018', 'DV001', 120),
    ('HDN_T11_018', 'DV002', 10),
    ('HDN_T11_018', 'DV003', 1),
    ('HDN_T11_018', 'DV004', 1),
    ('HDN_T11_018', 'DV005', 0),

    -- Hóa đơn 019
    ('HDN_T11_019', 'DV001', 130),
    ('HDN_T11_019', 'DV002', 11),
    ('HDN_T11_019', 'DV003', 1),
    ('HDN_T11_019', 'DV004', 1),
    ('HDN_T11_019', 'DV005', 1),

    -- Hóa đơn 020
    ('HDN_T11_020', 'DV001', 145),
    ('HDN_T11_020', 'DV002', 12),
    ('HDN_T11_020', 'DV003', 1),
    ('HDN_T11_020', 'DV004', 1),
    ('HDN_T11_020', 'DV005', 2);
