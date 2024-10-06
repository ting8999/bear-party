# 匯入所需的函式庫
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
from spectrogram import spectrogram_detect
from LOF import LOF_detect


# 匯入事件目錄
cat_directory = './output/'
cat_file = cat_directory + 'apollo12_catalog_GradeA_final.csv'
cat = pd.read_csv(cat_file)
r = 0   # 在哪一行

# 從目錄中取得到達時間
row = cat.iloc[r]
arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], '%Y-%m-%dT%H:%M:%S.%f')

# 取得相對到達時間及檔案名稱
arrival_time_rel = row['time_rel(sec)']
test_filename = row.filename

## 匯入 spectrogram 的 csv
spec_input = './space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/'      # Input miniseed
spec_directory = './output/'                                                                      # Output csv
spectrogram_detect(spec_input, spec_directory)
spec_file = spec_directory + 'spectrogram_output.csv'
spec = pd.read_csv(spec_file)
# 從目錄中取得到達時間
spec_row = spec.iloc[r]
# print(spec_row)
spec_arrival_time = datetime.strptime(spec_row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], '%Y-%m-%dT%H:%M:%S.%f')
# 取得相對到達時間及檔案名稱
spec_arrival_time_rel = spec_row['time_rel(sec)']
spec_test_filename = spec_row.filename

df = pd.read_csv('./output/LOF_output.csv')

# 將相同 file_name 的 time_rel(sec) 存成 array
result = df.groupby('filename')['time_rel(sec)'].apply(list).reset_index()
result_abs = df.groupby('filename')['time_abs(%Y-%m-%dT%H:%M:%S.%f)'].apply(list).reset_index()
# 如果你想把結果轉換成字典，可以這樣做
result_dict = result.set_index('filename')['time_rel(sec)'].to_dict()
result_abs_dict = result_abs.set_index('filename')['time_abs(%Y-%m-%dT%H:%M:%S.%f)'].to_dict()
index = cat.iloc[r, 0]+".csv"
LOF_arrival_time_rel = result_dict[index]
LOF_arrival_time = result_abs_dict[index]
## 匯入 LOF 的 csv

LOF_input = './space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/'           # Input csv
LOF_directory = './output/'                                                                      # Output csv
LOF_file = LOF_directory + 'LOF_output.csv'
LOF_detect(LOF_input, LOF_file)
LOF = pd.read_csv(LOF_file)
# 從目錄中取得到達時間
LOF_row = LOF.iloc[r]
# print(LOF_row)
#LOF_arrival_time = datetime.strptime(LOF_row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], '%Y-%m-%dT%H:%M:%S.%f')
# 取得相對到達時間及檔案名稱
#LOF_arrival_time_rel = LOF_row['time_rel(sec)']
LOF_test_filename = LOF_row.filename

## 讀取 miniseed 檔案
data_directory = './nasa_hackathon/space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/miniseed/'         # Input miniseed for create plot base
mseed_file = f'{data_directory}{test_filename}.mseed'
st = read(mseed_file)

# 擷取資料與時間
tr = st.traces[0].copy()
tr_times = tr.times()
tr_data = tr.data

# 取得資料的開始時間
starttime = tr.stats.starttime.datetime
arrival = (arrival_time - starttime).total_seconds()
spec_arrival = (spec_arrival_time - starttime).total_seconds()
LOF_arrival_time = pd.to_datetime(LOF_arrival_time)
LOF_arrival_all = [(time - starttime).total_seconds() for time in LOF_arrival_time]


# 設定頻率範圍
minfreq = 0.5
maxfreq = 1.0

# 創建經過濾波的資料副本
st_filt = st.copy()
st_filt.filter('bandpass', freqmin=minfreq, freqmax=maxfreq)
tr_filt = st_filt.traces[0].copy()
tr_times_filt = tr_filt.times()
tr_data_filt = tr_filt.data

# 創建頻譜圖
from scipy import signal
from matplotlib import cm

# 計算頻譜圖之值
f, t, sxx = signal.spectrogram(tr_data_filt, tr_filt.stats.sampling_rate)

# 繪製時間序列和頻譜圖
fig = plt.figure(figsize=(10, 10))

ax = plt.subplot(2, 1, 1)
ax.plot(tr_times_filt, tr_data_filt)
ax.axvline(x=arrival, color='red', label='Detection')
# ax.legend(loc='upper left')
ax.axvline(x=spec_arrival,c='green', label=f'Spactrogram_Estimated', linestyle='--')
label_added1 = False
for arrival in LOF_arrival_all:
    if not label_added1:
        ax.axvline(x=arrival, c='yellow', label='LOF_Estimated', linestyle='--')
        label_added1 = True  # 標籤已添加
    else:
        ax.axvline(x=arrival, c='yellow', linestyle='--')  # 不添加標籤
ax.legend(loc='upper left')
ax.set_xlim([min(tr_times_filt), max(tr_times_filt)])
ax.set_ylabel('Velocity (m/s)')
ax.set_xlabel('Time (s)')

ax2 = plt.subplot(2, 1, 2)
vals = ax2.pcolormesh(t, f, sxx, cmap=cm.jet, vmax=5e-17)
ax2.set_xlim([min(tr_times_filt), max(tr_times_filt)])
ax2.set_xlabel(f'Time (Day Hour:Minute)', fontweight='bold')
ax2.set_ylabel('Frequency (Hz)', fontweight='bold')
ax.set_title(f'{test_filename}', fontweight='bold')
# # 標記檢測到的事件和估算事件（多個事件）
ax2.axvline(x=arrival, c='red', label='Catalog Detection')
ax2.axvline(x=spec_arrival,c='green', label=f'Spactrogram_Estimated', linestyle='--')
label_added2 = False
for arrival in LOF_arrival_all:
    if not label_added2:
        ax2.axvline(x=arrival, c='yellow', label='LOF_Estimated', linestyle='--')
        label_added2 = True  # 標籤已添加
    else:
        ax2.axvline(x=arrival, c='yellow', linestyle='--')  # 不添加標籤
#ax2.axvline(x=LOF_arrival,c='yellow', label=f'LOF_Estimated', linestyle='--')

cbar = plt.colorbar(vals, orientation='horizontal')
cbar.set_label('Power ((m/s)^2/sqrt(Hz))', fontweight='bold')

ax2.legend(loc='upper left')

plt.show()
