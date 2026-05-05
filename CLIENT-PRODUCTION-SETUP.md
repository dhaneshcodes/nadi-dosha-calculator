# ✅ Client-Side Production Setup

## Changes Made

The client-side code (`script.js`) has been updated to automatically use the production API server when hosted on GitHub Pages.

## How It Works

### API Base URL Configuration

A new constant `API_BASE_URL` automatically detects the environment:

```javascript
const API_BASE_URL = (() => {
  const hostname = window.location.hostname;
  const isLocal = hostname === 'localhost' || 
                 hostname === '127.0.0.1' ||
                 window.location.protocol === 'file:';
  
  // Production API server
  const PRODUCTION_API = 'http://159.89.161.170:8000';
  
  // Use production API when not on localhost (e.g., GitHub Pages)
  return isLocal ? '' : PRODUCTION_API;
})();
```

### Behavior

- **On localhost** (`localhost`, `127.0.0.1`, or `file://`):
  - Uses relative URLs (e.g., `/api/calculate-nadi-complete`)
  - Assumes local server is running on same port
  - Works with `python server.py` for local development

- **On GitHub Pages** (or any other domain):
  - Uses production API: `http://159.89.161.170:8000`
  - All API calls go to the live server
  - No code changes needed when deploying

## Updated API Endpoints

All API calls now use `API_BASE_URL`:

1. **Main Calculation Endpoint**
   ```javascript
   fetch(`${API_BASE_URL}/api/calculate-nadi-complete`, ...)
   ```

2. **Geocoding Endpoints**
   ```javascript
   // Self-hosted geocode API
   `${API_BASE_URL}/api/geocode?city=...`
   
   // Photon API proxy
   `${API_BASE_URL}/api/photon?q=...`
   
   // Nominatim API proxy
   `${API_BASE_URL}/api/nominatim?q=...`
   ```

3. **Legacy Calculation Endpoint** (if used)
   ```javascript
   fetch(`${API_BASE_URL}/api/calculate-nadi`, ...)
   ```

## Testing

### Local Development
1. Start local server: `python server.py`
2. Open: `http://localhost:8000`
3. Check console: Should see `API Configuration: Local (localhost)`
4. API calls use relative URLs

### Production (GitHub Pages)
1. Deploy to GitHub Pages
2. Open your GitHub Pages URL
3. Check console: Should see `API Configuration: Production → http://159.89.161.170:8000`
4. API calls go to production server

## Console Logging

The app now logs which API configuration is being used:

```
🌐 API Configuration: Production → http://159.89.161.170:8000
```

or

```
🌐 API Configuration: Local (localhost)
```

## CORS Configuration

The production server (`159.89.161.170:8000`) has CORS configured to allow requests from any origin:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This means:
- ✅ GitHub Pages can call the API
- ✅ Any domain can call the API
- ✅ No CORS errors

## Deployment Checklist

- [x] API base URL configuration added
- [x] All API endpoints updated to use `API_BASE_URL`
- [x] Console logging for debugging
- [x] CORS configured on server
- [x] Production server is live at `159.89.161.170:8000`

## Next Steps

1. **Commit and Push** the updated `script.js` to GitHub
2. **GitHub Pages** will automatically deploy
3. **Test** the live site - it should now use the production API

## Troubleshooting

### API calls failing on GitHub Pages

1. **Check browser console** (F12):
   - Look for CORS errors
   - Check if `API_BASE_URL` is set correctly
   - Verify API endpoint URLs

2. **Check network tab**:
   - Requests should go to `http://159.89.161.170:8000`
   - Status should be 200 OK

3. **Verify server is running**:
   ```bash
   curl http://159.89.161.170:8000/api/health
   ```

### Still using localhost API

- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Check console for API configuration log

## Summary

✅ **Client code updated** to use production API automatically  
✅ **No manual configuration needed** - works on both localhost and GitHub Pages  
✅ **CORS configured** on server for cross-origin requests  
✅ **Ready for deployment** - just push to GitHub!

