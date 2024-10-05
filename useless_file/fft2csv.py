import csv
import os
from FFT import fft_process  # 引入 process_file 函數

# 定義資料夾路徑
folder = './data/lunar/training'  # 你的資料夾路徑
#folder = './fft_data'
# 遍歷資料夾中的所有文件，獲取 FFT 結果
FFT = []
for file in os.listdir(folder):
    if file.endswith('.mat'):
        file_path = os.path.join(folder, file)
        fft_result = fft_process(file_path)  # 呼叫 FFT 處理函數
        FFT.append(fft_result)

# 打印結果以確認
for res in FFT:
    print(res)

# 設置輸出資料夾
output_dir = './output'
os.makedirs(output_dir, exist_ok=True)

# 匯出到 CSV 檔案
csv_file_path = os.path.join(output_dir, 'FFT_output.csv')

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    # 設定欄位名稱
    fieldnames = ['filename', 'time_abs(%Y-%m-%dT%H:%M:%S.%f)', 'time_rel(sec)', 'event']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # 寫入標頭
    for result in FFT:
        # 將 FFT 的結果分別提取出來
        filename, time_abs, time_rel, event = result
        
        
        # time_abs 已經包含絕對時間
        time_str = time_abs  # 可根據需要進一步處理時間格式
        
        # 計算 time_rel (假設30秒的固定間隔)
        time_rel = time_rel  # 對應 FFT 的相對時間

        # 寫入資料行
        writer.writerow({
            'filename': filename,
            'time_abs(%Y-%m-%dT%H:%M:%S.%f)': time_str,
            'time_rel(sec)': time_rel,
            'event': event
        })

print("CSV 檔案已成功生成！")
