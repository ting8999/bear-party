import scipy.io
from keras.models import load_model
import numpy as np
import os
from datetime import datetime
# 定義資料夾路徑
folder = './test'  # 你的資料夾路徑

def convert_to_reltime(time_str):
    """將 ISO 8601 格式的時間字串 (格式: YYYY-MM-DDTHH:MM:SS.ssssss) 轉換為一天中的秒數"""
    # 提取時間部分 HH:MM:SS
    time_part = time_str.split('T')[1].split('.')[0]  # 只保留 HH:MM:SS
    time_obj = datetime.strptime(time_part, "%H:%M:%S")
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second


# 載入模型
model = load_model('QuakeOrNot_lstm.keras')
print(model.input_shape)

# 讀取測試資料
files = os.listdir(folder)
Abs_TimeData_new = []
TimeData_new = []
VelocityData_new = []
for file in files:
    f = os.path.join(folder,file)
    try: #Try to open the file
        mat = scipy.io.loadmat(f)
        #velocity = list(mat.keys())[-1]
        TimeData_new.append(mat["time_rel"][0])
        VelocityData_new.append(mat["velocity"][0])
    except ValueError: # Catch the exception if the file is not a valid .mat file
        print(f'Skipping file {file} as it is not a valid .mat file.')
TimeData_new = np.array(TimeData_new)
VelocityData_new = np.array(VelocityData_new)
#print(np.shape(TimeData_new))
#print(TimeData_new)
#print(np.shape(VelocityData_new))
#print(VelocityData_new)
#print(np.shape(VelocityData_new))

# 處理資料格式

new_data_reshaped = VelocityData_new.reshape((VelocityData_new.shape[0], VelocityData_new.shape[1], 1)) 
print(new_data_reshaped.shape)

# 進行預測
predictions = model.predict(new_data_reshaped)

# 若使用 one-hot encoding，取最大值的索引以獲得類別預測
predicted_classes = np.argmax(predictions, axis=1)

# 顯示預測結果
#print(predicted_classes)  # 輸出預測的類別

# 輸出結果
results = []
for i in range(len(Abs_TimeData_new)):
  results.append(Abs_TimeData_new[i])
results.append(Abs_TimeData_new)
#print(type(predicted_classes))
#print(type(TimeData_new))

list(zip(TimeData_new.tolist(), VelocityData_new.tolist(), predicted_classes.tolist()))