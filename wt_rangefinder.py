"""
War Thunder Rangefinder - Streamlined Edition
Always-on-top overlay for measuring distances on the map
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

@dataclass
class MapConfig:
    """Configuration for map measurements"""
    top_left: Optional[Tuple[int, int]] = None
    bottom_right: Optional[Tuple[int, int]] = None
    map_size_km: float = 65.0  # Default War Thunder map size in km
    grid_size_km: float = 2.0  # Size of one grid square in km
    grid_pixel_size: Optional[float] = None  # Measured pixel size of one grid square

    @property
    def is_configured(self) -> bool:
        return self.top_left is not None and self.bottom_right is not None

    @property
    def is_grid_measured(self) -> bool:
        return self.grid_pixel_size is not None

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
        """Convert pixel distance to kilometers"""
        if not self.is_configured:
            return 0
        avg_dimension = (self.width + self.height) / 2
        return (pixel_distance / avg_dimension) * self.map_size_km

    def auto_calculate_map_size(self) -> Optional[float]:
        """Auto-calculate map size based on grid measurements"""
        if not self.is_configured or not self.is_grid_measured:
            return None

        # Calculate average map dimension in pixels
        avg_dimension = (self.width + self.height) / 2

        # Calculate number of grid squares that fit in the map
        num_grids = avg_dimension / self.grid_pixel_size

        # Calculate total map size
        return num_grids * self.grid_size_km


class RangefinderOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WT Rangefinder")
        self.root.attributes('-topmost', True)  # Always on top
        self.root.attributes('-alpha', 0.9)  # Slight transparency
        self.root.overrideredirect(False)  # Keep window frame for easy moving
        
        # Configuration
        self.config = MapConfig()
        self.is_measuring = False
        self.detection_enabled = False
        self.measuring_points = []
        
        # Style
        self.setup_ui()
        self.setup_hotkeys()
        
        # Position window in top-right corner
        self.root.geometry('320x330+{}+50'.format(self.root.winfo_screenwidth() - 370))
        
    def setup_ui(self):
        """Create the UI elements"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="⚡ WT Rangefinder", 
                         font=('Segoe UI', 14, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Distance display
        self.distance_var = tk.StringVar(value="---")
        distance_frame = ttk.LabelFrame(main_frame, text="Distance", padding="10")
        distance_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        distance_label = ttk.Label(distance_frame, textvariable=self.distance_var,
                                   font=('Consolas', 24, 'bold'), 
                                   foreground='#00ff00')
        distance_label.pack()
        
        # Status
        self.status_var = tk.StringVar(value="Press F9 to setup map")
        status_label = ttk.Label(main_frame, textvariable=self.status_var,
                                font=('Segoe UI', 9), wraplength=280)
        status_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Controls frame
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        controls_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        controls_text = """F6  - Measure Grid Square
F9  - Setup Map Corners
F10 - Manual Measure (2 clicks)
F11 - Auto Detect Yellow Mark
ESC - Cancel Operation

TIP: Hold SHIFT+ALT in-game to
     show cursor for clicking!"""
        
        controls_label = ttk.Label(controls_frame, text=controls_text,
                                  font=('Consolas', 8), justify=tk.LEFT)
        controls_label.pack(anchor=tk.W)
        
        # Grid size config
        grid_frame = ttk.Frame(main_frame)
        grid_frame.grid(row=4, column=0, columnspan=2, pady=5)

        ttk.Label(grid_frame, text="Grid Size (km):",
                 font=('Segoe UI', 9)).grid(row=0, column=0, padx=5)

        self.grid_size_var = tk.StringVar(value="2.0")
        grid_size_entry = ttk.Entry(grid_frame, textvariable=self.grid_size_var,
                                    width=8, font=('Consolas', 9))
        grid_size_entry.grid(row=0, column=1, padx=5)

        grid_update_btn = ttk.Button(grid_frame, text="Update",
                                     command=self.update_grid_size, width=8)
        grid_update_btn.grid(row=0, column=2, padx=5)

        # Map size config
        config_frame = ttk.Frame(main_frame)
        config_frame.grid(row=5, column=0, columnspan=2, pady=5)

        ttk.Label(config_frame, text="Map Size (km):",
                 font=('Segoe UI', 9)).grid(row=0, column=0, padx=5)

        self.map_size_var = tk.StringVar(value="65.0")
        map_size_entry = ttk.Entry(config_frame, textvariable=self.map_size_var,
                                   width=8, font=('Consolas', 9))
        map_size_entry.grid(row=0, column=1, padx=5)

        update_btn = ttk.Button(config_frame, text="Update",
                               command=self.update_map_size, width=8)
        update_btn.grid(row=0, column=2, padx=5)
        
    def setup_hotkeys(self):
        """Setup global hotkeys"""
        keyboard.add_hotkey('f6', self.measure_grid)
        keyboard.add_hotkey('f9', self.setup_map_corners)
        keyboard.add_hotkey('f10', self.manual_measure)
        keyboard.add_hotkey('f11', self.auto_detect_marker)
        keyboard.add_hotkey('esc', self.cancel_operation)
        
    def update_status(self, message: str):
        """Update status message"""
        self.status_var.set(message)
        self.root.update()
        
    def update_map_size(self):
        """Update the map size configuration"""
        try:
            new_size = float(self.map_size_var.get())
            if new_size > 0:
                self.config.map_size_km = new_size
                self.update_status(f"Map size updated to {new_size} km")
            else:
                self.update_status("Error: Map size must be positive")
        except ValueError:
            self.update_status("Error: Invalid map size value")

    def update_grid_size(self):
        """Update the grid size configuration"""
        try:
            new_size = float(self.grid_size_var.get())
            if new_size > 0:
                self.config.grid_size_km = new_size
                self.update_status(f"Grid size updated to {new_size} km")
            else:
                self.update_status("Error: Grid size must be positive")
        except ValueError:
            self.update_status("Error: Invalid grid size value")

    def measure_grid(self):
        """Measure a single grid square to calibrate map size"""
        if self.is_measuring:
            return

        self.is_measuring = True
        self.measuring_points = []
        self.update_status("Press SHIFT+ALT, click two adjacent grid corners...")

        def on_click(x, y, button, pressed):
            if not pressed:
                return

            self.measuring_points.append((x, y))

            if len(self.measuring_points) == 1:
                self.update_status(f"✓ First corner set!\nPress SHIFT+ALT, click second corner...")
            elif len(self.measuring_points) == 2:
                # Calculate pixel distance between grid corners
                p1, p2 = self.measuring_points
                pixel_dist = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                self.config.grid_pixel_size = pixel_dist
                self.is_measuring = False
                self.update_status(f"✓ Grid measured: {pixel_dist:.1f} pixels = {self.config.grid_size_km} km")
                return False  # Stop listener

        from pynput import mouse
        listener = mouse.Listener(on_click=on_click)
        listener.start()
    
    def setup_map_corners(self):
        """Setup map corner coordinates"""
        if self.is_measuring:
            return

        self.is_measuring = True
        self.measuring_points = []
        self.update_status("Press SHIFT+ALT, then click TOP-LEFT corner...")

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

                # Auto-calculate map size if grid was measured
                if self.config.is_grid_measured:
                    auto_size = self.config.auto_calculate_map_size()
                    if auto_size:
                        self.config.map_size_km = auto_size
                        self.map_size_var.set(f"{auto_size:.1f}")
                        self.update_status(f"✓ Map configured! Auto-calculated size: {auto_size:.1f} km\nDimensions: {self.config.width}x{self.config.height}px")
                    else:
                        self.update_status(f"✓ Map configured!\nSize: {self.config.width}x{self.config.height}px")
                else:
                    self.update_status(f"✓ Map configured!\nSize: {self.config.width}x{self.config.height}px\nTIP: Use F6 first for auto-calculation")

                return False  # Stop listener

        from pynput import mouse
        listener = mouse.Listener(on_click=on_click)
        listener.start()
    
    def manual_measure(self):
        """Manual two-point measurement"""
        if not self.config.is_configured:
            self.update_status("⚠ Setup map corners first (F9)")
            return
        
        if self.is_measuring:
            return
        
        self.is_measuring = True
        self.measuring_points = []
        self.update_status("Press SHIFT+ALT, click FIRST point...")
        
        def on_click(x, y, button, pressed):
            if not pressed:
                return
            
            # Check if click is within map bounds
            if not (self.config.top_left[0] <= x <= self.config.bottom_right[0] and
                    self.config.top_left[1] <= y <= self.config.bottom_right[1]):
                self.update_status("⚠ Click inside the map area!")
                return
            
            self.measuring_points.append((x, y))
            
            if len(self.measuring_points) == 1:
                self.update_status(f"✓ Point 1 set!\nPress SHIFT+ALT, click SECOND point...")
            elif len(self.measuring_points) == 2:
                self.calculate_distance()
                self.is_measuring = False
                return False  # Stop listener
        
        from pynput import mouse
        listener = mouse.Listener(on_click=on_click)
        listener.start()
    
    def calculate_distance(self):
        """Calculate distance between two points"""
        if len(self.measuring_points) != 2:
            return
        
        p1, p2 = self.measuring_points
        
        # Calculate pixel distance
        pixel_dist = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        
        # Convert to kilometers
        km_dist = self.config.pixels_to_km(pixel_dist)
        
        # Convert to meters
        meters_dist = km_dist * 1000
        
        # Update display
        if meters_dist >= 1000:
            self.distance_var.set(f"{km_dist:.2f} km")
        else:
            self.distance_var.set(f"{int(meters_dist)} m")
        
        self.update_status(f"✓ Distance calculated!")
    
    def auto_detect_marker(self):
        """Auto-detect yellow squad marker using color detection"""
        if not self.config.is_configured:
            self.update_status("⚠ Setup map corners first (F9)")
            return
        
        self.update_status("🔍 Scanning for yellow marker...")
        
        # Capture map area
        screenshot = ImageGrab.grab(bbox=(
            self.config.top_left[0],
            self.config.top_left[1],
            self.config.bottom_right[0],
            self.config.bottom_right[1]
        ))
        
        # Convert to OpenCV format
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Yellow color range for War Thunder markers
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([35, 255, 255])
        
        # Create mask
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            self.update_status("❌ No yellow marker detected")
            self.distance_var.set("---")
            return
        
        # Get largest contour (likely the marker)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get marker center
        M = cv2.moments(largest_contour)
        if M["m00"] == 0:
            self.update_status("❌ Could not locate marker center")
            return
        
        marker_x = int(M["m10"] / M["m00"])
        marker_y = int(M["m01"] / M["m00"])
        
        # Player is typically at center of map
        player_x = self.config.width // 2
        player_y = self.config.height // 2
        
        # Calculate distance
        pixel_dist = np.sqrt((marker_x - player_x)**2 + (marker_y - player_y)**2)
        km_dist = self.config.pixels_to_km(pixel_dist)
        meters_dist = km_dist * 1000
        
        # Update display
        if meters_dist >= 1000:
            self.distance_var.set(f"{km_dist:.2f} km")
        else:
            self.distance_var.set(f"{int(meters_dist)} m")
        
        self.update_status(f"✓ Marker detected at ({marker_x}, {marker_y})")
    
    def cancel_operation(self):
        """Cancel current operation"""
        self.is_measuring = False
        self.measuring_points = []
        self.update_status("Operation cancelled")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    print("=" * 50)
    print("War Thunder Rangefinder - Streamlined Edition")
    print("=" * 50)
    print("\nFeatures:")
    print("- Always-on-top overlay")
    print("- Manual 2-point measurement")
    print("- Auto yellow marker detection")
    print("- Easy hotkey controls")
    print("\nStarting overlay...")
    
    app = RangefinderOverlay()
    app.run()


if __name__ == "__main__":
    main()
