#!/usr/bin/env python3
"""
Audio Setup Helper
Helps enable Stereo Mix and other audio devices
"""

import subprocess
import sys

print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║              AUDIO DEVICE SETUP HELPER                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

This script will help you enable audio recording devices.
""")

print("\n" + "="*70)
print("  STEP 1: Opening Windows Sound Settings")
print("="*70)

print("\nThis will open the Windows Sound Control Panel.")
print("Please follow these steps:\n")

print("FOR SYSTEM AUDIO (browser, apps, music):")
print("  1. Go to the 'Recording' tab")
print("  2. Right-click in the empty space")
print("  3. Check 'Show Disabled Devices'")
print("  4. Look for 'Stereo Mix' or 'Wave Out Mix' or 'What U Hear'")
print("  5. Right-click on it → Enable")
print("  6. Right-click again → Set as Default Device")
print()
print("FOR MICROPHONE:")
print("  1. In the 'Recording' tab")
print("  2. Find your microphone")
print("  3. Right-click → Enable")
print("  4. Right-click → Set as Default Communication Device")

input("\nPress ENTER to open Sound Control Panel...")

try:
    # Open Sound Control Panel
    subprocess.run(['control', 'mmsys.cpl', 'sounds'], shell=True)
    print("\n✓ Sound Control Panel opened")
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nManual way:")
    print("  1. Right-click speaker icon in taskbar")
    print("  2. Click 'Sounds'")
    print("  3. Go to 'Recording' tab")

print("\n" + "="*70)
print("  STEP 2: After enabling devices...")
print("="*70)

input("\nAfter you've enabled the devices, press ENTER to test...")

# Test audio devices again
print("\nTesting audio device detection...")
result = subprocess.run(
    ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
    capture_output=True, text=True
)

print("\n" + "="*70)
print("  DETECTED AUDIO DEVICES")
print("="*70)

audio_devices = []
for line in result.stderr.split('\n'):
    if '(audio)' in line and '"' in line:
        start = line.find('"') + 1
        end = line.find('"', start)
        if start > 0 and end > start:
            device = line[start:end]
            audio_devices.append(device)
            print(f"  ✓ {device}")

if audio_devices:
    print(f"\n✓ SUCCESS! Found {len(audio_devices)} audio device(s)")
    print("\nYou can now use these device names in the recorder.")
else:
    print("\n✗ Still no audio devices detected")
    print("\nPossible issues:")
    print("  1. Devices not properly enabled")
    print("  2. Need to restart the recorder")
    print("  3. Audio drivers need updating")
    print("  4. Privacy settings blocking microphone access")

print("\n" + "="*70)
print("  ALTERNATIVE: Install VB-Cable")
print("="*70)
print("""
If Stereo Mix doesn't exist or doesn't work, install VB-Cable:

1. Download from: https://vb-audio.com/Cable/
2. Install it (may need admin for install only)
3. It creates a virtual audio device that always works
4. Set VB-Cable as your default playback device
5. Then in recorder, select "CABLE Output" as audio input

This routes all system audio through a virtual cable that
FFmpeg can always record from.
""")

input("\nPress ENTER to exit...")
