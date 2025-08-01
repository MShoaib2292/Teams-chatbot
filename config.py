import os

class Config:
    def __init__(self):
        # OpenRouter Configuration
        self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
        self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
        self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
        
        # MCP Server Configuration - Check if URL is accessible
        self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://c34c410be489.ngrok-free.app/api/mcp')
        
        # Test MCP server connectivity at startup
        self._test_mcp_connection()
        
        # Production environment detection
        if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
            print("🚀 Production environment detected (Render)")
        
        # Debug logging
        print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
        print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
        print(f"🔧 Config - Model: {self.MODEL_NAME}")
        print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
        
        # Chatbot Configuration
        self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
        self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
        
        # Load system prompt from file or use default
        self.SYSTEM_PROMPT = self._load_system_prompt()
        
        print(f"✅ Config initialized successfully")
        print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")
    
    def _load_system_prompt(self):
        """Load system prompt from file or return default"""
        prompt_file = 'prompts/mcp_prompt.txt'
        
        try:
            # Try to load from file
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                print(f"✅ Loaded system prompt from: {prompt_file}")
                return content
        except FileNotFoundError:
            print(f"⚠️  Prompt file not found at: {prompt_file}")
            print(f"🔄 Using stored procedure-based system prompt")
            
            # Return stored procedure-based system prompt
            return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
        except Exception as e:
            print(f"❌ Error loading prompt file: {str(e)}")
            return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://4ff78e0c0217.ngrok-free.app/api/mcp')
    
    # Test MCP server connectivity at startup
    self._test_mcp_connection()
    
    # Production environment detection
    if os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER'):
        print("🚀 Production environment detected (Render)")
    
    # Debug logging
    print(f"🔧 Config - OpenRouter API Key: {self.OPENROUTER_API_KEY[:20]}...")
    print(f"🔧 Config - Base URL: {self.OPENAI_BASE_URL}")
    print(f"🔧 Config - Model: {self.MODEL_NAME}")
    print(f"🔧 Config - MCP Server URL: {self.MCP_SERVER_URL}")
    
    # Chatbot Configuration
    self.MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    self.TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Load system prompt from file or use default
    self.SYSTEM_PROMPT = self._load_system_prompt()
    
    print(f"✅ Config initialized successfully")
    print(f"📝 System prompt loaded: {len(self.SYSTEM_PROMPT)} characters")

def _load_system_prompt(self):
    """Load system prompt from file or return default"""
    prompt_file = 'prompts/mcp_prompt.txt'
    
    try:
        # Try to load from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ Loaded system prompt from: {prompt_file}")
            return content
    except FileNotFoundError:
        print(f"⚠️  Prompt file not found at: {prompt_file}")
        print(f"🔄 Using stored procedure-based system prompt")
        
        # Return stored procedure-based system prompt
        return """You are a medical assistant chatbot that translates user questions into calls to a stored procedure `[AI].[uspGetPatientDetailsMCP]` via an MCP server and .NET WebAPI.

This stored procedure supports filtering patient records using multiple parameters. All fields (except gender) are handled using `LIKE '%value%'` search inside the stored procedure.

### Stored Procedure Parameters and Behavior

You can filter by the following fields (all are optional):

| Field             | Parameter Name       | Type     | Matching Type     |
|------------------|----------------------|----------|--------------------|
| Patient ID       | @pPatientId          | INT      | LIKE as string     |
| NHI Number       | @pPatientNHI         | NVARCHAR | LIKE               |
| Full Name        | @pPatientFullName    | NVARCHAR | LIKE               |
| Date of Birth    | @pPatientDOB         | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Address          | @pFullAddress        | NVARCHAR | LIKE               |
| Provider Name    | @pProviderName       | NVARCHAR | LIKE               |
| Email            | @pEmail              | NVARCHAR | LIKE               |
| Phone Number     | @pPhoneNunmber       | NVARCHAR | LIKE               |
| Chart Number     | @pChartNumber        | NVARCHAR | LIKE               |
| Enrollment Date  | @pEnrollmentDate     | NVARCHAR | LIKE (yyyy-MM-dd)  |
| Funding Status   | @pFundingStatus      | NVARCHAR | LIKE               |
| Enrollment Status| @pEnrollmentStatus   | NVARCHAR | LIKE               |
| Gender           | @pGenderName         | NVARCHAR | EXACT MATCH        |

For all fields except `Gender`, the backend handles `LIKE '%value%'`. Gender must match exactly (e.g., 'male', 'female').

### Interpretation Rules

1. Parse all filters mentioned in the user's query.
2. Combine filters if more than one field is mentioned.
3. Use the value in `LIKE '%value%'` for all fields except Gender.
4. For Gender, the value must be an exact match.
5. If no filters are mentioned, fetch all patients (pass empty or null for all fields).
6. Return structured results or say: "No matching patient records found."

IMPORTANT: For ANY patient-related query, you MUST use the get_patients function. Never provide general responses about patients without calling the function first.

Always format patient results in clear HTML tables with all available columns and show total count.
"""
    except Exception as e:
        print(f"❌ Error loading prompt file: {str(e)}")
        return "You are a helpful medical assistant AI that can access patient information through the MCP server."
    
    def _test_mcp_connection(self):
        """Test MCP server connection at startup"""
        try:
            import requests
            response = requests.get(f"{self.MCP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL =
            if response.status_code == 200:
                print(f"✅ MCP Server is reachable")
            else:
                print(f"⚠️ MCP Server returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection failed: {str(e)}")
            print(f"🔧 Please check if {self.MCP_SERVER_URL} is accessible")

def __init__(self):
    # OpenRouter Configuration
    self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')
    self.MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    
    # MCP Server Configuration - Check if URL is accessible
    self.MCP_SERVER_URL =


