#!/usr/bin/env python3
import sys
import cv2
import os
import glob
import numpy as np
from edge_impulse_linux.runner import ImpulseRunner

def main():
    if len(sys.argv) != 2:
        print("使用方式: python3 classify_batch.py <model.eim>")
        sys.exit(1)

    model_path = sys.argv[1]
    # print(f"載入模型: {model_path}") # 註解掉避免干擾 Shell Script 輸出

    runner = ImpulseRunner(model_path)
    try:
        model_info = runner.init()
        params = model_info['model_parameters']
        input_w = params['image_input_width']
        input_h = params['image_input_height']
        channels = params.get('axis_count', 1) # 1=灰階, 3=RGB

        # === 關鍵修改：路徑改成 data/test/ ===
        image_files = glob.glob("data/test/*.jpg") + glob.glob("data/test/*.jpeg") + glob.glob("data/test/*.png")
        
        if not image_files:
            print("錯誤: 'data/test' 資料夾內找不到圖片！")
            sys.exit(1)

        print(f"找到 {len(image_files)} 張圖片，開始處理...")

        for img_path in image_files:
            # 讀取圖片
            img = cv2.imread(img_path)
            if img is None:
                continue

            # 前處理 (保持 0-255，不除以 255)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if channels == 1:
                img_input = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            else:
                img_input = img_rgb
            
            img_resized = cv2.resize(img_input, (input_w, input_h))
            features = img_resized.flatten().tolist()

            # 推論
            res = runner.classify(features)

            # --- 視覺化 (畫框框) ---
            if "bounding_boxes" in res["result"]:
                found = False
                for box in res["result"]["bounding_boxes"]:
                    if box['value'] > 0.5: # 門檻值
                        found = True
                        x = int(box['x'] * img.shape[1] / input_w)
                        y = int(box['y'] * img.shape[0] / input_h)
                        w = int(box['width'] * img.shape[1] / input_w)
                        h = int(box['height'] * img.shape[0] / input_h)

                        # 畫綠色框框
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        
                        # 寫標籤
                        label_text = f"{box['label']} ({box['value']:.2f})"
                        cv2.putText(img, label_text, (x, y-10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        print(f"  [偵測到] {os.path.basename(img_path)} -> {label_text}")

                # 儲存結果圖片
                filename, ext = os.path.splitext(img_path)
                save_path = f"{filename}_result{ext}"
                cv2.imwrite(save_path, img)

    finally:
        runner.stop()

if __name__ == "__main__":
    main()
