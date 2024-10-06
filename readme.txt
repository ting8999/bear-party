# Advanced Algorithms for Seismic Signal Analysis: SED, LOF, and LSTM

## Description
This project focuses on detecting seismic events on Mars and the Moon using a combination of three algorithms.The Spectrum Algorithm excels at accurately labeling seismic events by using clear physical criteria, though it may overlook smaller disturbances. LOF, on the other hand, is highly sensitive to these smaller disturbances, although it may flag non-seismic data. LSTM provides fast and reliable validation, combining the strengths of both approaches, making it a key tool in extraterrestrial seismology. Triple algorithms combination labeling seismic events comprehensively, enhancing both the accuracy and precision, resulting in more reliable results.
## Data Setup
1. **Set Paths and Data**  
   Configure the paths and prepare the data you plan to use, including CSV files and Miniseed files. Example path:  
   `./space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/`

2. **Move Training Data**  
   Place the training data in the following path:  
   `./space_apps_2024_seismic_detection/data/lunar/training/catalogs`

	you can change LOF.py
	def LOF_detect(folder_path, output_file_path, window_duration=3600, stride_duration=1800, anomaly_threshold=8)
	to
	def LOF_detect(folder_path, output_file_path, window_duration=900, stride_duration=450, anomaly_threshold=8)
## Execution
3. **Run the Main Program**  
   In the terminal, navigate to the project directory and execute the `main` file to start the project:
   ```bash
   python main.py

	here you can see all algorithm results

## Fusion Part

The script categorizes the dates into the following groups:
Dates duplicated in both files: Dates that are considered duplicated and present in both files, allowing for a maximum difference of 3600 seconds (1 hour).
Dates unique in both files: Dates that do not have duplicates and exist in both files.
Dates duplicated only in LOF: Dates that are duplicated and only present in the LOF file.
Dates duplicated only in Spectrogram: Dates that are duplicated and only present in the Spectrogram file.
Dates unique only in LOF: Dates that are unique and only present in the LOF file.
Dates unique only in Spectrogram: Dates that are unique and only present in the Spectrogram file.
Input Files
The script expects two input files:

LOF_output.csv: Contains time information for events detected by the LOF method.
spectrogram_output.csv: Contains time information for events detected by the Spectrogram method.
These files should be structured with a column named time_abs(%Y-%m-%dT%H:%M:%S.%f) containing the timestamps.

Running the Script
Save the script in a Python file, for example compare_seismic_dates.py. Then, run the script:
python weighted.py


Output
The script will generate an output CSV file named seismic_dates_comparison.csv. This file will contain the results of the comparison, with the following columns:

time_abs(%Y-%m-%dT%H:%M:%S.%f) (duplicates in both files): Dates from both files that match within a time difference of 3600 seconds.
time_abs(%Y-%m-%dT%H:%M:%S.%f) (unique in both files): Dates that exist in both files but are unique (not duplicated).
time_abs(%Y-%m-%dT%H:%M:%S.%f) (duplicates only in LOF): Dates that are duplicated and exist only in the LOF file.
time_abs(%Y-%m-%dT%H:%M:%S.%f) (duplicates only in Spectrogram): Dates that are duplicated and exist only in the Spectrogram file.
time_abs(%Y-%m-%dT%H:%M:%S.%f) (unique only in LOF): Dates that are unique and only present in the LOF file.
time_abs(%Y-%m-%dT%H:%M:%S.%f) (unique only in Spectrogram): Dates that are unique and only present in the Spectrogram file.