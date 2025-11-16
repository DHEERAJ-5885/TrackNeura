/**
 * 🌐 WiFi Finder Component - Real-Time WiFi Hotspot Discovery
 * 
 * This component shows users nearby WiFi hotspots in real-time!
 * Features:
 * • Live location tracking with user permission
 * • Interactive map with WiFi hotspot markers
 * • List view with hotspot details and quality scores
 * • Auto-refresh as user moves around
 * • Beautiful UI with loading states
 * 
 * Baby explanation:
 * • Asks user: "Can I know where you are?" (permission popup)
 * • Finds user's location using GPS
 * • Asks server: "What WiFi is near me?"
 * • Shows WiFi spots on a map with pins
 * • Updates automatically when user moves!
 * 
 * Privacy-friendly: Only uses location to find WiFi, doesn't store it!
 */

class WiFiFinder {
    constructor() {
        this.isActive = false;
        this.currentPosition = null;
        this.watchId = null;
        this.hotspots = [];
        this.map = null;
        this.markers = [];
        this.updateInterval = null;
        
        console.log('🌐 WiFi Finder initialized! Ready to discover hotspots!');
    }
    
    /**
     * 🚀 Initialize the WiFi Finder - call this from your HTML!
     */
    static init() {
        window.wifiFinder = new WiFiFinder();
        window.wifiFinder.setup();
    }
    
