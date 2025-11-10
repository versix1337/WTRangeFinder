# 📦 War Thunder Rangefinder - Complete Package

## 🎯 What's Included

This package contains TWO versions of the rangefinder:

### 1. **Standard Edition** (`wt_rangefinder.py`)
**Best for most users** - Simple, reliable, lightweight

Features:
- ✅ Always-on-top overlay
- ✅ Manual 2-point measurement (F10)
- ✅ Auto yellow marker detection (F11)
- ✅ Easy hotkey controls
- ✅ Works with windowed game
- ✅ Clean, simple interface

**Run with:** `run_rangefinder.bat`

---

### 2. **Pro Edition** (`wt_rangefinder_pro.py`)
**For advanced users** - Extra features and flexibility

All Standard features PLUS:
- ⭐ **Click-through mode (F12)** - Overlay becomes transparent to clicks
- ⭐ **Auto-scan mode (F8)** - Automatically scans for markers every 3s
- ⭐ More transparent overlay options
- ⭐ Real-time scanning display

**Run with:** `run_rangefinder_pro.bat`

---

## 🚀 Installation (First Time)

1. **Install Python** (if needed)
   - Download: https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during install!
   - Minimum version: Python 3.8

2. **Run Setup**
   ```
   Double-click: setup.bat
   ```
   Wait for it to complete (installs required packages)

3. **Done!** You're ready to use either version

---

## 🎮 Quick Usage Guide

### First-Time Setup (Do This Once)

1. **Launch War Thunder in WINDOWED mode**
   - Settings → Graphics → Screen Mode: **Windowed**
   
2. **Start rangefinder**
   - Standard: Double-click `run_rangefinder.bat`
   - Pro: Double-click `run_rangefinder_pro.bat`

3. **Configure map (F9)**
   - Open map in-game (M)
   - Press F9
   - Click TOP-LEFT corner of map
   - Click BOTTOM-RIGHT corner of map
   - ✓ Done! (only do this once per session)

### Using The Rangefinder

**Manual Mode (Most Accurate)**
1. Press **F10**
2. Click your position
3. Click target position
4. Distance shows in overlay

**Auto Mode (Fastest)**
1. Place yellow squad marker
2. Press **F11** (or F8 for auto-scan in Pro)
3. Distance calculated automatically

---

## 📁 File Structure

```
WT_Rangefinder/
├── wt_rangefinder.py          # Standard version
├── wt_rangefinder_pro.py      # Pro version with extras
├── requirements.txt            # Python dependencies
├── setup.bat                   # One-time installation
├── run_rangefinder.bat         # Run standard version
├── run_rangefinder_pro.bat    # Run pro version
├── build_exe.bat              # Build standalone .exe (optional)
├── README.md                   # Full documentation
├── QUICKSTART.md              # Quick reference guide
└── PACKAGE_INFO.md            # This file
```

---

## ⌨️ Hotkey Reference

### Standard Edition
| Key | Action |
|-----|--------|
| F9  | Setup map corners |
| F10 | Manual 2-point measure |
| F11 | Auto-detect yellow marker |
| ESC | Cancel operation |

### Pro Edition (All above PLUS)
| Key | Action |
|-----|--------|
| F12 | Toggle click-through mode |
| F8  | Toggle auto-scan (3s intervals) |

---

## 💡 Which Version Should I Use?

### Use **Standard** if you:
- Want simplicity
- Prefer manual control
- Don't need auto-scanning
- Want lowest resource usage

### Use **Pro** if you:
- Want click-through overlay
- Need auto-scanning
- Want maximum flexibility
- Don't mind slightly more complexity

**Can't decide?** Start with Standard - it does everything you need!

---

## 🔧 Advanced: Building Standalone .exe

Don't want to install Python on target computer? Build a standalone executable:

```
Double-click: build_exe.bat
```

This creates `dist/WT_Rangefinder.exe` that runs without Python installed!

---

## 📊 Comparison Table

| Feature | Standard | Pro |
|---------|----------|-----|
| Always-on-top | ✅ | ✅ |
| Manual measurement | ✅ | ✅ |
| Auto yellow marker | ✅ | ✅ |
| Simple hotkeys | ✅ | ✅ |
| **Click-through mode** | ❌ | ✅ |
| **Auto-scan mode** | ❌ | ✅ |
| **Adjustable transparency** | ❌ | ✅ |
| Resource usage | Lowest | Low |

---

## 🆚 Improvements Over Original Repository

### What's Better:

1. ✅ **Actually works as overlay** - Stays on top of windowed game
2. ✅ **No neural network** - Faster, lighter, simpler
3. ✅ **One-click setup** - Just run `setup.bat`
4. ✅ **Modern UI** - Clean, readable interface
5. ✅ **Hotkey controls** - No need to click overlay buttons
6. ✅ **Better documentation** - Clear instructions
7. ✅ **Two versions** - Standard for simplicity, Pro for features
8. ✅ **Windows optimized** - Native Windows integration
9. ✅ **Click-through mode** (Pro) - True overlay experience
10. ✅ **Auto-scan** (Pro) - Continuous monitoring

### Technical Improvements:

- **Lighter**: No YOLOv5, uses simple HSV color detection
- **Faster**: Real-time processing, no model inference
- **Simpler**: Standard Python libs, easy to modify
- **More reliable**: Direct pixel measurement, no training needed
- **Better UX**: Always-visible overlay with transparency

---

## ❓ Troubleshooting

### "Python not found"
- Install Python from python.org
- Must check "Add Python to PATH"
- Restart computer after install

### Overlay disappears behind game
- Make sure War Thunder is in **WINDOWED** mode (not fullscreen)
- Try running as administrator

### Auto-detection not working
- Ensure yellow marker is bright and visible
- Reconfigure map corners (F9)
- Use manual mode (F10) as alternative

### Click-through mode issues (Pro only)
- Only works on Windows
- Make sure you've updated the window after toggling
- Press F12 again to disable if stuck

---

## 📝 Tips & Best Practices

### For Best Accuracy:
1. Use **larger map zoom** in-game
2. Configure corners precisely (F9)
3. Use **manual mode (F10)** for critical shots
4. Update map size if on different map

### For Best Performance:
1. Use **Standard version** if you don't need extras
2. Disable auto-scan when not needed (Pro)
3. Close other overlays
4. Use windowed mode, not borderless windowed

### For Best Experience:
1. Position overlay where it doesn't block important UI
2. Learn the hotkeys - much faster than clicking
3. Reconfigure corners if you change resolution
4. Use click-through mode (Pro) for full immersion

---

## ⚖️ Legal & Fair Play

This tool:
- ✅ Does NOT modify game files
- ✅ Does NOT inject code
- ✅ Does NOT provide unfair advantages
- ✅ Only reads your screen (like a ruler)

**It's an overlay application** similar to Discord overlay, FPS counters, etc.

However:
- ⚠️ Use at your own discretion
- ⚠️ Check game/server rules
- ⚠️ Some servers may have overlay policies

---

## 🤝 Support & Community

### Need Help?
1. Read `QUICKSTART.md` for quick answers
2. Check `README.md` for detailed info
3. Review troubleshooting section above

### Want to Contribute?
- Feel free to modify and improve!
- Share your enhancements
- Report bugs or suggestions

---

## 📄 License

Free and open source. Created for the War Thunder community.
Use, modify, and distribute freely.

---

**Enjoy better ranging!** 🎯

*Remember: The most important thing is having fun. Use this tool to enhance your gameplay, not to replace skill development!*
