from flask import Flask, render_template, request, jsonify, make_response
from config import Config
from llm.router_api_llm import RouterAPILLM
import logging
import time
import os

app = Flask(__name__)
config = Config()

# CSP and Teams integration headers
def add_teams_headers(response):
    """Add headers required for Microsoft Teams integration"""
    response.headers['Content-Security-Policy'] = (
        "frame-ancestors 'self' https://teams.microsoft.com https://*.teams.microsoft.com "
        "https://*.skype.com https://*.teams.microsoft.us https://*.gov.teams.microsoft.us "
        "https://*.office.com https://*.sharepoint.com https://*.office365.com; "
        "default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data: blob:; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://res.cdn.office.net "
        "https://statics.teams.cdn.office.net https://teams.microsoft.com "
        "https://fonts.googleapis.com https://*.office.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com; "
        "font-src 'self' https://fonts.gstatic.com https://fonts.googleapis.com; "
        "img-src 'self' data: https: blob:; "
        "connect-src 'self' https: wss: data:;"
    )
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

@app.after_request
def after_request(response):
    return add_teams_headers(response)

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
    """Main chatbot interface - Teams compatible"""
    response = make_response(render_template('teams_index.html', timestamp=int(time.time())))
    return response

@app.route('/teams')
def teams_tab():
    """Dedicated Teams tab interface"""
    response = make_response(render_template('teams_index.html', timestamp=int(time.time())))
    return response

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with better error handling"""
    try:
        if not llm:
            return jsonify({
                'response': '❌ Chatbot is not properly initialized. Please check the configuration.',
                'error': True
            })
        
        data = request.get_json()
        if not data:
            return jsonify({
                'response': '❌ No data received',
                'error': True
            })
            
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'response': '⚠️ Please enter a message.',
                'error': True
            })
        
        logger.info(f"📝 Processing user message: {user_message}")
        
        # Add timeout to LLM processing
        try:
            response = llm.process_query(user_message)
            logger.info(f"✅ Generated response: {response[:100]}...")
            
            return jsonify({
                'response': response,
                'error': False
            })
            
        except Exception as llm_error:
            logger.error(f"❌ LLM Error: {str(llm_error)}")
            return jsonify({
                'response': f'❌ I encountered an error processing your request. Please try a simpler question or try again later.',
                'error': True
            })
        
    except Exception as e:
        logger.error(f"❌ Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': f'❌ Server error. Please try again.',
            'error': True
        }), 500

@app.route('/health')
def health():
    """Enhanced health check endpoint"""
    try:
        # Test MCP server connection
        mcp_status = "unknown"
        try:
            import requests
            mcp_response = requests.get(f"{config.MCP_SERVER_URL}/health", timeout=5)
            mcp_status = "healthy" if mcp_response.status_code == 200 else "unhealthy"
        except:
            mcp_status = "unreachable"
        
        return jsonify({
            'status': 'healthy',
            'service': 'MCP Medical Assistant Chatbot',
            'mcp_server_url': config.MCP_SERVER_URL,
            'mcp_server_status': mcp_status,
            'llm_initialized': llm is not None,
            'environment': 'production' if os.getenv('RENDER_SERVICE_NAME') else 'development',
            'timestamp': int(time.time())
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

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

@app.route('/privacy')
def privacy():
    """Privacy policy for Teams app"""
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    """Terms of use for Teams app"""
    return render_template('terms.html')

@app.route('/debug/mcp')
def debug_mcp():
    """Debug MCP server connection"""
    try:
        import requests
        
        # Test MCP server health
        mcp_health_url = f"{config.MCP_SERVER_URL}/health"
        patients_url = f"{config.MCP_SERVER_URL}/patients"
        
        debug_info = {
            "mcp_server_url": config.MCP_SERVER_URL,
            "health_check": "unknown",
            "patients_endpoint": "unknown",
            "error": None
        }
        
        try:
            # Test health endpoint
            health_response = requests.get(mcp_health_url, timeout=10)
            debug_info["health_check"] = {
                "status": health_response.status_code,
                "response": health_response.text[:200]
            }
        except Exception as e:
            debug_info["health_check"] = f"Error: {str(e)}"
        
        try:
            # Test patients endpoint
            patients_response = requests.get(patients_url, timeout=10)
            debug_info["patients_endpoint"] = {
                "status": patients_response.status_code,
                "response": patients_response.text[:200]
            }
        except Exception as e:
            debug_info["patients_endpoint"] = f"Error: {str(e)}"
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting MCP Chatbot Web Interface...")
    port = int(os.environ.get('PORT', 3000))
    print(f"💻 Server will run on port: {port}")
    print(f"🔗 MCP Server URL: {config.MCP_SERVER_URL}")
    
    # Use debug=False for production
    app.run(host='0.0.0.0', port=port, debug=False)







