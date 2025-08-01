import os
from waitress import serve
from web_app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"🚀 Starting production server on port {port}")
    serve(app, host='0.0.0.0', port=port)