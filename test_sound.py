import pygame
import time

pygame.init()
pygame.mixer.init()

print("Testing WAV file playback...")

# First, let's see what audio drivers are available
print(f"Mixer initialized: {pygame.mixer.get_init()}")

# Try to create a simple WAV file first
import wave
import struct
import math

print("\nCreating test.wav file...")
sample_rate = 22050
duration = 0.5
samples = int(sample_rate * duration)

with wave.open("test.wav", 'w') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)
    
    # Generate a simple sine wave
    for i in range(samples):
        value = int(16000 * math.sin(2 * math.pi * 440 * i / sample_rate))
        wav.writeframes(struct.pack('<h', value))

print("✅ Created test.wav")

# Now try to play it
test_file="./music/background_rock.mp3"#"test.wav"
try:
    print(f"\nAttempting to play {test_file}...")
    sound = pygame.mixer.Sound(f"{test_file}")
    sound.play()
    print("Playing... (you should hear a beep)")
    time.sleep(5.5)
    print("✅ Playback complete!")
except Exception as e:
    print(f"❌ Failed to play: {e}")

# Clean up
import os
os.remove("test.wav")
print("\nTest complete!")

pygame.quit()