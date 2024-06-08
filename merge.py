import subprocess
import os

directory_path = f"{os.path.dirname(__file__)}\\"
def reencode_video(input_file, output_file):
    """Re-encodes the input video to a common format with corrected timestamps."""
    command = [
        'ffmpeg', '-i', input_file,
        '-vf', 'setpts=PTS-STARTPTS',
        '-af', 'asetpts=PTS-STARTPTS',
        '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
        '-c:a', 'aac', '-b:a', '128k',
        output_file
    ]
    subprocess.run(command, check=True)

def create_filelist(filelist, output_file):
    """Creates a text file listing all videos to be merged."""
    with open(output_file, 'w') as f:
        for file in filelist:
            f.write(f"file '{file}'\n")

def merge_videos(filelist_txt, output_file):
    """Merges videos listed in a file into one video with timestamp correction."""
    command = [
        'ffmpeg', '-safe', '0', '-f', 'concat', '-segment_time_metadata', '1',
        '-i', filelist_txt,
        '-vf', 'select=concatdec_select',
        '-af', 'aselect=concatdec_select,aresample=async=1',
        output_file
    ]
    subprocess.run(command, check=True)

def main():
    folder_path = os.path.join(directory_path, "Video1")  # Change this to your folder path
    input_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mp4')]
    
    if not input_files:
        print("No MP4 files found in the specified folder.")
        return

    reencoded_files = []
    
    # Re-encode each video
    for i, input_file in enumerate(input_files):
        output_file = f'reencoded{i+1}.mp4'
        reencode_video(input_file, output_file)
        reencoded_files.append(output_file)
    
    # Create a filelist.txt
    filelist_txt = 'filelist.txt'
    create_filelist(reencoded_files, filelist_txt)
    
    # Merge the videos
    merged_output = 'merged_output.mp4'
    merge_videos(filelist_txt, merged_output)
    
    # Clean up intermediate files if needed
    for file in reencoded_files:
        os.remove(file)
    os.remove(filelist_txt)

    print(f"Merged video saved as {merged_output}")

if __name__ == "__main__":
    main()