#!/bin/bash
# upload_data.sh - 自動上傳數據到 Edge Impulse

set -e

# --- 顏色設定 ---
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# --- 檢查 API Key ---
if [ -z "$EI_API_KEY" ]; then
    echo -e "${RED}[ERROR] 未設定 EI_API_KEY 環境變數！${NC}"
    echo "請先執行: export EI_API_KEY='你的金鑰'"
    exit 1
fi

# --- 檢查參數 ---
if [ "$#" -lt 2 ]; then
    echo "使用方式: $0 <標籤> <圖片路徑...>"
    echo "範例: $0 coffee data/collected/coffee/*.jpg"
    exit 1
fi

LABEL=$1
shift
IMAGES=("$@")

# --- 日誌設定 ---
LOG_DIR="logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/upload_${LABEL}_${TIMESTAMP}.log"

echo -e "${GREEN}[INFO] 準備上傳 ${#IMAGES[@]} 張圖片，標籤: ${LABEL}${NC}"

# --- 執行上傳 (自動分配 80% 訓練 / 20% 測試) ---
edge-impulse-uploader \
    --api-key "$EI_API_KEY" \
    --category split \
    --label "$LABEL" \
    "${IMAGES[@]}" 2>&1 | tee "$LOG_FILE"

echo -e "${GREEN}[SUCCESS] 上傳完成！日誌已儲存至 $LOG_FILE${NC}"
