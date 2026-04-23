# ETL Doanh Số - Kế Hoạch Phân Bổ

Tự động tính doanh số thực tế theo khách hàng × tháng và ghi vào file báo cáo.

## Cấu trúc

```
etl_doanh_so/
├── input/       ← Đặt file "THEO DÕI ĐƠN HÀNG DOANH SỐ" vào đây
├── output/      ← File kết quả sau khi chạy ETL
├── template/    ← File KẾ HOẠCH gốc (readonly)
├── backup/      ← Tự động backup trước mỗi lần chạy
├── logs/        ← Log từng lần chạy
├── extract/     ← Đọc dữ liệu từ file input
├── transform/   ← Tính toán doanh số
└── load/        ← Ghi kết quả vào output
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy

```bash
python main.py
```

## Chạy theo lịch (Windows Task Scheduler)

Trỏ Task Scheduler vào file `scheduler/run.bat`

## Chuẩn bị file

1. Copy file `2026.QUÝ 1 - THEO DÕI ĐƠN HÀNG DOANH SỐ.xlsx` vào thư mục `input/`
2. Copy file `KẾ HOẠCH PHÂN BỔ DOANH SỐ QUÝ 1.2026.xlsx` vào thư mục `template/`
3. Chạy `python main.py`
4. Mở file trong `output/` để xem kết quả
