#!/usr/bin/env python3
import sys
import cv2
import numpy as np
from edge_impulse_linux.runner import ImpulseRunner

def main():
    if len(sys.argv) != 3:
        print("使用方式: python3 classify.py <model.eim> <圖片>")
        sys.exit(1)

    model_path = sys.argv[1]
    image_path = sys.argv[2]
    
    print(f"載入模型: {model_path}")
    print(f"載入圖片: {image_path}")

    runner = ImpulseRunner(model_path)
    try:
        model_info = runner.init()
        print("\n=== 模型參數檢查 ===")
        # 這是關鍵！直接看模型告訴我們它要什麼
        params = model_info['model_parameters']
        print(f"模型輸入寬度: {params['image_input_width']}")
        print(f"模型輸入高度: {params['image_input_height']}")
        
        # 判斷是 RGB (3通道) 還是 灰階 (1通道)
        # 有些舊版模型沒有 axis_count 欄位，預設視為 1 (灰階)
        channels = params.get('axis_count', 1) 
        if channels == 3:
            print("模型需求: RGB 彩色圖片 (3通道)")
        else:
            print("模型需求: Grayscale 灰階圖片 (1通道)")

        # 讀取圖片
        img = cv2.imread(image_path)
        if img is None:
            print("錯誤: 找不到圖片")
            sys.exit(1)

        # 1. 調整顏色 (根據模型需求自動切換)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if channels == 1:
            img_input = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        else:
            img_input = img_rgb
            
        # 2. 縮放
        img_resized = cv2.resize(img_input, (params['image_input_width'], params['image_input_height']))
        
        # 3. 【關鍵修正】不要除以 255.0！
        # 簡報第30頁的除錯重點通常是：如果原始特徵是 0-255，這裡就不要正規化
        # 我們直接傳送 0-255 的數值給 Runner
        img_processed = img_resized.flatten().tolist()

        # 執行推論
        res = runner.classify(img_processed)

        # 顯示結果
        print("\n=== 偵測結果 ===")
        print("原始數據:", res['result'])
        
        if "bounding_boxes" in res["result"]:
            found = False
            for box in res["result"]["bounding_boxes"]:
                print(f"物件: {box['label']} (信心度: {box['value']:.2f})")
                found = True
            
            if not found:
                print("未偵測到高於門檻的物件 (信心度可能過低)")
        else:
            print("沒有 bounding_boxes")

    finally:
        runner.stop()

if __name__ == "__main__":
    main()
