import subprocess
import threading
import pyaudio
import wave
from gpiozero import Button, LED
import time
import picamera2
from picamera2.encoders import H264Encoder, Quality


button = Button(3)
ledRed = LED(17)
ledGreen = LED(27)
ledYellow = LED(22)

ledYellow.on()
current = 1
camera = picamera2.Picamera2()


encoder = H264Encoder()

camera.framerate = 30

# Audio setup
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
AUDIO_FILENAME = 'audio.wav'


p = pyaudio.PyAudio()
audio_thread = None  

def record_audio():
    global audio_thread
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    with wave.open(AUDIO_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print("Audio saved")

def start_recording():
    global recording, audio_thread
    recording = True

    audio_thread = threading.Thread(target=record_audio)
    audio_thread.start()

    camera.start_recording(encoder, 'videos/video.h264', quality=Quality.VERY_HIGH)
    print("Started recording")

def stop_recording():
    global recording, audio_thread
    recording = False
    camera.stop_recording()
    print("Video recording stopped")
    if audio_thread is not None:
        audio_thread.join()

    print("Audio saved")
    combine_video_audio('videos/video.h264', 'audio.wav', 'videos/output_video.mp4')

    print("Data saved")

def combine_video_audio(video_filename, audio_filename, output_filename):
    temp_video_filename = 'videos/temp_video.mp4'
    ffmpeg_wrap_command = [
        'ffmpeg',
        '-framerate', '30',  
        '-i', video_filename,  
        '-c:v', 'copy', 
        '-an', 
        temp_video_filename  # Output MP4 container
    ]
    
    try:
        subprocess.run(ffmpeg_wrap_command, check=True)
        print(f"Raw video wrapped into {temp_video_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error wrapping raw video into MP4: {e}")
        return
    video_duration_command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', temp_video_filename]
    try:
        video_duration = float(subprocess.check_output(video_duration_command).decode().strip())
    except subprocess.CalledProcessError as e:
        print(f"Error getting video duration: {e}")
        return
    except ValueError as e:
        print(f"Error converting video duration to float: {e}")
        return

    command = [
        'ffmpeg',
        '-i', temp_video_filename, 
        '-i', audio_filename,  
        '-filter_complex', f"[1]apad=pad_len={int(video_duration * RATE)}[a]", 
        '-map', '0:v',
        '-map', '[a]',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_filename  
    ]

    subprocess.run(command)
    print(f"Video and audio combined into {output_filename}")
    subprocess.run(['rm', temp_video_filename])
    print("Temporary video file removed.")


ledYellow.on()
while True:
    if (current == 1):
        ledRed.off()
        ledGreen.on()
        ledYellow.off()
        print("Ready to start Recording")
    
    button.wait_for_press()
    current += 1
    if (current == 2):
        ledRed.on()
        ledYellow.off()
        ledGreen.off()
        start_recording()
    
    if (current == 3):
        ledRed.off()
        ledYellow.on()
        ledGreen.off()
        stop_recording()
        ledGreen.on()
        ledYellow.off()
        current = 1

    time.sleep(0.5)

