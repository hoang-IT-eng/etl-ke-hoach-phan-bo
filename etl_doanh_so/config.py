import os

# ── Đường dẫn ──────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR    = os.path.join(BASE_DIR, "input")
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
TEMPLATE_DIR = os.path.join(BASE_DIR, "template")
BACKUP_DIR   = os.path.join(BASE_DIR, "backup")
LOG_DIR      = os.path.join(BASE_DIR, "logs")

def _find_file(folder, keyword):
    """Tìm file trong folder theo keyword (không phân biệt encoding)."""
    for f in os.listdir(folder):
        if keyword.lower() in f.lower().encode('ascii', 'ignore').decode():
            return os.path.join(folder, f)
    # fallback: lấy file đầu tiên khớp extension
    for f in os.listdir(folder):
        if f.endswith('.xlsx'):
            return os.path.join(folder, f)
    return None

INPUT_FILE    = _find_file(INPUT_DIR,    "THEO DOI")
TEMPLATE_FILE = _find_file(TEMPLATE_DIR, "KE HOACH")
OUTPUT_FILE   = os.path.join(OUTPUT_DIR, os.path.basename(TEMPLATE_FILE)) if TEMPLATE_FILE else None

# ── Tham số báo cáo ────────────────────────────────────────────────────────
NAM          = 2026
QUY          = 1
THANG_LIST   = [1, 2, 3]          # các tháng trong quý

# ── Nhãn hàng tính vào doanh số ────────────────────────────────────────────
NHAN_HANG    = ["VACOSI", "HASI"]

# ── Sheet names ────────────────────────────────────────────────────────────
SHEET_SOURCE      = "Source"
SHEET_CHUYEN_VA   = "CHUYEN DS VA"
SHEET_CHUYEN_HASI = "CHUYEN DS HASI"
SHEET_KH_VACOSI   = "KH VACOSI"

# ── Vị trí cột trong sheet KH VACOSI (1-indexed) ──────────────────────────
COL_MA_KH    = 2   # B
COL_T1_TT    = 14  # N — 1.Thực tế
COL_T2_TT    = 16  # P — 2.Thực tế
COL_T3_TT    = 18  # R — 3.Thực tế
ROW_DATA_START = 7  # dòng đầu tiên có dữ liệu KH
