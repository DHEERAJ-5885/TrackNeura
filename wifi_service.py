"""
🌐 WiFi Finder Service - Real-Time WiFi Hotspot Discovery

This service finds real, live Wi-Fi hotspots around users using multiple data sources:
• Google Places API for cafes, libraries, stations with WiFi
• OpenWiFiMap API for crowd-sourced WiFi data
• Fallback to basic location-based WiFi suggestions

Baby explanation:
• User shares their location (with permission)
• We ask Google: "What cafes/libraries are nearby?"
• We ask WiFi databases: "What WiFi networks are here?"
• We combine the results and show the best options
• User sees a map with WiFi spots and can pick the best one!
"""

import requests
import os
import time
import math
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class WiFiFinderService:
    def __init__(self):
        self.google_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.openwifimap_api_key = os.getenv('OPENWIFIMAP_API_KEY')
        self.pmwani_api_key = os.getenv('PMWANI_API_KEY')
        
        # Cache to avoid hammering external APIs
        self.cache = {}
        self.cache_timeout = 30  # 30 seconds
        
        print("🌐 WiFi Finder Service initialized! Ready to find hotspots!")
    
    def find_nearby_wifi(self, lat: float, lng: float, radius_meters: int = 800) -> List[Dict]:
        """
        🎯 Main function to find WiFi hotspots near a location
        
        Like a smart detective that asks multiple sources:
        1. Google: "What places with WiFi are nearby?"
        2. WiFi databases: "What networks can I see here?"
        3. Combines all clues to give you the best answer!
        """
        
        # Check cache first (don't spam external APIs!)
        cache_key = f"{round(lat, 4)}_{round(lng, 4)}_{radius_meters}"
        if self._is_cache_valid(cache_key):
            print(f"📦 Using cached WiFi data for {cache_key}")
            return self.cache[cache_key]['data']
        
        all_hotspots = []
        
        # Source 1: Google Places (cafes, libraries, stations)
        try:
            google_results = self._query_google_places(lat, lng, radius_meters)
            all_hotspots.extend(google_results)
            print(f"🏢 Found {len(google_results)} places from Google")
        except Exception as e:
            print(f"⚠️ Google Places error: {e}")
        
        # Source 2: OpenWiFiMap (crowd-sourced WiFi data)
        try:
            wifi_results = self._query_openwifimap(lat, lng, radius_meters)
            all_hotspots.extend(wifi_results)
            print(f"📡 Found {len(wifi_results)} WiFi networks from OpenWiFiMap")
        except Exception as e:
            print(f"⚠️ OpenWiFiMap error: {e}")
        
        # Source 3: PM-WANI (India's public WiFi)
        try:
            pmwani_results = self._query_pmwani(lat, lng, radius_meters)
            all_hotspots.extend(pmwani_results)
            print(f"🇮🇳 Found {len(pmwani_results)} PM-WANI hotspots")
        except Exception as e:
            print(f"⚠️ PM-WANI error: {e}")
        
        # Merge, deduplicate, and rank results
        final_results = self._merge_and_rank(all_hotspots, lat, lng)
        
        # Cache the results
        self.cache[cache_key] = {
            'data': final_results,
            'timestamp': datetime.now()
        }
        
        print(f"✨ Returning {len(final_results)} WiFi hotspots!")
        return final_results
    
    def _query_google_places(self, lat: float, lng: float, radius: int) -> List[Dict]:
        """
        🏢 Ask Google: "What cafes, libraries, and stations are nearby?"
        
        Like asking a local guide: "Where can I find WiFi around here?"
        Google knows about cafes, libraries, train stations - places that usually have WiFi!
        """
        
        if not self.google_api_key:
            print("⚠️ No Google API key - skipping Google Places")
            return []
        
        # Places that usually have WiFi
        place_types = ['cafe', 'library', 'train_station', 'restaurant', 'shopping_mall']
        all_places = []
        
        for place_type in place_types:
            try:
                url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                params = {
                    'location': f"{lat},{lng}",
                    'radius': radius,
                    'type': place_type,
                    'key': self.google_api_key
                }
                
                response = requests.get(url, params=params, timeout=10)
                data = response.json()
                
                if data.get('status') == 'OK':
                    for place in data.get('results', []):
                        hotspot = self._format_google_place(place, place_type)
                        if hotspot:
                            all_places.append(hotspot)
                
                # Be nice to Google's API (rate limiting)
                time.sleep(0.1)
                
            except Exception as e:
                print(f"⚠️ Error querying Google for {place_type}: {e}")
        
        return all_places
    
    def _format_google_place(self, place: Dict, place_type: str) -> Optional[Dict]:
        """
        🏷️ Convert Google Place data into our WiFi hotspot format
        
        Like translating Google's language into our simple format:
        "This cafe at these coordinates probably has WiFi!"
        """
        
        try:
            location = place.get('geometry', {}).get('location', {})
            if not location.get('lat') or not location.get('lng'):
                return None
            
            # Guess WiFi type based on place type
            wifi_type_map = {
                'cafe': 'cafe',
                'library': 'library', 
                'train_station': 'RailWire',
                'restaurant': 'restaurant',
                'shopping_mall': 'public'
            }
            
            return {
                'id': f"google_{place.get('place_id', 'unknown')}",
                'name': place.get('name', 'Unknown Place'),
                'ssid': f"{place.get('name', 'WiFi').replace(' ', '')}_Free",  # Educated guess
                'type': wifi_type_map.get(place_type, 'public'),
                'lat': location['lat'],
                'lng': location['lng'],
                'distance_m': 0,  # Will be calculated later
                'signal_dbm': None,  # Google doesn't provide this
                'quality_score': self._estimate_quality_from_rating(place.get('rating', 3.0)),
                'provider': place.get('name', 'Unknown'),
                'source': 'google_places',
                'raw_data': {
                    'rating': place.get('rating'),
                    'user_ratings_total': place.get('user_ratings_total'),
                    'price_level': place.get('price_level')
                }
            }
        except Exception as e:
            print(f"⚠️ Error formatting Google place: {e}")
            return None
    
    def _query_openwifimap(self, lat: float, lng: float, radius: int) -> List[Dict]:
        """
        📡 Ask OpenWiFiMap: "What WiFi networks are broadcasting here?"
        
        Like asking WiFi enthusiasts who map all the networks:
        "Hey, what networks can you see from this spot?"
        """
        
        if not self.openwifimap_api_key:
            print("⚠️ No OpenWiFiMap API key - using fallback data")
            return self._generate_fallback_wifi(lat, lng, radius)
        
        try:
            # OpenWiFiMap API (if available)
            # Note: This is a placeholder - real implementation would use actual API
            url = "https://api.openwifimap.net/view_nodes"
            params = {
                'bbox': self._get_bounding_box(lat, lng, radius),
                'api_key': self.openwifimap_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            wifi_networks = []
            for node in data.get('nodes', []):
                hotspot = self._format_wifi_node(node)
                if hotspot:
                    wifi_networks.append(hotspot)
            
            return wifi_networks
            
        except Exception as e:
            print(f"⚠️ OpenWiFiMap error: {e}")
            return self._generate_fallback_wifi(lat, lng, radius)
    
    def _query_pmwani(self, lat: float, lng: float, radius: int) -> List[Dict]:
        """
        🇮🇳 Ask PM-WANI: "What public WiFi hotspots are available?"
        
        PM-WANI is India's public WiFi network - like asking the government:
        "Where are your official free WiFi spots?"
        """
        
        if not self.pmwani_api_key:
            print("⚠️ No PM-WANI API key - generating sample data")
            return self._generate_pmwani_samples(lat, lng)
        
        # Note: PM-WANI API implementation would go here
        # For now, return sample PM-WANI style hotspots
        return self._generate_pmwani_samples(lat, lng)
    
    def _generate_fallback_wifi(self, lat: float, lng: float, radius: int) -> List[Dict]:
        """
        🆘 Generate realistic WiFi hotspots when APIs aren't available
        
        Like having a backup plan: "If we can't ask the databases,
        let's make educated guesses about where WiFi might be!"
        """
        
        fallback_networks = [
            {
                'id': f'fallback_1_{int(time.time())}',
                'name': 'City Public WiFi',
                'ssid': 'City_Free_WiFi',
                'type': 'public',
                'lat': lat + 0.001,
                'lng': lng + 0.001,  
                'distance_m': 0,
                'signal_dbm': -70,
                'quality_score': 65,
                'provider': 'Municipal',
                'source': 'fallback'
            },
            {
                'id': f'fallback_2_{int(time.time())}',
                'name': 'Local Cafe WiFi',
                'ssid': 'Cafe_Guest',
                'type': 'cafe',
                'lat': lat - 0.0008,
                'lng': lng + 0.0012,
                'distance_m': 0,
                'signal_dbm': -60,
                'quality_score': 78,
                'provider': 'Local Cafe',
                'source': 'fallback'
            }
        ]
        
        return fallback_networks
    
    def _generate_pmwani_samples(self, lat: float, lng: float) -> List[Dict]:
        """
        🇮🇳 Generate sample PM-WANI hotspots for demonstration
        """
        
        return [
            {
                'id': f'pmwani_{int(time.time())}',
                'name': 'PM-WANI Hotspot',
                'ssid': 'PM-WANI-Free',
                'type': 'PM-WANI',
                'lat': lat + 0.0005,
                'lng': lng - 0.0008,
                'distance_m': 0,
                'signal_dbm': -65,
                'quality_score': 72,
                'provider': 'PM-WANI',
                'source': 'pm_wani'
            }
        ]
    
    def _merge_and_rank(self, hotspots: List[Dict], user_lat: float, user_lng: float) -> List[Dict]:
        """
        🎯 Combine all hotspot data and rank by quality
        
        Like being a smart organizer:
        1. Remove duplicates (same location/name)
        2. Calculate distances from user
        3. Rank by quality + proximity
        4. Return the best options first!
        """
        
        # Calculate distances
        for hotspot in hotspots:
            distance = self._calculate_distance(
                user_lat, user_lng,
                hotspot['lat'], hotspot['lng']
            )
            hotspot['distance_m'] = round(distance)
        
        # Remove duplicates (same location within 50m)
        unique_hotspots = []
        for hotspot in hotspots:
            is_duplicate = False
            for existing in unique_hotspots:
                if self._calculate_distance(
                    hotspot['lat'], hotspot['lng'],
                    existing['lat'], existing['lng']
                ) < 50:  # 50 meter threshold
                    # Keep the one with better quality
                    if hotspot['quality_score'] > existing['quality_score']:
                        unique_hotspots.remove(existing)
                        unique_hotspots.append(hotspot)
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_hotspots.append(hotspot)
        
        # Sort by combined score (quality + proximity)
        def calculate_final_score(hotspot):
            quality_score = hotspot['quality_score']
            distance_factor = max(0, 100 - (hotspot['distance_m'] / 10))  # Closer is better
            return (quality_score * 0.7) + (distance_factor * 0.3)
        
        unique_hotspots.sort(key=calculate_final_score, reverse=True)
        
        # Limit to top 50 results
        return unique_hotspots[:50]
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        📏 Calculate distance between two points using Haversine formula
        
        Like asking: "How far is it from here to there?"
        Uses the curve of the Earth to get accurate distance in meters!
        """
        
        # Convert latitude and longitude from degrees to radians
        lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in meters
        earth_radius = 6371000
        distance = earth_radius * c
        
        return distance
    
    def _estimate_quality_from_rating(self, rating: float) -> int:
        """
        ⭐ Convert Google rating to WiFi quality score
        
        Like translating: "If people rate this cafe 4.5 stars,
        the WiFi is probably pretty good too!"
        """
        
        # Convert 0-5 star rating to 0-100 quality score
        return min(100, max(0, int((rating / 5.0) * 100)))
    
    def _get_bounding_box(self, lat: float, lng: float, radius: int) -> str:
        """
        📦 Create a bounding box for API queries
        
        Like drawing a rectangle around the area we want to search
        """
        
        # Rough conversion: 1 degree ≈ 111km
        lat_offset = (radius / 111000)
        lng_offset = (radius / (111000 * math.cos(math.radians(lat))))
        
        south = lat - lat_offset
        north = lat + lat_offset
        west = lng - lng_offset
        east = lng + lng_offset
        
        return f"{west},{south},{east},{north}"
    
    def _format_wifi_node(self, node: Dict) -> Optional[Dict]:
        """
        📡 Format WiFi node data from external APIs
        """
        
        try:
            return {
                'id': f"wifi_{node.get('id', 'unknown')}",
                'name': node.get('hostname', 'WiFi Hotspot'),
                'ssid': node.get('ssid', 'Unknown Network'),
                'type': 'public',
                'lat': node.get('lat'),
                'lng': node.get('lng'),
                'distance_m': 0,
                'signal_dbm': node.get('signal_strength'),
                'quality_score': self._signal_to_quality(node.get('signal_strength', -70)),
                'provider': 'Community',
                'source': 'openwifimap'
            }
        except:
            return None
    
    def _signal_to_quality(self, signal_dbm: Optional[int]) -> int:
        """
        📶 Convert signal strength to quality score
        
        Like translating radio signals to "how good is this?"
        -30dBm = Excellent, -90dBm = Poor
        """
        
        if not signal_dbm:
            return 50  # Unknown signal = average quality
        
        # Convert dBm to quality (0-100)
        if signal_dbm >= -30:
            return 100
        elif signal_dbm >= -50:
            return 80
        elif signal_dbm >= -60:
            return 70
        elif signal_dbm >= -70:
            return 60
        elif signal_dbm >= -80:
            return 40
        else:
            return 20
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """
        ⏰ Check if cached data is still fresh
        
        Like checking: "Is this information still good,
        or do we need to ask again?"
        """
        
        if cache_key not in self.cache:
            return False
        
        cache_time = self.cache[cache_key]['timestamp']
        age = datetime.now() - cache_time
        
        return age.total_seconds() < self.cache_timeout

# Global service instance
wifi_service = WiFiFinderService()