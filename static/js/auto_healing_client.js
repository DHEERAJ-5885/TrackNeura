/**
 * ⭐ Auto-Healing Upload Client ⭐
 * ===============================
 * 
 * Hello tiny developer! This is like having a magic healing wand for your uploads!
 * 
 * Think of it like this:
 * - Your files are like little birds trying to fly to a tree
 * - Sometimes they get tired and need to rest (pause)
 * - Sometimes they get lost and need to try again (retry)
 * - We remember exactly where each bird was so they don't start over (resume)
 * - We check if each bird arrived safely and isn't hurt (corruption check)
 * 
 * This system watches the internet like a caring parent watching children play! 👶✨
 */

class AutoHealingUploadClient {
    constructor(options = {}) {
        // Baby, let's set up our healing powers!
        this.maxRetries = options.maxRetries || 5;
        this.baseRetryDelay = options.baseRetryDelay || 1000; // 1 second
        this.chunkSize = options.chunkSize || 1024 * 1024; // 1MB default
        this.baseUrl = options.baseUrl || '/api';
        
        // Our memory systems (like a friendly elephant that never forgets!)
        this.uploadStates = new Map(); // Active uploads
        this.networkStatus = true; // Is our internet playground open?
        this.healingAnimations = new Map(); // Pretty animations to show healing
        
        // Set up our network guardian (watches internet like a lighthouse!)
        this.setupNetworkWatcher();
        
        // Restore any uploads that were sleeping
        this.restoreUploadStates();
        
        console.log('🩺 Auto-Healing Upload Client initialized! Ready to heal! ✨');
    }
    
    /**
     * Baby, this watches the internet like a caring parent!
     * When the internet goes away, we pause everything and wait patiently.
     * When it comes back, we continue where we left off!
     */
    setupNetworkWatcher() {
        // Listen for when internet goes away (like when the playground closes)
        window.addEventListener('offline', () => {
            console.log('📵 Internet went away, pausing all uploads...');
            this.networkStatus = false;
            this.pauseAllUploads();
            this.showNetworkMessage('Waiting for internet...', 'warning');
        });
        
        // Listen for when internet comes back (like when the playground reopens!)
        window.addEventListener('online', () => {
            console.log('📶 Internet is back! Resuming uploads...');
            this.networkStatus = true;
            this.resumeAllUploads();
            this.showNetworkMessage('Internet restored! Continuing uploads...', 'success');
        });
        
        // Also check network strength every few seconds
        setInterval(() => {
            this.checkNetworkStrength();
        }, 3000);
    }
    
    /**
     * Baby, this checks how strong our internet is!
     * Like checking if the bridge to the playground is sturdy.
     */
    async checkNetworkStrength() {
        try {
            const startTime = Date.now();
            const response = await fetch(`${this.baseUrl}/ping`, { 
                method: 'HEAD',
                cache: 'no-cache' 
            });
            const endTime = Date.now();
            
            const latency = endTime - startTime;
            const isStrong = response.ok && latency < 2000; // Less than 2 seconds
            
            if (!isStrong && this.networkStatus) {
                console.log('⚠️ Network seems weak, adjusting chunk sizes...');
                this.adjustChunkSizesForWeakNetwork();
            }
            
        } catch (error) {
            console.log('📵 Network check failed, might be offline');
            if (this.networkStatus) {
                this.networkStatus = false;
                this.pauseAllUploads();
            }
        }
    }
    
    /**
     * Baby, this makes our file chunks smaller when internet is wobbly!
     * Like cutting food into smaller pieces when someone has trouble eating.
     */
    adjustChunkSizesForWeakNetwork() {
        for (let [uploadId, state] of this.uploadStates) {
            if (state.status === 'uploading') {
                const newChunkSize = Math.max(state.chunkSize / 2, 64 * 1024); // At least 64KB
                state.chunkSize = newChunkSize;
                console.log(`🔧 Adjusted chunk size for ${uploadId} to ${newChunkSize} bytes`);
            }
        }
    }
    
