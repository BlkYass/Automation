#!/usr/bin/env python3
"""
Interactive Screen Recorder with GUI
Similar to Screenity - Select windows, audio sources, and recording options
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import json
import os
from datetime import datetime
import sys

class ScreenRecorderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder - Like Screenity")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.recording_process = None
        self.is_recording = False
        self.windows_list = []
        self.audio_devices = []
        
        self.setup_ui()
        self.refresh_windows()
        self.refresh_audio_devices()
    
    def setup_ui(self):
        """Create the user interface"""
        
        # Title
        title_label = tk.Label(self.root, text="🎥 Screen Recorder", 
                              font=("Arial", 18, "bold"), fg="#2563eb")
        title_label.pack(pady=10)
        
        # Recording Mode Section
        mode_frame = tk.LabelFrame(self.root, text="📹 Recording Mode", 
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        mode_frame.pack(fill="x", padx=20, pady=5)
        
        self.recording_mode = tk.StringVar(value="fullscreen")
        
        tk.Radiobutton(mode_frame, text="🖥️  Full Screen", 
                      variable=self.recording_mode, value="fullscreen",
                      font=("Arial", 10)).pack(anchor="w")
        
        tk.Radiobutton(mode_frame, text="🪟  Specific Window", 
                      variable=self.recording_mode, value="window",
                      font=("Arial", 10), command=self.toggle_window_selection).pack(anchor="w")
        
        tk.Radiobutton(mode_frame, text="✂️  Custom Area (manual crop)", 
                      variable=self.recording_mode, value="area",
                      font=("Arial", 10)).pack(anchor="w")
        
        # Window Selection Section
        window_frame = tk.LabelFrame(self.root, text="🪟 Select Window", 
                                     font=("Arial", 10, "bold"), padx=10, pady=10)
        window_frame.pack(fill="x", padx=20, pady=5)
        
        # Refresh button and dropdown
        button_frame = tk.Frame(window_frame)
        button_frame.pack(fill="x")
        
        tk.Button(button_frame, text="🔄 Refresh Windows", 
                 command=self.refresh_windows, bg="#3b82f6", fg="white",
                 font=("Arial", 9)).pack(side="left", padx=5)
        
        self.window_var = tk.StringVar()
        self.window_dropdown = ttk.Combobox(button_frame, textvariable=self.window_var, 
                                           state="disabled", width=50)
        self.window_dropdown.pack(side="left", fill="x", expand=True, padx=5)
        
        # Audio Sources Section
        audio_frame = tk.LabelFrame(self.root, text="🔊 Audio Sources", 
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        audio_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Button(audio_frame, text="🔄 Refresh Audio Devices", 
                 command=self.refresh_audio_devices, bg="#3b82f6", fg="white",
                 font=("Arial", 9)).pack(anchor="w", pady=2)
        
        self.system_audio_var = tk.BooleanVar(value=True)
        self.system_audio_check = tk.Checkbutton(audio_frame, 
                                                 text="🔊 System Audio (Stereo Mix / Speakers)",
                                                 variable=self.system_audio_var,
                                                 font=("Arial", 10))
        self.system_audio_check.pack(anchor="w")
        
        self.system_audio_device = tk.StringVar()
        self.system_dropdown = ttk.Combobox(audio_frame, textvariable=self.system_audio_device,
                                           width=50, state="readonly")
        self.system_dropdown.pack(fill="x", padx=20, pady=2)
        
        self.mic_var = tk.BooleanVar(value=False)
        self.mic_check = tk.Checkbutton(audio_frame, 
                                       text="🎤 Microphone",
                                       variable=self.mic_var,
                                       font=("Arial", 10))
        self.mic_check.pack(anchor="w", pady=(10, 0))
        
        self.mic_device = tk.StringVar()
        self.mic_dropdown = ttk.Combobox(audio_frame, textvariable=self.mic_device,
                                        width=50, state="readonly")
        self.mic_dropdown.pack(fill="x", padx=20, pady=2)
        
        # Recording Settings Section
        settings_frame = tk.LabelFrame(self.root, text="⚙️ Recording Settings", 
                                      font=("Arial", 10, "bold"), padx=10, pady=10)
        settings_frame.pack(fill="x", padx=20, pady=5)
        
        # Quality
        quality_frame = tk.Frame(settings_frame)
        quality_frame.pack(fill="x", pady=2)
        tk.Label(quality_frame, text="Quality:", font=("Arial", 10)).pack(side="left")
        self.quality_var = tk.StringVar(value="high")
        ttk.Combobox(quality_frame, textvariable=self.quality_var, 
                    values=["low", "medium", "high", "ultra"], 
                    state="readonly", width=15).pack(side="left", padx=10)
        
        # FPS
        fps_frame = tk.Frame(settings_frame)
        fps_frame.pack(fill="x", pady=2)
        tk.Label(fps_frame, text="Frame Rate:", font=("Arial", 10)).pack(side="left")
        self.fps_var = tk.StringVar(value="30")
        ttk.Combobox(fps_frame, textvariable=self.fps_var, 
                    values=["15", "24", "30", "60"], 
                    state="readonly", width=15).pack(side="left", padx=10)
        
        # Custom Area Settings (hidden by default)
        self.area_frame = tk.Frame(settings_frame)
        
        area_label = tk.Label(self.area_frame, 
                            text="Custom Area (x, y, width, height):", 
                            font=("Arial", 10))
        area_label.pack(anchor="w")
        
        area_inputs = tk.Frame(self.area_frame)
        area_inputs.pack(fill="x")
        
        tk.Label(area_inputs, text="X:").pack(side="left")
        self.area_x = tk.Entry(area_inputs, width=8)
        self.area_x.insert(0, "0")
        self.area_x.pack(side="left", padx=2)
        
        tk.Label(area_inputs, text="Y:").pack(side="left")
        self.area_y = tk.Entry(area_inputs, width=8)
        self.area_y.insert(0, "0")
        self.area_y.pack(side="left", padx=2)
        
        tk.Label(area_inputs, text="W:").pack(side="left")
        self.area_width = tk.Entry(area_inputs, width=8)
        self.area_width.insert(0, "1920")
        self.area_width.pack(side="left", padx=2)
        
        tk.Label(area_inputs, text="H:").pack(side="left")
        self.area_height = tk.Entry(area_inputs, width=8)
        self.area_height.insert(0, "1080")
        self.area_height.pack(side="left", padx=2)
        
        # Status Section
        status_frame = tk.Frame(self.root)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = tk.Label(status_frame, text="⏸️ Ready to record", 
                                     font=("Arial", 11, "bold"), fg="#059669")
        self.status_label.pack()
        
        self.timer_label = tk.Label(status_frame, text="00:00:00", 
                                    font=("Arial", 14), fg="#6b7280")
        self.timer_label.pack()
        
        # Control Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.record_button = tk.Button(button_frame, text="🔴 Start Recording", 
                                      command=self.start_recording,
                                      bg="#dc2626", fg="white", 
                                      font=("Arial", 12, "bold"),
                                      width=20, height=2)
        self.record_button.pack(side="left", padx=5)
        
        self.stop_button = tk.Button(button_frame, text="⏹️ Stop Recording", 
                                    command=self.stop_recording,
                                    bg="#6b7280", fg="white", 
                                    font=("Arial", 12, "bold"),
                                    width=20, height=2, state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        # Output info
        self.output_label = tk.Label(self.root, text="", 
                                     font=("Arial", 9), fg="#6b7280", wraplength=550)
        self.output_label.pack(pady=5)
    
    def toggle_window_selection(self):
        """Enable/disable window selection based on mode"""
        mode = self.recording_mode.get()
        if mode == "window":
            self.window_dropdown.config(state="readonly")
        else:
            self.window_dropdown.config(state="disabled")
        
        if mode == "area":
            self.area_frame.pack(fill="x", pady=5)
        else:
            self.area_frame.pack_forget()
    
    def refresh_windows(self):
        """Get list of open windows"""
        try:
            # Use PowerShell to get window titles
            cmd = 'powershell "Get-Process | Where-Object {$_.MainWindowTitle -ne \\"\\"} | Select-Object MainWindowTitle"'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            windows = []
            for line in result.stdout.split('\n')[3:]:  # Skip header lines
                line = line.strip()
                if line and line != '':
                    windows.append(line)
            
            self.windows_list = windows
            self.window_dropdown['values'] = windows
            if windows:
                self.window_dropdown.current(0)
            
            messagebox.showinfo("Success", f"Found {len(windows)} windows")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get windows: {str(e)}")
    
    def refresh_audio_devices(self):
        """Get list of audio devices using FFmpeg"""
        try:
            cmd = ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
            result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)
            
            audio_devices = []
            for line in result.stdout.split('\n'):
                if '(audio)' in line and '"' in line:
                    # Extract device name between quotes
                    start = line.find('"') + 1
                    end = line.find('"', start)
                    if start > 0 and end > start:
                        device_name = line[start:end]
                        audio_devices.append(device_name)
            
            self.audio_devices = audio_devices
            
            # Separate into system audio and microphones
            system_devices = [d for d in audio_devices if 'stereo mix' in d.lower() or 'wave out' in d.lower() or 'loopback' in d.lower()]
            mic_devices = [d for d in audio_devices if 'microphone' in d.lower() or 'mic' in d.lower()]
            
            # If no explicit system devices found, use all as options
            if not system_devices:
                system_devices = audio_devices
            if not mic_devices:
                mic_devices = audio_devices
            
            self.system_dropdown['values'] = system_devices
            self.mic_dropdown['values'] = mic_devices
            
            if system_devices:
                self.system_dropdown.current(0)
            if mic_devices:
                self.mic_dropdown.current(0)
            
            messagebox.showinfo("Success", f"Found {len(audio_devices)} audio devices")
        except FileNotFoundError:
            messagebox.showerror("Error", "FFmpeg not found! Please install FFmpeg first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get audio devices: {str(e)}")
    
    def build_ffmpeg_command(self):
        """Build FFmpeg command based on user selections"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"recording_{timestamp}.mp4"
        
        cmd = ['ffmpeg']
        
        # Video input based on mode
        mode = self.recording_mode.get()
        fps = self.fps_var.get()
        
        if mode == "fullscreen":
            cmd.extend(['-f', 'gdigrab', '-framerate', fps, '-i', 'desktop'])
        elif mode == "window":
            window_title = self.window_var.get()
            if not window_title:
                raise ValueError("Please select a window")
            cmd.extend(['-f', 'gdigrab', '-framerate', fps, '-i', f'title={window_title}'])
        elif mode == "area":
            x = self.area_x.get()
            y = self.area_y.get()
            w = self.area_width.get()
            h = self.area_height.get()
            cmd.extend(['-f', 'gdigrab', '-framerate', fps, 
                       '-offset_x', x, '-offset_y', y,
                       '-video_size', f'{w}x{h}', '-i', 'desktop'])
        
        # Audio inputs
        audio_inputs = []
        audio_filters = []
        
        if self.system_audio_var.get() and self.system_audio_device.get():
            audio_inputs.extend(['-f', 'dshow', '-i', f'audio={self.system_audio_device.get()}'])
        
        if self.mic_var.get() and self.mic_device.get():
            audio_inputs.extend(['-f', 'dshow', '-i', f'audio={self.mic_device.get()}'])
        
        cmd.extend(audio_inputs)
        
        # Mix audio if both sources selected
        audio_count = sum([self.system_audio_var.get(), self.mic_var.get()])
        if audio_count > 1:
            cmd.extend(['-filter_complex', 'amix=inputs=2:duration=longest'])
        
        # Quality settings
        quality = self.quality_var.get()
        quality_map = {
            'low': ('ultrafast', '28'),
            'medium': ('fast', '23'),
            'high': ('medium', '20'),
            'ultra': ('slow', '18')
        }
        preset, crf = quality_map[quality]
        
        # Video codec
        cmd.extend(['-c:v', 'libx264', '-preset', preset, '-crf', crf])
        
        # Audio codec (if audio is included)
        if audio_count > 0:
            cmd.extend(['-c:a', 'aac', '-b:a', '192k'])
        
        cmd.append(output_file)
        
        return cmd, output_file
    
    def start_recording(self):
        """Start the recording"""
        try:
            cmd, output_file = self.build_ffmpeg_command()
            
            # Update UI
            self.is_recording = True
            self.record_button.config(state="disabled")
            self.stop_button.config(state="normal", bg="#dc2626")
            self.status_label.config(text="🔴 Recording...", fg="#dc2626")
            self.output_label.config(text=f"Saving to: {output_file}")
            
            # Start FFmpeg in a separate thread
            def run_ffmpeg():
                self.recording_process = subprocess.Popen(cmd, 
                                                         stdin=subprocess.PIPE,
                                                         stdout=subprocess.PIPE,
                                                         stderr=subprocess.PIPE)
                self.recording_process.wait()
            
            self.recording_thread = threading.Thread(target=run_ffmpeg, daemon=True)
            self.recording_thread.start()
            
            # Start timer
            self.start_time = datetime.now()
            self.update_timer()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {str(e)}")
            self.is_recording = False
            self.record_button.config(state="normal")
            self.stop_button.config(state="disabled")
    
    def stop_recording(self):
        """Stop the recording"""
        if self.recording_process:
            try:
                # Send 'q' to FFmpeg to stop gracefully
                self.recording_process.stdin.write(b'q')
                self.recording_process.stdin.flush()
                self.recording_process.wait(timeout=5)
            except:
                self.recording_process.terminate()
            
            self.is_recording = False
            self.record_button.config(state="normal")
            self.stop_button.config(state="disabled", bg="#6b7280")
            self.status_label.config(text="✅ Recording stopped", fg="#059669")
            
            messagebox.showinfo("Success", "Recording saved successfully!")
    
    def update_timer(self):
        """Update the recording timer"""
        if self.is_recording:
            elapsed = datetime.now() - self.start_time
            hours = int(elapsed.total_seconds() // 3600)
            minutes = int((elapsed.total_seconds() % 3600) // 60)
            seconds = int(elapsed.total_seconds() % 60)
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

def main():
    # Check if FFmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except FileNotFoundError:
        response = messagebox.askyesno(
            "FFmpeg Not Found",
            "FFmpeg is required but not found.\n\n"
            "Download FFmpeg portable version?\n"
            "(Will open browser to download page)"
        )
        if response:
            import webbrowser
            webbrowser.open('https://www.gyan.dev/ffmpeg/builds/')
        sys.exit(1)
    
    root = tk.Tk()
    app = ScreenRecorderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
