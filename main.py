import csv
import os
from datetime import datetime, timedelta
from fft_selection import process_file  # 引入 fft_selection.py 中的 process_file 函數
from Weighted_Fcn import Weighted_Fcn

# 定義資料根目錄
folder = './test'  

###################################################### 匯入演算法結果 ###################################################### 

## FFT ##
FFT = []
for file in os.listdir(folder):
    if file.endswith('.mat'):
        file_path = os.path.join(folder, file)
        fft_result = process_file(file_path)  # 呼叫 FFT 函數
        FFT.append(fft_result)

## STA/LTA ##
SLTA = []
for file in os.listdir(folder):
    if file.endswith('.mat'):
        file_path = os.path.join(folder, file)
        slta_result = process_file(file_path)
        SLTA.append(slta_result)

## LSTM ##
LSTM = []
for file in os.listdir(folder):
    if file.endswith('.mat'):
        file_path = os.path.join(folder, file)
        lstm_result = process_file(file_path)
        LSTM.append(lstm_result)

###################################################### 融合演算法 ###################################################### 
input_data = []
for i in range(len(FFT)):
    filename = FFT[i][0]
    time_abs = FFT[i][1]
    time_rel = FFT[i][2]
    value = [
        FFT[i][3],      # FFT value
        SLTA[i][3],     # FFT value
        LSTM[i][3]      # LSTM value
    ]
    input_data.append({"filename": filename, "time_abs": time_abs, "time_rel": time_rel,"value": value})

# 權重
weights = [0.5, 0.4, 0.3]

# 執行加權決策
output = Weighted_Fcn(input_data, weights)

###################################################### 輸出結果 ###################################################### 

output_dir = './output'
os.makedirs(output_dir, exist_ok=True)

# 輸出到 CSV 文件
csv_file_path = os.path.join(output_dir, 'output.csv')
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['filename', 'time_abs(%Y-%m-%dT%H:%M:%S.%f)', 'time_rel(sec)', 'event']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # 寫入標頭
    for i, result in enumerate(output):
        # 將時間轉換為所需的格式
        time_str = result['time_abs'].strftime('%Y-%m-%dT%H:%M:%S.%f') if isinstance(result['time_abs'], datetime) else str(result['time_abs'])
        time_rel = result['time_rel']  # 使用提供的相對時間
        filename = result['filename']  # 使用原始文件名
        writer.writerow({
            'filename': filename,
            'time_abs(%Y-%m-%dT%H:%M:%S.%f)': time_str,
            'time_rel(sec)': time_rel,
            'event': result['decision']  # 將 event 值設置為結果的 decision
        })

print("CSV 檔案已成功生成！")
