/**
 * 🤖 CHAT ASSISTANT COMPONENT
 * 
 * This is like a friendly chat room where users can talk to our Smart Brain!
 * It's designed to be:
 * • Beautiful and easy to use
 * • Safe and error-free
 * • Helpful and informative
 * • Non-intrusive to existing features
 * 
 * Think of it as a cozy corner where users can get instant help!
 */

import React, { useState, useEffect, useRef } from 'react';
import './ChatAssistant.css';

const ChatAssistant = () => {
    // 📚 State management (like organizing toys in different boxes)
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [smartBrain, setSmartBrain] = useState(null);
    
    // 📜 References for smooth scrolling and focus
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);
    
    /**
     * 🎬 Initialize the Smart Brain when component starts
     * Like waking up our friendly assistant!
     */
    useEffect(() => {
        try {
            // Check if SmartBrain is available
            if (window.SmartBrain) {
                const brain = new window.SmartBrain();
                setSmartBrain(brain);
                console.log('🤖 Chat Assistant connected to Smart Brain!');
                
                // Add a welcome message
                setMessages([{
                    id: 1,
                    type: 'bot',
                    message: "👋 Hi there! I'm your Smart Assistant! I know everything about this file-transfer system - auto-healing uploads, smart priorities, network monitoring, and more! What would you like to know?",
                    timestamp: new Date().toISOString()
                }]);
            } else {
                console.warn('⚠️ SmartBrain not found - loading fallback mode');
                setMessages([{
                    id: 1,
                    type: 'bot',
                    message: "🤖 Hello! I'm here to help, but I'm still loading my brain. Please refresh the page if you don't see me working properly!",
                    timestamp: new Date().toISOString()
                }]);
            }
        } catch (error) {
            console.error('💔 Chat Assistant initialization error:', error);
        }
    }, []);
    
    /**
     * 📜 Auto-scroll to bottom when new messages arrive
     * Like always looking at the newest part of the conversation!
     */
    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);
    
    /**
     * 🎯 Focus input when chat opens
     * Like automatically getting ready to type!
     */
    useEffect(() => {
        if (isOpen && inputRef.current) {
            inputRef.current.focus();
        }
    }, [isOpen]);
    
    /**
     * 💬 Send a message to the Smart Brain
     * Like asking a question to our friendly helper!
     */
    const sendMessage = async () => {
        if (!inputMessage.trim() || !smartBrain) return;
        
        const userMessage = {
            id: Date.now(),
            type: 'user',
            message: inputMessage.trim(),
            timestamp: new Date().toISOString()
        };
        
        // Add user message immediately
        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setIsTyping(true);
        
        try {
            // Get response from Smart Brain
            const response = await smartBrain.processMessage(userMessage.message);
            
            // Simulate a little thinking time (like a real conversation!)
            await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200));
            
            const botMessage = {
                id: Date.now() + 1,
                type: 'bot',
                message: response.message,
                category: response.category,
                confidence: response.confidence,
                timestamp: new Date().toISOString()
            };
            
            setMessages(prev => [...prev, botMessage]);
            
        } catch (error) {
            console.error('💔 Message processing error:', error);
            
            const errorMessage = {
                id: Date.now() + 1,
                type: 'bot',
                message: "😅 Oops! I had a tiny hiccup there. Please try asking your question again!",
                timestamp: new Date().toISOString()
            };
            
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsTyping(false);
        }
    };
    
    /**
     * ⌨️ Handle Enter key press
     * Like pressing the "send" button with the keyboard!
     */
    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };
    
    /**
     * 🎭 Toggle chat window open/closed
     * Like opening and closing a friendly door!
     */
    const toggleChat = () => {
        setIsOpen(!isOpen);
    };
    
    /**
     * 🧹 Clear all messages
     * Like starting a fresh conversation!
     */
    const clearMessages = () => {
        setMessages([{
            id: Date.now(),
            type: 'bot',
            message: "✨ Fresh start! What would you like to know about the file-transfer system?",
            timestamp: new Date().toISOString()
        }]);
    };
    
    /**
     * 🎓 Show help topics
     * Like showing all the fun things we can talk about!
     */
    const showHelp = () => {
        if (!smartBrain) return;
        
        const helpInfo = smartBrain.getHelpTopics();
        const helpMessage = `🎓 **I can help you with these topics:**

${helpInfo.topics.map(topic => `• **${topic.name}**: ${topic.description}`).join('\n')}

**Try asking questions like:**
${helpInfo.examples.map(example => `• "${example}"`).join('\n')}`;
        
        const botMessage = {
            id: Date.now(),
            type: 'bot',
            message: helpMessage,
            category: 'help',
            timestamp: new Date().toISOString()
        };
        
        setMessages(prev => [...prev, botMessage]);
    };
    
    /**
     * 🎨 Format message text with simple markdown-like formatting
     * Like making text pretty and easy to read!
     */
    const formatMessage = (text) => {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br />');
    };
    
    /**
     * 🎨 Get message bubble style based on confidence
     * Like choosing the right color crayon!
     */
    const getMessageStyle = (message) => {
        if (message.type === 'user') return 'user-message';
        
        const baseClass = 'bot-message';
        if (message.confidence === 'low') return `${baseClass} low-confidence`;
        if (message.category === 'social') return `${baseClass} social`;
        return baseClass;
    };
    
    return (
        <div className="chat-assistant">
            {/* 🎈 Chat Toggle Button - always visible */}
            <button 
                className={`chat-toggle ${isOpen ? 'active' : ''}`}
                onClick={toggleChat}
                title="Smart Assistant - Ask me anything!"
            >
                {isOpen ? '✕' : '🤖'}
                {!isOpen && <span className="chat-notification">AI</span>}
            </button>
            
            {/* 💬 Chat Window - shows when open */}
            {isOpen && (
                <div className="chat-window">
                    {/* 📋 Chat Header */}
                    <div className="chat-header">
                        <div className="chat-title">
                            <span className="brain-icon">🧠</span>
                            <div>
                                <h3>Smart Assistant</h3>
                                <p>Real-Time Intelligent Support</p>
                            </div>
                        </div>
                        <div className="chat-controls">
                            <button 
                                className="help-btn" 
                                onClick={showHelp}
                                title="Show help topics"
                            >
                                ❓
                            </button>
                            <button 
                                className="clear-btn" 
                                onClick={clearMessages}
                                title="Clear conversation"
                            >
                                🧹
                            </button>
                        </div>
                    </div>
                    
                    {/* 💬 Messages Container */}
                    <div className="chat-messages">
                        {messages.map((message) => (
                            <div key={message.id} className={`message ${getMessageStyle(message)}`}>
                                <div className="message-content">
                                    <div 
                                        className="message-text"
                                        dangerouslySetInnerHTML={{ 
                                            __html: formatMessage(message.message) 
                                        }}
                                    />
                                    <div className="message-time">
                                        {new Date(message.timestamp).toLocaleTimeString([], {
                                            hour: '2-digit',
                                            minute: '2-digit'
                                        })}
                                        {message.category && (
                                            <span className="message-category">
                                                {message.category}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                        
                        {/* 💭 Typing Indicator */}
                        {isTyping && (
                            <div className="message bot-message typing">
                                <div className="message-content">
                                    <div className="typing-indicator">
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                    </div>
                                </div>
                            </div>
                        )}
                        
                        {/* 📍 Scroll anchor */}
                        <div ref={messagesEndRef} />
                    </div>
                    
                    {/* ⌨️ Input Area */}
                    <div className="chat-input-area">
                        <div className="input-container">
                            <textarea
                                ref={inputRef}
                                value={inputMessage}
                                onChange={(e) => setInputMessage(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Ask me about uploads, healing, priorities, security..."
                                className="chat-input"
                                rows="1"
                                disabled={!smartBrain}
                            />
                            <button 
                                className="send-btn"
                                onClick={sendMessage}
                                disabled={!inputMessage.trim() || !smartBrain || isTyping}
                                title="Send message (Enter)"
                            >
                                {isTyping ? '⏳' : '📤'}
                            </button>
                        </div>
                        <div className="input-hint">
                            Press Enter to send • Shift+Enter for new line
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChatAssistant;