# ⚡ War Thunder Rangefinder - Streamlined Edition

A modern, easy-to-use overlay rangefinder for War Thunder that stays on top of your windowed game.

## ✨ Features

- **Always-on-Top Overlay** - Stays visible above your game window
- **Works with Windowed Mode** - Interact with game while rangefinder is active
- **Manual Measurement** - Click any two points to measure distance
- **Auto Yellow Marker Detection** - Automatically finds and measures squad markers
- **Simple Hotkeys** - Easy keyboard controls
- **Lightweight** - No heavy neural networks, fast and responsive
- **Clean UI** - Minimal, transparent interface

## 🚀 Quick Start

### Installation

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Python 3.8 or higher required

2. **Run Setup**
   - Double-click `setup.bat`
   - Wait for installation to complete

3. **Launch Rangefinder**
   - Double-click `run_rangefinder.bat`
   - Or run `python wt_rangefinder.py`

## 🎮 How to Use

### First Time Setup

1. **Start War Thunder** in **WINDOWED** or **BORDERLESS WINDOWED** mode
   - Settings > Graphics > Screen mode: Windowed
   
2. **Open your map** (M key by default)

3. **Press F9** to setup map corners
   - **IMPORTANT**: Hold **SHIFT+ALT** in War Thunder to show your cursor!
   - Click the **TOP-LEFT** corner of your map
   - Release and hold **SHIFT+ALT** again
   - Click the **BOTTOM-RIGHT** corner of your map
   - You only need to do this once per session!

### Measuring Distance

**Method 1: Manual Measurement (Most Accurate)**
- Press **F10**
- Hold **SHIFT+ALT** to show cursor in-game
- Click your position on the map
- Hold **SHIFT+ALT** again
- Click the target position
- Distance appears in the overlay!

**Method 2: Auto-Detect Yellow Marker**
- Place a squad marker (yellow circle) in the game
- Press **F11**
- Rangefinder automatically detects the marker and calculates distance!

### Hotkeys

| Key | Action |
|-----|--------|
| **F9** | Setup Map Corners (one-time setup) |
| **F10** | Manual 2-Point Measurement |
| **F11** | Auto-Detect Yellow Squad Marker |
| **ESC** | Cancel Current Operation |

## 📋 Configuration

### Map Size
The default map size is 65km (typical for War Thunder). If you're on a different map size:

1. Check the map size in-game (varies by battle type)
2. Enter the new size in the overlay's "Map Size (km)" field
3. Click "Update"

Common map sizes:
- **65km** - Most realistic battles
- **32km** - Some smaller maps
- **130km** - Some large EC maps

## 🎯 Tips for Best Results

### War Thunder Cursor Control
- **CRITICAL**: War Thunder hides your cursor by default
- Hold **SHIFT+ALT** to temporarily show cursor for clicking
- This is a War Thunder feature, not a rangefinder issue
- You'll need to do this each time you want to click the map

### For Manual Measurement (F10)
- Make sure to click **inside** the map area
- Click as precisely as possible on your targets
- Works with any map zoom level

### For Auto-Detection (F11)
- Works best with **bright yellow squad markers**
- Ensure good contrast between marker and map
- Assumes you are at the center of the map
- May require adjusting if player position is off-center

### Game Settings
For the best experience:
1. Use **Windowed** or **Borderless Windowed** mode
2. Enable **large minimap** (harder to misclick)
3. Increase **map zoom** for more accuracy

## 🔧 Troubleshooting

### "Python is not found"
- Install Python from python.org
- Make sure "Add Python to PATH" was checked during installation
- Restart your computer after installing

### "Module not found" errors
- Run `setup.bat` again
- Or manually: `pip install -r requirements.txt`

### Overlay not staying on top
- Make sure War Thunder is in **Windowed** mode (not fullscreen)
- Try restarting the rangefinder

### Auto-detection not finding marker
- Ensure squad marker is visible and bright yellow
- Try manual measurement (F10) instead
- Check that map corners are properly configured (F9)

### Clicks not registering
- Make sure you're clicking **inside** the map boundaries
- Verify map corners are set correctly (F9)
- Try manual measurement for more control

## 📊 Technical Details

- **Language**: Python 3
- **UI Framework**: Tkinter (built-in)
- **Image Processing**: OpenCV for marker detection
- **Dependencies**: Minimal, lightweight libraries only

## 🆚 Improvements Over Original

This streamlined version offers:

1. **No Neural Network** - Faster, lighter, simpler
2. **Always-on-Top** - Actually works with windowed games
3. **One-Click Setup** - Simple bat files, no complex configuration
4. **Better UI** - Modern, clean, easy to read
5. **Hotkey Controls** - No clicking overlay buttons
6. **Persistent** - Stays visible while gaming
7. **Flexible** - Manual + Auto modes

## ⚖️ Legal Notice

This tool is an **overlay application** that:
- Does NOT modify game files
- Does NOT inject code into the game
- Does NOT provide unfair advantages
- Only performs visual measurements on your screen

Similar to using a ruler on your monitor. Use at your own discretion.

## 🤝 Contributing

Feel free to fork, modify, and improve! This is a community tool.

## 📝 License

Free to use and modify. Created for the War Thunder community.

---

**Enjoy more accurate ranging!** 🎯
