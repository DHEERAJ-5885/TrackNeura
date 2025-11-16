"""
🤖 GEMINI AI CLIENT
This is like a friendly messenger that talks to Google's super-smart Gemini AI!

Think of it as:
• You ask a question
• This messenger carries it to Gemini
• Gemini thinks really hard
• This messenger brings back the answer
• Everyone is happy! ✨

It's built with enterprise-level security and error handling!
"""

import requests
import json
import time
from typing import Optional, Dict, Any

class GeminiClient:
    def __init__(self, api_key: str):
        """
        Initialize our Gemini messenger!
        Like giving our helper the special key to talk to the AI.
        """
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-pro"
        self.timeout = 30  # 30 seconds max wait time
        
        print("🤖 Gemini AI Client initialized! Ready to chat with super-smart AI!")
    
    def _make_request(self, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """
        This is the secret recipe for talking to Gemini!
        Like following instructions to ask the AI nicely.
        """
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        
        # This is how we package our question for Gemini
        headers = {
            "Content-Type": "application/json"
        }
        
        # Create the message in Gemini's favorite format
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": temperature,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
                "stopSequences": []
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        # Send our carefully packaged question to Gemini
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=self.timeout
        )
        
        return response
    
    def chat(self, user_message: str, context: str = "") -> Dict[str, Any]:
        """
        This is the main function - like having a conversation with Gemini!
        
        Baby explanation:
        • You say something
        • We ask Gemini nicely
        • Gemini thinks and responds
        • We give you the answer!
        """
        try:
            print(f"🧠 Asking Gemini: {user_message[:50]}...")
            
            # Create a smart prompt that gives Gemini context about your system
            system_context = f"""You are a helpful AI assistant for a file transfer system with these amazing features:
- Auto-Healing Upload Engine (automatically retries failed uploads)
- Smart Priority Engine (prioritizes important files using ML)
- Network Monitor (real-time connection monitoring)
- Chunk Corruption Detection (verifies file integrity)
- Resume System (continues interrupted uploads)
- Dashboard System (beautiful progress tracking)

Please provide helpful, accurate, and friendly responses. If the user asks about these features, explain them clearly. For other questions, provide general helpful assistance.

{context}

User question: {user_message}"""
            
            # Make the request to Gemini
            response = self._make_request(system_context, temperature=0.7)
            
            # Check if Gemini responded happily
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract Gemini's wise words
                if "candidates" in response_data and len(response_data["candidates"]) > 0:
                    candidate = response_data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        ai_response = candidate["content"]["parts"][0]["text"]
                        
                        print("✅ Gemini responded successfully!")
                        
                        return {
                            "success": True,
                            "response": ai_response,
                            "model": self.model,
                            "timestamp": time.time()
                        }
                
                # If we get here, something was weird in the response
                return {
                    "success": False,
                    "error": "Gemini gave us a confusing response format",
                    "details": response_data
                }
            
            else:
                # Gemini had a problem
                error_data = {}
                try:
                    error_data = response.json()
                except:
                    error_data = {"message": response.text}
                
                print(f"💔 Gemini error {response.status_code}: {error_data}")
                
                return {
                    "success": False,
                    "error": f"Gemini API error: {response.status_code}",
                    "details": error_data
                }
        
        except requests.exceptions.Timeout:
            print("⏰ Gemini took too long to respond")
            return {
                "success": False,
                "error": "Gemini is thinking too hard and timed out. Please try again!",
                "details": "Request timeout"
            }
        
        except requests.exceptions.ConnectionError:
            print("📡 Can't reach Gemini right now")
            return {
                "success": False,
                "error": "Can't connect to Gemini AI. Check your internet connection!",
                "details": "Connection error"
            }
        
        except Exception as e:
            print(f"💔 Unexpected error: {e}")
            return {
                "success": False,
                "error": "Something unexpected happened while talking to Gemini",
                "details": str(e)
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test if we can talk to Gemini - like saying 'hello' to make sure they're listening!
        """
        try:
            test_response = self.chat("Hello! Please respond with 'AI is working correctly!'")
            
            if test_response["success"]:
                return {
                    "success": True,
                    "message": "✅ Gemini AI is ready and working perfectly!",
                    "response": test_response["response"]
                }
            else:
                return {
                    "success": False,
                    "message": "💔 Gemini AI test failed",
                    "error": test_response["error"]
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": "💔 Gemini connection test failed",
                "error": str(e)
            }

# Global instance - like having one special messenger for the whole app
_gemini_client: Optional[GeminiClient] = None

def get_gemini_client() -> Optional[GeminiClient]:
    """
    Get our Gemini messenger - like asking for the smart friend who talks to AI!
    """
    global _gemini_client
    return _gemini_client

def initialize_gemini(api_key: str) -> bool:
    """
    Wake up our Gemini messenger - like introducing them to the AI!
    """
    global _gemini_client
    
    try:
        if not api_key or api_key.strip() == "":
            print("⚠️ No Gemini API key provided!")
            return False
        
        _gemini_client = GeminiClient(api_key)
        
        # Test the connection
        test_result = _gemini_client.test_connection()
        
        if test_result["success"]:
            print("🎉 Gemini AI is ready to help users!")
            return True
        else:
            print(f"💔 Gemini initialization failed: {test_result['message']}")
            _gemini_client = None
            return False
    
    except Exception as e:
        print(f"💔 Failed to initialize Gemini: {e}")
        _gemini_client = None
        return False

# Helper function for easy use in Flask routes
def ask_gemini(user_message: str, context: str = "") -> Dict[str, Any]:
    """
    Simple function to ask Gemini anything!
    Like having a magic 8-ball but infinitely smarter! ✨
    """
    client = get_gemini_client()
    
    if not client:
        return {
            "success": False,
            "error": "Gemini AI is not available right now. Please check the API key configuration.",
            "details": "No client initialized"
        }
    
    return client.chat(user_message, context)