    /**
     * Baby, this saves our upload progress so we never forget!
     * Like writing in a diary before going to sleep.
     */
    saveUploadState(uploadId, state) {
        try {
            const stateData = {
                uploadId,
                timestamp: new Date().toISOString(),
                state: state
            };
            
            localStorage.setItem(`healing_upload_${uploadId}`, JSON.stringify(stateData));
            console.log(`💾 Saved progress for upload ${uploadId}`);
            
        } catch (error) {
            console.warn('⚠️ Could not save upload state:', error);
        }
    }
    
    /**
     * Baby, this reads our old progress like opening a favorite book!
     * We can continue exactly where we left off.
     */
    loadUploadState(uploadId) {
        try {
            const saved = localStorage.getItem(`healing_upload_${uploadId}`);
            if (saved) {
                const stateData = JSON.parse(saved);
                console.log(`📖 Found saved progress for upload ${uploadId}`);
                return stateData.state;
            }
        } catch (error) {
            console.warn('⚠️ Could not load upload state:', error);
        }
        return null;
    }
    
    /**
     * Baby, this wakes up any uploads that were sleeping!
     * Like gently waking up children after a nap.
     */
    restoreUploadStates() {
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith('healing_upload_')) {
                const uploadId = key.replace('healing_upload_', '');
                const state = this.loadUploadState(uploadId);
                
                if (state && state.status !== 'completed') {
                    console.log(`🔄 Restoring upload ${uploadId}`);
                    this.uploadStates.set(uploadId, state);
                }
            }
        }
    }
    
    /**
     * Baby, this calculates a special fingerprint for each chunk!
     * Like how every person has unique fingerprints, every chunk gets a unique ID.
     */
    async calculateChunkChecksum(chunkData) {
        // Use the browser's built-in crypto for security (like a very smart lock!)
        const hashBuffer = await crypto.subtle.digest('SHA-256', chunkData);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        return hashHex;
    }
    
    /**
     * Baby, this decides how long to wait before trying again!
     * Like when you fall off your bike - we wait a little, then try again.
     */
    calculateRetryDelay(attemptNumber) {
        const delay = this.baseRetryDelay * Math.pow(2, attemptNumber - 1);
        return Math.min(delay, 60000); // Never wait more than 1 minute
    }
    
    /**
     * Baby, this shows pretty messages to tell you what's happening!
     * Like a friendly nurse explaining what medicine you're getting.
     */
    showHealingMessage(uploadId, message, type = 'info') {
        const event = new CustomEvent('healingUpdate', {
            detail: {
                uploadId,
                message,
                type,
                timestamp: new Date().toISOString()
            }
        });
        window.dispatchEvent(event);
        
        console.log(`🩹 ${message}`);
    }
    
    /**
     * Baby, this shows network status messages!
     * Like a traffic light telling you when it's safe to cross.
     */
    showNetworkMessage(message, type) {
        const event = new CustomEvent('networkStatusUpdate', {
            detail: { message, type, timestamp: new Date().toISOString() }
        });
        window.dispatchEvent(event);
    }
    
    /**
     * Baby, this tries to upload a chunk and heals it if something goes wrong!
     * Like a gentle doctor who keeps trying different treatments.
     */
    async healChunkUpload(uploadId, chunkNumber, chunkData, file) {
        const state = this.uploadStates.get(uploadId);
        const retryKey = `${uploadId}_${chunkNumber}`;
        
        // Calculate checksum for this chunk (like taking a photo for ID)
        const checksum = await this.calculateChunkChecksum(chunkData);
        
        let currentRetry = state.retryCount?.[retryKey] || 0;
        
        for (let attempt = currentRetry + 1; attempt <= this.maxRetries; attempt++) {
            try {
                // Show healing message
                if (attempt > 1) {
                    this.showHealingMessage(uploadId, `🩹 Retrying chunk ${chunkNumber + 1}... (attempt ${attempt}/${this.maxRetries})`, 'warning');
                } else {
                    this.showHealingMessage(uploadId, `📤 Uploading chunk ${chunkNumber + 1}...`, 'info');
                }
                
                // Create form data (like packing a gift to send)
                const formData = new FormData();
                formData.append('file', new Blob([chunkData]), file.name);
                formData.append('chunk_number', chunkNumber);
                formData.append('total_chunks', state.totalChunks);
                formData.append('upload_id', uploadId);
                formData.append('checksum', checksum);
                formData.append('chunk_size', chunkData.length);
                
                // Send the chunk with love and hope!
                const response = await fetch(`${this.baseUrl}/upload_chunk`, {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const result = await response.json();
                
                if (result.success) {
                    // Check if server checksum matches (make sure chunk wasn't hurt)
                    if (result.checksum && result.checksum !== checksum) {
                        console.warn(`💔 Corruption detected in chunk ${chunkNumber}!`);
                        this.showHealingMessage(uploadId, `💔 Fixing a broken piece (chunk ${chunkNumber + 1})...`, 'error');
                        continue; // Try again
                    }
                    
                    // Success! Clear retry count
                    if (state.retryCount) {
                        delete state.retryCount[retryKey];
                    }
                    
                    if (attempt > 1) {
                        this.showHealingMessage(uploadId, `✅ Chunk ${chunkNumber + 1} healed successfully after ${attempt} attempts!`, 'success');
                    } else {
                        this.showHealingMessage(uploadId, `✅ Chunk ${chunkNumber + 1} uploaded successfully!`, 'success');
                    }
                    return { success: true, checksum };
                }
                
                throw new Error(result.error || 'Unknown upload error');
                
            } catch (error) {
                console.warn(`⚠️ Chunk ${chunkNumber} attempt ${attempt} failed:`, error);
                
                // Record the retry
                if (!state.retryCount) state.retryCount = {};
                state.retryCount[retryKey] = attempt;
                
                // Wait before trying again (like resting between attempts)
                if (attempt < this.maxRetries) {
                    const delay = this.calculateRetryDelay(attempt);
                    this.showHealingMessage(uploadId, `⏳ Resting for ${(delay/1000).toFixed(1)}s before trying again...`, 'info');
                    await new Promise(resolve => setTimeout(resolve, delay));
                    
                    // Check if network is still available
                    if (!this.networkStatus) {
                        this.showHealingMessage(uploadId, '📵 Waiting for internet to come back...', 'warning');
                        return { success: false, error: 'Network unavailable', shouldPause: true };
                    }
                } else {
                    this.showHealingMessage(uploadId, `💔 Chunk ${chunkNumber + 1} failed after ${this.maxRetries} attempts`, 'error');
                }
            }
        }
        
        // All retries failed
        return { success: false, error: `Chunk ${chunkNumber + 1} failed after ${this.maxRetries} attempts` };
    }
    
    /**
     * Baby, this checks which chunks the server already has!
     * Like asking "which toys are already in the toy box?"
     */
    async checkExistingChunks(uploadId) {
        try {
            const response = await fetch(`${this.baseUrl}/check_chunks/${uploadId}`);
            if (response.ok) {
                const result = await response.json();
                return result.completed_chunks || [];
            }
        } catch (error) {
            console.warn('⚠️ Could not check existing chunks:', error);
        }
        return [];
    }
    
    /**
     * Baby, this is our main healing function for entire file uploads!
     * Like being a complete doctor for a patient from start to finish.
     */
    async healFileUpload(file, options = {}) {
        const uploadId = options.uploadId || `upload_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        const chunkSize = options.chunkSize || this.chunkSize;
        
        console.log(`🎯 Starting healing upload for ${file.name} (ID: ${uploadId})`);
        
        // Create or restore upload state
        let state = this.loadUploadState(uploadId) || {
            uploadId,
            fileName: file.name,
            fileSize: file.size,
            chunkSize,
            totalChunks: Math.ceil(file.size / chunkSize),
            completedChunks: new Set(),
            failedChunks: new Set(),
            retryCount: {},
            status: 'initializing',
            createdAt: new Date().toISOString(),
            healingEvents: []
        };
        
        this.uploadStates.set(uploadId, state);
        
        // Check what chunks already exist on server
        this.showHealingMessage(uploadId, 'Checking what parts are already uploaded...', 'info');
        const existingChunks = await this.checkExistingChunks(uploadId);
        existingChunks.forEach(chunk => state.completedChunks.add(chunk));
        
        const totalChunks = state.totalChunks;
        let currentChunk = 0;
        let consecutiveFailures = 0;
        
        state.status = 'uploading';
        this.saveUploadState(uploadId, state);
        
        // Create a healing progress tracker
        const progressTracker = {
            total: totalChunks,
            completed: state.completedChunks.size,
            failed: 0,
            healing: 0
        };
        
        // Main healing loop (like a gentle nurse making rounds)
        while (currentChunk < totalChunks && this.networkStatus) {
            // Skip already completed chunks
            if (state.completedChunks.has(currentChunk)) {
                currentChunk++;
                continue;
            }
            
            // Check if we need to jump back (like going back to check earlier work)
            if (consecutiveFailures >= 3) {
                const jumpBackTo = Math.max(0, currentChunk - 2);
                console.log(`🔄 Jumping back from chunk ${currentChunk} to ${jumpBackTo}`);
                this.showHealingMessage(uploadId, `Going back to double-check earlier pieces...`, 'warning');
                
                // Revalidate previous chunks
                for (let i = jumpBackTo; i < currentChunk; i++) {
                    if (state.completedChunks.has(i)) {
                        state.completedChunks.delete(i); // Will be re-validated
                    }
                }
                
                currentChunk = jumpBackTo;
                consecutiveFailures = 0;
                continue;
            }
            
            // Read chunk data
            const start = currentChunk * chunkSize;
            const end = Math.min(start + chunkSize, file.size);
            const chunkData = file.slice(start, end);
            const arrayBuffer = await chunkData.arrayBuffer();
            
            // Try to heal this chunk
            progressTracker.healing++;
            this.updateProgress(uploadId, progressTracker);
            
            const result = await this.healChunkUpload(uploadId, currentChunk, arrayBuffer, file);
            
            if (result.success) {
                state.completedChunks.add(currentChunk);
                progressTracker.completed++;
                progressTracker.healing--;
                consecutiveFailures = 0;
                
                // Add healing event
                state.healingEvents.push({
                    timestamp: new Date().toISOString(),
                    type: 'chunk_completed',
                    chunkNumber: currentChunk,
                    checksum: result.checksum
                });
                
            } else if (result.shouldPause) {
                // Network issues, pause upload
                state.status = 'paused_network';
                this.saveUploadState(uploadId, state);
                return { success: false, uploadId, status: 'paused', reason: 'network' };
                
            } else {
                state.failedChunks.add(currentChunk);
                progressTracker.failed++;
                progressTracker.healing--;
                consecutiveFailures++;
                
                // Add healing event
                state.healingEvents.push({
                    timestamp: new Date().toISOString(),
                    type: 'chunk_failed',
                    chunkNumber: currentChunk,
                    error: result.error
                });
            }
            
            // Update progress
            this.updateProgress(uploadId, progressTracker);
            this.saveUploadState(uploadId, state);
            
            currentChunk++;
            
            // Small pause between chunks (like taking a breath)
            await new Promise(resolve => setTimeout(resolve, 50));
        }
        
        // Check final status
        if (!this.networkStatus) {
            state.status = 'paused_network';
            this.saveUploadState(uploadId, state);
            return { success: false, uploadId, status: 'paused', reason: 'network' };
        }
        
        if (state.completedChunks.size === totalChunks) {
            // Complete success!
            state.status = 'completed';
            state.completedAt = new Date().toISOString();
            this.saveUploadState(uploadId, state);
            
            this.showHealingMessage(uploadId, `🎉 ${file.name} uploaded successfully!`, 'success');
            
            // Clean up
            localStorage.removeItem(`healing_upload_${uploadId}`);
            this.uploadStates.delete(uploadId);
            
            return { 
                success: true, 
                uploadId, 
                totalChunks, 
                healingEvents: state.healingEvents.length 
            };
            
        } else {
            // Partial failure
            state.status = 'failed';
            this.saveUploadState(uploadId, state);
            
            const failedChunkCount = state.failedChunks.size;
            const errorMessage = `Upload incomplete: ${state.completedChunks.size}/${totalChunks} chunks completed, ${failedChunkCount} chunks failed`;
            
            this.showHealingMessage(uploadId, `💔 ${errorMessage}. You can retry this upload!`, 'error');
            
            return { 
                success: false, 
                uploadId, 
                status: 'failed', 
                completed: state.completedChunks.size,
                total: totalChunks,
                failed: failedChunkCount,
                error: errorMessage
            };
        }
    }
    
    /**
     * Baby, this updates the pretty progress display!
     * Like a cheerful progress chart showing how much homework is done.
     */
    updateProgress(uploadId, progress) {
        const percentage = (progress.completed / progress.total) * 100;
        
        const event = new CustomEvent('healingProgress', {
            detail: {
                uploadId,
                percentage: Math.round(percentage * 100) / 100,
                completed: progress.completed,
                total: progress.total,
                failed: progress.failed,
                healing: progress.healing,
                status: percentage === 100 ? 'completed' : 'uploading'
            }
        });
        
        window.dispatchEvent(event);
    }
    
    /**
     * Baby, this pauses all uploads when internet goes away!
     * Like telling all children to sit quietly when the teacher leaves.
     */
    pauseAllUploads() {
        for (let [uploadId, state] of this.uploadStates) {
            if (state.status === 'uploading') {
                state.status = 'paused_network';
                this.saveUploadState(uploadId, state);
                this.showHealingMessage(uploadId, 'Upload paused - waiting for internet...', 'warning');
            }
        }
    }
    
    /**
     * Baby, this resumes all uploads when internet comes back!
     * Like telling children they can continue playing when teacher returns.
     */
    resumeAllUploads() {
        for (let [uploadId, state] of this.uploadStates) {
            if (state.status === 'paused_network') {
                state.status = 'uploading';
                this.saveUploadState(uploadId, state);
                this.showHealingMessage(uploadId, 'Resuming upload...', 'success');
                
                // Continue the upload (you would call healFileUpload again here)
                console.log(`🔄 Ready to resume upload ${uploadId}`);
            }
        }
    }
    
    /**
     * Baby, this gets a nice summary of all healing activities!
     * Like a report card showing how well our uploads are doing.
     */
    getHealingReport(uploadId) {
        const state = this.uploadStates.get(uploadId) || this.loadUploadState(uploadId);
        
        if (!state) {
            return null;
        }
        
        const events = state.healingEvents || [];
        const completed = events.filter(e => e.type === 'chunk_completed').length;
        const failed = events.filter(e => e.type === 'chunk_failed').length;
        const retries = Object.keys(state.retryCount || {}).length;
        
        return {
            uploadId,
            fileName: state.fileName,
            status: state.status,
            progress: (completed / state.totalChunks) * 100,
            totalChunks: state.totalChunks,
            completedChunks: completed,
            failedChunks: failed,
            totalRetries: retries,
            healingEvents: events.length,
            createdAt: state.createdAt,
            completedAt: state.completedAt
        };
    }
}

// Create global healing client (like having a friendly doctor always available!)
window.AutoHealingUploadClient = AutoHealingUploadClient;

console.log('✨ Auto-Healing Upload Client loaded! Ready to heal your uploads! 🩺');