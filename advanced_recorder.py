#!/usr/bin/env python3
"""
Advanced Screen Recorder - Multi-Monitor Support
Fixes: Audio detection, multi-monitor selection, file corruption
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading
import os
from datetime import datetime
import sys

class AdvancedRecorderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Screen Recorder")
        self.root.geometry("650x800")
        
        self.recording_process = None
        self.is_recording = False
        self.monitors = []
        self.audio_devices = []
        
        self.setup_ui()
        self.detect_monitors()
        self.detect_audio_devices()
    
    def setup_ui(self):
        """Create UI"""
        # Title
        title = tk.Label(self.root, text="🎥 Advanced Screen Recorder", 
                        font=("Arial", 18, "bold"), fg="#2563eb")
        title.pack(pady=10)
        
        # Monitor Selection
        monitor_frame = tk.LabelFrame(self.root, text="🖥️ Monitor Selection", 
                                     font=("Arial", 10, "bold"), padx=10, pady=10)
        monitor_frame.pack(fill="x", padx=20, pady=5)
        
        btn_frame = tk.Frame(monitor_frame)
        btn_frame.pack(fill="x")
        
        tk.Button(btn_frame, text="🔄 Detect Monitors", 
                 command=self.detect_monitors, bg="#3b82f6", fg="white").pack(side="left", padx=5)
        
        self.monitor_var = tk.StringVar()
        self.monitor_dropdown = ttk.Combobox(btn_frame, textvariable=self.monitor_var,
                                            state="readonly", width=50)
        self.monitor_dropdown.pack(side="left", fill="x", expand=True, padx=5)
        
        # Recording Mode
        mode_frame = tk.LabelFrame(self.root, text="📹 Recording Mode",
                                  font=("Arial", 10, "bold"), padx=10, pady=10)
        mode_frame.pack(fill="x", padx=20, pady=5)
        
        self.mode_var = tk.StringVar(value="monitor")
        tk.Radiobutton(mode_frame, text="🖥️ Full Desktop (all monitors)",
                      variable=self.mode_var, value="desktop").pack(anchor="w")
        tk.Radiobutton(mode_frame, text="🖥️ Selected Monitor Only",
                      variable=self.mode_var, value="monitor").pack(anchor="w")
        tk.Radiobutton(mode_frame, text="🪟 Specific Window",
                      variable=self.mode_var, value="window").pack(anchor="w")
        
        # Window selection
        win_frame = tk.Frame(mode_frame)
        win_frame.pack(fill="x", pady=5)
        
        tk.Button(win_frame, text="Refresh Windows", 
                 command=self.refresh_windows).pack(side="left", padx=5)
        
        self.window_var = tk.StringVar()
        self.window_dropdown = ttk.Combobox(win_frame, textvariable=self.window_var,
                                           state="readonly", width=45)
        self.window_dropdown.pack(side="left", fill="x", expand=True)
        
        # Audio Section
        audio_frame = tk.LabelFrame(self.root, text="🔊 Audio Sources",
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        audio_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Button(audio_frame, text="🔄 Detect Audio Devices",
                 command=self.detect_audio_devices, bg="#3b82f6", fg="white").pack(anchor="w", pady=2)
        
        self.audio_enabled = tk.BooleanVar(value=False)
        tk.Checkbutton(audio_frame, text="Enable Audio Recording",
                      variable=self.audio_enabled).pack(anchor="w")
        
        tk.Label(audio_frame, text="Select Audio Device:", font=("Arial", 9)).pack(anchor="w", pady=(5,0))
        
        self.audio_var = tk.StringVar()
        self.audio_dropdown = ttk.Combobox(audio_frame, textvariable=self.audio_var,
                                          state="readonly", width=55)
        self.audio_dropdown.pack(fill="x", pady=2)
        
        self.audio_status = tk.Label(audio_frame, text="", fg="#dc2626", font=("Arial", 8))
        self.audio_status.pack(anchor="w")
        
        # Settings
        settings_frame = tk.LabelFrame(self.root, text="⚙️ Settings",
                                      font=("Arial", 10, "bold"), padx=10, pady=10)
        settings_frame.pack(fill="x", padx=20, pady=5)
        
        # FPS
        fps_frame = tk.Frame(settings_frame)
        fps_frame.pack(fill="x", pady=2)
        tk.Label(fps_frame, text="Frame Rate:").pack(side="left")
        self.fps_var = tk.StringVar(value="30")
        ttk.Combobox(fps_frame, textvariable=self.fps_var,
                    values=["15", "20", "25", "30"], state="readonly", width=10).pack(side="left", padx=5)
        
        # Quality
        quality_frame = tk.Frame(settings_frame)
        quality_frame.pack(fill="x", pady=2)
        tk.Label(quality_frame, text="Quality (CRF):").pack(side="left")
        self.quality_var = tk.StringVar(value="23")
        ttk.Combobox(quality_frame, textvariable=self.quality_var,
                    values=["18 (Best)", "23 (Good)", "28 (Fast)"], state="readonly", width=15).pack(side="left", padx=5)
        
        # Output location
        output_frame = tk.Frame(settings_frame)
        output_frame.pack(fill="x", pady=5)
        tk.Label(output_frame, text="Save to:").pack(side="left")
        self.output_dir = tk.StringVar(value=os.getcwd())
        tk.Entry(output_frame, textvariable=self.output_dir, width=35).pack(side="left", padx=5)
        tk.Button(output_frame, text="Browse", command=self.browse_output).pack(side="left")
        
        # Status
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=10)
        
        self.status_label = tk.Label(status_frame, text="⏸️ Ready",
                                     font=("Arial", 12, "bold"), fg="#059669")
        self.status_label.pack()
        
        self.timer_label = tk.Label(status_frame, text="00:00:00",
                                    font=("Arial", 16), fg="#6b7280")
        self.timer_label.pack()
        
        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="🔴 Start Recording",
                                   command=self.start_recording,
                                   bg="#dc2626", fg="white",
                                   font=("Arial", 12, "bold"), width=18, height=2)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = tk.Button(btn_frame, text="⏹️ Stop",
                                  command=self.stop_recording,
                                  bg="#6b7280", fg="white",
                                  font=("Arial", 12, "bold"), width=18, height=2,
                                  state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        # Info
        self.info_label = tk.Label(self.root, text="", font=("Arial", 9),
                                   fg="#6b7280", wraplength=600)
        self.info_label.pack(pady=5)
    
    def detect_monitors(self):
        """Detect all monitors using PowerShell"""
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
                                  capture_output=True, text=True, timeout=10)
            
            self.monitors = []
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    parts = line.strip().split('|')
                    if len(parts) == 5:
                        self.monitors.append({
                            'name': parts[0],
                            'x': int(parts[1]),
                            'y': int(parts[2]),
                            'width': int(parts[3]),
                            'height': int(parts[4])
                        })
            
            if self.monitors:
                options = [f"{m['name']} - {m['width']}x{m['height']}" for m in self.monitors]
                self.monitor_dropdown['values'] = options
                self.monitor_dropdown.current(0)
                messagebox.showinfo("Success", f"Found {len(self.monitors)} monitor(s)")
            else:
                messagebox.showwarning("Warning", "No monitors detected, will use full desktop")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect monitors: {e}")
    
    def detect_audio_devices(self):
        """Detect audio devices"""
        try:
            cmd = ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
            result = subprocess.run(cmd, capture_output=True, text=True,
                                  stderr=subprocess.STDOUT, timeout=10)
            
            self.audio_devices = []
            for line in result.stdout.split('\n'):
                if '(audio)' in line and '"' in line:
                    start = line.find('"') + 1
                    end = line.find('"', start)
                    if start > 0 and end > start:
                        device = line[start:end]
                        self.audio_devices.append(device)
            
            if self.audio_devices:
                self.audio_dropdown['values'] = self.audio_devices
                self.audio_dropdown.current(0)
                self.audio_status.config(text=f"✓ Found {len(self.audio_devices)} device(s)", fg="#059669")
                messagebox.showinfo("Audio Devices", 
                                  f"Found {len(self.audio_devices)} audio device(s):\n\n" + 
                                  "\n".join(f"• {d}" for d in self.audio_devices))
            else:
                self.audio_status.config(text="✗ No audio devices found!", fg="#dc2626")
                messagebox.showwarning("No Audio", 
                                     "No audio devices detected!\n\n" +
                                     "To enable audio:\n" +
                                     "1. Right-click speaker icon → Sounds\n" +
                                     "2. Recording tab\n" +
                                     "3. Right-click → Show Disabled Devices\n" +
                                     "4. Enable 'Stereo Mix' or your microphone")
                
        except FileNotFoundError:
            self.audio_status.config(text="✗ FFmpeg not found!", fg="#dc2626")
            messagebox.showerror("Error", "FFmpeg not found!")
        except Exception as e:
            self.audio_status.config(text=f"✗ Error: {str(e)}", fg="#dc2626")
    
    def refresh_windows(self):
        """Get list of windows"""
        try:
            ps_cmd = 'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object -ExpandProperty MainWindowTitle'
            result = subprocess.run(['powershell', '-Command', ps_cmd],
                                  capture_output=True, text=True, timeout=10)
            
            windows = [w.strip() for w in result.stdout.split('\n') if w.strip()]
            
            if windows:
                self.window_dropdown['values'] = windows
                self.window_dropdown.current(0)
                messagebox.showinfo("Windows", f"Found {len(windows)} windows")
            else:
                messagebox.showwarning("Warning", "No windows found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get windows: {e}")
    
    def browse_output(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)
    
    def build_command(self):
        """Build FFmpeg command"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = os.path.join(self.output_dir.get(), f"recording_{timestamp}.mp4")
        
        cmd = ['ffmpeg']
        
        # Video input
        mode = self.mode_var.get()
        fps = self.fps_var.get()
        
        if mode == "desktop":
            cmd.extend(['-f', 'gdigrab', '-framerate', fps, '-i', 'desktop'])
        
        elif mode == "monitor":
            if not self.monitors:
                raise ValueError("No monitors detected")
            
            idx = self.monitor_dropdown.current()
            mon = self.monitors[idx]
            cmd.extend([
                '-f', 'gdigrab',
                '-framerate', fps,
                '-offset_x', str(mon['x']),
                '-offset_y', str(mon['y']),
                '-video_size', f"{mon['width']}x{mon['height']}",
                '-i', 'desktop'
            ])
        
        elif mode == "window":
            window = self.window_var.get()
            if not window:
                raise ValueError("Please select a window")
            cmd.extend(['-f', 'gdigrab', '-framerate', fps, '-i', f'title={window}'])
        
        # Audio input
        if self.audio_enabled.get() and self.audio_var.get():
            cmd.extend(['-f', 'dshow', '-i', f'audio={self.audio_var.get()}'])
        
        # Codec settings
        crf = self.quality_var.get().split()[0]
        cmd.extend([
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-crf', crf,
            '-pix_fmt', 'yuv420p'  # Important for compatibility!
        ])
        
        if self.audio_enabled.get() and self.audio_var.get():
            cmd.extend(['-c:a', 'aac', '-b:a', '192k'])
        
        cmd.append(output)
        
        return cmd, output
    
    def start_recording(self):
        """Start recording"""
        try:
            cmd, output = self.build_command()
            
            self.info_label.config(text=f"Saving to: {output}")
            self.status_label.config(text="🔴 Recording...", fg="#dc2626")
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal", bg="#dc2626")
            
            self.is_recording = True
            self.start_time = datetime.now()
            self.output_file = output
            
            def run():
                self.recording_process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                self.recording_process.wait()
            
            threading.Thread(target=run, daemon=True).start()
            self.update_timer()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start: {e}")
            self.reset_ui()
    
    def stop_recording(self):
        """Stop recording"""
        if self.recording_process:
            try:
                self.recording_process.stdin.write(b'q')
                self.recording_process.stdin.flush()
                self.recording_process.wait(timeout=5)
            except:
                self.recording_process.terminate()
        
        self.is_recording = False
        self.reset_ui()
        
        if os.path.exists(self.output_file):
            size = os.path.getsize(self.output_file) / (1024*1024)
            messagebox.showinfo("Success", 
                              f"Recording saved!\n\n" +
                              f"File: {os.path.basename(self.output_file)}\n" +
                              f"Size: {size:.1f} MB")
        else:
            messagebox.showerror("Error", "Recording file not created!")
    
    def reset_ui(self):
        """Reset UI after recording"""
        self.status_label.config(text="⏸️ Ready", fg="#059669")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled", bg="#6b7280")
        self.timer_label.config(text="00:00:00")
    
    def update_timer(self):
        """Update timer"""
        if self.is_recording:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

def main():
    # Check FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except:
        messagebox.showerror("Error", 
                           "FFmpeg not found!\n\n" +
                           "Download from: https://www.gyan.dev/ffmpeg/builds/")
        return
    
    root = tk.Tk()
    app = AdvancedRecorderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
