from obspy import read
from scipy.io import savemat
import os

# MINISEED 文件目录
mseed_directory = './space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA'
output_directory = './data/lunar/training/all_data'
os.makedirs(output_directory, exist_ok=True)

# 目标采样率
target_sampling_rate = 6.625

# 遍历目录下的所有 .mseed 文件
for filename in os.listdir(mseed_directory):
    if filename.endswith(".mseed"):
        mseed_file_path = os.path.join(mseed_directory, filename)

        # 读取 MINISEED 文件
        mseed_stream = read(mseed_file_path)

        # 提取 HHZ 通道
        hhz_stream = mseed_stream.select(channel='MHZ')

        # 重新采样到目标频率
        hhz_stream.resample(sampling_rate=target_sampling_rate)

        if len(hhz_stream) > 0:
            hhz_trace = hhz_stream[0]
            times_rel = hhz_trace.times()  # 相对于开始时间的时间序列
            times_abs = [hhz_trace.stats.starttime + t for t in times_rel]  # 绝对时间序列
            velocities = hhz_trace.data  # 速度数据

            # 将绝对时间转换为字符串格式
            time_abs_str = [t.strftime("%Y-%m-%dT%H:%M:%S.%f") for t in times_abs]

            # 构建保存到 .mat 文件的数据结构
            extracted_data = {
                'time_abs': time_abs_str,
                'time_rel': times_rel,
                'velocity': velocities
            }

            # 保存到 .mat 文件，文件名与原始文件名一致
            output_file_name = f'{os.path.splitext(filename)[0]}.mat'
            output_file_path = os.path.join(output_directory, output_file_name)
            savemat(output_file_path, extracted_data)

print("MINISEED 数据已全部转换为 .mat 文件。")
