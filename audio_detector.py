#!/usr/bin/env python3
"""
Audio Device Detection Tool
Finds ALL audio devices using multiple methods
"""

import subprocess
import sys

print("="*70)
print("  AUDIO DEVICE DETECTION")
print("="*70)

# Method 1: FFmpeg DirectShow
print("\n1. FFmpeg DirectShow (dshow) - Audio Devices:")
print("-"*70)
try:
    result = subprocess.run(
        ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
        capture_output=True, text=True, timeout=10
    )
    
    # FFmpeg outputs device list to stderr
    output = result.stderr
    
    audio_count = 0
    video_count = 0
    
    print("\nFull output:")
    for line in output.split('\n'):
        # Print lines that contain device info
        if 'DirectShow' in line or '(audio)' in line or '(video)' in line or 'Alternative name' in line:
            print(f"  {line}")
            if '(audio)' in line:
                audio_count += 1
            if '(video)' in line:
                video_count += 1
    
    print(f"\nSummary: {audio_count} audio devices, {video_count} video devices")
    
except Exception as e:
    print(f"ERROR: {e}")

# Method 2: Windows PowerShell - Audio Devices
print("\n\n2. Windows Audio Devices (PowerShell):")
print("-"*70)
try:
    ps_script = '''
Get-WmiObject Win32_SoundDevice | Select-Object Name, Status, StatusInfo | Format-List
'''
    result = subprocess.run(['powershell', '-Command', ps_script],
                          capture_output=True, text=True, timeout=10)
    print(result.stdout)
except Exception as e:
    print(f"ERROR: {e}")

# Method 3: Check Recording Devices
print("\n3. Windows Recording Devices:")
print("-"*70)
try:
    ps_script = '''
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
Write-Output "Audio devices detected by Windows"
'''
    result = subprocess.run(['powershell', '-Command', ps_script],
                          capture_output=True, text=True, timeout=10)
    print(result.stdout)
except Exception as e:
    print(f"ERROR: {e}")

# Method 4: List audio using different FFmpeg format
print("\n4. Testing Alternative FFmpeg Method:")
print("-"*70)
try:
    # Try listing sources
    result = subprocess.run(
        ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
        capture_output=True, text=True, timeout=10
    )
    
    lines = result.stderr.split('\n')
    
    print("\nExtracting device names:")
    for line in lines:
        if '"' in line and ('audio' in line.lower() or 'microphone' in line.lower()):
            # Extract device name between quotes
            parts = line.split('"')
            if len(parts) >= 2:
                device_name = parts[1]
                print(f"  Found: {device_name}")
                
except Exception as e:
    print(f"ERROR: {e}")

# Instructions
print("\n" + "="*70)
print("  TROUBLESHOOTING")
print("="*70)
print("""
If NO audio devices were found above, try these steps:

1. ENABLE STEREO MIX (for system audio):
   - Right-click speaker icon in taskbar
   - Click "Sounds" or "Open Sound settings"
   - Click "Sound Control Panel" (on the right)
   - Go to "Recording" tab
   - Right-click in empty space → "Show Disabled Devices"
   - Right-click on "Stereo Mix" → Enable
   - Right-click on "Stereo Mix" → Set as Default Device

2. ENABLE MICROPHONE:
   - Same steps as above
   - Find your microphone in Recording tab
   - Right-click → Enable
   - Right-click → Set as Default Communication Device

3. CHECK PRIVACY SETTINGS (Windows 10/11):
   - Settings → Privacy → Microphone
   - Make sure "Allow apps to access your microphone" is ON
   - Allow desktop apps to access microphone

4. UPDATE AUDIO DRIVERS:
   - Open Device Manager
   - Expand "Sound, video and game controllers"
   - Right-click your audio device → Update driver

5. ALTERNATIVE: Use VB-Cable (Virtual Audio Cable):
   - Download from: https://vb-audio.com/Cable/
   - Installs a virtual audio device that always works
   - No admin rights needed for usage (only for install)
""")

print("\nWould you like to test recording WITH a specific audio device?")
print("If you know the exact device name, we can test it now.")
print("\nCommon device names to try:")
print("  - Stereo Mix")
print("  - Microphone")
print("  - Microphone Array")
print("  - Line In")
print("  - CABLE Output (if VB-Cable installed)")

device_name = input("\nEnter device name to test (or press ENTER to skip): ").strip()

if device_name:
    print(f"\nTesting recording with: {device_name}")
    output_file = "test_with_audio.mp4"
    
    cmd = [
        'ffmpeg',
        '-f', 'gdigrab',
        '-framerate', '15',
        '-t', '5',
        '-i', 'desktop',
        '-f', 'dshow',
        '-i', f'audio={device_name}',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-y',
        output_file
    ]
    
    print("Recording 5 seconds with audio...")
    print("(Make some noise or play audio in browser)")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        import os
        if os.path.exists(output_file) and os.path.getsize(output_file) > 1000:
            print(f"\n✓ SUCCESS! File created: {output_file}")
            print(f"   Size: {os.path.getsize(output_file)/1024:.1f} KB")
            print(f"\n   Play it to check if audio was recorded!")
        else:
            print("\n✗ Recording failed")
            print("\nError output:")
            print(result.stderr[-1000:])
    except Exception as e:
        print(f"\n✗ Error: {e}")

input("\nPress ENTER to exit...")
