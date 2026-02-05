# 🎥 Screenity-Like Screen Recorder - Complete Guide

## Features (Just Like Screenity!)

✅ **Multiple Recording Modes:**
- Full screen recording
- Specific window recording
- Custom area recording

✅ **Flexible Audio Options:**
- System audio (speakers/browser sounds) 
- Microphone input
- Both simultaneously (mixed audio)

✅ **Quality Controls:**
- Frame rate selection (15/24/30/60 FPS)
- Quality presets (low/medium/high/ultra)

✅ **User-Friendly GUI:**
- No command line needed
- Visual selection of windows and audio devices
- Real-time recording timer
- Start/Stop controls

---

## 🚀 Quick Start

### 1. Install Requirements

**Python** (if not already installed):
- Download from: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation

**FFmpeg** (portable, no admin needed):
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Get `ffmpeg-release-essentials.zip`
3. Extract to: `C:\Users\YourName\ffmpeg\`
4. Add to PATH OR place the script in the `bin` folder

### 2. Run the Recorder

**Option A: Double-click the batch file**
```
start_recorder.bat
```

**Option B: Run with Python**
```bash
python screenity_like_recorder.py
```

---

## 📖 How to Use

### Step 1: Choose Recording Mode

1. **🖥️ Full Screen** - Records entire desktop
   - Best for: Tutorials, presentations
   
2. **🪟 Specific Window** - Records only one application
   - Best for: App demos, focusing on one program
   - Click "Refresh Windows" to see all open windows
   - Select your target window from dropdown
   
3. **✂️ Custom Area** - Records specific region
   - Best for: Specific part of screen
   - Enter coordinates: X, Y, Width, Height
   - Example: X=100, Y=100, W=1280, H=720

### Step 2: Select Audio Sources

Click "🔄 Refresh Audio Devices" to scan available audio

**System Audio (Stereo Mix):**
- ✅ Check this to record computer sounds
- Captures: Browser audio, apps, music, videos
- Select your "Stereo Mix" or loopback device

**Microphone:**
- ✅ Check this to record your voice
- Select your microphone from dropdown

**Both:**
- ✅ Check both for narrated tutorials with system sounds
- Audio will be automatically mixed

### Step 3: Configure Settings

**Quality:**
- **Low** - Smallest file, fast encoding
- **Medium** - Balanced (recommended)
- **High** - Better quality, larger files
- **Ultra** - Best quality, slow encoding

**Frame Rate:**
- **15 FPS** - Basic screen recording, smaller files
- **24 FPS** - Smooth for most uses
- **30 FPS** - Standard (recommended)
- **60 FPS** - Very smooth, larger files

### Step 4: Record!

1. Click **🔴 Start Recording**
2. The timer will start counting
3. Do your recording
4. Click **⏹️ Stop Recording** when done
5. File is automatically saved with timestamp

---

## 🔧 Troubleshooting

### Problem: No System Audio

**Solutions:**

1. **Enable Stereo Mix (Windows 10/11):**
   ```
   Right-click speaker icon → Sounds → Recording tab
   Right-click empty space → Show Disabled Devices
   Right-click "Stereo Mix" → Enable
   ```

2. **If Stereo Mix doesn't exist:**
   - Try VoiceMeeter (free virtual audio mixer)
   - Or use VB-Audio Virtual Cable
   - Download: https://vb-audio.com/Cable/

3. **Alternative: Use "What U Hear" or "Wave Out Mix"**
   - Some audio drivers use different names
   - Check all devices in the dropdown

### Problem: Can't Record Specific Window

**Solutions:**
- Make sure window is visible (not minimized)
- Some apps (like games) block window capture
- Try full screen mode instead
- Check window name exactly matches

### Problem: FFmpeg Not Found

**Solutions:**
1. Make sure ffmpeg.exe is in your PATH
2. Or place scripts in FFmpeg's `bin` folder
3. Or run from Command Prompt:
   ```
   set PATH=%PATH%;C:\path\to\ffmpeg\bin
   python screenity_like_recorder.py
   ```

### Problem: Window List is Empty

**Solutions:**
- Click "Refresh Windows" button
- Make sure target applications are running
- Don't minimize the windows you want to record

### Problem: Audio Devices Not Showing

**Solutions:**
1. Click "Refresh Audio Devices"
2. Check Windows Sound settings
3. Restart the application
4. Make sure audio devices are not in use by other apps

### Problem: Recording Stops Immediately

**Common causes:**
- Wrong audio device name
- Try recording without audio first
- Check FFmpeg console output for errors

### Problem: Large File Sizes

**Solutions:**
- Lower quality setting (medium or low)
- Reduce frame rate (15 or 24 FPS)
- Use shorter recording sessions
- Reduce video resolution (custom area mode)

---

## 💡 Tips & Best Practices

### For Tutorial Videos:
- Mode: Specific Window
- Audio: System + Microphone
- Quality: High
- FPS: 30

### For Quick Demos:
- Mode: Full Screen
- Audio: System only
- Quality: Medium
- FPS: 24

### For Gaming (if supported):
- Mode: Full Screen
- Audio: System + Microphone
- Quality: Ultra
- FPS: 60

### To Minimize File Size:
- Mode: Custom Area (smaller region)
- Quality: Low
- FPS: 15
- Record only what's needed

### For Professional Videos:
- Test audio levels first
- Close unnecessary applications
- Use high quality settings
- Consider using external mic for better audio

---

## 📁 Output Files

**Location:** Same folder as the script

**Naming:** `recording_YYYYMMDD_HHMMSS.mp4`
- Example: `recording_20240205_143022.mp4`

**Format:** MP4 (H.264 video, AAC audio)
- Compatible with all video players
- Can be uploaded directly to YouTube, etc.

---

## 🔄 Comparison with Screenity

| Feature | Screenity | This Tool |
|---------|-----------|-----------|
| Full Screen Recording | ✅ | ✅ |
| Window Recording | ✅ | ✅ |
| Custom Area | ✅ | ✅ |
| System Audio | ✅ | ✅ |
| Microphone | ✅ | ✅ |
| Mix Audio Sources | ✅ | ✅ |
| Quality Settings | ✅ | ✅ |
| **No Admin Needed** | ✅ | ✅ |
| **Works Offline** | ❌ | ✅ |
| **No Browser Required** | ❌ | ✅ |

---

## ⚙️ Advanced: Command Line Usage

If you prefer command line, here are example commands:

**Full screen with system audio:**
```bash
ffmpeg -f gdigrab -framerate 30 -i desktop -f dshow -i audio="Stereo Mix" -c:v libx264 -preset ultrafast -crf 23 -c:a aac output.mp4
```

**Specific window:**
```bash
ffmpeg -f gdigrab -framerate 30 -i title="Google Chrome" -c:v libx264 -preset ultrafast -crf 23 output.mp4
```

**Custom area:**
```bash
ffmpeg -f gdigrab -framerate 30 -offset_x 100 -offset_y 100 -video_size 1280x720 -i desktop -c:v libx264 -preset ultrafast -crf 23 output.mp4
```

**System audio + Microphone:**
```bash
ffmpeg -f gdigrab -framerate 30 -i desktop -f dshow -i audio="Stereo Mix" -f dshow -i audio="Microphone" -filter_complex amix=inputs=2 -c:v libx264 -preset ultrafast -crf 23 -c:a aac output.mp4
```

---

## 🆘 Need More Help?

1. Check the error messages in the console
2. Try recording without audio first
3. Test with full screen mode first
4. Make sure FFmpeg is properly installed
5. Check that audio devices are enabled in Windows

---

## 📝 Notes

- First time may take a moment to scan windows/devices
- System audio requires "Stereo Mix" or equivalent to be enabled
- Some DRM-protected content may not be recordable
- Recording may use CPU resources - close unnecessary apps
- On company laptops, some group policies may restrict recordings

---

**Enjoy your recordings! 🎬**
