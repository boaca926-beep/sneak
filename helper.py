import wave
import struct
import math
import os

def download_music(url, filename):
    """Download music file from URL"""
    try:
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False
        
def create_beep_sounds():
    """Create WAV files for the snake game"""
    sample_rate = 22050
    
    # Create eat.wav
    if not os.path.exists("eat.wav"):
        print("Creating eat.wav...")
        duration = 0.1
        samples = int(sample_rate * duration)
        
        with wave.open("eat.wav", 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            
            # Square wave for sharp "chomp" sound
            for i in range(samples):
                if (i * 880 // sample_rate) % 2 == 0:
                    value = 20000
                else:
                    value = -20000
                wav.writeframes(struct.pack('<h', value))
        print("✅ Created eat.wav")
    
    # Create game_over.wav
    if not os.path.exists("game_over.wav"):
        print("Creating game_over.wav...")
        duration = 0.8
        samples = int(sample_rate * duration)
        
        with wave.open("game_over.wav", 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            
            # Descending tone with fade out
            for i in range(samples):
                freq = 440 - (i * 220 / samples)
                volume = 1.0 - (i / samples)
                value = int(15000 * volume * math.sin(2 * math.pi * freq * i / sample_rate))
                wav.writeframes(struct.pack('<h', value))
        print("✅ Created game_over.wav")
    
    # Create background music (FIXED INDENTATION - now outside the previous block)
    if not os.path.exists("background.wav"):
        print("Creating background music...")
        duration = 10.0  # 10 seconds of music
        samples = int(sample_rate * duration)
        
        with wave.open("background.wav", 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            
            # Create a simple melody
            melody = [
                (262, 0.5),  # C4
                (294, 0.5),  # D4
                (330, 0.5),  # E4
                (349, 0.5),  # F4
                (392, 0.5),  # G4
                (440, 0.5),  # A4
                (494, 0.5),  # B4
                (523, 1.0),  # C5
            ]
            
            # Generate the melody
            sample_pos = 0
            for freq, dur in melody:
                note_samples = int(sample_rate * dur)
                for i in range(note_samples):
                    if sample_pos < samples:
                        # Add some harmony (two frequencies)
                        value = int(8000 * math.sin(2 * math.pi * freq * sample_pos / sample_rate))
                        value += int(4000 * math.sin(2 * math.pi * (freq * 1.5) * sample_pos / sample_rate))
                        wav.writeframes(struct.pack('<h', value))
                        sample_pos += 1
            
            # Fill remaining with silence
            while sample_pos < samples:
                wav.writeframes(struct.pack('<h', 0))
                sample_pos += 1
        
        print("✅ Created background.wav")
    
    return True

# Free royalty-free game music URLs (replace with actual working URLs)
# These are example URLs - you'll need to find actual working links

music_files = {
    "background1.wav": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    # Or use these alternative sources:
}

# Method 2: Use youtube-dl to download from YouTube
def download_from_youtube():
    """Download music from YouTube (requires yt-dlp)"""
    try:
        import subprocess
        # Download a free game music track
        url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "wav", 
            "-o", "background.wav", url
        ])
        print("✅ Downloaded music from YouTube")
    except:
        print("❌ YouTube download failed")

if __name__ == "__main__":
    create_beep_sounds()
    print("\n✅ All sound files ready! Run: uv run snake.py")

    print("Downloading background music...")
    for filename, url in music_files.items():
        if not os.path.exists(filename):
            download_music(url, filename)