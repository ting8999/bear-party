# 匯入所需的函式庫
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
from spectrogram import spectrogram_detect

# 匯入事件目錄
cat_directory = './output/'
cat_file = cat_directory + 'apollo12_catalog_GradeA_final.csv'
cat = pd.read_csv(cat_file)
r = 7   # 在哪一行

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
spec_arrival_time = datetime.strptime(spec_row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], '%Y-%m-%dT%H:%M:%S.%f')

# 取得相對到達時間及檔案名稱
spec_arrival_time_rel = spec_row['time_rel(sec)']
spec_test_filename = spec_row.filename

## 讀取 miniseed 檔案
data_directory = './space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/'         # Input miniseed for create plot base
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
ax.legend(loc='upper left')
ax.axvline(x=spec_arrival,c='green', label=f'Spactrogram_Estimated', linestyle='--')
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
# for i, event_time in enumerate(event_times):
#     ax2.axvline(x=event_time, c='yellow', label=f'Estimated Event {i+1}', linestyle='--')

cbar = plt.colorbar(vals, orientation='horizontal')
cbar.set_label('Power ((m/s)^2/sqrt(Hz))', fontweight='bold')

ax2.legend(loc='upper left')

# # STA/LTA 參數
# from obspy.signal.trigger import classic_sta_lta, trigger_onset

# df = tr.stats.sampling_rate
# sta_len = 120
# lta_len = 600

# # 使用 STA/LTA 計算特徵函數
# cft = classic_sta_lta(tr_data, int(sta_len * df), int(lta_len * df))

# # 繪製特徵函數
# fig, ax = plt.subplots(1, 1, figsize=(12, 3))
# ax.plot(tr_times, cft)
# ax.set_xlim([min(tr_times), max(tr_times)])
# ax.set_xlabel('Time (s)')
# ax.set_ylabel('Characteristic function')

# # 設定觸發閾值
# thr_on = 4
# thr_off = 1.5
# on_off = np.array(trigger_onset(cft, thr_on, thr_off))

# # 繪製觸發點
# colors = plt.get_cmap('tab10', len(on_off))
# fig, ax = plt.subplots(1, 1, figsize=(12, 3))

# for i in range(len(on_off)):
#     triggers = on_off[i]
#     color = colors(i % 10)
#     ax.axvline(x=tr_times[triggers[0]], color=color, label=f'Trig. On {i}')
#     ax.axvline(x=tr_times[triggers[1]], color=color, linestyle='--', label=f'Trig. Off {i}')

# ax.plot(tr_times, tr_data)
# ax.set_xlim([min(tr_times), max(tr_times)])
# ax.legend()

# # 將檢測時間整理到一個 dataframe
# detection_times = []
# fnames = []
# event_flags = []

# for i in range(len(on_off)):
#     triggers = on_off[i]
#     on_time = starttime + timedelta(seconds=tr_times[triggers[0]])
#     on_time_str = datetime.strftime(on_time, '%Y-%m-%dT%H:%M:%S.%f')
#     detection_times.append(on_time_str)
#     fnames.append(test_filename)
#     event_flags.append(1)

# 整理檢測結果成 dataframe
# detect_df = pd.DataFrame(data={'filename': fnames, 'time_abs(%Y-%m-%dT%H:%M:%S.%f)': detection_times, 'time_rel(sec)': [tr_times[on_off[i][0]] for i in range(len(on_off))], 'event': event_flags})
# detect_df.to_csv('./output/catalog.csv', index=False)

plt.show()
