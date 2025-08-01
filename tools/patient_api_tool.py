import requests
import json
from typing import Dict, Any, Optional

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
    def __init__(self, mcp_server_url):
        self.base_url = mcp_server_url.rstrip('/')
        print(f"🔧 PatientAPITool initialized with MCP server: {self.base_url}")
        
        # Test connection immediately
        try:
            test_response = requests.get(f"{self.base_url}/patients", timeout=5)
            print(f"✅ MCP Server connection test: {test_response.status_code}")
        except Exception as e:
            print(f"❌ MCP Server connection test failed: {e}")
    
    def get_patients(self, **kwargs) -> Dict[str, Any]:
        """Get list of patients with optional filters - calls MCP server /patients endpoint"""
        try:
            # Build parameters for MCP server
            params = {}
            
            # Convert kwargs to API parameters
            for key, value in kwargs.items():
                if value is not None and value != '':
                    params[key] = str(value)
                    print(f"🔧 Adding parameter: {key}='{value}'")
            
            url = f"{self.base_url}/patients"
            print(f"🔍 CALLING MCP SERVER: {url}")
            print(f"📋 WITH PARAMETERS: {params}")
            
            response = requests.get(url, params=params, timeout=30)
            print(f"🌐 MCP SERVER RESPONSE STATUS: {response.status_code}")
            print(f"🌐 MCP SERVER RESPONSE TEXT: {response.text[:500]}...")
            
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ MCP SERVER PARSED RESULT: Success={result.get('Success')}, Data count={len(result.get('Data', []))}")
            
            # Log sample data to verify it's real data
            if result.get('Data') and len(result['Data']) > 0:
                sample_patient = result['Data'][0]
                print(f"📊 SAMPLE PATIENT FROM MCP: {sample_patient}")
            
            return result
            
        except requests.RequestException as e:
            print(f"❌ MCP server request failed: {str(e)}")
            return {"Success": False, "Message": f"MCP Server Error: {str(e)}", "Data": None}
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return {"Success": False, "Message": f"Unexpected Error: {str(e)}", "Data": None}
    
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












