import pandas as pd
from config import INPUT_FILE, SHEET_SOURCE, NHAN_HANG


def load_source() -> pd.DataFrame:
    """
    Đọc sheet Source từ file input.
    Trả về DataFrame đã lọc theo nhãn hàng cần tính.
    """
    df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_SOURCE, header=0)

    # Đổi tên cột gọn hơn để dùng nội bộ
    df = df.rename(columns={
        "Month":            "thang",
        "Mã khách hàng":    "ma_kh",
        "NHÃN HÀNG":        "nhan_hang",
        "Doanh số bán":     "doanh_so_ban",
        "Giá trị trả lại":  "gia_tri_tra_lai",
    })

    # Chỉ giữ các cột cần thiết
    df = df[["thang", "ma_kh", "nhan_hang", "doanh_so_ban", "gia_tri_tra_lai"]]

    # Lọc nhãn hàng
    df = df[df["nhan_hang"].isin(NHAN_HANG)]

    # Đảm bảo kiểu số
    df["doanh_so_ban"]    = pd.to_numeric(df["doanh_so_ban"],    errors="coerce").fillna(0)
    df["gia_tri_tra_lai"] = pd.to_numeric(df["gia_tri_tra_lai"], errors="coerce").fillna(0)

    return df
