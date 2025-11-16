/**
 * ⭐ Healing Upload Integration ⭐
 * ===============================
 * 
 * Hello beautiful developer! This adds healing magic to your existing upload page!
 * Like adding a gentle nurse to watch over your playground.
 * 
 * This works with your existing upload.html and makes uploads super strong! 💪✨
 */

class HealingUploadUI {
    constructor() {
        this.healingClient = null;
        this.activeUploads = new Map();
        this.setupHealingUI();
        this.initializeHealingClient();
        
        console.log('🎨 Healing Upload UI initialized! Making uploads beautiful and strong! ✨');
    }
    
    /**
     * Baby, this creates our healing client (like hiring a gentle doctor)!
     */
    async initializeHealingClient() {
        if (typeof AutoHealingUploadClient !== 'undefined') {
            this.healingClient = new AutoHealingUploadClient({
                maxRetries: 5,
                baseRetryDelay: 1000, // 1 second
                chunkSize: 1024 * 1024, // 1MB chunks
                baseUrl: '/api'
            });
            
            // Listen for healing events
            this.setupHealingEventListeners();
            
            console.log('🩺 Healing client ready! Your uploads are now protected! 💝');
        } else {
            console.warn('⚠️ AutoHealingUploadClient not available - uploads will use basic mode');
        }
    }
    
    /**
     * Baby, this listens for healing messages and shows them prettily!
     */
    setupHealingEventListeners() {
        // Listen for healing progress updates
        window.addEventListener('healingProgress', (event) => {
            const { uploadId, percentage, completed, total, failed, healing, status } = event.detail;
            this.updateHealingProgress(uploadId, percentage, completed, total, failed, healing, status);
        });
        
        // Listen for healing messages
        window.addEventListener('healingUpdate', (event) => {
            const { uploadId, message, type, timestamp } = event.detail;
            this.showHealingMessage(uploadId, message, type);
        });
        
        // Listen for network status updates
        window.addEventListener('networkStatusUpdate', (event) => {
            const { message, type, timestamp } = event.detail;
            this.showNetworkStatus(message, type);
        });
    }
    
