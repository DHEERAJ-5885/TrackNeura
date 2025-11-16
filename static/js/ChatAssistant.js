/**
 * 🤖 CHAT ASSISTANT - Vanilla JavaScript Version
 * 
 * This creates our Smart Chatbot Assistant that works with your Flask templates!
 * It's designed to be:
 * • Easy to add to any HTML page
 * • Non-intrusive to existing features
 * • Beautiful and responsive
 * • Smart and helpful
 * 
 * Just include this file and call ChatAssistant.init() - that's it!
 */

class ChatAssistant {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.smartBrain = null;
        this.isTyping = false;
        
        console.log('🤖 Chat Assistant initializing...');
    }
    
    /**
     * 🎬 Initialize the chatbot - call this from your HTML!
     */
    static init() {
        window.chatAssistant = new ChatAssistant();
        window.chatAssistant.setup();
    }
    
    /**
     * 🏗️ Set up the chatbot UI and logic
     */
    async setup() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.createUI());
        } else {
            this.createUI();
        }
        
        // Initialize Smart Brain
        try {
            if (window.SmartBrain) {
                this.smartBrain = new window.SmartBrain();
                console.log('🧠 Smart Brain connected!');
                
                // Add welcome message
                this.addMessage({
                    type: 'bot',
                    message: "👋 Hi there! I'm your Smart Assistant! I know everything about this file-transfer system - auto-healing uploads, smart priorities, network monitoring, and more! What would you like to know?",
                    category: 'greeting'
                });
            }
        } catch (error) {
            console.error('💔 Smart Brain initialization error:', error);
        }
    }
    
    /**
     * 🎨 Create the chatbot UI
     */
    createUI() {
        // Create the main container
        const container = document.createElement('div');
        container.className = 'chat-assistant';
        container.innerHTML = this.getHTML();
        
        // Add styles
        this.addStyles();
        
        // Append to body
        document.body.appendChild(container);
        
        // Bind event listeners
        this.bindEvents();
        
        console.log('🤖 Chat Assistant UI created!');
    }
    
    /**
     * 📝 Get the HTML structure
     */
    getHTML() {
        return `
            <!-- 🎈 Chat Toggle Button -->
            <button class="chat-toggle" id="chatToggle" title="Smart Assistant - Ask me anything!">
                🤖
                <span class="chat-notification">AI</span>
            </button>
            
            <!-- 💬 Chat Window -->
            <div class="chat-window" id="chatWindow" style="display: none;">
                <!-- 📋 Chat Header -->
                <div class="chat-header">
                    <div class="chat-title">
                        <span class="brain-icon">🧠</span>
                        <div>
                            <h3>Smart Assistant</h3>
                            <p>Real-Time Intelligent Support</p>
                        </div>
                    </div>
                    <div class="chat-controls">
                        <button class="help-btn" id="helpBtn" title="Show help topics">❓</button>
                        <button class="clear-btn" id="clearBtn" title="Clear conversation">🧹</button>
                    </div>
                </div>
                
                <!-- 💬 Messages Container -->
                <div class="chat-messages" id="chatMessages">
                    <!-- Messages will be added here -->
                </div>
                
                <!-- ⌨️ Input Area -->
                <div class="chat-input-area">
                    <div class="input-container">
                        <textarea 
                            id="chatInput" 
                            class="chat-input" 
                            placeholder="Ask me about uploads, healing, priorities, security..."
                            rows="1"
                        ></textarea>
                        <button class="send-btn" id="sendBtn" title="Send message (Enter)">📤</button>
                    </div>
                    <div class="input-hint">
                        Press Enter to send • Shift+Enter for new line
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * 🎨 Add CSS styles
     */
    addStyles() {
        const styles = `
            <style>
            /* 🎨 Chat Assistant Styles */
            .chat-assistant {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 1000;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .chat-toggle {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-size: 24px;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
                transition: all 0.3s ease;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .chat-toggle:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
            }
            
            .chat-toggle.active {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            }
            
            .chat-notification {
                position: absolute;
                top: -5px;
                right: -5px;
                background: #ff4757;
                color: white;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                font-size: 12px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            
            .chat-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 380px;
                height: 500px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                animation: slideUp 0.3s ease-out;
            }
            
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 16px 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .chat-title {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .brain-icon {
                font-size: 24px;
                animation: think 3s ease-in-out infinite;
            }
            
            @keyframes think {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            .chat-title h3 {
                margin: 0;
                font-size: 16px;
                font-weight: 600;
            }
            
            .chat-title p {
                margin: 0;
                font-size: 12px;
                opacity: 0.9;
            }
            
            .chat-controls {
                display: flex;
                gap: 8px;
            }
            
            .help-btn, .clear-btn {
                background: rgba(255, 255, 255, 0.2);
                border: none;
                color: white;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                cursor: pointer;
                transition: background 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
            }
            
            .help-btn:hover, .clear-btn:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 16px;
                background: #f8f9fa;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .chat-messages::-webkit-scrollbar {
                width: 6px;
            }
            
            .chat-messages::-webkit-scrollbar-track {
                background: transparent;
            }
            
            .chat-messages::-webkit-scrollbar-thumb {
                background: #dee2e6;
                border-radius: 3px;
            }
            
            .message {
                display: flex;
                margin-bottom: 8px;
            }
            
            .message-content {
                max-width: 80%;
                padding: 12px 16px;
                border-radius: 18px;
                position: relative;
            }
            
            .user-message {
                justify-content: flex-end;
            }
            
            .user-message .message-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-bottom-right-radius: 6px;
            }
            
            .bot-message {
                justify-content: flex-start;
            }
            
            .bot-message .message-content {
                background: white;
                color: #2c3e50;
                border: 1px solid #e9ecef;
                border-bottom-left-radius: 6px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            }
            
            .bot-message.social .message-content {
                background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
                border: 1px solid #e17055;
            }
            
            .bot-message.low-confidence .message-content {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
            }
            
            .message-text {
                line-height: 1.4;
                word-wrap: break-word;
            }
            
            .message-time {
                font-size: 11px;
                opacity: 0.7;
                margin-top: 4px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .typing .message-content {
                background: white;
                border: 1px solid #e9ecef;
                padding: 16px 20px;
            }
            
            .typing-indicator {
                display: flex;
                gap: 4px;
                align-items: center;
            }
            
            .typing-indicator span {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #adb5bd;
                animation: typing 1.4s ease-in-out infinite;
            }
            
            .typing-indicator span:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .typing-indicator span:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes typing {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.4;
                }
                30% {
                    transform: translateY(-10px);
                    opacity: 1;
                }
            }
            
            .chat-input-area {
                background: white;
                border-top: 1px solid #e9ecef;
                padding: 16px;
            }
            
            .input-container {
                display: flex;
                gap: 8px;
                align-items: flex-end;
            }
            
            .chat-input {
                flex: 1;
                border: 1px solid #dee2e6;
                border-radius: 20px;
                padding: 12px 16px;
                font-size: 14px;
                font-family: inherit;
                resize: none;
                max-height: 100px;
                transition: border-color 0.3s ease;
                outline: none;
            }
            
            .chat-input:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .send-btn {
                width: 40px;
                height: 40px;
                border: none;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
            }
            
            .send-btn:hover:not(:disabled) {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
            
            .send-btn:disabled {
                background: #dee2e6;
                cursor: not-allowed;
            }
            
            .input-hint {
                font-size: 11px;
                color: #6c757d;
                margin-top: 8px;
                text-align: center;
            }
            
            @media (max-width: 768px) {
                .chat-window {
                    width: calc(100vw - 40px);
                    max-width: 380px;
                    height: 70vh;
                    max-height: 500px;
                }
            }
            </style>
        `;
        
        document.head.insertAdjacentHTML('beforeend', styles);
    }
    
    /**
     * 🔗 Bind event listeners
     */
    bindEvents() {
        const toggleBtn = document.getElementById('chatToggle');
        const sendBtn = document.getElementById('sendBtn');
        const helpBtn = document.getElementById('helpBtn');
        const clearBtn = document.getElementById('clearBtn');
        const chatInput = document.getElementById('chatInput');
        
        toggleBtn.addEventListener('click', () => this.toggleChat());
        sendBtn.addEventListener('click', () => this.sendMessage());
        helpBtn.addEventListener('click', () => this.showHelp());
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
            chatInput.style.height = Math.min(chatInput.scrollHeight, 100) + 'px';
        });
    }
    
    /**
     * 🎭 Toggle chat window
     */
    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('chatWindow');
        const toggleBtn = document.getElementById('chatToggle');
        
        if (this.isOpen) {
            chatWindow.style.display = 'flex';
            toggleBtn.innerHTML = '✕';
            toggleBtn.classList.add('active');
            document.getElementById('chatInput').focus();
        } else {
            chatWindow.style.display = 'none';
            toggleBtn.innerHTML = '🤖<span class="chat-notification">AI</span>';
            toggleBtn.classList.remove('active');
        }
    }
    
    /**
     * 💬 Send a message
     */
    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message || !this.smartBrain) return;
        
        // Add user message
        this.addMessage({
            type: 'user',
            message: message
        });
        
        input.value = '';
        input.style.height = 'auto';
        
        // Show typing indicator
        this.showTyping();
        
        try {
            // Get response from Smart Brain
            const response = await this.smartBrain.processMessage(message);
            
            // Simulate thinking time
            await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200));
            
            this.hideTyping();
            
            // Add bot response
            this.addMessage({
                type: 'bot',
                message: response.message,
                category: response.category,
                confidence: response.confidence
            });
            
        } catch (error) {
            console.error('💔 Message processing error:', error);
            this.hideTyping();
            this.addMessage({
                type: 'bot',
                message: "😅 Oops! I had a tiny hiccup there. Please try asking your question again!",
                category: 'error'
            });
        }
    }
    
    /**
     * 💭 Show typing indicator
     */
    showTyping() {
        this.isTyping = true;
        const messagesContainer = document.getElementById('chatMessages');
        
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typingIndicator';
        typingDiv.className = 'message bot-message typing';
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    /**
     * 🚫 Hide typing indicator
     */
    hideTyping() {
        this.isTyping = false;
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
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
        const messagesContainer = document.getElementById('chatMessages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.type}-message`;
        
        if (message.category === 'social') {
            messageDiv.classList.add('social');
        } else if (message.confidence === 'low') {
            messageDiv.classList.add('low-confidence');
        }
        
        const timeString = new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-text">${this.formatMessage(message.message)}</div>
                <div class="message-time">
                    ${timeString}
                    ${message.category ? `<span class="message-category">${message.category}</span>` : ''}
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
    }
    
    /**
     * 🎨 Format message text
     */
    formatMessage(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br />');
    }
    
    /**
     * 📜 Scroll to bottom of messages
     */
    scrollToBottom() {
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    /**
     * 🎓 Show help topics
     */
    showHelp() {
        if (!this.smartBrain) return;
        
        const helpInfo = this.smartBrain.getHelpTopics();
        const helpMessage = `🎓 **I can help you with these topics:**

${helpInfo.topics.map(topic => `• **${topic.name}**: ${topic.description}`).join('\n')}

**Try asking questions like:**
${helpInfo.examples.map(example => `• "${example}"`).join('\n')}`;
        
        this.addMessage({
            type: 'bot',
            message: helpMessage,
            category: 'help'
        });
    }
    
    /**
     * 🧹 Clear all messages
     */
    clearMessages() {
        this.messages = [];
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.innerHTML = '';
        
        this.addMessage({
            type: 'bot',
            message: "✨ Fresh start! What would you like to know about the file-transfer system?",
            category: 'greeting'
        });
    }
}

// 🌟 Auto-initialize when this script loads
console.log('🤖 Chat Assistant script loaded! Ready to help!');

// Make it available globally
window.ChatAssistant = ChatAssistant;