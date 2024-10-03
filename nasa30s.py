from obspy import read
from scipy.io import savemat
import os

# MINISEED 文件目录
mseed_directory = './space_apps_2024_seismic_detection/data/lunar/test/data/S12_GradeB/'
output_directory = 'lunar_data'
os.makedirs(output_directory, exist_ok=True)

# 目标采样率
target_sampling_rate = 6.625
segment_duration = 30  # 每段的时间长度为 30 秒

# 遍历目录下的所有 .mseed 文件
for filename in os.listdir(mseed_directory):
    if filename.endswith(".mseed"):
        mseed_file_path = os.path.join(mseed_directory, filename)

        # 读取MINISEED文件
        mseed_stream = read(mseed_file_path)

        # 提取HHZ通道
        hhz_stream = mseed_stream.select(channel='MHZ')

        # 重新采样到目标频率
        hhz_stream.resample(sampling_rate=target_sampling_rate)

        if len(hhz_stream) > 0:
            hhz_trace = hhz_stream[0]
            start_time = hhz_trace.stats.starttime
            end_time = hhz_trace.stats.endtime
            total_duration = end_time - start_time

            # 计算总共可以切分的 30 秒段数
            num_segments = int(total_duration // segment_duration)

            for i in range(num_segments):
                # 切取每个 30 秒的时间段
                segment_start_time = start_time + i * segment_duration
                segment_end_time = segment_start_time + segment_duration
                segment = hhz_stream.slice(starttime=segment_start_time, endtime=segment_end_time)

                if len(segment) > 0:
                    hhz_segment_trace = segment[0]
                    times_rel = hhz_segment_trace.times()  # 相对于开始时间的时间序列
                    velocities = hhz_segment_trace.data  # 速度数据

                    # 构建保存到 .mat 文件的数据结构
                    extracted_data = {
                        'time_rel': times_rel,
                        'velocity': velocities
                    }

                    # 保存到 .mat 文件，文件名包含原始文件名和段编号
                    output_file_name = f'{os.path.splitext(filename)[0]}_segment_{i+1}.mat'
                    output_file_path = os.path.join(output_directory, output_file_name)
                    savemat(output_file_path, extracted_data)

print("所有数据切分并转换完成，保存为.mat文件。")
