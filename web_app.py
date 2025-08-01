from flask import Flask, render_template, request, jsonify
from config import Config
from llm.router_api_llm import RouterAPILLM
import logging
import time
import os

app = Flask(__name__)
config = Config()

# Setup logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    llm = RouterAPILLM(config)
    logger.info("✅ LLM initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize LLM: {str(e)}")
    llm = None

@app.route('/')
def index():
    """Main chatbot interface"""
    return render_template('index.html', timestamp=int(time.time()))

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        if not llm:
            return jsonify({
                'response': '❌ Chatbot is not properly initialized. Please check the configuration.',
                'error': True
            })
        
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'response': '⚠️ Please enter a message.',
                'error': True
            })
        
        logger.info(f"📝 Processing user message: {user_message}")
        response = llm.process_query(user_message)
        logger.info(f"✅ Generated response: {response[:100]}...")
        
        return jsonify({
            'response': response,
            'error': False
        })
        
    except Exception as e:
        logger.error(f"❌ Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': f'❌ Error: {str(e)}',
            'error': True
        })

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'service': 'MCP Medical Assistant Chatbot',
        'mcp_server_url': config.MCP_SERVER_URL,
        'llm_initialized': llm is not None,
        'environment': 'production' if os.getenv('RENDER_SERVICE_NAME') else 'development'
    })

@app.route('/status')
def status():
    """Detailed status endpoint"""
    return jsonify({
        'chatbot_status': 'running',
        'mcp_server': config.MCP_SERVER_URL,
        'model': config.MODEL_NAME,
        'max_tokens': config.MAX_TOKENS,
        'temperature': config.TEMPERATURE,
        'llm_ready': llm is not None
    })

if __name__ == '__main__':
    print("🚀 Starting MCP Chatbot Web Interface...")
    port = int(os.environ.get('PORT', 3000))
    print(f"💻 Server will run on port: {port}")
    print(f"🔗 MCP Server URL: {config.MCP_SERVER_URL}")
    
    # Use debug=False for production
    app.run(host='0.0.0.0', port=port, debug=False)

