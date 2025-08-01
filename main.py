import sys
from config import Config
from llm.router_api_llm import RouterAPILLM

def print_grid_response(response):
    """Print response in a simple grid format"""
    print("\n" + "="*60)
    print("🤖 MCP CHATBOT RESPONSE")
    print("="*60)
    
    lines = response.split('\n')
    for line in lines:
        if line.strip():
            print(f"│ {line:<56} │")
    
    print("="*60 + "\n")

def main():
    print("🚀 Starting MCP Chatbot...")
    print("💡 Ask questions about patients, appointments, or notes")
    print("❌ Type 'exit' to quit\n")
    
    try:
        config = Config()
        llm = RouterAPILLM(config)
        
        while True:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            try:
                response = llm.process_query(user_input)
                print_grid_response(response)
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Failed to start chatbot: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()