    /**
     * Baby, this creates beautiful healing UI elements!
     * Like decorating a hospital room to make it cheerful.
     */
    setupHealingUI() {
        // Create healing status container
        const healingContainer = document.createElement('div');
        healingContainer.id = 'healing-status-container';
        healingContainer.className = 'healing-status-container';
        healingContainer.innerHTML = `
            <div class="healing-header">
                <h3>🩺 Auto-Healing Upload Status</h3>
                <div class="network-status" id="network-status">
                    <span class="status-indicator online"></span>
                    <span class="status-text">Network: Healthy</span>
                </div>
            </div>
            <div class="healing-uploads" id="healing-uploads">
                <!-- Active healing uploads will appear here -->
            </div>
        `;
        
        // Add healing styles
        const healingStyles = document.createElement('style');
        healingStyles.textContent = `
            .healing-status-container {
                background: linear-gradient(135deg, #f8f9ff 0%, #e8f4ff 100%);
                border: 2px solid #d4e7ff;
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .healing-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px solid #d4e7ff;
            }
            
            .healing-header h3 {
                margin: 0;
                color: #2c5282;
                font-size: 1.2em;
            }
            
            .network-status {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.9em;
            }
            
            .status-indicator {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }
            
            .status-indicator.online {
                background-color: #48bb78;
                box-shadow: 0 0 0 0 rgba(72, 187, 120, 0.7);
            }
            
            .status-indicator.offline {
                background-color: #f56565;
                box-shadow: 0 0 0 0 rgba(245, 101, 101, 0.7);
            }
            
            .status-indicator.weak {
                background-color: #ed8936;
                box-shadow: 0 0 0 0 rgba(237, 137, 54, 0.7);
            }
            
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(72, 187, 120, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(72, 187, 120, 0); }
                100% { box-shadow: 0 0 0 0 rgba(72, 187, 120, 0); }
            }
            
            .healing-upload-item {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            
            .healing-upload-item:hover {
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
                transform: translateY(-1px);
            }
            
            .upload-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }
            
            .upload-filename {
                font-weight: 600;
                color: #2d3748;
                font-size: 1em;
            }
            
            .upload-status {
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: 500;
                text-transform: uppercase;
            }
            
            .upload-status.uploading {
                background-color: #bee3f8;
                color: #2b6cb0;
            }
            
            .upload-status.healing {
                background-color: #fbb6ce;
                color: #b83280;
                animation: healing-pulse 1.5s infinite;
            }
            
            .upload-status.completed {
                background-color: #c6f6d5;
                color: #276749;
            }
            
            .upload-status.failed {
                background-color: #fed7d7;
                color: #c53030;
            }
            
            @keyframes healing-pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            
            .healing-progress {
                margin: 10px 0;
            }
            
            .progress-bar {
                width: 100%;
                height: 8px;
                background-color: #e2e8f0;
                border-radius: 4px;
                overflow: hidden;
                position: relative;
            }
            
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #4299e1, #63b3ed);
                border-radius: 4px;
                transition: width 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .progress-fill.healing {
                background: linear-gradient(90deg, #ed64a6, #f687b3);
                animation: healing-gradient 2s infinite;
            }
            
            @keyframes healing-gradient {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }
            
            .progress-text {
                display: flex;
                justify-content: space-between;
                font-size: 0.8em;
                color: #4a5568;
                margin-top: 5px;
            }
            
            .healing-messages {
                max-height: 120px;
                overflow-y: auto;
                margin-top: 10px;
                padding: 10px;
                background-color: #f7fafc;
                border-radius: 6px;
                border: 1px solid #e2e8f0;
            }
            
            .healing-message {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 4px 0;
                font-size: 0.85em;
                border-bottom: 1px solid #e2e8f0;
            }
            
            .healing-message:last-child {
                border-bottom: none;
            }
            
            .message-icon {
                font-size: 1em;
            }
            
            .message-text {
                flex-grow: 1;
                color: #4a5568;
            }
            
            .message-time {
                font-size: 0.75em;
                color: #a0aec0;
            }
            
            .healing-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
                gap: 10px;
                margin-top: 10px;
                padding: 10px;
                background-color: #f7fafc;
                border-radius: 6px;
            }
            
            .stat-item {
                text-align: center;
            }
            
            .stat-value {
                font-size: 1.2em;
                font-weight: 700;
                color: #2d3748;
            }
            
            .stat-label {
                font-size: 0.7em;
                color: #718096;
                text-transform: uppercase;
                margin-top: 2px;
            }
            
            .network-message {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 10000;
                animation: slideIn 0.3s ease;
                max-width: 300px;
            }
            
            .network-message.success {
                background-color: #48bb78;
            }
            
            .network-message.warning {
                background-color: #ed8936;
            }
            
            .network-message.error {
                background-color: #f56565;
            }
            
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            .healing-actions {
                display: flex;
                gap: 10px;
                justify-content: center;
                margin: 10px 0;
            }
            
            .retry-btn, .cancel-btn {
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 0.9em;
                font-weight: 500;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .retry-btn {
                background: linear-gradient(135deg, #4299e1, #63b3ed);
                color: white;
            }
            
            .retry-btn:hover {
                background: linear-gradient(135deg, #3182ce, #4299e1);
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(66, 153, 225, 0.3);
            }
            
            .cancel-btn {
                background: linear-gradient(135deg, #f56565, #fc8181);
                color: white;
            }
            
            .cancel-btn:hover {
                background: linear-gradient(135deg, #e53e3e, #f56565);
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(245, 101, 101, 0.3);
            }
            
            .upload-status.retrying {
                background-color: #fbb6ce;
                color: #b83280;
                animation: healing-pulse 1.5s infinite;
            }
        `;
        
        // Add styles to page
        document.head.appendChild(healingStyles);
        
        // Find a good place to add the healing container
        const existingUploadArea = document.querySelector('.upload-area') || 
                                 document.querySelector('#upload-section') ||
                                 document.querySelector('main') ||
                                 document.body;
        
        if (existingUploadArea) {
            existingUploadArea.appendChild(healingContainer);
        }
    }
    
