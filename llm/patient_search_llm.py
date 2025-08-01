import requests
import json
from datetime import datetime
from typing import Dict, Any
from tools.patient_search_tool import PatientSearchTool, PATIENT_SEARCH_SCHEMAS

class PatientSearchLLM:
    def __init__(self, config):
        self.config = config
        self.base_url = config.OPENAI_BASE_URL
        self.api_key = config.OPENROUTER_API_KEY
        self.patient_tool = PatientSearchTool(config.MCP_SERVER_URL)
    
    def process_query(self, user_query: str) -> str:
        """Process user query for patient search"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Patient Search Chatbot"
            }
            
            system_prompt = """You are a medical assistant that helps search for patient information.

When displaying patient results, you MUST:
1. Format ALL patient data as HTML tables with ALL columns
2. Calculate age from PatientDOB and display both age and formatted DOB
3. Show complete result sets (no limits)
4. Include summary with total count

MANDATORY: Display ALL these columns in HTML table format:
- Patient ID, Patient Full Name, Patient NHI, Chart Number
- Gender, Age (calculated), Date of Birth (formatted)  
- Provider Name, Email, Phone Number, Full Address
- Enrollment Date, Funding Status, Enrollment Status

For DOB processing:
- Calculate age from PatientDOB field
- Format DOB as YYYY-MM-DD for display
- Handle various date formats (ISO, with/without time)

Example HTML structure:
<div class="summary-info">Found X patients in the live database</div>
<table class="patient-table">
<thead><tr><th>Patient ID</th><th>Name</th><th>NHI</th><th>Chart Number</th><th>Gender</th><th>Age</th><th>DOB</th><th>Provider</th><th>Email</th><th>Phone</th><th>Address</th><th>Enrollment Date</th><th>Funding Status</th><th>Enrollment Status</th></tr></thead>
<tbody>
[patient rows with calculated age and formatted DOB]
</tbody>
</table>
<div class="summary-info">Total: X patients displayed</div>

CRITICAL: Always calculate age from PatientDOB and format dates properly for frontend display."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
            
            payload = {
                "model": self.config.MODEL_NAME,
                "messages": messages,
                "functions": PATIENT_SEARCH_SCHEMAS,
                "function_call": "auto",
                "max_tokens": self.config.MAX_TOKENS,
                "temperature": self.config.TEMPERATURE
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            message = result['choices'][0]['message']
            
            if 'function_call' in message and message['function_call']:
                function_name = message['function_call']['name']
                function_args = json.loads(message['function_call']['arguments'])
                
                print(f"🤖 Calling function: {function_name} with args: {function_args}")
                
                # Execute the search
                if function_name == "search_patients":
                    function_result = self.patient_tool.search_patients(**function_args)
                    # Process patient data to calculate ages and format dates
                    function_result = self._process_patient_data(function_result)
                else:
                    function_result = {"Success": False, "Message": f"Unknown function: {function_name}", "Data": None}
                
                # Get final response with the search results
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "function_call": message['function_call']
                })
                
                messages.append({
                    "role": "function", 
                    "name": function_name,
                    "content": json.dumps(function_result)
                })
                
                final_payload = {
                    "model": self.config.MODEL_NAME,
                    "messages": messages,
                    "max_tokens": self.config.MAX_TOKENS,
                    "temperature": self.config.TEMPERATURE
                }
                
                final_response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=final_payload
                )
                
                final_response.raise_for_status()
                final_result = final_response.json()
                
                return final_result['choices'][0]['message']['content']
            else:
                return message['content']
                
        except requests.exceptions.RequestException as e:
            return f"❌ API request failed: {str(e)}"
        except Exception as e:
            return f"❌ Error processing query: {str(e)}"
    
    def _process_patient_data(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Process patient data to calculate ages and format dates"""
        if not result.get('Success') or not result.get('Data'):
            return result
            
        patients = result['Data']
        
        # Calculate ages and format data for ALL patients
        for patient in patients:
            if patient.get('patientDOB'):
                try:
                    # Parse DOB and calculate age
                    dob_str = patient['patientDOB']
                    if 'T' in dob_str:
                        dob = datetime.fromisoformat(dob_str.replace('Z', '+00:00'))
                    else:
                        dob = datetime.strptime(dob_str[:10], '%Y-%m-%d')
                    
                    today = datetime.now()
                    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                    patient['calculatedAge'] = age
                    patient['formattedDOB'] = dob.strftime('%Y-%m-%d')
                except:
                    patient['calculatedAge'] = 'Unknown'
                    patient['formattedDOB'] = patient.get('patientDOB', 'Unknown')
            else:
                patient['calculatedAge'] = 'Unknown'
                patient['formattedDOB'] = 'Unknown'
        
        return result



