"""
🤖 Smart Chatbot Integration Script
This safely adds the chatbot to all HTML templates without breaking anything!
"""

import os
import re

def add_chatbot_to_template(template_path):
    """Add chatbot scripts to a template file safely"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if chatbot is already added
        if 'SmartBrain.js' in content or 'ChatAssistant.js' in content:
            print(f"✅ Chatbot already exists in {template_path}")
            return
        
        # Find the closing body tag
        closing_body_pattern = r'</body>\s*</html>\s*$'
        
        if re.search(closing_body_pattern, content, re.MULTILINE | re.DOTALL):
            # Add chatbot scripts before closing body tag
            chatbot_scripts = '''
    <!-- 🤖 SMART CHATBOT ASSISTANT -->
    <script src="/static/js/SmartBrain.js"></script>
    <script src="/static/js/ChatAssistant.js"></script>
    <script>
        // Initialize the Smart Chatbot Assistant
        document.addEventListener('DOMContentLoaded', function() {
            // Wait a moment for all systems to load
            setTimeout(() => {
                ChatAssistant.init();
                console.log('🤖 Smart Assistant activated!');
            }, 1500);
        });
    </script>
</body>
</html>'''
            
            # Replace the closing tags
            new_content = re.sub(closing_body_pattern, chatbot_scripts, content, flags=re.MULTILINE | re.DOTALL)
            
            # Write back to file
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"🎉 Chatbot added to {template_path}")
            
        else:
            print(f"⚠️ Could not find closing body tag in {template_path}")
            
    except Exception as e:
        print(f"💔 Error processing {template_path}: {e}")

def main():
    """Main function to add chatbot to all templates"""
    print("🤖 Adding Smart Chatbot Assistant to all templates...")
    
    templates_dir = "templates"
    template_files = [
        'index.html',
        'dashboard.html',
        'upload.html',
        'smart_dashboard.html',
        'preview.html'
    ]
    
    for template_file in template_files:
        template_path = os.path.join(templates_dir, template_file)
        if os.path.exists(template_path):
            add_chatbot_to_template(template_path)
        else:
            print(f"⚠️ Template not found: {template_path}")
    
    print("🎉 Chatbot integration complete!")

if __name__ == "__main__":
    main()