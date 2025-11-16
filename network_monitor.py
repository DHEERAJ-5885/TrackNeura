"""
🌐 Network Monitor - Real-Time WiFi & Connection Status
======================================================

Hello little one! This is like having a magic mirror that shows how fast 
your internet playground is working right now!

Think of it like this:
- WiFi is like a invisible bridge to the internet playground
- Upload speed is how fast you can throw paper planes across the bridge
- Download speed is how fast paper planes come back to you
- Latency is how long your "hello!" takes to reach your friend
- Jitter is how wobbly your voice sounds
- Packet loss is how many of your paper planes get lost in the wind

This helper watches all of these things every second and tells you 
if your internet bridge is strong or needs fixing!
"""

import time
import subprocess
import re
import platform
import psutil
import json
from typing import Dict, Optional
from datetime import datetime

class NetworkMonitor:
    """
    A gentle network detective that watches your internet playground!
    Like a wise owl that sees everything happening on your WiFi bridge.
    """
    
    def __init__(self):
        """Baby, let's start watching your internet playground!"""
        self.system = platform.system().lower()
        self.last_bytes_sent = 0
        self.last_bytes_received = 0
        self.last_check_time = time.time()
        self.speed_history = []  # Like keeping a diary of how fast things were
        
    def get_wifi_name(self) -> str:
        """
        Baby, this finds out what your WiFi playground is called!
        Like asking "What's the name of this park we're playing in?"
        """
        try:
            if self.system == "windows":
                # Windows way to find WiFi name (like asking Windows nicely)
                result = subprocess.run(
                    ["netsh", "wlan", "show", "interfaces"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'SSID' in line and 'BSSID' not in line:
                            # Found the WiFi name! Like finding a name tag!
                            return line.split(':')[1].strip()
            
            elif self.system == "darwin":  # macOS
                # Mac way to find WiFi name
                result = subprocess.run(
                    ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'SSID:' in line:
                            return line.split(':')[1].strip()
            
            elif self.system == "linux":
                # Linux way to find WiFi name
                result = subprocess.run(
                    ["iwgetid", "-r"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if result.returncode == 0:
                    return result.stdout.strip()
        
        except Exception as e:
            # If we can't find the WiFi name, that's okay!
            print(f"Gentle note: Couldn't find WiFi name because: {e}")
        
        return "Unknown Network"  # Like saying "I don't know this playground's name"
    
    def ping_test(self, host: str = "8.8.8.8") -> Dict[str, float]:
        """
        Baby, this is like shouting "Hello!" and timing how long it takes 
        for the echo to come back from the internet playground!
        """
        try:
            if self.system == "windows":
                # Windows ping (like Windows saying hello)
                result = subprocess.run(
                    ["ping", "-n", "4", host], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
            else:
                # Unix/Linux/Mac ping (like Unix saying hello)
                result = subprocess.run(
                    ["ping", "-c", "4", host], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
            
            if result.returncode == 0:
                # Parse the ping results (like reading the echo times)
                times = []
                for line in result.stdout.split('\n'):
                    if 'time=' in line or 'time<' in line:
                        # Found a time! Like catching an echo!
                        match = re.search(r'time[<=](\d+\.?\d*)ms', line)
                        if match:
                            times.append(float(match.group(1)))
                
                if times:
                    # Calculate the ping statistics (like average echo time)
                    avg_latency = sum(times) / len(times)
                    min_latency = min(times)
                    max_latency = max(times)
                    
                    # Jitter is how much the times wobble (like measuring shakiness)
                    jitter = max_latency - min_latency if len(times) > 1 else 0
                    
                    return {
                        'latency': round(avg_latency, 2),
                        'jitter': round(jitter, 2),
                        'packet_loss': 0.0  # If we got here, no packets were lost!
                    }
        
        except Exception as e:
            print(f"Gentle note: Ping test had a little problem: {e}")
        
        # If ping didn't work, return gentle default values
        return {
            'latency': 0.0,
            'jitter': 0.0,
            'packet_loss': 0.0
        }
    
    def get_network_speed(self) -> Dict[str, float]:
        """
        Baby, this measures how fast data is flying across your internet bridge!
        Like counting how many paper planes fly by each second!
        """
        try:
            # Get network statistics (like counting all the data packets)
            stats = psutil.net_io_counters()
            current_time = time.time()
            
            # Calculate time difference (how much time passed)
            time_diff = current_time - self.last_check_time
            
            if time_diff > 0 and self.last_bytes_sent > 0:
                # Calculate upload speed (how fast we send data out)
                bytes_sent_diff = stats.bytes_sent - self.last_bytes_sent
                bytes_received_diff = stats.bytes_recv - self.last_bytes_received
                
                # Convert to Mbps (like converting to "paper planes per second")
                upload_speed = (bytes_sent_diff * 8) / (time_diff * 1024 * 1024)  # bits per second to Mbps
                download_speed = (bytes_received_diff * 8) / (time_diff * 1024 * 1024)
                
                # Keep history for our sparkline chart (like keeping a diary)
                self.speed_history.append({
                    'time': current_time,
                    'upload': max(0, upload_speed),  # Never negative speeds!
                    'download': max(0, download_speed)
                })
                
                # Keep only last 60 seconds of history (like remembering last minute)
                self.speed_history = [
                    entry for entry in self.speed_history 
                    if current_time - entry['time'] <= 60
                ]
                
                # Update our memory for next time
                self.last_bytes_sent = stats.bytes_sent
                self.last_bytes_received = stats.bytes_recv
                self.last_check_time = current_time
                
                return {
                    'upload_speed': round(max(0, upload_speed), 2),
                    'download_speed': round(max(0, download_speed), 2)
                }
            else:
                # First time or no time passed, just remember current values
                self.last_bytes_sent = stats.bytes_sent
                self.last_bytes_received = stats.bytes_recv
                self.last_check_time = current_time
                
        except Exception as e:
            print(f"Gentle note: Speed test had a little problem: {e}")
        
        # Return gentle default values if something went wrong
        return {
            'upload_speed': 0.0,
            'download_speed': 0.0
        }
    
    def get_network_health(self, latency: float, jitter: float, packet_loss: float, 
                          upload_speed: float) -> str:
        """
        Baby, this is our wise detective that looks at all the clues and tells us
        if our internet playground is healthy or needs some care!
        
        Like a gentle doctor checking if everything is working well!
        """
        
        # Count problems (like counting boo-boos)
        problems = 0
        
        # Check latency (how long hellos take)
        if latency > 100:  # More than 100ms is like a very slow echo
            problems += 2
        elif latency > 50:  # More than 50ms is like a slow echo
            problems += 1
        
        # Check jitter (how wobbly the connection is)
        if jitter > 50:  # Very wobbly
            problems += 2
        elif jitter > 20:  # A little wobbly
            problems += 1
        
        # Check packet loss (how many paper planes got lost)
        if packet_loss > 5:  # Lost too many planes!
            problems += 2
        elif packet_loss > 1:  # Lost a few planes
            problems += 1
        
        # Check upload speed (how fast we can send)
        if upload_speed < 1:  # Very slow sending
            problems += 1
        
        # Decide health status (like giving a report card)
        if problems == 0:
            return "Excellent"  # Perfect playground!
        elif problems <= 2:
            return "Good"       # Pretty good playground!
        elif problems <= 4:
            return "Weak"       # Playground needs some fixing
        else:
            return "Poor"       # Playground needs lots of care
    
    def get_complete_status(self) -> Dict:
        """
        Baby, this gathers ALL the information about your internet playground
        and puts it in a nice little report!
        
        Like making a complete health report for your WiFi bridge!
        """
        try:
            # Get WiFi name (what playground are we in?)
            wifi_name = self.get_wifi_name()
            
            # Test the connection (shout hello and listen for echo)
            ping_results = self.ping_test()
            
            # Measure speeds (count paper planes)
            speed_results = self.get_network_speed()
            
            # Ask our detective what they think
            health_status = self.get_network_health(
                ping_results['latency'],
                ping_results['jitter'], 
                ping_results['packet_loss'],
                speed_results['upload_speed']
            )
            
            # Create our complete report
            return {
                'wifi_name': wifi_name,
                'upload_speed': speed_results['upload_speed'],
                'download_speed': speed_results['download_speed'],
                'latency': ping_results['latency'],
                'jitter': ping_results['jitter'],
                'packet_loss': ping_results['packet_loss'],
                'health_status': health_status,
                'timestamp': datetime.now().isoformat(),
                'speed_history': self.speed_history[-30:],  # Last 30 measurements for chart
                'success': True
            }
            
        except Exception as e:
            # If something goes wrong, return a gentle error message
            return {
                'wifi_name': 'Unknown',
                'upload_speed': 0.0,
                'download_speed': 0.0,
                'latency': 0.0,
                'jitter': 0.0,
                'packet_loss': 0.0,
                'health_status': 'Unknown',
                'timestamp': datetime.now().isoformat(),
                'speed_history': [],
                'success': False,
                'error': str(e)
            }

# Create our gentle network monitor (like hiring a kind playground supervisor)
network_monitor = NetworkMonitor()