# 🚀 Quick Start Guide

## Problem: "Failed to fetch" or CORS Error?

### ❌ Wrong Way (Causes Errors):
```
Double-clicking index.html
→ Opens as file:///C:/nadi-dosha-calculator/index.html
→ CORS blocks API requests
→ "Failed to fetch" error ❌
```

### ✅ Right Way (Works Perfectly):
```
Run a local web server
→ Opens as http://localhost:8000
→ API requests work
→ No errors! ✅
```

---

## 🎯 How to Fix It

### Method 1: Using Python (Recommended)

**Windows:**
1. Open folder in File Explorer
2. Double-click `start-server.bat`
3. Browser opens automatically at http://localhost:8000

**Mac/Linux:**
1. Open Terminal in this folder
2. Run: `chmod +x start-server.sh`
3. Run: `./start-server.sh`
4. Open browser to http://localhost:8000

### Method 2: One Command

**If you have Python:**
```bash
python -m http.server 8000
```

**If you have Node.js:**
```bash
npx http-server -p 8000
```

**If you have PHP:**
```bash
php -S localhost:8000
```

Then open: **http://localhost:8000**

---

## 🤔 Why Does This Happen?

### The Technical Explanation:

1. **Browser Security**: Modern browsers implement CORS (Cross-Origin Resource Sharing) for security
2. **file:// Protocol**: When you open HTML directly, it uses `file://` protocol
3. **Blocked Requests**: Browsers block API requests from `file://` to prevent security issues
4. **http:// Protocol**: Web servers use `http://` protocol, which allows API requests

### Visual:
```
file://     →  Nominatim API  ❌ BLOCKED by CORS
http://     →  Nominatim API  ✅ ALLOWED
```

---

## 📝 Step-by-Step Instructions

### For Windows Users:

1. **Open Command Prompt or PowerShell** in this folder:
   - Right-click in the folder
   - Select "Open in Terminal" or "Open PowerShell here"

2. **Run the command:**
   ```bash
   python -m http.server 8000
   ```

3. **You'll see:**
   ```
   Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```

5. **Done!** The app will now work perfectly 🎉

### To Stop the Server:
- Press `Ctrl + C` in the terminal

---

## 💡 Pro Tips

### Keep the Server Running
- Leave the terminal window open while using the app
- Don't close the terminal or the server will stop

### Check if Server is Running
- Go to http://localhost:8000
- If you see the app, it's working!
- If you see "Unable to connect", the server isn't running

### Using a Different Port
If port 8000 is busy:
```bash
python -m http.server 9000  # Use port 9000
```
Then open http://localhost:9000

---

## 🆘 Troubleshooting

### "python is not recognized"
**Problem**: Python not installed  
**Solution**: 
1. Install Python from python.org
2. Or use another method (Node.js, PHP)

### Port Already in Use
**Problem**: Port 8000 is busy  
**Solution**: Use a different port:
```bash
python -m http.server 9000
```

### Still Getting CORS Error
**Problem**: Opening file directly instead of using server  
**Solution**: 
1. Check URL bar - should show `http://localhost:8000`
2. NOT `file:///C:/...`
3. If it shows `file://`, you need to use the server

---

## ✅ Verification Checklist

Before using the app, verify:
- [ ] Server is running (terminal shows "Serving HTTP...")
- [ ] Browser URL shows `http://localhost:8000` (NOT `file://`)
- [ ] You can see the app interface
- [ ] Console shows no CORS errors (F12 → Console tab)

If all checked ✅ → You're good to go! 🎉

---

## 🎯 Quick Test

1. Start server: `python -m http.server 8000`
2. Open: http://localhost:8000
3. Enter:
   - Date: 20-12-1998
   - Time: 14:30
   - Place: Mumbai, Maharashtra, India
4. Click "Calculate Nadi"
5. If results appear → Everything works! ✅

---

## 📚 More Help

- **Full Documentation**: See README.md
- **CORS Explained**: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- **Python Simple Server**: https://docs.python.org/3/library/http.server.html

