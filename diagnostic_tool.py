#!/usr/bin/env python3
"""
Complete Recording Diagnostic Tool
Tests everything and creates working recordings
"""

import subprocess
import sys
import os
from datetime import datetime

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def run_command(cmd, timeout=30):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, 
                              timeout=timeout, stderr=subprocess.STDOUT)
        return result.stdout, result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1
    except Exception as e:
        return f"ERROR: {str(e)}", -1

def test_ffmpeg():
    """Test FFmpeg"""
    print_header("1. Testing FFmpeg")
    output, code = run_command(['ffmpeg', '-version'], timeout=5)
    
    if code == 0:
        print("✓ FFmpeg is working!")
        version = output.split('\n')[0]
        print(f"  {version}")
        return True
    else:
        print("✗ FFmpeg NOT working!")
        print(f"  Error: {output}")
        return False

def get_screen_info():
    """Get information about all monitors"""
    print_header("2. Detecting Monitors")
    
    # Use PowerShell to get screen info
    ps_cmd = '''
    Add-Type -AssemblyName System.Windows.Forms
    $screens = [System.Windows.Forms.Screen]::AllScreens
    foreach ($screen in $screens) {
        Write-Output "Monitor: $($screen.DeviceName)"
        Write-Output "Primary: $($screen.Primary)"
        Write-Output "Bounds: $($screen.Bounds.X),$($screen.Bounds.Y),$($screen.Bounds.Width),$($screen.Bounds.Height)"
        Write-Output "---"
    }
    '''
    
    cmd = ['powershell', '-Command', ps_cmd]
    output, code = run_command(cmd)
    
    monitors = []
    current = {}
    
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('Monitor:'):
            current['name'] = line.split(':', 1)[1].strip()
        elif line.startswith('Primary:'):
            current['primary'] = 'True' in line
        elif line.startswith('Bounds:'):
            bounds = line.split(':', 1)[1].strip().split(',')
            if len(bounds) == 4:
                current['x'] = int(bounds[0])
                current['y'] = int(bounds[1])
                current['width'] = int(bounds[2])
                current['height'] = int(bounds[3])
        elif line == '---' and current:
            monitors.append(current.copy())
            current = {}
    
    if monitors:
        print(f"\n✓ Found {len(monitors)} monitor(s):\n")
        for i, mon in enumerate(monitors, 1):
            primary = " (PRIMARY)" if mon.get('primary') else ""
            print(f"  Monitor {i}{primary}:")
            print(f"    Position: X={mon.get('x', 0)}, Y={mon.get('y', 0)}")
            print(f"    Size: {mon.get('width', 0)}x{mon.get('height', 0)}")
    else:
        print("✗ Could not detect monitors")
        print("  Defaulting to full desktop capture")
    
    return monitors

def list_audio_devices():
    """List all audio devices"""
    print_header("3. Detecting Audio Devices")
    
    cmd = ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
    output, _ = run_command(cmd, timeout=10)
    
    audio_devices = []
    
    print("\n🔊 Audio Devices Found:\n")
    for line in output.split('\n'):
        if '(audio)' in line and '"' in line:
            start = line.find('"') + 1
            end = line.find('"', start)
            if start > 0 and end > start:
                device = line[start:end]
                audio_devices.append(device)
                print(f"  • {device}")
    
    if not audio_devices:
        print("  ✗ NO audio devices detected!")
        print("\n  Possible reasons:")
        print("    - Audio drivers not properly installed")
        print("    - Devices disabled in Windows Sound settings")
        print("    - Need to enable 'Stereo Mix' for system audio")
    
    return audio_devices

def test_simple_recording():
    """Test simple 3-second recording"""
    print_header("4. Test Recording (3 seconds, no audio)")
    
    output = f"test_{datetime.now().strftime('%H%M%S')}.mp4"
    
    print("\nStarting 3-second test recording...")
    print("Move your mouse to see if it's working...")
    
    cmd = [
        'ffmpeg',
        '-f', 'gdigrab',
        '-framerate', '15',
        '-t', '3',
        '-i', 'desktop',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-pix_fmt', 'yuv420p',
        '-y',
        output
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, text=True)
    
    stdout, stderr = process.communicate(timeout=10)
    
    if os.path.exists(output):
        size = os.path.getsize(output)
        if size > 1000:
            print(f"\n✓ SUCCESS! Test file created: {output}")
            print(f"  Size: {size/1024:.1f} KB")
            print(f"\n  Try playing: {output}")
            return True, output
        else:
            print(f"\n✗ File too small ({size} bytes)")
    else:
        print("\n✗ File not created")
    
    print("\nFFmpeg errors (last 30 lines):")
    print('\n'.join(stderr.split('\n')[-30:]))
    return False, None

def test_monitor_recording(monitors):
    """Test recording from specific monitor"""
    if not monitors or len(monitors) <= 1:
        return
    
    print_header("5. Test Multi-Monitor Recording")
    
    print("\nWhich monitor do you want to test?")
    for i, mon in enumerate(monitors, 1):
        primary = " (PRIMARY)" if mon.get('primary') else ""
        print(f"  {i}. Monitor {i}{primary} - {mon.get('width')}x{mon.get('height')}")
    
    try:
        choice = int(input("\nEnter number (or 0 to skip): "))
        if choice == 0 or choice > len(monitors):
            return
        
        mon = monitors[choice - 1]
        output = f"test_monitor{choice}_{datetime.now().strftime('%H%M%S')}.mp4"
        
        print(f"\nRecording Monitor {choice} for 3 seconds...")
        
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
            output
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=10)
        
        if os.path.exists(output) and os.path.getsize(output) > 1000:
            size = os.path.getsize(output) / 1024
            print(f"\n✓ SUCCESS! Monitor {choice} recorded: {output}")
            print(f"  Size: {size:.1f} KB")
        else:
            print("\n✗ Recording failed")
            
    except ValueError:
        print("Invalid choice")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║         SCREEN RECORDER DIAGNOSTIC TOOL                       ║
    ║         This will test your recording setup                   ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Test 1: FFmpeg
    if not test_ffmpeg():
        print("\n❌ Cannot continue without FFmpeg")
        input("\nPress ENTER to exit...")
        return
    
    # Test 2: Monitors
    monitors = get_screen_info()
    
    # Test 3: Audio
    audio_devices = list_audio_devices()
    
    # Test 4: Simple recording
    success, filename = test_simple_recording()
    
    if not success:
        print("\n❌ Basic recording failed!")
        print("\nThis usually means:")
        print("  1. FFmpeg cannot access your screen")
        print("  2. Missing codecs")
        print("  3. Permission issues")
        input("\nPress ENTER to exit...")
        return
    
    # Test 5: Multi-monitor
    if len(monitors) > 1:
        test_monitor_recording(monitors)
    
    # Summary
    print_header("DIAGNOSTIC SUMMARY")
    print(f"\n✓ FFmpeg: Working")
    print(f"✓ Monitors: {len(monitors)} detected")
    print(f"{'✓' if audio_devices else '✗'} Audio: {len(audio_devices)} devices")
    print(f"{'✓' if success else '✗'} Recording: {'Working' if success else 'Failed'}")
    
    if not audio_devices:
        print("\n⚠️  AUDIO ISSUE DETECTED:")
        print("  To enable audio recording:")
        print("  1. Right-click speaker icon → Sounds")
        print("  2. Recording tab")
        print("  3. Right-click → Show Disabled Devices")
        print("  4. Enable 'Stereo Mix' or 'Microphone'")
    
    print("\n" + "="*70)
    input("\nPress ENTER to exit...")

if __name__ == "__main__":
    main()