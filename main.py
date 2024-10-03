import csv
from datetime import datetime, timedelta

def weighted_decision(data, weights):
    results = []
    
    for entry in data:
        # 取得該時間段的數據
        binary_data = entry['value']
        
        # 計算加權和
        weighted_sum = sum(w * d for w, d in zip(weights, binary_data))
        
        # 根據加權和決定結果
        if weighted_sum >= sum(weights) / 2:
            decision = 1
        else:
            decision = 0
        
        # 儲存結果
        results.append({
            "time": entry['time'],
            "decision": decision
        })
    
    return results

# 模擬三個演算法的輸出
STA_LTA = [
    tr_times[triggers[0]], 1
    {"time": "0", "value": 1},
    {"time": "30", "value": 0},
    {"time": "60", "value": 1},
    {"time": "90", "value": 1},
    {"time": "120", "value": 1}
]

# LSTM 原本是 list 形式
LSTM = [1, 0, 1, 0, 1]

FFT = [
    {"time": "45", "value": 1},
    {"time": "48", "value": 1},
    {"time": "10:10", "value": 1},
    {"time": "10:15", "value": 1},
    {"time": "10:20", "value": 0}
]

# 將 LSTM 轉換成字典列表形式
LSTM_converted = [{"time": STA_LTA[i]["time"], "value": LSTM[i]} for i in range(len(LSTM))]

# 整合三個演算法的輸出，將每個時間段的數據結合起來
input_data = []
for i in range(len(STA_LTA)):
    time = STA_LTA[i]["time"]
    value = [
        STA_LTA[i]["value"],
        LSTM_converted[i]["value"],
        FFT[i]["value"]
    ]
    input_data.append({"time": time, "value": value})

# 權重
weights = [0.5, 0.4, 0.3]

# 執行加權決策
output = weighted_decision(input_data, weights)

# 輸出結果到 CSV 檔案
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['filename', 'time_abs(%Y-%m-%dT%H:%M:%S.%f)', 'time_rel(sec)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # 寫入標頭
    for i, result in enumerate(output):
        # 將時間轉換為所需的格式
        time_str = f"2024-10-03T{result['time']}:00.000000"  # 假設日期為 2024-10-03
        time_rel = i * 300  # 假設每個時間段間隔為 5 分鐘 (300 秒)
        filename = f"data_{i + 1}.txt"  # 假設文件名格式為 data_1.txt, data_2.txt, ...
        decision = result['decision']
        writer.writerow({
            'filename': filename,
            'time_abs(%Y-%m-%dT%H:%M:%S.%f)': time_str,
            'time_rel(sec)': time_rel
        })

print("CSV 檔案已成功生成！")
