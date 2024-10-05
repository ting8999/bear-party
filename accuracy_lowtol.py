import pandas as pd
from datetime import datetime

# 載入兩個 CSV 檔案
output_df = pd.read_csv('./data/lunar/training/output/catalog_output.csv')
final_df = pd.read_csv('./data/lunar/training/catalogs/apollo12_catalog_GradeA_final.csv')

# 假設時間欄位為 'time_abs'，時間格式為 '%Y-%m-%dT%H:%M:%S.%f'
output_times = pd.to_datetime(output_df['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], format='%Y-%m-%dT%H:%M:%S.%f')
final_times = pd.to_datetime(final_df['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], format='%Y-%m-%dT%H:%M:%S.%f')

# 計算正確匹配的數量
tolerance = pd.Timedelta(seconds=3000)  # 允許的時間差為 ±3000 秒
correct_matches = 0
used_indices = set()  # 記錄已匹配的 final_times 索引
extra_detections = 0  # 記錄多餘的偵測數量

matched_pairs = []  # 儲存匹配的時間對
extra_detections_list = []  # 儲存多餘偵測的時間
missed_detections_list = []  # 儲存未被匹配的正確答案時間

# 遍歷 catalog_output 的每一個時間，找出是否在 apollo12_catalog 裡有匹配
for output_time in output_times:
    matched = False
    for idx, final_time in enumerate(final_times):
        if idx not in used_indices and abs(output_time - final_time) <= tolerance:
            correct_matches += 1
            used_indices.add(idx)
            matched_pairs.append((output_time, final_time))
            matched = True
            break
    # 如果這個 output_time 沒有匹配的話，計算為多餘偵測
    if not matched:
        extra_detections += 1
        extra_detections_list.append(output_time)

# 記錄未被匹配的正確答案時間
for idx, final_time in enumerate(final_times):
    if idx not in used_indices:
        missed_detections_list.append(final_time)

# 將匹配結果、多餘偵測和未匹配的結果輸出為 CSV
output_data = {
    '匹配的 catalog_output 時間': [pair[0].strftime('%Y-%m-%dT%H:%M:%S.%f') for pair in matched_pairs],
    '匹配的 apollo12_catalog 時間': [pair[1].strftime('%Y-%m-%dT%H:%M:%S.%f') for pair in matched_pairs],
    '多餘偵測的時間 (catalog_output)': [time.strftime('%Y-%m-%dT%H:%M:%S.%f') for time in extra_detections_list],
    '未匹配的正確答案時間 (apollo12_catalog)': [time.strftime('%Y-%m-%dT%H:%M:%S.%f') for time in missed_detections_list]
}

output_df_result = pd.DataFrame.from_dict(output_data, orient='index').transpose()
output_df_result.to_csv('./matching_results.csv', index=False, encoding='utf-8-sig')

# 計算正確率
total_events = len(final_times)  # 總事件數（應偵測到的正確事件數）
total_errors = extra_detections + len(missed_detections_list)  # 錯誤事件數，包括多餘偵測和漏檢
accuracy = correct_matches / (total_events + total_errors) * 100  # 正確率的計算

# 打印詳細結果
print(f'總事件數 (final_df): {total_events}')
print(f'正確匹配的數量 (correct_matches): {correct_matches}')
print(f'多餘偵測的數量 (extra_detections): {extra_detections}')
print(f'未匹配的正確答案數量 (missed_detections): {len(missed_detections_list)}')
print(f'正確率: {accuracy:.2f}%')
print('匹配結果已輸出至 matching_results.csv')
