import openpyxl
import pandas as pd
import logging
from config import (
    OUTPUT_FILE, SHEET_KH_VACOSI,
    COL_MA_KH, COL_T1_TT, COL_T2_TT, COL_T3_TT,
    ROW_DATA_START,
)

logger = logging.getLogger(__name__)


def write_ke_hoach(df_result: pd.DataFrame) -> int:
    """
    Ghi cột Thực tế (N, P, R) vào file output.
    Chỉ ghi đúng 3 cột, giữ nguyên toàn bộ phần còn lại.

    Trả về số dòng đã ghi.
    """
    # Tạo lookup dict: ma_kh → (t1, t2, t3)
    lookup = {
        str(row["ma_kh"]).strip(): (row["t1_tt"], row["t2_tt"], row["t3_tt"])
        for _, row in df_result.iterrows()
    }

    wb = openpyxl.load_workbook(OUTPUT_FILE)
    ws = wb[SHEET_KH_VACOSI]

    written = 0
    for row in ws.iter_rows(min_row=ROW_DATA_START):
        ma_kh_cell = row[COL_MA_KH - 1]  # 0-indexed
        ma_kh = str(ma_kh_cell.value).strip() if ma_kh_cell.value else ""

        if not ma_kh:
            continue

        if ma_kh in lookup:
            t1, t2, t3 = lookup[ma_kh]
            row[COL_T1_TT - 1].value = round(t1)
            row[COL_T2_TT - 1].value = round(t2)
            row[COL_T3_TT - 1].value = round(t3)
            written += 1
        else:
            # KH có trong template nhưng không có trong Source → ghi 0
            row[COL_T1_TT - 1].value = 0
            row[COL_T2_TT - 1].value = 0
            row[COL_T3_TT - 1].value = 0
            logger.warning(f"Không tìm thấy dữ liệu cho KH: {ma_kh}")

    wb.save(OUTPUT_FILE)
    logger.info(f"Đã ghi {written} khách hàng vào {OUTPUT_FILE}")
    return written
