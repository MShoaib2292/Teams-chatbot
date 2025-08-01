from flask import Flask, render_template, request, jsonify
from config import Config
from llm.router_api_llm import RouterAPILLM
import logging
import time

app = Flask(__name__)
config = Config()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    llm = RouterAPILLM(config)
    logger.info("LLM initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLM: {str(e)}")
    llm = None

@app.route('/')
def index():
    # Add timestamp for cache busting
    return render_template('index.html', timestamp=int(time.time()))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not llm:
            return jsonify({'response': 'Chatbot is not properly initialized. Please check the configuration.'})
        
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'response': 'Please enter a message.'})
        
        logger.info(f"Processing user message: {user_message}")
        response = llm.process_query(user_message)
        logger.info(f"Generated response: {response[:100]}...")
        
        return jsonify({'response': response})
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'response': f'Error: {str(e)}'})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'mcp_server_url': config.MCP_SERVER_URL,
        'llm_initialized': llm is not None
    })

if __name__ == '__main__':
    print("🚀 Starting MCP Chatbot Web Interface...")
    print("💻 Open your browser and go to: http://localhost:3000")
    print(f"🔗 MCP Server URL: {config.MCP_SERVER_URL}")
    app.run(host='localhost', port=3000, debug=True)

