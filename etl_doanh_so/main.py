import os
import shutil
import logging
from datetime import datetime

from config import (
    INPUT_FILE, OUTPUT_FILE, TEMPLATE_FILE,
    BACKUP_DIR, LOG_DIR,
)
from extract.source    import load_source
from extract.chuyen_ds import load_chuyen_ds
from transform.doanh_so_kh import calc_thuc_te_kh
from load.ke_hoach     import write_ke_hoach


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger("main")


def backup_output():
    """Copy output hiện tại vào backup/ trước khi ghi đè."""
    if os.path.exists(OUTPUT_FILE):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = os.path.splitext(os.path.basename(OUTPUT_FILE))
        dest = os.path.join(BACKUP_DIR, f"{fname[0]}_{ts}{fname[1]}")
        shutil.copy2(OUTPUT_FILE, dest)
        return dest
    return None


def prepare_output():
    """Copy template → output (reset về trạng thái sạch)."""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    shutil.copy2(TEMPLATE_FILE, OUTPUT_FILE)


def main():
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("BẮT ĐẦU ETL DOANH SỐ")
    logger.info("=" * 60)

    # Kiểm tra file input tồn tại
    if not os.path.exists(INPUT_FILE):
        logger.error(f"Không tìm thấy file input: {INPUT_FILE}")
        raise FileNotFoundError(INPUT_FILE)

    if not os.path.exists(TEMPLATE_FILE):
        logger.error(f"Không tìm thấy file template: {TEMPLATE_FILE}")
        raise FileNotFoundError(TEMPLATE_FILE)

    # 1. Backup output cũ
    backed = backup_output()
    if backed:
        logger.info(f"Đã backup output cũ → {backed}")

    # 2. Copy template → output
    prepare_output()
    logger.info(f"Đã copy template → output")

    # 3. Extract
    logger.info("Đang đọc Source...")
    df_source = load_source()
    logger.info(f"  Source: {len(df_source):,} dòng giao dịch")

    logger.info("Đang đọc Chuyển doanh số...")
    df_chuyen = load_chuyen_ds()
    logger.info(f"  Chuyển DS: {len(df_chuyen):,} khách hàng")

    # 4. Transform
    logger.info("Đang tính thực tế theo KH × tháng...")
    df_result = calc_thuc_te_kh(df_source, df_chuyen)
    logger.info(f"  Kết quả: {len(df_result):,} khách hàng có doanh số")

    # 5. Load
    logger.info("Đang ghi vào file output...")
    written = write_ke_hoach(df_result)
    logger.info(f"  Đã ghi {written} dòng")

    logger.info("=" * 60)
    logger.info("ETL HOÀN THÀNH")
    logger.info(f"Output: {OUTPUT_FILE}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
