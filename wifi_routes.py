"""
🌐 WiFi Finder Routes - Flask endpoints for WiFi discovery

This module provides REST API endpoints for finding WiFi hotspots:
• POST /api/wifi/nearby - Find WiFi near user location
• GET /api/wifi/status - Check service status

Baby explanation:
• Frontend says: "I'm at this location, find WiFi!"
• Backend asks WiFi databases and Google: "What's nearby?"
• Backend returns: "Here are the best WiFi spots!"
• Frontend shows them on a map!
"""

from flask import Blueprint, request, jsonify
from wifi_service import wifi_service
import time

# Create Flask blueprint for WiFi routes
wifi_bp = Blueprint('wifi', __name__)

@wifi_bp.route('/api/wifi/nearby', methods=['POST'])
def find_nearby_wifi():
    """
    🎯 Find WiFi hotspots near a location
    
    Input: { "lat": 26.9124, "lng": 75.7873, "radiusMeters": 800 }
    Output: List of WiFi hotspots with details
    
    Like being a WiFi scout: "Tell me where you are,
    and I'll find the best internet spots around you!"
    """
    
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided',
                'message': 'Please send location data in JSON format'
            }), 400
        
        # Validate required fields
        lat = data.get('lat')
        lng = data.get('lng')
        
        if lat is None or lng is None:
            return jsonify({
                'success': False,
                'error': 'Missing coordinates',
                'message': 'Please provide both lat and lng coordinates'
            }), 400
        
        # Validate coordinate ranges
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({
                'success': False,
                'error': 'Invalid coordinates',
                'message': 'Latitude must be -90 to 90, longitude must be -180 to 180'
            }), 400
        
        # Get optional radius (default 800 meters)
        radius_meters = data.get('radiusMeters', 800)
        
        # Validate radius
        if not (50 <= radius_meters <= 5000):
            return jsonify({
                'success': False,
                'error': 'Invalid radius',
                'message': 'Radius must be between 50 and 5000 meters'
            }), 400
        
        print(f"🔍 Searching for WiFi near {lat}, {lng} within {radius_meters}m")
        
        # Find WiFi hotspots
        start_time = time.time()
        hotspots = wifi_service.find_nearby_wifi(lat, lng, radius_meters)
        search_time = round((time.time() - start_time) * 1000)  # Convert to milliseconds
        
        # Format response
        response = {
            'success': True,
            'data': hotspots,
            'meta': {
                'count': len(hotspots),
                'search_location': {'lat': lat, 'lng': lng},
                'radius_meters': radius_meters,
                'search_time_ms': search_time,
                'timestamp': int(time.time())
            }
        }
        
        print(f"✅ Found {len(hotspots)} WiFi hotspots in {search_time}ms")
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid data format',
            'message': str(e)
        }), 400
        
    except Exception as e:
        print(f"💥 Error finding WiFi: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'Something went wrong while searching for WiFi hotspots',
            'fallback_data': wifi_service._generate_fallback_wifi(
                data.get('lat', 0), data.get('lng', 0), 800
            ) if data and data.get('lat') and data.get('lng') else []
        }), 500

@wifi_bp.route('/api/wifi/status', methods=['GET'])
def wifi_service_status():
    """
    📊 Check WiFi service status and configuration
    
    Like asking: "Is the WiFi finder working?
    What features are available?"
    """
    
    try:
        # Check which external services are configured
        google_available = bool(wifi_service.google_api_key)
        openwifi_available = bool(wifi_service.openwifimap_api_key)
        pmwani_available = bool(wifi_service.pmwani_api_key)
        
        # Calculate service level
        configured_services = sum([google_available, openwifi_available, pmwani_available])
        
        if configured_services == 0:
            service_level = 'basic'
            message = 'Running with fallback data only. Configure API keys for better results.'
        elif configured_services == 1:
            service_level = 'good'
            message = 'Some external services available. Add more API keys for comprehensive results.'
        elif configured_services == 2:
            service_level = 'excellent'
            message = 'Multiple data sources available for comprehensive WiFi discovery.'
        else:
            service_level = 'premium'
            message = 'All data sources available for maximum WiFi discovery coverage.'
        
        return jsonify({
            'success': True,
            'status': 'active',
            'service_level': service_level,
            'message': message,
            'features': {
                'google_places': google_available,
                'openwifimap': openwifi_available,
                'pmwani': pmwani_available,
                'fallback_data': True,
                'caching': True,
                'distance_calculation': True
            },
            'cache_info': {
                'timeout_seconds': wifi_service.cache_timeout,
                'cached_locations': len(wifi_service.cache)
            },
            'api_info': {
                'max_radius_meters': 5000,
                'min_radius_meters': 50,
                'default_radius_meters': 800,
                'max_results': 50
            }
        })
        
    except Exception as e:
        print(f"💥 Error checking WiFi service status: {e}")
        return jsonify({
            'success': False,
            'status': 'error',
            'message': 'Unable to check service status',
            'error': str(e)
        }), 500

@wifi_bp.route('/api/wifi/test', methods=['GET'])
def test_wifi_service():
    """
    🧪 Test the WiFi service with sample data
    
    Like doing a practice run: "Let's make sure everything works
    before users start using it!"
    """
    
    try:
        # Test with sample coordinates (somewhere in India)
        test_lat = 26.9124  # Example: Jaipur
        test_lng = 75.7873
        test_radius = 500
        
        print(f"🧪 Testing WiFi service with coordinates {test_lat}, {test_lng}")
        
        # Run the search
        start_time = time.time()
        test_results = wifi_service.find_nearby_wifi(test_lat, test_lng, test_radius)
        test_time = round((time.time() - start_time) * 1000)
        
        return jsonify({
            'success': True,
            'message': 'WiFi service test completed successfully',
            'test_results': {
                'coordinates': {'lat': test_lat, 'lng': test_lng},
                'radius_meters': test_radius,
                'found_hotspots': len(test_results),
                'search_time_ms': test_time,
                'sample_hotspots': test_results[:3] if test_results else []
            },
            'service_working': True
        })
        
    except Exception as e:
        print(f"💥 WiFi service test failed: {e}")
        return jsonify({
            'success': False,
            'message': 'WiFi service test failed',
            'error': str(e),
            'service_working': False
        }), 500

# Helper function to register routes
def register_wifi_routes(app):
    """
    🔌 Register WiFi routes with the Flask app
    
    Like connecting the WiFi finder to your app:
    "Hey app, these are the new WiFi endpoints!"
    """
    
    app.register_blueprint(wifi_bp)
    print("🌐 WiFi Finder routes registered successfully!")
    print("📍 Available endpoints:")
    print("   POST /api/wifi/nearby - Find WiFi hotspots")
    print("   GET /api/wifi/status - Check service status")
    print("   GET /api/wifi/test - Test the service")

# Export for easy import
__all__ = ['wifi_bp', 'register_wifi_routes']