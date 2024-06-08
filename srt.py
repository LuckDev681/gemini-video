import srt
import os

def create_srt_file(data, output_file):
    with open(output_file, 'w') as file:
        index = 1
        for  entry in data:
            start_time = entry["start_time"]
            end_time = entry["end_time"]
            text = entry["text"]
            file.write(f"\n{start_time} --> {end_time}\n{text}\n\n")
            index += 1