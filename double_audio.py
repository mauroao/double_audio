import sys
import os
import subprocess

def extract_audio(input_file, output_file):
    subprocess.run(['ffmpeg', '-i', input_file, '-vn', '-acodec', 'copy', output_file])

def concatenate_audio(input_file, output_file):
    subprocess.run(['ffmpeg', '-i', f'concat:{input_file}|{input_file}', '-c', 'copy', output_file])

def get_video_duration(input_file):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file], capture_output=True, text=True)
    return float(result.stdout)

def truncate_audio(input_file, output_file, duration):
    subprocess.run(['ffmpeg', '-i', input_file, '-t', str(duration), '-c', 'copy', output_file])

def create_output_file(video_file, audio_file, output_file):
    subprocess.run(['ffmpeg', '-i', video_file, '-i', audio_file, '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_file])

if len(sys.argv) != 4:
    print("Usage: python script.py file1 file2 file3")
    sys.exit(1)

file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]

# Get the video track duration of file1
duration1 = get_video_duration(file1)

# Extract audio from file1 and save it to temp_audio1
temp_audio1 = 'temp_audio1.aac'
extract_audio(file1, temp_audio1)

# Subtract n seconds from temp_audio1 and save to temp_audio2
temp_audio2 = 'temp_audio2.aac'
truncate_audio(temp_audio1, temp_audio2, (duration1 - 15))

# Concatenate the audio file with itself to double the duration
double_audio = 'double_audio.aac'
concatenate_audio(temp_audio2, double_audio)

# Get the video track duration of file2
duration2 = get_video_duration(file2)

# Truncate the audio duration of double_audio to match the video duration
truncated_audio = 'truncated_audio.aac'
truncate_audio(double_audio, truncated_audio, duration2)

# Create file3 with the video track from file2 and audio track from truncated_audio
create_output_file(file2, truncated_audio, file3)

# Clean up temporary audio files
os.remove(temp_audio1)
os.remove(temp_audio2)
os.remove(double_audio)
os.remove(truncated_audio)

