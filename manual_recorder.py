#!/usr/bin/env python3
"""
Manual Screen Recorder with Audio
Type your exact audio device names
"""

import subprocess
import os
from datetime import datetime
import sys

print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         MANUAL SCREEN RECORDER WITH AUDIO                     ║
║         (When auto-detection doesn't work)                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")

print("This tool lets you manually enter your audio device names.")
print("First, let's find your audio devices...\n")

# Show available devices
print("Running: ffmpeg -list_devices true -f dshow -i dummy\n")
result = subprocess.run(
    ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
    capture_output=True, text=True
)

print("="*70)
print(result.stderr)
print("="*70)

print("\nLook for lines like:")
print('  [dshow @ ...] "Stereo Mix (Realtek Audio)" (audio)')
print('  [dshow @ ...] "Microphone Array (Intel)" (audio)')
print("\nThe device name is between the quotes.")

# Get configuration
print("\n" + "="*70)
print("  RECORDING CONFIGURATION")
print("="*70)

# Recording mode
print("\n1. Recording Mode:")
print("   1 = Full Desktop (all monitors)")
print("   2 = Monitor 1 (primary)")
print("   3 = Monitor 2")
print("   4 = Monitor 3")

mode = input("\nEnter choice (1-4): ").strip()

# Audio configuration
print("\n2. Audio Configuration:")
use_audio = input("   Do you want to record audio? (y/n): ").strip().lower() == 'y'

audio_device = None
if use_audio:
    print("\n   Enter the EXACT audio device name from the list above.")
    print("   Common examples:")
    print("     - Stereo Mix")
    print("     - Stereo Mix (Realtek High Definition Audio)")
    print("     - Microphone Array (Realtek Audio)")
    print("     - Microphone (USB Audio Device)")
    print("\n   Copy the name EXACTLY as shown (including spaces and parentheses)")
    audio_device = input("\n   Audio device name: ").strip()
    
    if not audio_device:
        print("   No device entered, recording without audio.")
        use_audio = False

# Quality settings
print("\n3. Quality Settings:")
print("   Frame rate:")
print("     1 = 15 FPS (smooth enough, smaller files)")
print("     2 = 30 FPS (standard, recommended)")
print("     3 = 60 FPS (very smooth, large files)")

fps_choice = input("\n   Choose (1-3, default=2): ").strip()
fps_map = {'1': '15', '2': '30', '3': '60'}
fps = fps_map.get(fps_choice, '30')

print("\n   Quality:")
print("     1 = Low (CRF 28, small files)")
print("     2 = Good (CRF 23, balanced)")
print("     3 = High (CRF 18, large files)")

quality_choice = input("\n   Choose (1-3, default=2): ").strip()
quality_map = {'1': '28', '2': '23', '3': '18'}
crf = quality_map.get(quality_choice, '23')

# Duration
duration = input("\n4. Recording duration in seconds (or press ENTER for manual stop): ").strip()

# Build command
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"recording_{timestamp}.mp4"

cmd = ['ffmpeg']

# Video input based on mode
if mode == '1':
    cmd.extend(['-f', 'gdigrab', '-framerate', fps, '-i', 'desktop'])
elif mode == '2':
    cmd.extend(['-f', 'gdigrab', '-framerate', fps, '-i', 'desktop'])
elif mode == '3':
    # For monitor 2, you'll need to adjust offset_x and video_size
    # Example for a 1920x1080 second monitor
    cmd.extend([
        '-f', 'gdigrab', '-framerate', fps,
        '-offset_x', '1920', '-offset_y', '0',
        '-video_size', '1920x1080',
        '-i', 'desktop'
    ])
elif mode == '4':
    # For monitor 3, adjust accordingly
    cmd.extend([
        '-f', 'gdigrab', '-framerate', fps,
        '-offset_x', '3840', '-offset_y', '0',
        '-video_size', '1920x1080',
        '-i', 'desktop'
    ])

# Duration
if duration and duration.isdigit():
    cmd.extend(['-t', duration])

# Audio input
if use_audio and audio_device:
    cmd.extend(['-f', 'dshow', '-i', f'audio={audio_device}'])

# Video codec
cmd.extend([
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-crf', crf,
    '-pix_fmt', 'yuv420p'
])

# Audio codec
if use_audio and audio_device:
    cmd.extend(['-c:a', 'aac', '-b:a', '192k'])

# Output
cmd.append(output_file)

# Show command
print("\n" + "="*70)
print("  COMMAND TO EXECUTE")
print("="*70)
print(" ".join(cmd))
print("="*70)

confirm = input("\nStart recording? (y/n): ").strip().lower()

if confirm != 'y':
    print("Cancelled.")
    sys.exit(0)

# Start recording
print(f"\n🔴 RECORDING TO: {output_file}")
print("\nPress Ctrl+C to stop (or wait for duration to complete)")
print("-"*70)

try:
    process = subprocess.run(cmd)
    
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"\n✓ Recording saved: {output_file}")
        print(f"  Size: {size:.2f} MB")
        
        # Check if it has audio
        probe_cmd = ['ffprobe', '-i', output_file, '-show_streams', '-select_streams', 'a', '-loglevel', 'error']
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
        
        if probe_result.stdout:
            print("  ✓ Audio stream detected")
        else:
            print("  ⚠ No audio stream (video only)")
    else:
        print("\n✗ Recording file was not created")
        
except KeyboardInterrupt:
    print("\n\n⏹️  Recording stopped by user")
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"✓ Recording saved: {output_file}")
        print(f"  Size: {size:.2f} MB")
except Exception as e:
    print(f"\n✗ Error: {e}")

input("\nPress ENTER to exit...")