    /**
     * Baby, this starts a healing upload for a file!
     * Like taking a child to see a gentle doctor.
     */
    async startHealingUpload(file, options = {}) {
        if (!this.healingClient) {
            console.warn('⚠️ Healing client not available, using basic upload');
            return this.fallbackUpload(file, options);
        }
        
        const uploadId = options.uploadId || `healing_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        // Create UI for this upload
        this.createUploadUI(uploadId, file.name, file.size);
        
        // Store file reference for retry functionality
        this.activeUploads.set(uploadId, { 
            filename: file.name, 
            fileSize: file.size, 
            file: file,
            options: options,
            element: null,  // Will be set in createUploadUI
            status: 'uploading',
            retryCount: 0
        });
        
        try {
            // Start the healing upload
            const result = await this.healingClient.healFileUpload(file, {
                uploadId,
                chunkSize: options.chunkSize || 1024 * 1024 // 1MB
            });
            
            if (result.success) {
                this.showUploadComplete(uploadId, result);
                console.log(`🎉 Healing upload completed: ${file.name}`);
            } else {
                this.showUploadError(uploadId, result);
                console.error(`💔 Healing upload failed: ${file.name}`, result);
                
                // Update status for retry functionality
                const uploadInfo = this.activeUploads.get(uploadId);
                if (uploadInfo) {
                    uploadInfo.status = 'failed';
                    uploadInfo.lastError = result.error || 'Unknown error';
                }
            }
            
            return result;
            
        } catch (error) {
            console.error('💔 Healing upload error:', error);
            this.showUploadError(uploadId, { error: error.message });
            
            // Update status for retry functionality
            const uploadInfo = this.activeUploads.get(uploadId);
            if (uploadInfo) {
                uploadInfo.status = 'failed';
                uploadInfo.lastError = error.message;
            }
            
            return { success: false, error: error.message };
        }
    }
    
    /**
     * Baby, this creates a beautiful progress display for each upload!
     * Like making a personalized get-well card for each patient.
     */
    createUploadUI(uploadId, filename, fileSize) {
        const healingUploads = document.getElementById('healing-uploads');
        
        const uploadItem = document.createElement('div');
        uploadItem.className = 'healing-upload-item';
        uploadItem.id = `healing-upload-${uploadId}`;
        
        uploadItem.innerHTML = `
            <div class="upload-header">
                <div class="upload-filename">${filename}</div>
                <div class="upload-status uploading">Initializing</div>
            </div>
            
            <div class="healing-progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 0%"></div>
                </div>
                <div class="progress-text">
                    <span class="progress-percentage">0%</span>
                    <span class="progress-size">${this.formatFileSize(fileSize)}</span>
                </div>
            </div>
            
            <div class="healing-actions" id="actions-${uploadId}" style="display: none; margin: 10px 0;">
                <button class="retry-btn" onclick="window.healingUploadUI.retryUpload('${uploadId}')">
                    🔄 Retry Upload
                </button>
                <button class="cancel-btn" onclick="window.healingUploadUI.cancelUpload('${uploadId}')">
                    ❌ Cancel
                </button>
            </div>
            
            <div class="healing-stats">
                <div class="stat-item">
                    <div class="stat-value" id="completed-${uploadId}">0</div>
                    <div class="stat-label">Completed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="healing-${uploadId}">0</div>
                    <div class="stat-label">Healing</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="failed-${uploadId}">0</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="retries-${uploadId}">0</div>
                    <div class="stat-label">Retries</div>
                </div>
            </div>
            
            <div class="healing-messages" id="messages-${uploadId}">
                <div class="healing-message">
                    <span class="message-icon">🩺</span>
                    <span class="message-text">Starting healing upload...</span>
                    <span class="message-time">${new Date().toLocaleTimeString()}</span>
                </div>
            </div>
        `;
        
        healingUploads.appendChild(uploadItem);
        
        // Update the upload info with the element reference
        const uploadInfo = this.activeUploads.get(uploadId);
        if (uploadInfo) {
            uploadInfo.element = uploadItem;
        } else {
            this.activeUploads.set(uploadId, { filename, fileSize, element: uploadItem });
        }
    }
    
    /**
     * Baby, this updates the progress display with healing information!
     * Like updating a medical chart with the latest improvements.
     */
    updateHealingProgress(uploadId, percentage, completed, total, failed, healing, status) {
        const uploadItem = document.getElementById(`healing-upload-${uploadId}`);
        if (!uploadItem) return;
        
        // Update progress bar
        const progressFill = uploadItem.querySelector('.progress-fill');
        const progressPercentage = uploadItem.querySelector('.progress-percentage');
        
        if (progressFill && progressPercentage) {
            progressFill.style.width = `${percentage}%`;
            progressPercentage.textContent = `${percentage.toFixed(1)}%`;
            
            // Add healing animation if actively healing
            if (healing > 0) {
                progressFill.classList.add('healing');
            } else {
                progressFill.classList.remove('healing');
            }
        }
        
        // Update status
        const statusElement = uploadItem.querySelector('.upload-status');
        if (statusElement) {
            statusElement.className = 'upload-status ' + status;
            
            switch (status) {
                case 'uploading':
                    statusElement.textContent = healing > 0 ? 'Healing' : 'Uploading';
                    break;
                case 'completed':
                    statusElement.textContent = 'Completed';
                    break;
                case 'failed':
                    statusElement.textContent = 'Failed';
                    break;
                default:
                    statusElement.textContent = status;
            }
        }
        
        // Update stats
        const completedStat = document.getElementById(`completed-${uploadId}`);
        const healingStat = document.getElementById(`healing-${uploadId}`);
        const failedStat = document.getElementById(`failed-${uploadId}`);
        
        if (completedStat) completedStat.textContent = completed;
        if (healingStat) healingStat.textContent = healing;
        if (failedStat) failedStat.textContent = failed;
    }
    
    /**
     * Baby, this shows healing messages in a pretty way!
     * Like a nurse writing notes about how the patient is feeling.
     */
    showHealingMessage(uploadId, message, type) {
        const messagesContainer = document.getElementById(`messages-${uploadId}`);
        if (!messagesContainer) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = 'healing-message';
        
        // Choose emoji based on message type
        let emoji = '🩹'; // Default healing emoji
        switch (type) {
            case 'success': emoji = '✅'; break;
            case 'error': emoji = '💔'; break;
            case 'warning': emoji = '⚠️'; break;
            case 'info': emoji = 'ℹ️'; break;
        }
        
        messageElement.innerHTML = `
            <span class="message-icon">${emoji}</span>
            <span class="message-text">${message}</span>
            <span class="message-time">${new Date().toLocaleTimeString()}</span>
        `;
        
        messagesContainer.appendChild(messageElement);
        
        // Keep only the last 10 messages
        const messages = messagesContainer.querySelectorAll('.healing-message');
        if (messages.length > 10) {
            messages[0].remove();
        }
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    /**
     * Baby, this shows network status changes!
     * Like announcing when the playground opens or closes.
     */
    showNetworkStatus(message, type) {
        // Update network indicator
        const networkStatus = document.getElementById('network-status');
        if (networkStatus) {
            const indicator = networkStatus.querySelector('.status-indicator');
            const text = networkStatus.querySelector('.status-text');
            
            if (indicator && text) {
                indicator.className = `status-indicator ${type === 'success' ? 'online' : type === 'warning' ? 'weak' : 'offline'}`;
                text.textContent = message;
            }
        }
        
        // Show popup message
        const popup = document.createElement('div');
        popup.className = `network-message ${type}`;
        popup.textContent = message;
        
        document.body.appendChild(popup);
        
        // Remove popup after 3 seconds
        setTimeout(() => {
            popup.remove();
        }, 3000);
    }
    
    /**
     * Baby, this marks an upload as completed with celebration!
     * Like throwing a little party when someone gets better.
     */
    showUploadComplete(uploadId, result) {
        const uploadItem = document.getElementById(`healing-upload-${uploadId}`);
        if (!uploadItem) return;
        
        // Update status
        const statusElement = uploadItem.querySelector('.upload-status');
        if (statusElement) {
            statusElement.className = 'upload-status completed';
            statusElement.textContent = 'Completed';
        }
        
        // Show celebration message
        this.showHealingMessage(uploadId, 
            `🎉 Upload completed successfully! ${result.healingEvents || 0} healing events.`, 
            'success'
        );
        
        // Clean up after 30 seconds
        setTimeout(() => {
            uploadItem.style.opacity = '0.5';
            setTimeout(() => uploadItem.remove(), 5000);
        }, 30000);
    }
    
    /**
     * Baby, this shows when an upload couldn't be healed completely.
     * Like explaining that sometimes we need to try again later.
     */
    showUploadError(uploadId, result) {
        const uploadItem = document.getElementById(`healing-upload-${uploadId}`);
        if (!uploadItem) return;
        
        // Update status
        const statusElement = uploadItem.querySelector('.upload-status');
        if (statusElement) {
            statusElement.className = 'upload-status failed';
            statusElement.textContent = 'Failed';
        }
        
        // Show retry actions
        const actionsElement = document.getElementById(`actions-${uploadId}`);
        if (actionsElement) {
            actionsElement.style.display = 'flex';
        }
        
        // Show error message
        this.showHealingMessage(uploadId, 
            `💔 Upload failed: ${result.error || 'Unknown error'}. You can retry the upload!`, 
            'error'
        );
    }
    
    /**
     * Baby, this retries a failed upload!
     * Like giving a child another chance to climb the stairs.
     */
    async retryUpload(uploadId) {
        const uploadInfo = this.activeUploads.get(uploadId);
        if (!uploadInfo || !uploadInfo.file) {
            console.warn('⚠️ Cannot retry - upload info not found');
            return;
        }
        
        console.log(`🔄 Retrying upload: ${uploadInfo.filename}`);
        
        // Update retry count
        uploadInfo.retryCount = (uploadInfo.retryCount || 0) + 1;
        uploadInfo.status = 'retrying';
        
        // Update UI
        const statusElement = document.querySelector(`#healing-upload-${uploadId} .upload-status`);
        if (statusElement) {
            statusElement.className = 'upload-status uploading';
            statusElement.textContent = `Retrying (${uploadInfo.retryCount})`;
        }
        
        // Hide retry actions
        const actionsElement = document.getElementById(`actions-${uploadId}`);
        if (actionsElement) {
            actionsElement.style.display = 'none';
        }
        
        // Update retry count in stats
        const retryElement = document.getElementById(`retries-${uploadId}`);
        if (retryElement) {
            retryElement.textContent = uploadInfo.retryCount;
        }
        
        // Show retry message
        this.showHealingMessage(uploadId, 
            `🔄 Retrying upload (attempt ${uploadInfo.retryCount})...`, 
            'info'
        );
        
        // Reset progress
        const progressFill = document.querySelector(`#healing-upload-${uploadId} .progress-fill`);
        const progressPercentage = document.querySelector(`#healing-upload-${uploadId} .progress-percentage`);
        if (progressFill) progressFill.style.width = '0%';
        if (progressPercentage) progressPercentage.textContent = '0%';
        
        try {
            // Start the healing upload again
            const result = await this.healingClient.healFileUpload(uploadInfo.file, {
                uploadId: `${uploadId}_retry_${uploadInfo.retryCount}`,
                chunkSize: uploadInfo.options?.chunkSize || 512 * 1024 // Use smaller chunks for retry
            });
            
            if (result.success) {
                uploadInfo.status = 'completed';
                this.showUploadComplete(uploadId, result);
                console.log(`🎉 Retry successful: ${uploadInfo.filename}`);
            } else {
                uploadInfo.status = 'failed';
                uploadInfo.lastError = result.error || 'Retry failed';
                this.showUploadError(uploadId, result);
                console.error(`💔 Retry failed: ${uploadInfo.filename}`, result);
            }
            
        } catch (error) {
            console.error('💔 Retry error:', error);
            uploadInfo.status = 'failed';
            uploadInfo.lastError = error.message;
            this.showUploadError(uploadId, { error: error.message });
        }
    }
    
