#!/usr/bin/env python3
"""
Simple Diagnostic Tool - Tests your recording setup
"""

import subprocess
import os
from datetime import datetime

print("="*70)
print("  SCREEN RECORDER DIAGNOSTIC")
print("="*70)

# Test 1: FFmpeg
print("\n1. Testing FFmpeg...")
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✓ FFmpeg is working!")
        version = result.stdout.split('\n')[0]
        print(f"   {version}")
    else:
        print("   ✗ FFmpeg error")
except Exception as e:
    print(f"   ✗ Error: {e}")
    input("\nPress ENTER to exit...")
    exit(1)

# Test 2: Detect Monitors
print("\n2. Detecting Monitors...")
try:
    ps_script = '''
Add-Type -AssemblyName System.Windows.Forms
$screens = [System.Windows.Forms.Screen]::AllScreens
$index = 0
foreach ($screen in $screens) {
    $index++
    $primary = if ($screen.Primary) { " (PRIMARY)" } else { "" }
    Write-Output "Monitor $index$primary|$($screen.Bounds.X)|$($screen.Bounds.Y)|$($screen.Bounds.Width)|$($screen.Bounds.Height)"
}
'''
    
    result = subprocess.run(['powershell', '-Command', ps_script], 
                          capture_output=True, text=True)
    
    monitors = []
    for line in result.stdout.strip().split('\n'):
        if '|' in line:
            parts = line.strip().split('|')
            if len(parts) == 5:
                monitors.append({
                    'name': parts[0],
                    'x': int(parts[1]),
                    'y': int(parts[2]),
                    'width': int(parts[3]),
                    'height': int(parts[4])
                })
    
    if monitors:
        print(f"   ✓ Found {len(monitors)} monitor(s):")
        for mon in monitors:
            print(f"      • {mon['name']}: {mon['width']}x{mon['height']} at ({mon['x']},{mon['y']})")
    else:
        print("   ⚠ No monitors detected (will use full desktop)")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Audio Devices
print("\n3. Detecting Audio Devices...")
try:
    result = subprocess.run(['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
                          capture_output=True, text=True)
    
    # Audio devices are in stderr for this command
    output = result.stderr
    
    audio_devices = []
    print("   Scanning...")
    
    for line in output.split('\n'):
        if '(audio)' in line and '"' in line:
            start = line.find('"') + 1
            end = line.find('"', start)
            if start > 0 and end > start:
                device = line[start:end]
                audio_devices.append(device)
                print(f"      • {device}")
    
    if audio_devices:
        print(f"\n   ✓ Found {len(audio_devices)} audio device(s)")
    else:
        print("\n   ✗ NO audio devices found!")
        print("\n   To enable audio:")
        print("      1. Right-click speaker icon → Sounds")
        print("      2. Recording tab")
        print("      3. Right-click → Show Disabled Devices")
        print("      4. Enable 'Stereo Mix' and/or your microphone")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Quick Recording Test
print("\n4. Testing Recording (3 seconds)...")
print("   Creating test video...")

output = f"test_recording_{datetime.now().strftime('%H%M%S')}.mp4"

cmd = [
    'ffmpeg',
    '-f', 'gdigrab',
    '-framerate', '15',
    '-t', '3',
    '-i', 'desktop',
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-pix_fmt', 'yuv420p',  # Critical for VLC!
    '-y',
    output
]

try:
    print("   Recording... (move your mouse)")
    process = subprocess.run(cmd, capture_output=True, timeout=10)
    
    if os.path.exists(output):
        size = os.path.getsize(output)
        if size > 1000:
            print(f"\n   ✓ SUCCESS! Test file created: {output}")
            print(f"   File size: {size/1024:.1f} KB")
            print(f"\n   Try playing it: {output}")
        else:
            print(f"\n   ✗ File too small ({size} bytes)")
            print("   Recording may have failed")
    else:
        print("\n   ✗ File not created")
        
except subprocess.TimeoutExpired:
    print("\n   ✗ Timeout - recording took too long")
except Exception as e:
    print(f"\n   ✗ Error: {e}")

# Test 5: Monitor-Specific Recording
if len(monitors) > 1:
    print(f"\n5. Testing Monitor Selection...")
    print(f"   Available monitors:")
    for i, mon in enumerate(monitors, 1):
        print(f"      {i}. {mon['name']}")
    
    try:
        choice = input("\n   Enter monitor number to test (or press ENTER to skip): ").strip()
        if choice and choice.isdigit() and 1 <= int(choice) <= len(monitors):
            mon = monitors[int(choice) - 1]
            output2 = f"test_monitor{choice}_{datetime.now().strftime('%H%M%S')}.mp4"
            
            cmd = [
                'ffmpeg',
                '-f', 'gdigrab',
                '-framerate', '15',
                '-t', '3',
                '-offset_x', str(mon['x']),
                '-offset_y', str(mon['y']),
                '-video_size', f"{mon['width']}x{mon['height']}",
                '-i', 'desktop',
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-pix_fmt', 'yuv420p',
                '-y',
                output2
            ]
            
            print(f"   Recording monitor {choice} for 3 seconds...")
            subprocess.run(cmd, capture_output=True, timeout=10)
            
            if os.path.exists(output2) and os.path.getsize(output2) > 1000:
                size = os.path.getsize(output2) / 1024
                print(f"\n   ✓ SUCCESS! Monitor recorded: {output2}")
                print(f"   File size: {size:.1f} KB")
            else:
                print("\n   ✗ Monitor recording failed")
    except:
        pass

# Summary
print("\n" + "="*70)
print("  SUMMARY")
print("="*70)
print(f"FFmpeg: Working ✓")
print(f"Monitors: {len(monitors) if monitors else 0} detected")
print(f"Audio: {len(audio_devices) if 'audio_devices' in locals() else 0} devices found")
print(f"Recording: {'Working ✓' if os.path.exists(output) else 'Failed ✗'}")
print("="*70)

input("\nPress ENTER to exit...")