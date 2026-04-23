import pandas as pd
from config import INPUT_FILE, SHEET_CHUYEN_VA, SHEET_CHUYEN_HASI


def _load_sheet(sheet_name: str, col_thang: list) -> pd.DataFrame:
    """
    Đọc sheet chuyển doanh số, trả về DataFrame [ma_kh, t1, t2, t3].
    col_thang: tên 3 cột tháng trong sheet (vd: ['Tháng 1','Tháng 2','Tháng 3'])
    """
    df = pd.read_excel(INPUT_FILE, sheet_name=sheet_name, header=1)

    # Bỏ dòng không có mã KH
    df = df.dropna(subset=["MÃ KH"])
    df = df[df["MÃ KH"].astype(str).str.strip() != ""]

    df = df.rename(columns={"MÃ KH": "ma_kh"})

    # Lấy đúng 3 cột tháng
    keep = ["ma_kh"] + col_thang
    df = df[keep].copy()
    df.columns = ["ma_kh", "t1", "t2", "t3"]

    for c in ["t1", "t2", "t3"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    return df


def load_chuyen_ds() -> pd.DataFrame:
    """
    Gộp chuyển doanh số VACOSI + HASI theo mã KH.
    Trả về DataFrame [ma_kh, t1, t2, t3].
    """
    df_va   = _load_sheet(SHEET_CHUYEN_VA,   ["Tháng 1", "Tháng 2", "Tháng 3"])
    df_hasi = _load_sheet(SHEET_CHUYEN_HASI, ["Tháng 10", "Tháng 11", "Tháng 12"])

    # HASI sheet dùng tên tháng 10/11/12 nhưng thực tế map vào quý hiện tại
    # → đổi tên để gộp được
    df_hasi.columns = ["ma_kh", "t1", "t2", "t3"]

    df = pd.concat([df_va, df_hasi], ignore_index=True)
    df = df.groupby("ma_kh")[["t1", "t2", "t3"]].sum().reset_index()

    return df
