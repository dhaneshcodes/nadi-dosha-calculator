# 🚀 Quick Start - NEW Server

## Important: Use the NEW Server

You need to use `server.py` instead of `proxy-server.py` to access the calculation API.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Start the NEW Server

**Windows:**
```bash
python server.py
```

Or use the batch file:
```bash
START-NEW-SERVER.bat
```

**Mac/Linux:**
```bash
python3 server.py
```

## Step 3: Access the Application

- **Main App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## What's Different?

### OLD Server (`proxy-server.py`)
- ❌ Only proxies external APIs (Nominatim, Photon, TimeAPI)
- ❌ No calculation endpoint
- ❌ Calculations done client-side (visible in browser)

### NEW Server (`server.py`)
- ✅ Proxies external APIs (same as before)
- ✅ **NEW**: `/api/calculate-nadi` endpoint
- ✅ Calculations done server-side (protected)
- ✅ Rate limiting
- ✅ API documentation

## Troubleshooting

### "Module not found: server"

Make sure you're in the project root directory:
```bash
cd C:\nadi-dosha-calculator
python server.py
```

### "Port 8000 already in use"

Stop the old `proxy-server.py` first:
1. Press `Ctrl+C` in the terminal running `proxy-server.py`
2. Wait a few seconds
3. Run `python server.py`

### Still seeing empty network calls?

1. **Check browser console (F12)**: Look for error messages
2. **Check server terminal**: Look for error logs
3. **Verify endpoint**: Visit http://localhost:8000/docs to see API documentation
4. **Test API directly**: Use the Swagger UI at /docs to test the endpoint

### API returns 404

Make sure you're running `server.py`, not `proxy-server.py`!

## Testing the API

Open browser console (F12) and you should see:
- API request logs
- API response logs
- Any errors

If you see "API Response status: 404", you're running the old server.

