import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
import matplotlib.pyplot as plt
import os
from glob import glob

# 定義資料夾路徑
folder_path = '/content/test2'  # 請將這個路徑修改為你的原始資料夾路徑
output_file_path = '/content/output.csv'  # 定義結果保存的路徑

# 查找資料夾中所有的 CSV 檔案
file_paths = glob(os.path.join(folder_path, '*.csv'))

# 定義窗口大小和步幅
window_duration = 900  # 窗口大小，單位：秒
stride_duration = 450  # 步幅大小，單位：秒
anomaly_threshold = 8  # 異常點的閾值

# 初始化匯出文件，只在第一次寫入欄位標題
header_written = False

# 遍歷所有的 CSV 檔案
for file_path in file_paths:
    # 讀取檔案
    df = pd.read_csv(file_path)
    file_name = os.path.basename(file_path)

    # 讀取時間和速度數據
    time = df['time_rel(sec)'].values
    velocity = df['velocity(m/s)'].values

    # 計算每秒數據點數量
    time_diff = np.diff(time)
    sampling_rate = 1 / np.mean(time_diff)  # 每秒數據點數

    def sliding_window(df, window_size, stride):
        windows = []
        for i in range(0, len(df) - window_size + 1, stride):
            window = df.iloc[i:i + window_size]
            windows.append(window)
        return windows

    # 將秒數轉換為數據點數量
    window_size = int(window_duration * sampling_rate)
    stride = int(stride_duration * sampling_rate)

    windows = sliding_window(df, window_size, stride)
    print(f"檔案 {file_name} 中共有 {len(windows)} 個窗口")

    all_anomalies = []
    window_start_times = []  # 保存異常窗口的開始時間

    for i, window in enumerate(windows):
        lof = LocalOutlierFactor(n_neighbors=20)
        window['lof_score'] = lof.fit_predict(window[['velocity(m/s)']])
        window['lof_anomaly'] = window['lof_score'] == -1  # 標記異常點 (-1 表示離群點)
        anomalies = window[window['lof_anomaly']]

        # 如果有異常點
        if not anomalies.empty:
            all_anomalies.append(anomalies)

            # 如果異常點數量超過閾值，則標註窗口開始時間
            if len(anomalies) > anomaly_threshold:
                window_start_time = window['time_rel(sec)'].iloc[0]  # 窗口的開始時間
                window_start_times.append(window_start_time)  # 保存該時間點

    # 將所有異常點整合到一個 DataFrame 中
    if len(all_anomalies) > 0:
        anomalies_df = pd.concat(all_anomalies)

        # 匹配異常點所在的時間
        matched = df[df['time_rel(sec)'].isin(window_start_times)]
        if not matched.empty:
            # 添加檔名列
            matched['檔名'] = file_name

            # 假設原始資料中有 time_abs 列
            if 'time_abs(%Y-%m-%dT%H:%M:%S.%f)' in df.columns:
                # 重新排列欄位順序
                matched_df = matched[['檔名', 'time_abs(%Y-%m-%dT%H:%M:%S.%f)', 'time_rel(sec)']]

                # 匯出到 CSV，文件名中加入 matched，並保存到 /content/ 資料夾
                matched_df.to_csv(output_file_path, mode='a', header=not header_written, index=False)

                # 更新標誌，確保只寫入一次標題行
                header_written = True

                print(f"匹配結果已追加保存到: {output_file_path}")
            else:
                print(f"檔案 {file_name} 中沒有 'time_abs(%Y-%m-%dT%H:%M:%S.%f)' 欄位。")
        else:
            print(f"未在檔案 {file_name} 中找到匹配的 time_rel(sec) 值。")
    else:
        print(f"檔案 {file_name} 中沒有找到異常點。")
