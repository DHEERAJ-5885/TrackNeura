/**
 * 🤖 REAL AI CHATBOT ASSISTANT - Powered by Gemini AI
 * 
 * This is like a beautiful chat room where users can talk to Google's Gemini AI!
 * It's designed to be:
 * • Intelligent and dynamic (real AI responses, not static)
 * • Beautiful and responsive
 * • Easy to use and understand
 * • Safe and error-free
 * 
 * Baby explanation:
 * • You type a question (anything you want!)
 * • It sends to Google's super-smart Gemini AI
 * • Gemini thinks really hard and gives you a smart answer
 * • You see the answer in a pretty chat bubble!
 * 
 * No static responses - every answer is fresh from the AI! ✨
 */

class GeminiChatAssistant {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.isWaitingForAI = false;
        this.conversationHistory = [];
        
        console.log('🤖 Real AI Chat Assistant initializing with Gemini power!');
    }
    
    /**
     * 🎬 Initialize the AI chatbot - call this from your HTML!
     */
    static init() {
        window.geminiChatAssistant = new GeminiChatAssistant();
        window.geminiChatAssistant.setup();
    }
    
    /**
     * 🏗️ Set up the chatbot UI and connect to Gemini AI
     */
    async setup() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.createUI());
        } else {
            this.createUI();
        }
        
        // Check if Gemini AI is available
        try {
            const status = await this.checkAIStatus();
            if (status.ai_available) {
                console.log('🎉 Gemini AI is ready for intelligent conversations!');
                this.addMessage({
                    type: 'bot',
                    message: "👋 Hi there! I'm your AI assistant powered by Google's Gemini! I can help you with anything - upload questions, file management, troubleshooting, or just casual conversation. What would you like to know?",
                    category: 'greeting'
                });
            } else {
                console.warn('⚠️ Gemini AI not available:', status.message);
                this.addMessage({
                    type: 'bot',
                    message: "🤖 Hello! I'm your AI assistant, but I'm having trouble connecting to my smart brain right now. The admin needs to configure the Gemini API key. In the meantime, I can still try to help with basic questions!",
                    category: 'warning'
                });
            }
        } catch (error) {
            console.error('💔 Error checking AI status:', error);
            this.addMessage({
                type: 'bot',
                message: "😅 Hi! I'm your AI assistant, but I'm having some connection issues. Please try refreshing the page or check your internet connection!",
                category: 'error'
            });
        }
    }
    
    /**
     * 📊 Check if Gemini AI is available and ready
     */
    async checkAIStatus() {
        try {
            const response = await fetch('/api/ai/status');
            return await response.json();
        } catch (error) {
            console.error('Error checking AI status:', error);
            return { ai_available: false, message: 'Connection error' };
        }
    }
    
    /**
     * 🎨 Create the beautiful chat UI
     */
    createUI() {
        // Create the main container
        const container = document.createElement('div');
        container.className = 'gemini-chat-assistant';
        container.innerHTML = this.getHTML();
        
        // Add styles
        this.addStyles();
        
        // Append to body
        document.body.appendChild(container);
        
        // Bind event listeners
        this.bindEvents();
        
        console.log('🎨 Gemini AI Chat UI created successfully!');
    }
    
    /**
     * 📝 Get the HTML structure for the chat interface
     */
    getHTML() {
        return `
            <!-- 🚀 Chat Toggle Button -->
            <button class="gemini-chat-toggle" id="geminiChatToggle" title="AI Assistant - Ask me anything!">
                🤖
                <span class="gemini-chat-notification">AI</span>
            </button>
            
            <!-- 💬 Chat Window -->
            <div class="gemini-chat-window" id="geminiChatWindow" style="display: none;">
                <!-- 📋 Chat Header -->
                <div class="gemini-chat-header">
                    <div class="chat-title">
                        <span class="ai-icon">🧠</span>
                        <div>
                            <h3>AI Assistant</h3>
                            <p>Powered by Google Gemini</p>
                        </div>
                    </div>
                    <div class="chat-controls">
                        <button class="status-btn" id="statusBtn" title="Check AI status">📊</button>
                        <button class="clear-btn" id="clearBtn" title="Clear conversation">🧹</button>
                    </div>
                </div>
                
                <!-- 💬 Messages Container -->
                <div class="gemini-chat-messages" id="geminiChatMessages">
                    <!-- Messages will be added here dynamically -->
                </div>
                
                <!-- ⌨️ Input Area -->
                <div class="gemini-chat-input-area">
                    <div class="input-container">
                        <textarea 
                            id="geminiChatInput" 
                            class="gemini-chat-input" 
                            placeholder="Ask me anything! I'm powered by Google's Gemini AI..."
                            rows="1"
                        ></textarea>
                        <button class="send-btn" id="geminiSendBtn" title="Send message (Enter)">
                            <span class="send-icon">🚀</span>
                        </button>
                    </div>
                    <div class="input-hint">
                        Press Enter to send • I can answer anything with AI intelligence!
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * 🎨 Add beautiful CSS styles for the chat interface
     */
    addStyles() {
        const styles = `
            <style>
            /* 🎨 Gemini AI Chat Assistant Styles */
            .gemini-chat-assistant {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 1001;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            /* 🚀 AI-Powered Toggle Button */
            .gemini-chat-toggle {
                width: 64px;
                height: 64px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
                color: white;
                font-size: 26px;
                cursor: pointer;
                box-shadow: 0 4px 24px rgba(66, 133, 244, 0.3);
                transition: all 0.3s ease;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: aiPulse 3s ease-in-out infinite;
            }
            
            @keyframes aiPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            .gemini-chat-toggle:hover {
                transform: translateY(-3px) scale(1.1);
                box-shadow: 0 8px 32px rgba(66, 133, 244, 0.4);
            }
            
            .gemini-chat-toggle.active {
                background: linear-gradient(135deg, #ea4335 0%, #fbbc04 100%);
                animation: none;
            }
            
            /* 🔔 AI Notification Badge */
            .gemini-chat-notification {
                position: absolute;
                top: -8px;
                right: -8px;
                background: linear-gradient(135deg, #34a853 0%, #fbbc04 100%);
                color: white;
                border-radius: 50%;
                width: 28px;
                height: 28px;
                font-size: 13px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: aiNotificationPulse 2s infinite;
                border: 2px solid white;
            }
            
            @keyframes aiNotificationPulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            
            /* 💬 AI Chat Window */
            .gemini-chat-window {
                position: absolute;
                bottom: 85px;
                right: 0;
                width: 400px;
                height: 550px;
                background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                animation: aiSlideUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                border: 1px solid rgba(66, 133, 244, 0.1);
            }
            
            @keyframes aiSlideUp {
                from {
                    opacity: 0;
                    transform: translateY(30px) scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            /* 📋 AI Chat Header */
            .gemini-chat-header {
                background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
                color: white;
                padding: 20px 24px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .chat-title {
                display: flex;
                align-items: center;
                gap: 16px;
            }
            
            .ai-icon {
                font-size: 28px;
                animation: aiThink 4s ease-in-out infinite;
            }
            
            @keyframes aiThink {
                0%, 100% { transform: scale(1) rotate(0deg); }
                25% { transform: scale(1.1) rotate(5deg); }
                75% { transform: scale(1.1) rotate(-5deg); }
            }
            
            .chat-title h3 {
                margin: 0;
                font-size: 18px;
                font-weight: 600;
            }
            
            .chat-title p {
                margin: 0;
                font-size: 13px;
                opacity: 0.9;
                font-weight: 400;
            }
            
            .chat-controls {
                display: flex;
                gap: 12px;
            }
            
            .status-btn, .clear-btn {
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
            
            .status-btn:hover, .clear-btn:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: scale(1.1);
            }
            
            /* 💬 Messages Container */
            .gemini-chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                background: linear-gradient(180deg, #f8f9ff 0%, #ffffff 100%);
                display: flex;
                flex-direction: column;
                gap: 16px;
            }
            
            /* Custom AI Scrollbar */
            .gemini-chat-messages::-webkit-scrollbar {
                width: 8px;
            }
            
            .gemini-chat-messages::-webkit-scrollbar-track {
                background: transparent;
            }
            
            .gemini-chat-messages::-webkit-scrollbar-thumb {
                background: linear-gradient(145deg, #4285f4, #34a853);
                border-radius: 4px;
            }
            
            /* 💭 Individual Messages */
            .ai-message {
                display: flex;
                margin-bottom: 12px;
                animation: messageSlideIn 0.3s ease-out;
            }
            
            @keyframes messageSlideIn {
                from {
                    opacity: 0;
                    transform: translateY(15px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .ai-message-content {
                max-width: 85%;
                padding: 16px 20px;
                border-radius: 20px;
                position: relative;
                word-wrap: break-word;
                line-height: 1.5;
            }
            
            /* 👤 User Messages */
            .user-message {
                justify-content: flex-end;
            }
            
            .user-message .ai-message-content {
                background: linear-gradient(135deg, #4285f4 0%, #1a73e8 100%);
                color: white;
                border-bottom-right-radius: 8px;
                box-shadow: 0 4px 16px rgba(66, 133, 244, 0.3);
            }
            
            /* 🤖 AI Messages */
            .bot-message {
                justify-content: flex-start;
            }
            
            .bot-message .ai-message-content {
                background: linear-gradient(135deg, #ffffff 0%, #f1f3f4 100%);
                color: #202124;
                border: 1px solid rgba(66, 133, 244, 0.1);
                border-bottom-left-radius: 8px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            }
            
            /* 🎨 Special Message Types */
            .bot-message.greeting .ai-message-content {
                background: linear-gradient(135deg, #e8f0fe 0%, #f8f9ff 100%);
                border: 1px solid rgba(66, 133, 244, 0.2);
            }
            
            .bot-message.warning .ai-message-content {
                background: linear-gradient(135deg, #fef7e0 0%, #fefbf0 100%);
                border: 1px solid rgba(251, 188, 4, 0.3);
                color: #b7900d;
            }
            
            .bot-message.error .ai-message-content {
                background: linear-gradient(135deg, #fce8e6 0%, #fef2f2 100%);
                border: 1px solid rgba(234, 67, 53, 0.3);
                color: #c5221f;
            }
            
            /* ⏰ Message Time */
            .ai-message-time {
                font-size: 11px;
                opacity: 0.6;
                margin-top: 8px;
                text-align: right;
            }
            
            /* 💭 AI Thinking Indicator */
            .ai-thinking {
                justify-content: flex-start;
            }
            
            .ai-thinking .ai-message-content {
                background: linear-gradient(135deg, #e8f0fe 0%, #f1f3f4 100%);
                border: 1px solid rgba(66, 133, 244, 0.2);
                padding: 20px 24px;
            }
            
            .thinking-indicator {
                display: flex;
                gap: 6px;
                align-items: center;
                color: #4285f4;
            }
            
            .thinking-dots {
                display: flex;
                gap: 4px;
            }
            
            .thinking-dots span {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #4285f4;
                animation: aiThinking 1.4s ease-in-out infinite;
            }
            
            .thinking-dots span:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .thinking-dots span:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes aiThinking {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.4;
                }
                30% {
                    transform: translateY(-12px);
                    opacity: 1;
                }
            }
            
            /* ⌨️ Input Area */
            .gemini-chat-input-area {
                background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
                border-top: 1px solid rgba(66, 133, 244, 0.1);
                padding: 20px;
            }
            
            .input-container {
                display: flex;
                gap: 12px;
                align-items: flex-end;
            }
            
            .gemini-chat-input {
                flex: 1;
                border: 2px solid rgba(66, 133, 244, 0.2);
                border-radius: 24px;
                padding: 14px 20px;
                font-size: 15px;
                font-family: inherit;
                resize: none;
                max-height: 120px;
                min-height: 48px;
                transition: all 0.3s ease;
                outline: none;
                background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
            }
            
            .gemini-chat-input:focus {
                border-color: #4285f4;
                box-shadow: 0 0 0 4px rgba(66, 133, 244, 0.1);
                background: #ffffff;
            }
            
            .gemini-chat-input:disabled {
                background: #f1f3f4;
                color: #5f6368;
                cursor: not-allowed;
            }
            
            .send-btn {
                width: 48px;
                height: 48px;
                border: none;
                border-radius: 50%;
                background: linear-gradient(135deg, #4285f4 0%, #1a73e8 100%);
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
            }
            
            .send-btn:hover:not(:disabled) {
                transform: translateY(-2px) scale(1.1);
                box-shadow: 0 8px 24px rgba(66, 133, 244, 0.4);
            }
            
            .send-btn:disabled {
                background: #dadce0;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .input-hint {
                font-size: 12px;
                color: #5f6368;
                margin-top: 12px;
                text-align: center;
            }
            
            /* 📱 Mobile Responsiveness */
            @media (max-width: 768px) {
                .gemini-chat-assistant {
                    bottom: 15px;
                    right: 15px;
                }
                
                .gemini-chat-window {
                    width: calc(100vw - 30px);
                    max-width: 400px;
                    height: 75vh;
                    max-height: 550px;
                    right: -15px;
                }
                
                .gemini-chat-toggle {
                    width: 60px;
                    height: 60px;
                    font-size: 24px;
                }
            }
            
            @media (max-width: 480px) {
                .gemini-chat-window {
                    bottom: 80px;
                    right: -15px;
                    width: calc(100vw - 30px);
                    height: 70vh;
                }
                
                .ai-message-content {
                    max-width: 90%;
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
        const toggleBtn = document.getElementById('geminiChatToggle');
        const sendBtn = document.getElementById('geminiSendBtn');
        const statusBtn = document.getElementById('statusBtn');
        const clearBtn = document.getElementById('clearBtn');
        const chatInput = document.getElementById('geminiChatInput');
        
        toggleBtn.addEventListener('click', () => this.toggleChat());
        sendBtn.addEventListener('click', () => this.sendMessage());
        statusBtn.addEventListener('click', () => this.showAIStatus());
        clearBtn.addEventListener('click', () => this.clearMessages());
        
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        chatInput.addEventListener('input', () => {
            chatInput.style.height = 'auto';
            chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
        });
    }
    
    /**
     * 🎭 Toggle chat window open/closed
     */
    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('geminiChatWindow');
        const toggleBtn = document.getElementById('geminiChatToggle');
        
        if (this.isOpen) {
            chatWindow.style.display = 'flex';
            toggleBtn.innerHTML = '✕';
            toggleBtn.classList.add('active');
            document.getElementById('geminiChatInput').focus();
        } else {
            chatWindow.style.display = 'none';
            toggleBtn.innerHTML = '🤖<span class="gemini-chat-notification">AI</span>';
            toggleBtn.classList.remove('active');
        }
    }
    
    /**
     * 💬 Send a message to Gemini AI
     */
    async sendMessage() {
        const input = document.getElementById('geminiChatInput');
        const message = input.value.trim();
        
        if (!message || this.isWaitingForAI) return;
        
        // Add user message
        this.addMessage({
            type: 'user',
            message: message
        });
        
        input.value = '';
        input.style.height = 'auto';
        
        // Show AI thinking
        this.showThinking();
        
        try {
            // Send to Gemini AI
            const response = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            this.hideThinking();
            
            if (data.success) {
                // Add AI response
                this.addMessage({
                    type: 'bot',
                    message: data.response,
                    category: 'ai_response'
                });
                
                console.log('🎉 Gemini AI responded successfully!');
                
            } else {
                // Show error with fallback
                this.addMessage({
                    type: 'bot',
                    message: data.fallback_response || data.error || "I'm having trouble thinking right now. Please try again!",
                    category: 'error'
                });
                
                console.error('💔 AI Error:', data.error);
            }
            
        } catch (error) {
            console.error('💔 Network error:', error);
            this.hideThinking();
            
            this.addMessage({
                type: 'bot',
                message: "😅 I'm having trouble connecting to my AI brain. Please check your internet connection and try again!",
                category: 'error'
            });
        }
    }
    
    /**
     * 💭 Show AI thinking indicator
     */
    showThinking() {
        this.isWaitingForAI = true;
        const messagesContainer = document.getElementById('geminiChatMessages');
        
        const thinkingDiv = document.createElement('div');
        thinkingDiv.id = 'aiThinkingIndicator';
        thinkingDiv.className = 'ai-message ai-thinking';
        thinkingDiv.innerHTML = `
            <div class="ai-message-content">
                <div class="thinking-indicator">
                    <span>🤖 AI is thinking</span>
                    <div class="thinking-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(thinkingDiv);
        this.scrollToBottom();
        
        // Disable input while thinking
        document.getElementById('geminiChatInput').disabled = true;
        document.getElementById('geminiSendBtn').disabled = true;
    }
    
    /**
     * 🚫 Hide AI thinking indicator
     */
    hideThinking() {
        this.isWaitingForAI = false;
        const thinkingIndicator = document.getElementById('aiThinkingIndicator');
        if (thinkingIndicator) {
            thinkingIndicator.remove();
        }
        
        // Re-enable input
        document.getElementById('geminiChatInput').disabled = false;
        document.getElementById('geminiSendBtn').disabled = false;
    }
    
    /**
     * ➕ Add a message to the chat
     */
    addMessage(messageData) {
        const message = {
            id: Date.now() + Math.random(),
            timestamp: new Date().toISOString(),
            ...messageData
        };
        
        this.messages.push(message);
        this.renderMessage(message);
        this.scrollToBottom();
    }
    
    /**
     * 🎨 Render a message in the UI
     */
    renderMessage(message) {
        const messagesContainer = document.getElementById('geminiChatMessages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ${message.type}-message`;
        
        if (message.category) {
            messageDiv.classList.add(message.category);
        }
        
        const timeString = new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        messageDiv.innerHTML = `
            <div class="ai-message-content">
                <div class="message-text">${this.formatMessage(message.message)}</div>
                <div class="ai-message-time">${timeString}</div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
    }
    
    /**
     * 🎨 Format message text with simple markdown
     */
    formatMessage(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br />');
    }
    
    /**
     * 📜 Scroll to bottom of messages
     */
    scrollToBottom() {
        const messagesContainer = document.getElementById('geminiChatMessages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    /**
     * 📊 Show AI status information
     */
    async showAIStatus() {
        try {
            const status = await this.checkAIStatus();
            
            let statusMessage = '';
            let category = 'info';
            
            if (status.ai_available) {
                statusMessage = `✅ AI Status: Online and ready! I'm connected to Google's Gemini AI model and ready for intelligent conversations.`;
                category = 'greeting';
            } else {
                statusMessage = `⚠️ AI Status: ${status.message}. I might have limited capabilities right now.`;
                category = 'warning';
            }
            
            this.addMessage({
                type: 'bot',
                message: statusMessage,
                category: category
            });
            
        } catch (error) {
            this.addMessage({
                type: 'bot',
                message: "📊 I'm having trouble checking my AI status right now. But I'm still here to help!",
                category: 'error'
            });
        }
    }
    
    /**
     * 🧹 Clear all messages
     */
    clearMessages() {
        this.messages = [];
        const messagesContainer = document.getElementById('geminiChatMessages');
        messagesContainer.innerHTML = '';
        
        this.addMessage({
            type: 'bot',
            message: "✨ Fresh conversation started! I'm ready for new questions. What would you like to know?",
            category: 'greeting'
        });
    }
}

// 🌟 Auto-initialize when this script loads
console.log('🤖 Gemini AI Chat Assistant script loaded! Ready for intelligent conversations!');

// Make it available globally
window.GeminiChatAssistant = GeminiChatAssistant;