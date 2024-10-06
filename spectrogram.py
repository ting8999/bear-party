import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import os
from scipy import signal

def spectrogram_detect(data_directory, output_directory, 
                  minfreq=0.5, maxfreq=1.0, 
                  gradient_threshold_percentile=95, 
                  energy_threshold_percentile=99.5, 
                  min_event_interval=100):
    # Initialize lists for output data
    all_detection_times = []
    all_filenames = []
    all_event_flags = []
    all_time_rels = []

    # A set to track unique events to avoid duplicates
    unique_events = set()

    # Traverse the directory and process each MINISEED file
    for filename in os.listdir(data_directory):
        if filename.endswith('.mseed'):
            mseed_file = os.path.join(data_directory, filename)
            
            # Read the MINISEED file
            st = read(mseed_file)
            tr = st.traces[0].copy()
            tr_times = tr.times()
            tr_data = tr.data
            starttime = tr.stats.starttime.datetime

            # Create a filtered copy of the trace
            st_filt = st.copy()
            st_filt.filter('bandpass', freqmin=minfreq, freqmax=maxfreq)
            tr_filt = st_filt.traces[0].copy()
            tr_times_filt = tr_filt.times()
            tr_data_filt = tr_filt.data

            # Create a spectrogram
            f, t, sxx = signal.spectrogram(tr_data_filt, tr_filt.stats.sampling_rate)

            # Calculate the sum of power across frequencies for each time slice
            sxx_sum = np.sum(sxx, axis=0)

            # Smooth the summed power to reduce noise
            sxx_sum_smooth = signal.savgol_filter(sxx_sum, window_length=51, polyorder=3)

            # Calculate the gradient of the smoothed power signal
            gradient = np.gradient(sxx_sum_smooth)

            # Define thresholds for significant gradient and energy
            gradient_threshold = np.percentile(gradient, gradient_threshold_percentile)
            energy_threshold = np.percentile(sxx_sum_smooth, energy_threshold_percentile)

            # Find significant events based on gradient and energy conditions
            significant_gradient_indices = np.where((gradient > gradient_threshold) & (sxx_sum_smooth > energy_threshold))[0]

            # Filter out events that are too close to each other
            filtered_event_times = []
            for idx in significant_gradient_indices:
                if len(filtered_event_times) == 0 or (idx - filtered_event_times[-1]) > min_event_interval:
                    filtered_event_times.append(idx)
            # Convert indices to time values and record detection times
            for event_idx in filtered_event_times:
                event_time = t[event_idx]
                abs_time = starttime + timedelta(seconds=event_time)
                abs_time_str = datetime.strftime(abs_time, '%Y-%m-%dT%H:%M:%S.%f')

                # Check if this event has already been detected
                if abs_time_str not in unique_events:
                    # Add to the set of unique events
                    unique_events.add(abs_time_str)

                    # Append to output lists
                    all_detection_times.append(abs_time_str)
                    all_filenames.append(filename)
                    all_event_flags.append(1)
                    all_time_rels.append(event_time)

            # print(f"Processed {mseed_file}")

    # Compile the dataframe of detections
    detect_df = pd.DataFrame(data={
        'filename': all_filenames, 
        'time_abs(%Y-%m-%dT%H:%M:%S.%f)': all_detection_times, 
        'time_rel(sec)': all_time_rels, 
        'event': all_event_flags
    })

    # Save the results to a CSV file
    output_file = os.path.join(output_directory, 'spectrogram_output.csv')
    detect_df.to_csv(output_file, index=False)

    print(f"Detection results saved to {output_file}")
    print('spectrogram has done')

# 使用範例
# data_directory = './space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/'   # Input miniseed
# output_directory = './output/'          # Output csv
# spectrogram_detect(data_directory, output_directory)
