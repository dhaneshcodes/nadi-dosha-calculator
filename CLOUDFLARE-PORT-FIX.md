# 🔧 Cloudflare Port Configuration

## Issue
- Cloudflare proxy routes to **port 80** by default
- Your server runs on **port 8000**

## Solution Options

### Option 1: Change Server to Port 80 (Recommended - Simplest)

Update `server.py`:
```python
PORT = 80  # Change from 8000 to 80
```

**Note:** Port 80 requires root/admin privileges. The server might already be running as root.

### Option 2: Use Cloudflare Workers (Advanced)

Create a Cloudflare Worker to route to port 8000.

### Option 3: Use Nginx Reverse Proxy (Best Practice)

Set up Nginx on port 80, proxy to Python server on 8000.

## Quick Fix: Change Server Port

Since you're running as root, just change the port:

```python
# In server.py, line 207
PORT = 80  # Instead of 8000
```

Then restart the server.

