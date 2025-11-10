"""
War Thunder Rangefinder - Advanced Edition
Includes click-through overlay mode for maximum game interaction
"""

import tkinter as tk
from tkinter import ttk
import pyautogui
import numpy as np
from PIL import Image, ImageGrab, ImageTk
import cv2
import keyboard
import threading
import time
from dataclasses import dataclass
from typing import Optional, Tuple
import sys
import ctypes
from ctypes import wintypes

# Windows API for click-through window
try:
    user32 = ctypes.windll.user32
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    WS_EX_TRANSPARENT = 0x00000020
    
    def make_click_through(hwnd):
        """Make window click-through on Windows"""
        style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT)
    
    def remove_click_through(hwnd):
        """Remove click-through from window"""
        style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style & ~WS_EX_TRANSPARENT)
except:
    def make_click_through(hwnd): pass
    def remove_click_through(hwnd): pass


@dataclass
class MapConfig:
    """Configuration for map measurements"""
    top_left: Optional[Tuple[int, int]] = None
    bottom_right: Optional[Tuple[int, int]] = None
    map_size_km: float = 65.0
    
    @property
    def is_configured(self) -> bool:
        return self.top_left is not None and self.bottom_right is not None
    
    @property
    def width(self) -> int:
        if not self.is_configured:
            return 0
        return self.bottom_right[0] - self.top_left[0]
    
    @property
    def height(self) -> int:
        if not self.is_configured:
            return 0
        return self.bottom_right[1] - self.top_left[1]
    
    def pixels_to_km(self, pixel_distance: float) -> float:
        if not self.is_configured:
            return 0
        avg_dimension = (self.width + self.height) / 2
        return (pixel_distance / avg_dimension) * self.map_size_km


class AdvancedRangefinderOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WT Rangefinder Pro")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.85)
        self.root.overrideredirect(False)
        
        self.config = MapConfig()
        self.is_measuring = False
        self.measuring_points = []
        self.click_through_mode = False
        self.auto_scan_enabled = False
        self.scan_thread = None
        
        self.setup_ui()
        self.setup_hotkeys()
        
        # Position window
        self.root.geometry('360x320+{}+50'.format(self.root.winfo_screenwidth() - 410))
        
        # Get window handle for click-through
        self.root.update()
        self.hwnd = None
        try:
            self.hwnd = int(self.root.frame(), 16)
        except:
            pass
    
    def setup_ui(self):
        """Create UI elements"""
        style = ttk.Style()
        style.theme_use('clam')
        
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title with mode indicator
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        title = ttk.Label(title_frame, text="⚡ WT Rangefinder Pro", 
                         font=('Segoe UI', 13, 'bold'))
        title.pack()
        
        self.mode_var = tk.StringVar(value="Normal Mode")
        mode_label = ttk.Label(title_frame, textvariable=self.mode_var,
                              font=('Segoe UI', 8), foreground='#888')
        mode_label.pack()
        
        # Distance display
        self.distance_var = tk.StringVar(value="---")
        distance_frame = ttk.LabelFrame(main_frame, text="Distance", padding="10")
        distance_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        distance_label = ttk.Label(distance_frame, textvariable=self.distance_var,
                                   font=('Consolas', 22, 'bold'), 
                                   foreground='#00ff00')
        distance_label.pack()
        
        # Status
        self.status_var = tk.StringVar(value="Press F9 to setup map")
        status_label = ttk.Label(main_frame, textvariable=self.status_var,
                                font=('Segoe UI', 8), wraplength=320)
        status_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Controls
        controls_frame = ttk.LabelFrame(main_frame, text="Hotkeys", padding="8")
        controls_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        controls_text = """F9  - Setup Map      F12 - Click-Through Mode
F10 - Manual Measure F8  - Toggle Auto-Scan
F11 - Detect Marker  ESC - Cancel

TIP: Use SHIFT+ALT in-game to show cursor!"""
        
        controls_label = ttk.Label(controls_frame, text=controls_text,
                                  font=('Consolas', 7), justify=tk.LEFT)
        controls_label.pack(anchor=tk.W)
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="8")
        options_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Map size
        size_frame = ttk.Frame(options_frame)
        size_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(size_frame, text="Map Size:", 
                 font=('Segoe UI', 8)).pack(side=tk.LEFT, padx=2)
        
        self.map_size_var = tk.StringVar(value="65.0")
        map_size_entry = ttk.Entry(size_frame, textvariable=self.map_size_var,
                                   width=6, font=('Consolas', 8))
        map_size_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(size_frame, text="km", 
                 font=('Segoe UI', 8)).pack(side=tk.LEFT)
        
        ttk.Button(size_frame, text="Set", command=self.update_map_size,
                  width=5).pack(side=tk.RIGHT, padx=2)
        
        # Auto-scan toggle
        self.auto_scan_var = tk.BooleanVar(value=False)
        auto_check = ttk.Checkbutton(options_frame, text="Auto-scan yellow marker (F8)",
                                     variable=self.auto_scan_var,
                                     command=self.toggle_auto_scan)
        auto_check.pack(anchor=tk.W, pady=2)
        
    def setup_hotkeys(self):
        """Setup hotkeys"""
        keyboard.add_hotkey('f9', self.setup_map_corners)
        keyboard.add_hotkey('f10', self.manual_measure)
        keyboard.add_hotkey('f11', self.auto_detect_marker)
        keyboard.add_hotkey('f12', self.toggle_click_through)
        keyboard.add_hotkey('f8', self.toggle_auto_scan)
        keyboard.add_hotkey('esc', self.cancel_operation)
    
    def toggle_click_through(self):
        """Toggle click-through mode"""
        if not self.hwnd:
            self.update_status("⚠ Click-through not available")
            return
        
        self.click_through_mode = not self.click_through_mode
        
        if self.click_through_mode:
            make_click_through(self.hwnd)
            self.mode_var.set("🖱️ Click-Through Mode")
            self.update_status("✓ Click-through enabled - Press F12 to disable")
            self.root.attributes('-alpha', 0.6)  # More transparent
        else:
            remove_click_through(self.hwnd)
            self.mode_var.set("Normal Mode")
            self.update_status("Click-through disabled")
            self.root.attributes('-alpha', 0.85)
    
    def toggle_auto_scan(self):
        """Toggle automatic scanning"""
        self.auto_scan_enabled = not self.auto_scan_enabled
        self.auto_scan_var.set(self.auto_scan_enabled)
        
        if self.auto_scan_enabled:
            self.update_status("🔄 Auto-scan enabled (every 3s)")
            self.start_auto_scan()
        else:
            self.update_status("Auto-scan disabled")
            self.stop_auto_scan()
    
    def start_auto_scan(self):
        """Start auto-scanning thread"""
        if self.scan_thread and self.scan_thread.is_alive():
            return
        
        def scan_loop():
            while self.auto_scan_enabled:
                if self.config.is_configured and not self.is_measuring:
                    self.auto_detect_marker()
                time.sleep(3)
        
        self.scan_thread = threading.Thread(target=scan_loop, daemon=True)
        self.scan_thread.start()
    
    def stop_auto_scan(self):
        """Stop auto-scanning"""
        self.auto_scan_enabled = False
        if self.scan_thread:
            self.scan_thread.join(timeout=1)
    
    def update_status(self, message: str):
        """Update status"""
        self.status_var.set(message)
        self.root.update()
    
    def update_map_size(self):
        """Update map size"""
        try:
            new_size = float(self.map_size_var.get())
            if new_size > 0:
                self.config.map_size_km = new_size
                self.update_status(f"✓ Map size: {new_size} km")
            else:
                self.update_status("⚠ Invalid map size")
        except ValueError:
            self.update_status("⚠ Invalid map size")
    
    def setup_map_corners(self):
        """Setup map corners"""
        if self.is_measuring:
            return
        
        # Temporarily disable click-through
        was_click_through = self.click_through_mode
        if was_click_through:
            self.toggle_click_through()
        
        self.is_measuring = True
        self.measuring_points = []
        self.update_status("Press SHIFT+ALT, click TOP-LEFT...")
        
        def on_click(x, y, button, pressed):
            if not pressed:
                return
            
            self.measuring_points.append((x, y))
            
            if len(self.measuring_points) == 1:
                self.update_status(f"✓ Top-left set!\nPress SHIFT+ALT, click BOTTOM-RIGHT...")
            elif len(self.measuring_points) == 2:
                self.config.top_left = self.measuring_points[0]
                self.config.bottom_right = self.measuring_points[1]
                self.is_measuring = False
                self.update_status(f"✓ Map configured: {self.config.width}x{self.config.height}px")
                
                # Re-enable click-through if it was on
                if was_click_through:
                    self.root.after(500, self.toggle_click_through)
                
                return False
        
        from pynput import mouse
        listener = mouse.Listener(on_click=on_click)
        listener.start()
    
    def manual_measure(self):
        """Manual measurement"""
        if not self.config.is_configured:
            self.update_status("⚠ Setup map first (F9)")
            return
        
        if self.is_measuring:
            return
        
        # Temporarily disable click-through
        was_click_through = self.click_through_mode
        if was_click_through:
            self.toggle_click_through()
        
        self.is_measuring = True
        self.measuring_points = []
        self.update_status("Press SHIFT+ALT, click FIRST point...")
        
        def on_click(x, y, button, pressed):
            if not pressed:
                return
            
            if not (self.config.top_left[0] <= x <= self.config.bottom_right[0] and
                    self.config.top_left[1] <= y <= self.config.bottom_right[1]):
                self.update_status("⚠ Click inside map!")
                return
            
            self.measuring_points.append((x, y))
            
            if len(self.measuring_points) == 1:
                self.update_status(f"✓ Point 1 set!\nPress SHIFT+ALT, click SECOND point...")
            elif len(self.measuring_points) == 2:
                self.calculate_distance()
                self.is_measuring = False
                
                # Re-enable click-through if it was on
                if was_click_through:
                    self.root.after(500, self.toggle_click_through)
                
                return False
        
        from pynput import mouse
        listener = mouse.Listener(on_click=on_click)
        listener.start()
    
    def calculate_distance(self):
        """Calculate distance"""
        if len(self.measuring_points) != 2:
            return
        
        p1, p2 = self.measuring_points
        pixel_dist = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        km_dist = self.config.pixels_to_km(pixel_dist)
        meters_dist = km_dist * 1000
        
        if meters_dist >= 1000:
            self.distance_var.set(f"{km_dist:.2f} km")
        else:
            self.distance_var.set(f"{int(meters_dist)} m")
        
        self.update_status(f"✓ Distance: {int(meters_dist)}m")
    
    def auto_detect_marker(self):
        """Auto-detect yellow marker"""
        if not self.config.is_configured:
            if not self.auto_scan_enabled:
                self.update_status("⚠ Setup map first (F9)")
            return
        
        if not self.auto_scan_enabled:
            self.update_status("🔍 Scanning...")
        
        try:
            screenshot = ImageGrab.grab(bbox=(
                self.config.top_left[0],
                self.config.top_left[1],
                self.config.bottom_right[0],
                self.config.bottom_right[1]
            ))
            
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([35, 255, 255])
            
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                if not self.auto_scan_enabled:
                    self.update_status("❌ No marker found")
                    self.distance_var.set("---")
                return
            
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M["m00"] == 0:
                return
            
            marker_x = int(M["m10"] / M["m00"])
            marker_y = int(M["m01"] / M["m00"])
            
            player_x = self.config.width // 2
            player_y = self.config.height // 2
            
            pixel_dist = np.sqrt((marker_x - player_x)**2 + (marker_y - player_y)**2)
            km_dist = self.config.pixels_to_km(pixel_dist)
            meters_dist = km_dist * 1000
            
            if meters_dist >= 1000:
                self.distance_var.set(f"{km_dist:.2f} km")
            else:
                self.distance_var.set(f"{int(meters_dist)} m")
            
            if not self.auto_scan_enabled:
                self.update_status(f"✓ Marker found: {int(meters_dist)}m")
                
        except Exception as e:
            if not self.auto_scan_enabled:
                self.update_status(f"❌ Error: {str(e)[:30]}")
    
    def cancel_operation(self):
        """Cancel operation"""
        self.is_measuring = False
        self.measuring_points = []
        self.update_status("Operation cancelled")
    
    def run(self):
        """Start application"""
        self.root.mainloop()


def main():
    print("=" * 60)
    print("War Thunder Rangefinder - Advanced Edition")
    print("=" * 60)
    print("\nFeatures:")
    print("✓ Always-on-top overlay")
    print("✓ Click-through mode (F12)")
    print("✓ Auto-scan yellow markers (F8)")
    print("✓ Manual measurement")
    print("✓ Lightweight and fast")
    print("\nStarting...")
    
    app = AdvancedRangefinderOverlay()
    app.run()


if __name__ == "__main__":
    main()
