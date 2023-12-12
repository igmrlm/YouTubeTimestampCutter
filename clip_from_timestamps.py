import os
import subprocess
import argparse

# Function to convert timestamp to seconds
def timestamp_to_seconds(timestamp):
    mm, ss = map(int, timestamp.split(':'))
    return mm * 60 + ss

def create_keyframe_database(video_file):
    print("Creating Keyframe Database. This may take some time, please wait.")
    keyframe_database = {}
    ffprobe_command = f"ffprobe -i \"{video_file}\" -skip_frame nokey -select_streams v -show_entries frame=pkt_dts_time -of compact=p=0:nk=1 -v 0"
    try:
        output = subprocess.check_output(ffprobe_command, shell=True)
        frame_times = [float(time) for time in output.decode().split('\n') if time]
        if frame_times:
            for time in frame_times:
                keyframe_database[time] = time
        else:
            print("No keyframes found.")
    except subprocess.CalledProcessError as e:
        print("Error executing ffprobe:", e)
    return keyframe_database

def find_nearest_keyframe(timestamp, keyframe_database):
    return min(keyframe_database, key=lambda x: abs(x - timestamp))

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Extract video clips based on timestamps')
parser.add_argument('video_file', help='Input video file')
parser.add_argument('timestamp_file', help='Timestamp file')
args = parser.parse_args()

# Read timestamps from file
timestamp_file = args.timestamp_file
with open(timestamp_file, 'r') as file:
    timestamps = [line.strip() for line in file.readlines()]

# Video file and output directory
video_file = args.video_file
output_directory = 'output_clips'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Extract input file name without extension
input_filename = os.path.splitext(os.path.basename(video_file))[0]

print("Video Timestamp Extractor: This Python script helps extract video clips based on provided timestamps from a video file. It utilizes ffprobe and ffmpeg to locate keyframes and extract clips accurately.")
print("https://github.com/igmrlm/YouTubeTimestampCutter")
print("https://YouTube.com/NathanaelNewton")

print("Loading video:")
print(video_file)

print("Loading timestamps from:")
print(timestamp_file)


# Create keyframe database
keyframe_db = create_keyframe_database(video_file)

# Extract clips based on timestamps
for i, timestamp in enumerate(range(len(timestamps) - 1), start=1):
    start_time_str, description = timestamps[timestamp].split(' ', 1)
    end_time_str, _ = timestamps[timestamp + 1].split(' ', 1)
    
    start_time = timestamp_to_seconds(start_time_str)
    end_time = timestamp_to_seconds(end_time_str)
    
    # Find nearest keyframes to the provided timestamps
    start_keyframe = find_nearest_keyframe(start_time, keyframe_db)
    end_keyframe = find_nearest_keyframe(end_time, keyframe_db)
    
    # Use ffmpeg to extract the clip with input file name + numbering + timestamp description
    output_filename = f"{output_directory}/{input_filename}_{i:03d}_{description}.mp4"
    start_keyframe = round(start_keyframe, 3)
    end_keyframe = round(end_keyframe, 3)
    
    ffmpeg_command = f'ffmpeg -i "{video_file}" -ss {start_keyframe} -to {end_keyframe} -c copy "{output_filename}"'
    subprocess.call(ffmpeg_command, shell=True)

print("Extraction completed.")
print("Files are saved in .\output_clips")
