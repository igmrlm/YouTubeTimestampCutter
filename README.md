# Video Timestamp Extractor

This Python script helps extract video clips based on provided timestamps from a video file. It utilizes `ffprobe` and `ffmpeg` to locate keyframes and extract clips accurately.

## Purpose

This program allows you to copy the list of timestamps from your full-length YouTube video into a text file and then automatically cut it into separate videos based on those timestamps. 

## Features

- Extracts video clips from a larger video file using timestamp references.
- Utilizes `ffprobe` to locate keyframes for precise clip extraction.
  ffprobe_command = f"ffprobe -i \"{video_file}\" -skip_frame nokey -select_streams v -show_entries frame=pkt_dts_time -of compact=p=0:nk=1 -v 0"
- Provides flexibility in specifying timestamps for extraction.
- Does not re-encode the video making it extremely fast and lossless

## Requirements

- Python 3.x
- `ffprobe` and `ffmpeg` installed and accessible from the command line.

## Usage

python clip_from_timestamps.py 'input_video.mp4' 'timestamps.txt'
