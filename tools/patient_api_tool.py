import requests
import json
from typing import Dict, Any, List, Optional

# Function schemas for OpenAI/OpenRouter - Match stored procedure exactly
PATIENT_FUNCTION_SCHEMAS = [
    {
        "name": "get_patients",
        "description": "Search for patients using stored procedure [AI].[uspGetPatientDetailsMCP]. All parameters are optional. All fields except Gender use LIKE '%value%' matching. Gender requires exact match.",
        "parameters": {
            "type": "object",
            "properties": {
                "PatientId": {
                    "type": "string",
                    "description": "Patient ID (LIKE search as string)"
                },
                "PatientNHI": {
                    "type": "string", 
                    "description": "Patient NHI number (LIKE search)"
                },
                "PatientFullName": {
                    "type": "string",
                    "description": "Patient Full Name (LIKE search)"
                },
                "PatientDOB": {
                    "type": "string",
                    "description": "Date of Birth in yyyy-MM-dd format (LIKE search)"
                },
                "FullAddress": {
                    "type": "string",
                    "description": "Full Address (LIKE search)"
                },
                "ProviderName": {
                    "type": "string",
                    "description": "Provider Name (LIKE search)"
                },
                "Email": {
                    "type": "string",
                    "description": "Email address (LIKE search)"
                },
                "PhoneNumber": {
                    "type": "string",
                    "description": "Phone Number (LIKE search)"
                },
                "ChartNumber": {
                    "type": "string",
                    "description": "Chart Number (LIKE search)"
                },
                "EnrollmentDate": {
                    "type": "string",
                    "description": "Enrollment Date in yyyy-MM-dd format (LIKE search)"
                },
                "FundingStatus": {
                    "type": "string",
                    "description": "Funding Status (LIKE search)"
                },
                "EnrollmentStatus": {
                    "type": "string",
                    "description": "Enrollment Status (LIKE search)"
                },
                "GenderName": {
                    "type": "string",
                    "description": "Gender - EXACT MATCH ONLY: 'male' or 'female'"
                }
            },
            "required": []
        }
    }
]

class PatientAPITool:
    def __init__(self, mcp_server_url: str):
        self.mcp_server_url = mcp_server_url.rstrip('/')
        self.timeout = 30
        
        # Add headers for ngrok
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'ngrok-skip-browser-warning': 'true'  # Skip ngrok browser warning
        }
        
        print(f"🔧 PatientAPITool initialized with URL: {self.mcp_server_url}")
    
    def get_patients(self, **filters) -> Dict[str, Any]:
        """Get patients with optional filters"""
        try:
            url = f"{self.mcp_server_url}/patients"
            
            # Clean filters - remove None/empty values
            clean_filters = {k: v for k, v in filters.items() if v is not None and str(v).strip()}
            
            print(f"🔍 Making request to: {url}")
            print(f"📋 Filters: {clean_filters}")
            
            response = requests.post(
                url, 
                json=clean_filters,
                headers=self.headers,
                timeout=self.timeout
            )
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Successfully retrieved {len(data.get('patients', []))} patients")
                return data
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return {
                    "patients": [],
                    "total_count": 0,
                    "error": f"API returned status {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            print(f"⏰ Request timeout after {self.timeout} seconds")
            return {
                "patients": [],
                "total_count": 0,
                "error": "Request timeout - MCP server may be slow"
            }
        except requests.exceptions.ConnectionError:
            print(f"🔌 Connection error to MCP server")
            return {
                "patients": [],
                "total_count": 0,
                "error": "Cannot connect to MCP server"
            }
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return {
                "patients": [],
                "total_count": 0,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def get_patient_details(self, patient_id: int) -> Dict[str, Any]:
        """Get specific patient details by ID - calls MCP server /patients/{id} endpoint"""
        try:
            url = f"{self.base_url}/patients/{patient_id}"
            print(f"🔍 Calling MCP server: {url}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ MCP server response: Success={result.get('Success')}")
            
            return result
            
        except requests.RequestException as e:
            print(f"❌ MCP server request failed: {str(e)}")
            return {"Success": False, "Message": f"MCP Server Error: {str(e)}", "Data": None}

    def search_patients(self, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """Search for patients with enhanced error handling"""
        try:
            url = f"{self.base_url}/patients"
            print(f"🔍 Calling MCP server: {url}")
            print(f"📋 Search params: {search_params}")
            
            # Add timeout and better error handling
            response = requests.get(url, params=search_params, timeout=30)
            
            print(f"📡 Response status: {response.status_code}")
            print(f"📡 Response headers: {dict(response.headers)}")
            
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ MCP server response: Success={result.get('Success')}")
            print(f"📊 Data count: {len(result.get('Data', []))}")
            
            return result
            
        except requests.exceptions.Timeout:
            print(f"⏰ MCP server timeout")
            return {"Success": False, "Message": "MCP Server timeout - please try again", "Data": []}
        except requests.exceptions.ConnectionError:
            print(f"🔌 MCP server connection error")
            return {"Success": False, "Message": "Cannot connect to MCP Server", "Data": []}
        except requests.RequestException as e:
            print(f"❌ MCP server request failed: {str(e)}")
            return {"Success": False, "Message": f"MCP Server Error: {str(e)}", "Data": []}
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return {"Success": False, "Message": f"Unexpected error: {str(e)}", "Data": []}

# Updated Function Schemas for OpenAI/OpenRouter
PATIENT_FUNCTION_SCHEMAS = [
    {
        "name": "get_patients",
        "description": "Search for patients using various criteria. All parameters are optional.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_name": {
                    "type": "string",
                    "description": "Patient full name to search for"
                },
                "patient_nhi": {
                    "type": "string",
                    "description": "Patient NHI number"
                },
                "patient_id": {
                    "type": "integer",
                    "description": "Specific patient ID"
                },
                "practice_id": {
                    "type": "integer",
                    "description": "Practice ID"
                },
                "provider_name": {
                    "type": "string",
                    "description": "Healthcare provider name"
                },
                "email": {
                    "type": "string",
                    "description": "Patient email"
                },
                "phone_number": {
                    "type": "string",
                    "description": "Patient phone number"
                },
                "gender": {
                    "type": "string",
                    "description": "Patient gender"
                }
            },
            "required": []
        }
    }
    # {
    #     "name": "get_patient_details",
    #     "description": "Get detailed information for a specific patient by ID",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "patient_id": {
    #                 "type": "integer",
    #                 "description": "The patient ID to retrieve details for"
    #             }
    #         },
    #         "required": ["patient_id"]
    #     }
    # }
]














