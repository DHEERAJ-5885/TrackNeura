"""
🤖 Gemini AI Flask Routes
This adds the chat endpoint to your Flask app - like giving your system a smart voice!

Baby explanation:
• User types a question
• This endpoint receives it
• Sends it to Gemini AI  
• Returns Gemini's smart answer
• Everyone is happy! ✨
"""

from flask import request, jsonify
from gemini_client import ask_gemini, initialize_gemini, get_gemini_client

def add_ai_routes(app):
    """Add AI chat routes to the Flask app"""
    
    @app.route('/api/ai/chat', methods=['POST'])
    def ai_chat():
        """
        🤖 AI Chat Endpoint - where the magic happens!
        
        This is like a friendly translator between users and Gemini AI.
        What users say goes in, what Gemini thinks comes out!
        """
        try:
            # Get the user's message (like listening to what they want to know)
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'error': 'No data provided. Please send a message!',
                    'details': 'Missing JSON body'
                }), 400
            
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return jsonify({
                    'success': False,
                    'error': 'Please provide a message to chat with the AI!',
                    'details': 'Empty message field'
                }), 400
            
            # Check if message is too long (Gemini has limits)
            if len(user_message) > 5000:
                return jsonify({
                    'success': False,
                    'error': 'Message is too long! Please keep it under 5000 characters.',
                    'details': f'Message length: {len(user_message)} characters'
                }), 400
            
            print(f"🤖 User asked: {user_message[:100]}...")
            
            # Create context about your amazing system
            system_context = f"""
            You are helping users with an advanced file transfer system that has these incredible features:
            
            🩺 Auto-Healing Upload Engine: Automatically retries failed uploads, detects corruption, and heals broken transfers
            🎯 Smart Priority Engine: Uses machine learning to prioritize important files first
            📡 Network Monitor: Real-time connection monitoring and automatic reconnection
            🔄 Resume System: Continues interrupted uploads exactly where they left off  
            🛡️ Security Features: Checksum verification, secure chunking, and data integrity protection
            📊 Dashboard System: Beautiful real-time progress tracking and system monitoring
            
            Please provide helpful, accurate, and friendly responses. If users ask about these features, explain them clearly and enthusiastically. For other questions, provide general helpful assistance.
            
            Keep your tone friendly, informative, and encouraging!
            """
            
            # Ask Gemini AI for help!
            ai_response = ask_gemini(user_message, system_context)
            
            if ai_response['success']:
                print("✅ Gemini responded successfully!")
                
                return jsonify({
                    'success': True,
                    'response': ai_response['response'],
                    'model': ai_response.get('model', 'gemini-pro'),
                    'timestamp': ai_response.get('timestamp'),
                    'message': 'AI response generated successfully'
                })
            
            else:
                print(f"💔 Gemini error: {ai_response['error']}")
                
                # Provide a friendly fallback response
                fallback_message = "I'm having trouble connecting to my AI brain right now. Please check that the Gemini API key is configured correctly, or try again in a moment!"
                
                return jsonify({
                    'success': False,
                    'error': ai_response['error'],
                    'fallback_response': fallback_message,
                    'details': ai_response.get('details', 'Unknown error'),
                    'message': 'AI service temporarily unavailable'
                }), 503
        
        except Exception as e:
            print(f"💔 AI chat endpoint error: {e}")
            
            return jsonify({
                'success': False,
                'error': 'Something unexpected happened while processing your request',
                'details': str(e),
                'fallback_response': 'I apologize, but I encountered an error. Please try again!',
                'message': 'Internal server error'
            }), 500
    
    @app.route('/api/ai/status', methods=['GET'])
    def ai_status():
        """
        📊 AI Status Endpoint - check if Gemini is ready to chat!
        
        Like asking "Is the smart friend available to talk?"
        """
        try:
            client = get_gemini_client()
            
            if client:
                # Test the connection
                test_result = client.test_connection()
                
                return jsonify({
                    'success': True,
                    'ai_available': test_result['success'],
                    'message': test_result['message'],
                    'model': 'gemini-pro',
                    'status': 'operational' if test_result['success'] else 'error'
                })
            
            else:
                return jsonify({
                    'success': False,
                    'ai_available': False,
                    'message': 'Gemini AI client is not initialized. Please check the API key configuration.',
                    'status': 'not_configured'
                })
        
        except Exception as e:
            print(f"💔 AI status check error: {e}")
            
            return jsonify({
                'success': False,
                'ai_available': False,
                'message': 'Error checking AI status',
                'error': str(e),
                'status': 'error'
            }), 500

# Helper function to initialize Gemini AI with API key
def setup_gemini_ai(api_key):
    """
    🎬 Initialize Gemini AI - like introducing the smart friend to your system!
    
    Call this when your app starts up with your API key.
    """
    if not api_key or api_key.strip() == "" or api_key == "your-gemini-api-key-here":
        print("⚠️ No Gemini API key provided! AI chat will not be available.")
        print("💡 To enable AI chat, add your Gemini API key to the configuration.")
        return False
    
    print("🤖 Initializing Gemini AI...")
    success = initialize_gemini(api_key)
    
    if success:
        print("🎉 Gemini AI is ready to chat with users!")
    else:
        print("💔 Failed to initialize Gemini AI. Check your API key and internet connection.")
    
    return success