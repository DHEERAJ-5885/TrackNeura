/**
 * 🧠 SMART BRAIN - Real-Time Intelligent Support Orchestrator
 * 
 * This is like a tiny talking baby robot's brain that:
 * • Listens carefully to what users ask
 * • Thinks about the best answer using real project knowledge
 * • Responds honestly and helpfully
 * • Never lies or makes up answers
 * 
 * Think of it as teaching a super-smart kindergarten assistant!
 */

class SmartBrain {
    constructor() {
        console.log('🧠 Smart Brain initializing... Hello there!');
        
        // These are all the smart things our chatbot knows about!
        this.knowledgeBase = {
            // Auto-Healing Upload Engine Knowledge
            autoHealing: {
                keywords: ['heal', 'healing', 'auto-heal', 'fix', 'repair', 'broken', 'corrupt', 'retry', 'failed'],
                responses: [
                    "🩺 Our Auto-Healing Upload Engine is like a gentle doctor for your files! It automatically detects problems and fixes them by retrying failed chunks up to 3 times.",
                    "✨ When uploads get hurt, the healing engine jumps into action! It uses smart retry logic with exponential backoff (2s, 4s, 8s delays) to give your files the best chance.",
                    "🔧 The healing system can detect corruption, network issues, and server problems - then automatically tries different approaches to make your upload successful!"
                ]
            },
            
            // Speed and Performance Knowledge
            speed: {
                keywords: ['speed', 'fast', 'slow', 'performance', 'optimize', 'quick', 'delay', 'time'],
                responses: [
                    "🚀 Your system uses smart chunking (256KB pieces) and concurrent uploads to maximize speed! The Priority Engine also makes important files go first.",
                    "⚡ Speed depends on your network and file size. Large files are split into chunks and uploaded in parallel for the fastest possible transfer!",
                    "🎯 The Dynamic Queue Scheduler automatically adjusts upload speed based on network conditions - it's like having a smart traffic controller!"
                ]
            },
            
            // Security Knowledge
            security: {
                keywords: ['secure', 'security', 'safe', 'privacy', 'protect', 'encrypt', 'checksum'],
                responses: [
                    "🔒 Every file chunk gets a unique checksum (like a fingerprint) to verify it arrived safely without corruption or tampering.",
                    "🛡️ Your uploads use secure HTTP connections and each chunk is verified independently - if any piece gets damaged, it's automatically re-uploaded!",
                    "✅ The system creates unique upload IDs and stores metadata securely. Only you can access your upload sessions and file data."
                ]
            },
            
            // Resume and Recovery Knowledge
            resume: {
                keywords: ['resume', 'continue', 'pause', 'stop', 'restart', 'recover', 'progress'],
                responses: [
                    "⏯️ You can pause and resume uploads anytime! The system remembers exactly where you left off and continues from that chunk.",
                    "🔄 If your internet drops or browser closes, don't worry! Your progress is saved and you can resume right where you stopped.",
                    "💾 Upload states are persistent - even if you refresh the page, your healing uploads remember their progress and keep going!"
                ]
            },
            
            // Network and Connectivity Knowledge
            network: {
                keywords: ['network', 'internet', 'connection', 'wifi', 'offline', 'online', 'disconnect'],
                responses: [
                    "📡 The Network Monitor watches your connection in real-time! When internet drops, uploads pause automatically and resume when you're back online.",
                    "🌐 If network issues occur, the system intelligently waits and retries instead of failing completely - like a patient friend who waits for you!",
                    "📶 Your connection status is monitored continuously, so uploads adapt to network changes and give you the best possible experience."
                ]
            },
            
            // Priority Engine Knowledge
            priority: {
                keywords: ['priority', 'important', 'urgent', 'first', 'order', 'queue', 'smart'],
                responses: [
                    "🎯 The Priority Engine uses machine learning to automatically detect which files are most important! It considers file type, size, name patterns, and user behavior.",
                    "⭐ Important files (like documents, presentations, code) get uploaded first, while less critical files (like large media) wait their turn - it's like having a smart assistant!",
                    "🧠 The ML model learns from your usage patterns to get better at prioritizing what matters most to you personally."
                ]
            },
            
            // Corruption and Error Handling
            corruption: {
                keywords: ['corrupt', 'error', 'broken', 'damage', 'checksum', 'integrity', 'verify'],
                responses: [
                    "🔍 Every chunk gets checked with MD5 checksums! If any corruption is detected, that piece is automatically re-uploaded until it's perfect.",
                    "💔 When files get damaged during transfer, the Jump-Back Recovery system goes back a few chunks to double-check and re-upload any problems.",
                    "✨ The system has multiple layers of protection: checksums, retry logic, corruption detection, and automatic healing - your files are super safe!"
                ]
            },
            
            // Dashboard and Monitoring
            dashboard: {
                keywords: ['dashboard', 'status', 'monitor', 'track', 'view', 'progress', 'stats'],
                responses: [
                    "📊 The dashboard shows real-time upload progress, healing events, network status, and system health - like a mission control center!",
                    "👀 You can watch live progress bars, see which chunks are uploading, track retry attempts, and monitor your connection status.",
                    "📈 All your upload history, success rates, and system statistics are beautifully displayed so you always know what's happening!"
                ]
            }
        };
        
        // Friendly fallback responses when we're not sure
        this.fallbackResponses = [
            "🤔 I'm still learning about that! But I know lots about uploads, healing, priorities, and network monitoring. Try asking about those!",
            "💭 Hmm, I'm not quite sure about that specific question. I'm great at helping with file transfers, auto-healing, and system features though!",
            "🌟 That's an interesting question! I specialize in upload healing, priority systems, and network monitoring. What would you like to know about those?",
            "🎓 I'm still studying that topic! But I'm an expert on auto-healing uploads, smart priorities, and recovery systems. Ask me about those!"
        ];
        
        // Common greetings and social responses
        this.socialResponses = {
            greetings: {
                keywords: ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
                responses: [
                    "👋 Hello there! I'm your Smart Assistant, ready to help with anything about uploads, healing, priorities, or network monitoring!",
                    "🌟 Hi! I'm here to help you understand how this amazing file-transfer system works. What would you like to know?",
                    "😊 Greetings! I'm your friendly AI assistant, specializing in auto-healing uploads and smart file management. How can I help?"
                ]
            },
            thanks: {
                keywords: ['thank', 'thanks', 'appreciate', 'helpful'],
                responses: [
                    "😊 You're so welcome! I love helping you understand this awesome system!",
                    "🌟 Happy to help! That's what I'm here for - making file transfers easy and stress-free!",
                    "💝 Aww, thank you! I enjoy explaining how all these smart features work together!"
                ]
            }
        };
    }
    
    /**
     * 🎯 Main thinking function - this is where the magic happens!
     * Like teaching a child to read a question and find the best answer.
     */
    async processMessage(userMessage) {
        try {
            console.log('🤔 Smart Brain thinking about:', userMessage);
            
            // Clean up the message (like helping a child speak clearly)
            const cleanMessage = userMessage.toLowerCase().trim();
            
            // First, check if it's a social interaction
            const socialResponse = this.checkSocialInteraction(cleanMessage);
            if (socialResponse) {
                return this.formatResponse(socialResponse, 'social');
            }
            
            // Find the best knowledge category
            const bestMatch = this.findBestMatch(cleanMessage);
            
            if (bestMatch) {
                const response = this.selectRandomResponse(bestMatch.responses);
                return this.formatResponse(response, bestMatch.category);
            }
            
            // If no good match, use a friendly fallback
            const fallback = this.selectRandomResponse(this.fallbackResponses);
            return this.formatResponse(fallback, 'fallback');
            
        } catch (error) {
            console.error('💔 Smart Brain had a little hiccup:', error);
            return this.formatResponse(
                "😅 Oops! I had a tiny brain freeze there. Please try asking your question again!",
                'error'
            );
        }
    }
    
    /**
     * 🔍 Find the best matching knowledge category
     * Like teaching a child to match toys with the right boxes!
     */
    findBestMatch(message) {
        let bestScore = 0;
        let bestCategory = null;
        let bestMatch = null;
        
        // Check each knowledge category
        for (const [category, knowledge] of Object.entries(this.knowledgeBase)) {
            let score = 0;
            
            // Count how many keywords match
            for (const keyword of knowledge.keywords) {
                if (message.includes(keyword)) {
                    score += 1;
                    // Bonus points for exact word matches
                    const wordBoundary = new RegExp(`\\b${keyword}\\b`, 'i');
                    if (wordBoundary.test(message)) {
                        score += 1;
                    }
                }
            }
            
            // Remember the best match
            if (score > bestScore) {
                bestScore = score;
                bestCategory = category;
                bestMatch = knowledge;
            }
        }
        
        // Only return if we found a decent match
        if (bestScore > 0) {
            return {
                category: bestCategory,
                score: bestScore,
                responses: bestMatch.responses
            };
        }
        
        return null;
    }
    
    /**
     * 👋 Check for social interactions like greetings
     * Like teaching a child good manners!
     */
    checkSocialInteraction(message) {
        for (const [type, social] of Object.entries(this.socialResponses)) {
            for (const keyword of social.keywords) {
                if (message.includes(keyword)) {
                    return this.selectRandomResponse(social.responses);
                }
            }
        }
        return null;
    }
    
    /**
     * 🎲 Pick a random response to keep things interesting
     * Like having different ways to explain the same thing!
     */
    selectRandomResponse(responses) {
        const randomIndex = Math.floor(Math.random() * responses.length);
        return responses[randomIndex];
    }
    
    /**
     * ✨ Format the final response with metadata
     * Like putting a pretty bow on a gift!
     */
    formatResponse(message, category) {
        return {
            message: message,
            category: category,
            timestamp: new Date().toISOString(),
            confidence: category === 'fallback' ? 'low' : 'high'
        };
    }
    
    /**
     * 🎓 Get available help topics
     * Like showing a child all the fun things they can learn about!
     */
    getHelpTopics() {
        return {
            topics: [
                { name: 'Auto-Healing', description: 'How the system fixes broken uploads automatically' },
                { name: 'Speed & Performance', description: 'Making uploads as fast as possible' },
                { name: 'Security', description: 'Keeping your files safe and secure' },
                { name: 'Resume & Recovery', description: 'Pausing and continuing uploads' },
                { name: 'Network Monitoring', description: 'Watching your internet connection' },
                { name: 'Priority System', description: 'Smart file ordering and ML prioritization' },
                { name: 'Corruption Detection', description: 'Verifying file integrity and fixing problems' },
                { name: 'Dashboard', description: 'Monitoring and tracking your uploads' }
            ],
            examples: [
                "How does auto-healing work?",
                "Why are my uploads so fast?",
                "Are my files secure?",
                "Can I resume a paused upload?",
                "What happens if my internet disconnects?",
                "How does the priority system choose which files to upload first?"
            ]
        };
    }
}

// Make it available globally (like putting it in the toy box for everyone!)
window.SmartBrain = SmartBrain;

console.log('🧠 Smart Brain loaded and ready to help! 🌟');