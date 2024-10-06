import pandas as pd

# 讀取兩個輸出的CSV檔案
lof_output = pd.read_csv('./LOF_output.csv')
spectrogram_output = pd.read_csv('./spectrogram_output.csv')

# 抽取兩個資料中的時間欄位，並過濾掉無效的數據
lof_dates = lof_output['time_abs(%Y-%m-%dT%H:%M:%S.%f)'].dropna()
spectrogram_dates = spectrogram_output['time_abs(%Y-%m-%dT%H:%M:%S.%f)'].dropna()

# 轉換為日期格式，忽略無法轉換的值
lof_dates = pd.to_datetime(lof_dates, errors='coerce').dropna()
spectrogram_dates = pd.to_datetime(spectrogram_dates, errors='coerce').dropna()

# 將日期資料轉換為排序的列表進行逐一比較
lof_list = sorted(lof_dates)
spectrogram_list = sorted(spectrogram_dates)

# 找出時間差在 3600 秒內的匹配日期，並保留所有匹配的資料
both_have = []
lof_matched = set()
spectrogram_matched = set()

i, j = 0, 0
while i < len(lof_list) and j < len(spectrogram_list):
    delta = abs((lof_list[i] - spectrogram_list[j]).total_seconds())
    if delta <= 3600:
        both_have.append((lof_list[i], spectrogram_list[j]))
        lof_matched.add(lof_list[i])
        spectrogram_matched.add(spectrogram_list[j])
        i += 1
        j += 1
    elif lof_list[i] < spectrogram_list[j]:
        i += 1
    else:
        j += 1

# 找出沒有重複的日期且兩個檔案都有的情況（時間差大於3600秒，但不重複）
lof_unique = set(lof_dates) - lof_matched
spectrogram_unique = set(spectrogram_dates) - spectrogram_matched
unique_in_both = lof_unique.intersection(spectrogram_unique)

# 將重複的日期資料列出
lof_duplicates = lof_dates[lof_dates.duplicated(keep=False)]
spectrogram_duplicates = spectrogram_dates[spectrogram_dates.duplicated(keep=False)]

duplicates_only_lof = lof_duplicates[~lof_duplicates.isin(spectrogram_dates)]
duplicates_only_spectrogram = spectrogram_duplicates[~spectrogram_duplicates.isin(lof_dates)]

# 找出沒有重複且只存在於 LOF 和 Spectrogram 中的日期
unique_only_lof = lof_unique - unique_in_both
unique_only_spectrogram = spectrogram_unique - unique_in_both

# 將所有匹配的資料格式化
both_have_formatted = [f"{lof.strftime('%Y-%m-%dT%H:%M:%S.%f')} ~ {spec.strftime('%Y-%m-%dT%H:%M:%S.%f')}" for lof, spec in both_have]
unique_in_both_formatted = [date.strftime('%Y-%m-%dT%H:%M:%S.%f') for date in unique_in_both]
duplicates_only_lof_formatted = [date.strftime('%Y-%m-%dT%H:%M:%S.%f') for date in duplicates_only_lof]
duplicates_only_spectrogram_formatted = [date.strftime('%Y-%m-%dT%H:%M:%S.%f') for date in duplicates_only_spectrogram]
unique_only_lof_formatted = [date.strftime('%Y-%m-%dT%H:%M:%S.%f') for date in unique_only_lof]
unique_only_spectrogram_formatted = [date.strftime('%Y-%m-%dT%H:%M:%S.%f') for date in unique_only_spectrogram]

# 創建結果的 DataFrame，標頭名稱保持一致
result_df = pd.DataFrame({
    'time_abs(%Y-%m-%dT%H:%M:%S.%f) (duplicates in both files)': pd.Series(both_have_formatted),
    'time_abs(%Y-%m-%dT%H:%M:%S.%f) (unique in both files)': pd.Series(unique_in_both_formatted),
    'time_abs(%Y-%m-%dT%H:%M:%S.%f) (duplicates only in LOF)': pd.Series(duplicates_only_lof_formatted),
    'time_abs(%Y-%m-%dT%H:%M:%S.%f) (duplicates only in Spectrogram)': pd.Series(duplicates_only_spectrogram_formatted),
    'time_abs(%Y-%m-%dT%H:%M:%S.%f) (unique only in LOF)': pd.Series(unique_only_lof_formatted),
    'time_abs(%Y-%m-%dT%H:%M:%S.%f) (unique only in Spectrogram)': pd.Series(unique_only_spectrogram_formatted),
})

# 保存結果到 CSV 文件
result_df.to_csv('weithed_data.csv', index=False)
