#!/usr/bin/env python3
"""
Simple CORS Proxy Server for Nominatim API
Solves 403 Forbidden and CORS issues on localhost

Usage: python proxy-server.py
Then open: http://localhost:8000
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import urllib.parse
import json
import time

class CORSProxyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # Check if this is an API proxy request
        if self.path.startswith('/api/nominatim'):
            self.proxy_nominatim()
        elif self.path.startswith('/api/photon'):
            self.proxy_photon()
        elif self.path.startswith('/api/timeapi'):
            self.proxy_timeapi()
        else:
            # Serve static files normally
            super().do_GET()

    def proxy_nominatim(self):
        """Proxy requests to Nominatim API"""
        try:
            # Extract query from path
            query = self.path.replace('/api/nominatim?', '')
            
            # Build Nominatim URL
            nominatim_url = f'https://nominatim.openstreetmap.org/search?{query}'
            
            # Make request with proper headers
            req = urllib.request.Request(
                nominatim_url,
                headers={
                    'User-Agent': 'NadiDoshaCalculator/1.0 (Educational Purpose)',
                    'Accept': 'application/json'
                }
            )
            
            # Add rate limiting (1 request per second)
            time.sleep(1)
            
            # Get response
            with urllib.request.urlopen(req) as response:
                data = response.read()
                
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(data)
            
        except Exception as e:
            self.send_error(500, f'Proxy error: {str(e)}')

    def proxy_photon(self):
        """Proxy requests to Photon API"""
        try:
            query = self.path.replace('/api/photon?', '')
            photon_url = f'https://photon.komoot.io/api/?{query}'
            
            req = urllib.request.Request(photon_url)
            with urllib.request.urlopen(req) as response:
                data = response.read()
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(data)
            
        except Exception as e:
            self.send_error(500, f'Proxy error: {str(e)}')

    def proxy_timeapi(self):
        """Proxy requests to TimeAPI"""
        try:
            query = self.path.replace('/api/timeapi?', '')
            timeapi_url = f'https://timeapi.io/api/TimeZone/coordinate?{query}'
            
            req = urllib.request.Request(timeapi_url)
            with urllib.request.urlopen(req) as response:
                data = response.read()
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(data)
            
        except Exception as e:
            self.send_error(500, f'Proxy error: {str(e)}')

if __name__ == '__main__':
    PORT = 8000
    
    print('=' * 60)
    print('Nadi Dosha Calculator - CORS Proxy Server')
    print('=' * 60)
    print(f'\nServer running at: http://localhost:{PORT}')
    print(f'Proxy endpoints:')
    print(f'   - /api/nominatim - Nominatim geocoding')
    print(f'   - /api/photon - Photon geocoding')
    print(f'   - /api/timeapi - TimeAPI timezone')
    print(f'\nOpen your browser to: http://localhost:{PORT}')
    print(f'Press Ctrl+C to stop the server\n')
    print('=' * 60)
    
    server = HTTPServer(('', PORT), CORSProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\nServer stopped. Goodbye!')

