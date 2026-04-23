import pandas as pd


def calc_thuc_te_kh(df_source: pd.DataFrame, df_chuyen: pd.DataFrame) -> pd.DataFrame:
    """
    Tính doanh số thực tế theo KH × tháng.

    Logic tái tạo công thức BB6 trong Excel:
        Thực tế tháng X = (Doanh số bán - Giá trị trả lại) + Chuyển doanh số

    Trả về DataFrame [ma_kh, t1_tt, t2_tt, t3_tt]
    """
    # Doanh số thuần = bán - trả
    df_source = df_source.copy()
    df_source["ds_thuan"] = df_source["doanh_so_ban"] - df_source["gia_tri_tra_lai"]

    # Group by KH × tháng
    pivot = (
        df_source
        .groupby(["ma_kh", "thang"])["ds_thuan"]
        .sum()
        .unstack(level="thang", fill_value=0)
    )

    # Đảm bảo có đủ 3 cột tháng dù tháng nào đó không có dữ liệu
    for t in [1, 2, 3]:
        if t not in pivot.columns:
            pivot[t] = 0

    pivot = pivot[[1, 2, 3]].reset_index()
    pivot.columns = ["ma_kh", "t1_tt", "t2_tt", "t3_tt"]

    # Cộng chuyển doanh số
    if not df_chuyen.empty:
        pivot = pivot.merge(df_chuyen, on="ma_kh", how="left")
        pivot["t1"] = pivot["t1"].fillna(0)
        pivot["t2"] = pivot["t2"].fillna(0)
        pivot["t3"] = pivot["t3"].fillna(0)
        pivot["t1_tt"] += pivot["t1"]
        pivot["t2_tt"] += pivot["t2"]
        pivot["t3_tt"] += pivot["t3"]
        pivot = pivot.drop(columns=["t1", "t2", "t3"])

    return pivot
