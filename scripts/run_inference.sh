#!/bin/bash
# run_inference.sh - 自動化推論腳本

set -e # 遇到錯誤立即停止

# 定義顏色
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 設定路徑
MODEL_PATH="models/model.eim"
SCRIPT_PATH="scripts/classify_batch.py"

echo -e "${GREEN}[INFO] 開始執行自動化推論...${NC}"

# 1. 檢查檔案是否存在
if [ ! -f "$MODEL_PATH" ]; then
    echo -e "${RED}[ERROR] 找不到模型: $MODEL_PATH ${NC}"
    exit 1
fi

if [ ! -f "$SCRIPT_PATH" ]; then
    echo -e "${RED}[ERROR] 找不到 Python 腳本: $SCRIPT_PATH ${NC}"
    exit 1
fi

# 2. 給予執行權限
chmod +x "$MODEL_PATH"

# 3. 執行 Python 推論
echo "----------------------------------------"
python3 "$SCRIPT_PATH" "$MODEL_PATH"
echo "----------------------------------------"

# 4. 檢查結果
if ls data/test/*_result.* 1> /dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS] 推論完成！結果圖片已存於 data/test/ 資料夾${NC}"
else
    echo -e "${RED}[WARNING] 推論完成但未產生結果圖${NC}"
fi
