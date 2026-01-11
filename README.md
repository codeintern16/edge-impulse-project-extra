# Edge Impulse 物件偵測專案 (Linux/WSL)

這是一個基於 Edge Impulse 的物件偵測專案，專為 Linux (WSL) 環境設計。
我們使用 Python SDK 進行推論，並撰寫了自動化 Shell Script 來實現批次處理與結果視覺化。

## 👥 團隊成員與分工
* **組長：** 413411330 - 環境建置、自動化腳本撰寫、Git 版本控制
* **組員：** 413411330 - 模型訓練、資料蒐集
* **組員：** 黃健峰 - 測試與驗證

## 🛠️ 專案結構
```text
.
├── models/         # 存放 .eim 模型檔案 (已透過 .gitignore 排除)
├── scripts/        # Python 推論程式與 Shell 自動化腳本
├── data/test/      # 測試圖片與推論結果
├── results/        # (選用) 存放歷史推論紀錄
└── README.md       # 專案說明文件
### 1. 安裝套件
```bash
sudo apt-get update
sudo apt-get install libopencv-dev python3-opencv
# 如果遇到 externally-managed-environment 錯誤，請加上 --break-system-packages
pip3 install edge_impulse_linux opencv-python numpy --break-system-packages

