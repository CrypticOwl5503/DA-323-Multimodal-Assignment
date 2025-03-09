import os
import time
import datetime
import subprocess
from pydub import AudioSegment

# Define radio streams and their URLs
radio_stations = {
    "NPR_News": "https://npr-ice.streamguys1.com/live.mp3",
    "Jazz24": "https://live.wostreaming.net/direct/ppm-jazz24aac-ibc1",
    "ClassicFM": "http://media-ice.musicradio.com/ClassicFMMP3",
    "SomaFM_Groove": "https://ice4.somafm.com/groovesalad-128-mp3",
    "BBC_WorldService": "http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-einws"
}

# Directory to store recordings
output_dir = "recordings"
os.makedirs(output_dir, exist_ok=True)

# Function to record audio
def record_audio(station_name, stream_url, duration=60):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{station_name}_{timestamp}.mp3"
    filepath = os.path.join(output_dir, filename)

    print(f"Recording {station_name} for {duration} seconds...")

    # Run ffmpeg command to record the stream
    command = [
        "ffmpeg", "-i", stream_url, "-t", str(duration), "-y",
        "-acodec", "mp3", filepath
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return filename, filepath, timestamp, duration

# Record 30 audio samples from different stations
audio_metadata = []
for i in range(30):
    station_name, stream_url = list(radio_stations.items())[i % len(radio_stations)]
    duration = 30 + (i % 3) * 30  # Vary duration between 30-90s

    try:
        filename, filepath, timestamp, duration = record_audio(station_name, stream_url, duration)
        audio_metadata.append([station_name, filename, timestamp, duration])
        time.sleep(2)  # Small delay to avoid overwhelming the system
    except Exception as e:
        print(f"Error recording {station_name}: {e}")

print("Recording complete!")

# Save metadata to CSV
import csv

metadata_file = os.path.join(output_dir, "audio_metadata.csv")
with open(metadata_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Station Name", "Filename", "Timestamp", "Duration"])
    writer.writerows(audio_metadata)

print(f"Metadata saved to {metadata_file}")
