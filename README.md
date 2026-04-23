# ETL Kế Hoạch Phân Bổ Doanh Số

Tự động tính doanh số thực tế theo khách hàng × tháng và ghi vào file báo cáo **Kế Hoạch Phân Bổ Doanh Số**.

## Tổng quan

Công ty **GREENMODE** (thương hiệu VACOSI, HASI) quản lý doanh số qua Excel. Pipeline này tự động hóa bước điền số liệu thực tế vào báo cáo kế hoạch, thay thế việc nhập tay từng tháng.

```
[THEO DÕI ĐƠN HÀNG DOANH SỐ.xlsx]
        ↓ Extract (sheet Source ~28k dòng)
        ↓ Transform (group by KH × tháng, tính DS thuần)
        ↓ Load (ghi cột Thực tế vào KẾ HOẠCH PHÂN BỔ)
[KẾ HOẠCH PHÂN BỔ DOANH SỐ.xlsx] ← output
```

## Cấu trúc project

```
etl_doanh_so/
├── main.py              # Entry point
├── config.py            # Cấu hình đường dẫn, tháng, nhãn hàng
├── requirements.txt
├── extract/
│   ├── source.py        # Đọc sheet Source
│   └── chuyen_ds.py     # Đọc sheet CHUYEN DS VA + HASI
├── transform/
│   └── doanh_so_kh.py   # Tính thực tế KH × tháng
├── load/
│   └── ke_hoach.py      # Ghi cột N, P, R vào output
├── scheduler/
│   └── run.bat          # Windows Task Scheduler
├── input/               # Đặt file nguồn vào đây (không commit)
├── output/              # File kết quả (không commit)
├── template/            # File KẾ HOẠCH gốc (không commit)
├── backup/              # Tự động backup (không commit)
└── logs/                # Log từng lần chạy (không commit)
```

## Cài đặt

```bash
pip install -r etl_doanh_so/requirements.txt
```

## Chuẩn bị file

| Thư mục | File cần đặt |
|---------|-------------|
| `input/` | `2026.QUÝ 1 - THEO DÕI ĐƠN HÀNG DOANH SỐ.xlsx` |
| `template/` | `KẾ HOẠCH PHÂN BỔ DOANH SỐ QUÝ 1.2026.xlsx` |

## Chạy

```bash
cd etl_doanh_so
python main.py
```

Log sẽ được ghi vào `logs/etl_YYYYMMDD_HHMMSS.log`.

## Chạy theo lịch (Windows Task Scheduler)

Trỏ Task Scheduler vào `etl_doanh_so/scheduler/run.bat`, set lịch chạy đầu mỗi ngày hoặc cuối tháng.

## Logic tính doanh số thực tế

Tái tạo công thức Excel `BB6` trong sheet `VA+520`:

```
Thực tế tháng X = (Doanh số bán - Giá trị trả lại) + Chuyển doanh số
```

Lọc nhãn hàng: `VACOSI` + `HASI`

Ghi vào 3 cột trong sheet `KH VACOSI`:
- Cột N — 1.Thực tế (Tháng 1)
- Cột P — 2.Thực tế (Tháng 2)
- Cột R — 3.Thực tế (Tháng 3)