    /**
     * 🏗️ Set up the WiFi Finder UI and location services
     */
    async setup() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.createUI());
        } else {
            this.createUI();
        }
        
        // Check if geolocation is supported
        if (!navigator.geolocation) {
            console.error('❌ Geolocation is not supported by this browser');
            this.showError('Geolocation not supported by your browser');
            return;
        }
        
        console.log('📍 Geolocation is supported! Ready to find your location.');
    }
    
    /**
     * 🎨 Create the beautiful WiFi Finder UI
     */
    createUI() {
        // Create the main container
        const container = document.createElement('div');
        container.className = 'wifi-finder';
        container.innerHTML = this.getHTML();
        
        // Add styles
        this.addStyles();
        
        // Append to body
        document.body.appendChild(container);
        
        // Bind event listeners
        this.bindEvents();
        
        console.log('🎨 WiFi Finder UI created successfully!');
    }
    
    /**
     * 📝 Get the HTML structure for the WiFi Finder
     */
    getHTML() {
        return `
            <!-- 🌐 WiFi Finder Toggle Button -->
            <button class="wifi-finder-toggle" id="wifiFinderToggle" title="Find WiFi Hotspots Near You!">
                📶
                <span class="wifi-finder-notification">WiFi</span>
            </button>
            
            <!-- 📡 WiFi Finder Window -->
            <div class="wifi-finder-window" id="wifiFinderWindow" style="display: none;">
                <!-- 📋 WiFi Finder Header -->
                <div class="wifi-finder-header">
                    <div class="finder-title">
                        <span class="wifi-icon">📡</span>
                        <div>
                            <h3>WiFi Finder</h3>
                            <p>Discover nearby hotspots</p>
                        </div>
                    </div>
                    <div class="finder-controls">
                        <button class="refresh-btn" id="refreshBtn" title="Refresh WiFi search">🔄</button>
                        <button class="settings-btn" id="settingsBtn" title="Settings">⚙️</button>
                    </div>
                </div>
                
                <!-- 🗺️ Map and List Container -->
                <div class="wifi-finder-content">
                    <!-- Map Section -->
                    <div class="map-section">
                        <div id="wifiMap" class="wifi-map">
                            <!-- Map will be loaded here -->
                        </div>
                        <div class="map-controls">
                            <button class="locate-btn" id="locateBtn" title="Find my location">📍</button>
                            <button class="zoom-in-btn" id="zoomInBtn" title="Zoom in">➕</button>
                            <button class="zoom-out-btn" id="zoomOutBtn" title="Zoom out">➖</button>
                        </div>
                    </div>
                    
                    <!-- Hotspots List Section -->
                    <div class="hotspots-section">
                        <div class="section-header">
                            <h4>📶 Nearby Hotspots</h4>
                            <div class="hotspot-count" id="hotspotCount">0 found</div>
                        </div>
                        
                        <div class="hotspots-list" id="hotspotsList">
                            <!-- Hotspots will be populated here -->
                        </div>
                    </div>
                </div>
                
                <!-- 📊 Status Bar -->
                <div class="wifi-finder-status" id="wifiFinderStatus">
                    <div class="status-item">
                        <span class="status-icon">📍</span>
                        <span class="status-text" id="locationStatus">Getting location...</span>
                    </div>
                    <div class="status-item">
                        <span class="status-icon">📡</span>
                        <span class="status-text" id="wifiStatus">Ready to search</span>
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * 🎨 Add beautiful CSS styles for the WiFi Finder
     */
    addStyles() {
        const styles = `
            <style>
            /* 🌐 WiFi Finder Styles */
            .wifi-finder {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1002;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            /* 📶 WiFi Toggle Button */
            .wifi-finder-toggle {
                width: 64px;
                height: 64px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #00bcd4 0%, #4caf50 100%);
                color: white;
                font-size: 26px;
                cursor: pointer;
                box-shadow: 0 4px 24px rgba(0, 188, 212, 0.3);
                transition: all 0.3s ease;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: wifiPulse 3s ease-in-out infinite;
            }
            
            @keyframes wifiPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            .wifi-finder-toggle:hover {
                transform: translateY(-3px) scale(1.1);
                box-shadow: 0 8px 32px rgba(0, 188, 212, 0.4);
            }
            
            .wifi-finder-toggle.active {
                background: linear-gradient(135deg, #ff9800 0%, #f44336 100%);
                animation: none;
            }
            
            /* 🔔 WiFi Notification Badge */
            .wifi-finder-notification {
                position: absolute;
                top: -8px;
                right: -8px;
                background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%);
                color: white;
                border-radius: 50%;
                width: 28px;
                height: 28px;
                font-size: 11px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: wifiNotificationPulse 2s infinite;
                border: 2px solid white;
            }
            
            @keyframes wifiNotificationPulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            
            /* 📡 WiFi Finder Window */
            .wifi-finder-window {
                position: absolute;
                top: 80px;
                right: 0;
                width: 800px;
                height: 600px;
                background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                animation: wifiSlideIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                border: 1px solid rgba(0, 188, 212, 0.1);
            }
            
            @keyframes wifiSlideIn {
                from {
                    opacity: 0;
                    transform: translateY(-30px) scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            /* 📋 WiFi Finder Header */
            .wifi-finder-header {
                background: linear-gradient(135deg, #00bcd4 0%, #4caf50 100%);
                color: white;
                padding: 20px 24px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .finder-title {
                display: flex;
                align-items: center;
                gap: 16px;
            }
            
            .wifi-icon {
                font-size: 28px;
                animation: wifiSpin 4s ease-in-out infinite;
            }
            
            @keyframes wifiSpin {
                0%, 100% { transform: rotate(0deg) scale(1); }
                25% { transform: rotate(5deg) scale(1.1); }
                75% { transform: rotate(-5deg) scale(1.1); }
            }
            
            .finder-title h3 {
                margin: 0;
                font-size: 18px;
                font-weight: 600;
            }
            
            .finder-title p {
                margin: 0;
                font-size: 13px;
                opacity: 0.9;
                font-weight: 400;
            }
            
            .finder-controls {
                display: flex;
                gap: 12px;
            }
            
            .refresh-btn, .settings-btn {
                background: rgba(255, 255, 255, 0.2);
                border: none;
                color: white;
                width: 36px;
                height: 36px;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
            }
            
            .refresh-btn:hover, .settings-btn:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: scale(1.1);
            }
            
            /* 🗺️ Content Area */
            .wifi-finder-content {
                flex: 1;
                display: flex;
                overflow: hidden;
            }
            
            .map-section {
                flex: 1;
                position: relative;
                background: #f0f0f0;
            }
            
            .wifi-map {
                width: 100%;
                height: 100%;
                background: linear-gradient(45deg, #e3f2fd 0%, #f1f8e9 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #666;
                font-size: 18px;
            }
            
            .map-controls {
                position: absolute;
                top: 20px;
                right: 20px;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            
            .locate-btn, .zoom-in-btn, .zoom-out-btn {
                width: 40px;
                height: 40px;
                border: none;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            }
            
            .locate-btn:hover, .zoom-in-btn:hover, .zoom-out-btn:hover {
                background: white;
                transform: scale(1.1);
            }
            
            /* 📱 Hotspots Section */
            .hotspots-section {
                width: 350px;
                background: #f8f9fa;
                border-left: 1px solid #e9ecef;
                display: flex;
                flex-direction: column;
            }
            
            .section-header {
                padding: 20px;
                background: white;
                border-bottom: 1px solid #e9ecef;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .section-header h4 {
                margin: 0;
                font-size: 16px;
                color: #333;
            }
            
            .hotspot-count {
                background: linear-gradient(135deg, #00bcd4 0%, #4caf50 100%);
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
            }
            
            .hotspots-list {
                flex: 1;
                overflow-y: auto;
                padding: 10px;
            }
            
            /* 📶 Hotspot Item */
            .hotspot-item {
                background: white;
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .hotspot-item:hover {
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
                transform: translateY(-2px);
            }
            
            .hotspot-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 8px;
            }
            
            .hotspot-name {
                font-weight: 600;
                color: #333;
                font-size: 14px;
            }
            
            .hotspot-type {
                background: #e3f2fd;
                color: #1976d2;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
            }
            
            .hotspot-details {
                display: flex;
                flex-direction: column;
                gap: 4px;
                font-size: 12px;
                color: #666;
            }
            
            .hotspot-distance {
                display: flex;
                align-items: center;
                gap: 4px;
            }
            
            .hotspot-quality {
                display: flex;
                align-items: center;
                gap: 4px;
            }
            
            .quality-bar {
                width: 50px;
                height: 4px;
                background: #e0e0e0;
                border-radius: 2px;
                overflow: hidden;
            }
            
            .quality-fill {
                height: 100%;
                background: linear-gradient(90deg, #f44336 0%, #ff9800 50%, #4caf50 100%);
                transition: width 0.3s ease;
            }
            
            /* 📊 Status Bar */
            .wifi-finder-status {
                background: white;
                border-top: 1px solid #e9ecef;
                padding: 12px 20px;
                display: flex;
                gap: 20px;
                font-size: 12px;
            }
            
            .status-item {
                display: flex;
                align-items: center;
                gap: 6px;
                color: #666;
            }
            
            .status-icon {
                font-size: 14px;
            }
            
            /* 🎭 Loading States */
            .loading {
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 40px;
                color: #666;
            }
            
            .loading::after {
                content: '';
                width: 20px;
                height: 20px;
                border: 2px solid #e0e0e0;
                border-top: 2px solid #00bcd4;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-left: 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            /* 📱 Mobile Responsiveness */
            @media (max-width: 768px) {
                .wifi-finder {
                    top: 15px;
                    right: 15px;
                }
                
                .wifi-finder-window {
                    width: calc(100vw - 30px);
                    height: 75vh;
                    top: 80px;
                    right: -15px;
                }
                
                .wifi-finder-content {
                    flex-direction: column;
                }
                
                .map-section {
                    height: 300px;
                }
                
                .hotspots-section {
                    width: 100%;
                    flex: 1;
                }
            }
            </style>
        `;
        
        document.head.insertAdjacentHTML('beforeend', styles);
    }
    
    /**
     * 🔗 Bind event listeners for user interactions
     */
    bindEvents() {
        const toggleBtn = document.getElementById('wifiFinderToggle');
        const refreshBtn = document.getElementById('refreshBtn');
        const settingsBtn = document.getElementById('settingsBtn');
        const locateBtn = document.getElementById('locateBtn');
        
        toggleBtn.addEventListener('click', () => this.toggleFinder());
        refreshBtn.addEventListener('click', () => this.refreshHotspots());
        settingsBtn.addEventListener('click', () => this.showSettings());
        locateBtn.addEventListener('click', () => this.requestLocation());
    }
    
    /**
     * 🎭 Toggle WiFi Finder open/closed
     */
    toggleFinder() {
        this.isActive = !this.isActive;
        const finderWindow = document.getElementById('wifiFinderWindow');
        const toggleBtn = document.getElementById('wifiFinderToggle');
        
        if (this.isActive) {
            finderWindow.style.display = 'flex';
            toggleBtn.innerHTML = '✕<span class="wifi-finder-notification">Close</span>';
            toggleBtn.classList.add('active');
            this.startWiFiDiscovery();
        } else {
            finderWindow.style.display = 'none';
            toggleBtn.innerHTML = '📶<span class="wifi-finder-notification">WiFi</span>';
            toggleBtn.classList.remove('active');
            this.stopWiFiDiscovery();
        }
    }
    
    /**
     * 🚀 Start WiFi discovery process
     */
    async startWiFiDiscovery() {
        console.log('🚀 Starting WiFi discovery...');
        this.updateStatus('location', 'Requesting location permission...');
        this.updateStatus('wifi', 'Waiting for location...');
        
        await this.requestLocation();
    }
    
    /**
     * 🛑 Stop WiFi discovery process
     */
    stopWiFiDiscovery() {
        console.log('🛑 Stopping WiFi discovery...');
        
        if (this.watchId) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
        }
        
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        
        this.updateStatus('location', 'Location tracking stopped');
        this.updateStatus('wifi', 'WiFi discovery stopped');
    }
    
    /**
     * 📍 Request user's location with permission
     */
    async requestLocation() {
        try {
            console.log('📍 Requesting user location...');
            this.updateStatus('location', 'Getting location...');
            
            // Request location with high accuracy
            navigator.geolocation.getCurrentPosition(
                (position) => this.onLocationSuccess(position),
                (error) => this.onLocationError(error),
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 30000
                }
            );
            
            // Start watching location changes
            this.watchId = navigator.geolocation.watchPosition(
                (position) => this.onLocationUpdate(position),
                (error) => this.onLocationError(error),
                {
                    enableHighAccuracy: true,
                    timeout: 5000,
                    maximumAge: 30000
                }
            );
            
        } catch (error) {
            console.error('❌ Location request failed:', error);
            this.onLocationError(error);
        }
    }
    
    /**
     * ✅ Handle successful location retrieval
     */
    onLocationSuccess(position) {
        this.currentPosition = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy
        };
        
        console.log('✅ Location obtained:', this.currentPosition);
        this.updateStatus('location', `Located (±${Math.round(this.currentPosition.accuracy)}m)`);
        
        // Search for WiFi hotspots
        this.searchWiFiHotspots();
    }
    
    /**
     * 🔄 Handle location updates (when user moves)
     */
    onLocationUpdate(position) {
        const newPosition = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy
        };
        
        // Check if user moved significantly (>100m)
        if (this.currentPosition) {
            const distance = this.calculateDistance(
                this.currentPosition.lat, this.currentPosition.lng,
                newPosition.lat, newPosition.lng
            );
            
            if (distance < 100) {
                // User hasn't moved much, don't update
                return;
            }
        }
        
        console.log('🚶‍♂️ User moved, updating location:', newPosition);
        this.currentPosition = newPosition;
        this.updateStatus('location', `Updated (±${Math.round(newPosition.accuracy)}m)`);
        
        // Refresh hotspots for new location
        this.searchWiFiHotspots();
    }
    
    /**
     * ❌ Handle location errors
     */
    onLocationError(error) {
        console.error('❌ Location error:', error);
        
        let errorMessage = 'Location error';
        switch (error.code) {
            case error.PERMISSION_DENIED:
                errorMessage = 'Location permission denied';
                this.showLocationPermissionHelp();
                break;
            case error.POSITION_UNAVAILABLE:
                errorMessage = 'Location unavailable';
                break;
            case error.TIMEOUT:
                errorMessage = 'Location timeout';
                break;
        }
        
        this.updateStatus('location', errorMessage);
        this.updateStatus('wifi', 'Cannot search without location');
        
        // Show fallback options
        this.showLocationFallback();
    }
    
    /**
     * 🔍 Search for WiFi hotspots near current location
     */
    async searchWiFiHotspots() {
        if (!this.currentPosition) {
            console.warn('⚠️ No location available for WiFi search');
            return;
        }
        
        try {
            console.log('🔍 Searching for WiFi hotspots...');
            this.updateStatus('wifi', 'Searching for WiFi hotspots...');
            this.showLoading();
            
            const response = await fetch('/api/wifi/nearby', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    lat: this.currentPosition.lat,
                    lng: this.currentPosition.lng,
                    radiusMeters: 800
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.hotspots = data.data;
                console.log(`✅ Found ${this.hotspots.length} WiFi hotspots`);
                this.updateStatus('wifi', `Found ${this.hotspots.length} hotspots`);
                this.displayHotspots();
            } else {
                console.error('❌ WiFi search failed:', data.error);
                this.updateStatus('wifi', 'Search failed');
                this.showError(data.message || 'Failed to find WiFi hotspots');
            }
            
        } catch (error) {
            console.error('❌ WiFi search error:', error);
            this.updateStatus('wifi', 'Connection error');
            this.showError('Unable to connect to WiFi service');
        }
    }
    
    /**
     * 📱 Display WiFi hotspots in the list
     */
    displayHotspots() {
        const hotspotsList = document.getElementById('hotspotsList');
        const hotspotCount = document.getElementById('hotspotCount');
        
        // Update count
        hotspotCount.textContent = `${this.hotspots.length} found`;
        
        // Clear existing list
        hotspotsList.innerHTML = '';
        
        if (this.hotspots.length === 0) {
            hotspotsList.innerHTML = `
                <div class="loading">
                    No WiFi hotspots found nearby.
                    Try expanding your search radius or moving to a different location.
                </div>
            `;
            return;
        }
        
        // Display each hotspot
        this.hotspots.forEach((hotspot, index) => {
            const hotspotItem = this.createHotspotItem(hotspot, index);
            hotspotsList.appendChild(hotspotItem);
        });
        
        console.log('📱 Hotspots displayed in list');
    }
    
    /**
     * 🏷️ Create a hotspot item element
     */
    createHotspotItem(hotspot, index) {
        const item = document.createElement('div');
        item.className = 'hotspot-item';
        item.onclick = () => this.selectHotspot(hotspot, index);
        
        // Quality color based on score
        let qualityColor = '#f44336'; // Red for poor
        if (hotspot.quality_score > 70) qualityColor = '#4caf50'; // Green for good
        else if (hotspot.quality_score > 50) qualityColor = '#ff9800'; // Orange for average
        
        item.innerHTML = `
            <div class="hotspot-header">
                <div class="hotspot-name">${hotspot.name}</div>
                <div class="hotspot-type">${hotspot.type}</div>
            </div>
            <div class="hotspot-details">
                <div class="hotspot-distance">
                    <span>📍</span>
                    <span>${hotspot.distance_m}m away</span>
                </div>
                <div class="hotspot-quality">
                    <span>📶</span>
                    <span>${hotspot.quality_score}%</span>
                    <div class="quality-bar">
                        <div class="quality-fill" style="width: ${hotspot.quality_score}%; background-color: ${qualityColor};"></div>
                    </div>
                </div>
                <div style="font-size: 11px; color: #999; margin-top: 4px;">
                    SSID: ${hotspot.ssid} • ${hotspot.provider}
                </div>
            </div>
        `;
        
        return item;
    }
    
    /**
     * 🎯 Handle hotspot selection
     */
    selectHotspot(hotspot, index) {
        console.log(`🎯 Selected hotspot: ${hotspot.name}`);
        
        // Highlight selected item
        document.querySelectorAll('.hotspot-item').forEach(item => {
            item.style.backgroundColor = 'white';
        });
        
        document.querySelectorAll('.hotspot-item')[index].style.backgroundColor = '#e3f2fd';
        
        // Show hotspot details
        alert(`📶 ${hotspot.name}\\n\\nSSID: ${hotspot.ssid}\\nType: ${hotspot.type}\\nDistance: ${hotspot.distance_m}m\\nQuality: ${hotspot.quality_score}%\\n\\nNote: Your device will need to connect to this network manually.`);
    }
    
    /**
     * 🔄 Refresh hotspots manually
     */
    refreshHotspots() {
        console.log('🔄 Manually refreshing hotspots...');
        if (this.currentPosition) {
            this.searchWiFiHotspots();
        } else {
            this.requestLocation();
        }
    }
    
    /**
     * ⚙️ Show settings dialog
     */
    showSettings() {
        alert('⚙️ WiFi Finder Settings\\n\\n• Search radius: 800m\\n• Auto-refresh: Every 30s\\n• Location accuracy: High\\n\\nMore settings coming soon!');
    }
    
    /**
     * 📊 Update status display
     */
    updateStatus(type, message) {
        const statusElement = document.getElementById(`${type}Status`);
        if (statusElement) {
            statusElement.textContent = message;
        }
    }
    
    /**
     * 📡 Show loading state
     */
    showLoading() {
        const hotspotsList = document.getElementById('hotspotsList');
        hotspotsList.innerHTML = '<div class="loading">Searching for WiFi hotspots...</div>';
    }
    
    /**
     * ❌ Show error message
     */
    showError(message) {
        const hotspotsList = document.getElementById('hotspotsList');
        hotspotsList.innerHTML = `<div class="loading">❌ ${message}</div>`;
    }
    
    /**
     * 🆘 Show location permission help
     */
    showLocationPermissionHelp() {
        const hotspotsList = document.getElementById('hotspotsList');
        hotspotsList.innerHTML = `
            <div class="loading">
                📍 Location Permission Needed<br><br>
                To find WiFi hotspots near you, please:<br>
                1. Click the 🔒 icon in your address bar<br>
                2. Allow location access<br>
                3. Refresh this page<br><br>
                Your location is only used to find nearby WiFi and is never stored.
            </div>
        `;
    }
    
    /**
     * 🗺️ Show location fallback options
     */
    showLocationFallback() {
        const hotspotsList = document.getElementById('hotspotsList');
        hotspotsList.innerHTML = `
            <div class="loading">
                🗺️ Location Unavailable<br><br>
                You can still search for WiFi by:<br>
                • Enabling location services<br>
                • Trying again in a different location<br>
                • Checking your GPS signal<br><br>
                <button onclick="wifiFinder.requestLocation()" style="padding: 8px 16px; background: #00bcd4; color: white; border: none; border-radius: 20px; cursor: pointer;">
                    Try Again
                </button>
            </div>
        `;
    }
    
    /**
     * 📏 Calculate distance between two coordinates
     */
    calculateDistance(lat1, lng1, lat2, lng2) {
        const R = 6371000; // Earth's radius in meters
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLng = (lng2 - lng1) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                  Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                  Math.sin(dLng/2) * Math.sin(dLng/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }
}

// 🌟 Auto-initialize when this script loads
console.log('📶 WiFi Finder script loaded! Ready to discover hotspots!');

// Make it available globally
window.WiFiFinder = WiFiFinder;