    /**
     * Baby, this cancels a failed upload!
     * Like deciding to try a different playground game.
     */
    cancelUpload(uploadId) {
        const uploadItem = document.getElementById(`healing-upload-${uploadId}`);
        if (uploadItem) {
            uploadItem.style.opacity = '0.5';
            uploadItem.style.transition = 'opacity 0.3s ease';
            
            // Show cancellation message
            this.showHealingMessage(uploadId, 
                '❌ Upload cancelled by user', 
                'info'
            );
            
            // Remove after animation
            setTimeout(() => {
                uploadItem.remove();
                this.activeUploads.delete(uploadId);
            }, 2000);
        }
    }
    
    /**
     * Baby, this formats file sizes nicely!
     * Like explaining how big something is in words a child would understand.
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    /**
     * Baby, this is a backup upload method for when healing isn't available.
     * Like having a simple Band-Aid when the fancy medicine isn't ready.
     */
    async fallbackUpload(file, options) {
        console.log('📋 Using fallback upload for:', file.name);
        
        // Use your existing upload logic here
        // This would integrate with whatever upload system you already have
        
        return {
            success: false,
            error: 'Healing system not available - please refresh and try again'
        };
    }
}

// Initialize healing UI when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.healingUploadUI = new HealingUploadUI();
    console.log('🎨 Healing Upload UI ready! Your uploads are now magical! ✨');
});

// Make it globally available for integration
window.HealingUploadUI = HealingUploadUI;