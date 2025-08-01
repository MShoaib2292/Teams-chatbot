import requests
import json
from typing import Dict, Any, Optional

class PatientSearchTool:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def search_patients(self, **kwargs) -> Dict[str, Any]:
        """Search for patients using any combination of parameters"""
        try:
            # Build parameters from kwargs
            params = {}
            
            # Map common search terms to API parameters
            param_mapping = {
                'practice_id': 'PracticeId',
                'patient_id': 'PatientId',
                'patient_nhi': 'PatientNHI', 
                'patient_name': 'PatientFullName',
                'full_name': 'PatientFullName',
                'name': 'PatientFullName',
                'dob': 'PatientDOB',
                'date_of_birth': 'PatientDOB',
                'address': 'FullAddress',
                'provider': 'ProviderName',
                'provider_name': 'ProviderName',
                'email': 'Email',
                'phone': 'PhoneNumber',
                'phone_number': 'PhoneNumber',
                'chart_number': 'ChartNumber',
                'enrollment_date': 'EnrollmentDate',
                'funding_status': 'FundingStatus',
                'enrollment_status': 'EnrollmentStatus',
                'gender': 'GenderName'
            }
            
            # Convert kwargs to API parameters
            for key, value in kwargs.items():
                if value is not None and value != '':
                    api_param = param_mapping.get(key.lower(), key)
                    params[api_param] = str(value)
            
            print(f"🔍 Searching patients with: {params}")
            
            response = requests.get(f"{self.base_url}/patients", params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            return {"Success": False, "Message": f"API Error: {str(e)}", "Data": None}

# Function schemas for the LLM
PATIENT_SEARCH_SCHEMAS = [
    {
        "name": "search_patients",
        "description": "Search for patients using various criteria. All parameters are optional - you can search by any combination or get all patients with no parameters.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {
                    "type": "integer",
                    "description": "Specific patient ID"
                },
                "patient_name": {
                    "type": "string", 
                    "description": "Patient full name (partial matches work)"
                },
                "patient_nhi": {
                    "type": "string",
                    "description": "Patient NHI number"
                },
                "dob": {
                    "type": "string",
                    "description": "Date of birth (YYYY-MM-DD format)"
                },
                "email": {
                    "type": "string",
                    "description": "Patient email address"
                },
                "phone": {
                    "type": "string", 
                    "description": "Patient phone number"
                },
                "provider_name": {
                    "type": "string",
                    "description": "Healthcare provider name"
                },
                "gender": {
                    "type": "string",
                    "description": "Patient gender"
                },
                "chart_number": {
                    "type": "string",
                    "description": "Patient chart number"
                }
            },
            "required": []
        }
    }
]