import openai
import json
import re
from datetime import datetime
from typing import Dict, Any, List
from tools.patient_api_tool import PatientAPITool, PATIENT_FUNCTION_SCHEMAS

class RouterAPILLM:
    def __init__(self, config):
        # Initialize OpenAI client for OpenRouter
        self.client = openai.OpenAI(
            base_url=config.OPENAI_BASE_URL,
            api_key=config.OPENROUTER_API_KEY,
        )
        
        self.config = config
        self.patient_tool = PatientAPITool(config.MCP_SERVER_URL)
        self.model = config.MODEL_NAME
        self.system_prompt = config.SYSTEM_PROMPT
        
        print(f"✅ RouterAPILLM initialized with OpenAI SDK")
        print(f"   Model: {self.model}")
        print(f"   Base URL: {config.OPENAI_BASE_URL}")
        print(f"   System prompt: {len(self.system_prompt)} chars")
    
    def process_query(self, user_input: str) -> str:
        """Process user query with better error handling"""
        try:
            # Add timeout and better error handling
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            print(f"🤖 Sending request to LLM...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                functions=PATIENT_FUNCTION_SCHEMAS,
                function_call="auto",
                temperature=0.1,
                max_tokens=1000,  # Reduced from 2000
                timeout=30,  # Add 30 second timeout
                extra_headers={
                    "HTTP-Referer": "https://teams-chatbot-at8z.onrender.com",
                    "X-Title": "Medical Assistant Chatbot"
                }
            )
            
            message = response.choices[0].message
            
            if message.function_call:
                function_name = message.function_call.name
                function_args = json.loads(message.function_call.arguments)
                
                print(f"🤖 LLM called function: {function_name}")
                
                # Add timeout to function execution
                function_result = self._execute_function_with_timeout(function_name, function_args)
                
                if function_result.get('Success'):
                    return self._format_response(function_result, function_name)
                else:
                    return f"❌ Error: {function_result.get('Message', 'Unknown error')}"
            else:
                return message.content or "❌ No response received"
                
        except Exception as e:
            print(f"❌ Error in process_query: {str(e)}")
            return f"❌ Sorry, I encountered an error: {str(e)}"

    def _format_patients_as_html_table(self, result):
        """Format patient data as HTML table with proper DOB handling"""
        if not result.get('Success') or not result.get('Data'):
            return "No patients found."
        
        patients = result['Data']
        total_count = len(patients)
        
        # Process patient data to calculate ages and format DOB
        for patient in patients:
            # Handle DOB field (could be PatientDOB or patientDOB)
            dob_value = patient.get('PatientDOB') or patient.get('patientDOB')
            if dob_value:
                try:
                    # Parse DOB and calculate age
                    dob_str = str(dob_value)
                    if 'T' in dob_str:
                        dob = datetime.fromisoformat(dob_str.replace('Z', '+00:00'))
                    else:
                        dob = datetime.strptime(dob_str[:10], '%Y-%m-%d')
                    
                    today = datetime.now()
                    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                    patient['calculatedAge'] = age
                    patient['formattedDOB'] = dob.strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"❌ DOB parsing error for {dob_value}: {str(e)}")
                    patient['calculatedAge'] = 'Unknown'
                    patient['formattedDOB'] = str(dob_value)[:10] if dob_value else 'Unknown'
            else:
                patient['calculatedAge'] = 'Unknown'
                patient['formattedDOB'] = 'Unknown'
        
        # CRITICAL: Show ALL patients, not just 5
        html = f'<div class="summary-info">Found {total_count} patients in the live database</div>\n\n'
        html += '<table class="patient-table">\n<thead>\n<tr>\n'
        html += '<th>Name</th><th>NHI</th><th>Chart Number</th>'
        html += '<th>Gender</th><th>Age</th><th>DOB</th><th>Provider</th><th>Email</th><th>Phone</th>'
        html += '<th>Address</th><th>Enrollment Date</th><th>Funding Status</th><th>Enrollment Status</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        
        # Process ALL patients - no limit
        for patient in patients:
            html += '<tr>\n'
            html += f'<td>{patient.get("PatientFullName") or patient.get("patientFullName", "")}</td>\n'
            html += f'<td>{patient.get("PatientNHI") or patient.get("patientNHI", "")}</td>\n'
            html += f'<td>{patient.get("ChartNumber") or patient.get("chartNumber", "")}</td>\n'
            html += f'<td>{patient.get("GenderName") or patient.get("genderName", "")}</td>\n'
            html += f'<td>{patient.get("calculatedAge", "")}</td>\n'
            html += f'<td>{patient.get("formattedDOB", "")}</td>\n'
            html += f'<td>{patient.get("ProviderName") or patient.get("providerName", "")}</td>\n'
            html += f'<td>{patient.get("Email") or patient.get("email", "")}</td>\n'
            html += f'<td>{patient.get("PhoneNumber") or patient.get("phoneNumber", "")}</td>\n'
            html += f'<td>{patient.get("FullAddress") or patient.get("fullAddress", "")}</td>\n'
            html += f'<td>{patient.get("EnrollmentDate") or patient.get("enrollmentDate", "")}</td>\n'
            html += f'<td>{patient.get("FundingStatus") or patient.get("fundingStatus", "")}</td>\n'
            html += f'<td>{patient.get("EnrollmentStatus") or patient.get("enrollmentStatus", "")}</td>\n'
            html += '</tr>\n'
        
        html += '</tbody>\n</table>\n'
        html += f'<div class="summary-info">Total: {total_count} patients displayed</div>'
        
        return html
    
    def _execute_function(self, function_name: str, function_args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the specified function with given arguments"""
        try:
            print(f"🎯 EXECUTING FUNCTION: {function_name}")
            print(f"🎯 WITH ARGUMENTS: {function_args}")
            
            if function_name == "get_patients":
                result = self.patient_tool.get_patients(**function_args)
                print(f"🎯 FUNCTION RESULT: Success={result.get('Success')}, Data count={len(result.get('Data', []))}")
                return result
            else:
                return {"Success": False, "Message": f"Unknown function: {function_name}", "Data": None}
            
        except Exception as e:
            print(f"❌ Function execution error: {str(e)}")
            return {"Success": False, "Message": f"Function execution error: {str(e)}", "Data": None}

    def _execute_function_with_timeout(self, function_name: str, function_args: dict, timeout=15):
        """Execute function with timeout"""
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Function execution timed out")
        
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)
            
            result = self._execute_function(function_name, function_args)
            
            signal.alarm(0)  # Cancel alarm
            return result
            
        except TimeoutError:
            return {"Success": False, "Message": "Request timed out", "Data": None}
        except Exception as e:
            signal.alarm(0)  # Cancel alarm
            return {"Success": False, "Message": str(e), "Data": None}

    def _process_patients_data(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Process patients data and calculate ages for ALL patients"""
        if not result.get('Success') or not result.get('Data'):
            return result
        
        patients = result['Data']
        
        # Calculate ages and format data for ALL patients - NO LIMIT
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
        
        # Add summary information for ALL patients
        result['Summary'] = {
            'totalPatients': len(patients),
            'displayMessage': f"Found {len(patients)} patients in the live database"
        }
        
        return result

    def _extract_parameters_manually(self, user_input: str) -> Dict[str, Any]:
        """Enhanced parameter extraction for all 13 stored procedure parameters"""
        params = {}
        user_lower = user_input.lower()
        
        print(f"🔍 PARSING: '{user_input}'")
        
        def normalize_date(date_str):
            """Normalize various date formats to YYYY-MM-DD"""
            if not date_str:
                return date_str
            try:
                # Handle YYYY-MM-DD format (already correct)
                if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                    return date_str
                
                # Handle dd/MM/yyyy format
                if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
                    dt = datetime.strptime(date_str, '%d/%m/%Y')
                    return dt.strftime('%Y-%m-%d')
                
                # Handle MM/dd/yyyy format
                if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
                    dt = datetime.strptime(date_str, '%m/%d/%Y')
                    return dt.strftime('%Y-%m-%d')
                
                # Handle dd-MM-yyyy format
                if re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
                    dt = datetime.strptime(date_str, '%d-%m-%Y')
                    return dt.strftime('%Y-%m-%d')
                
                # If just year, return as is for LIKE search
                if re.match(r'^\d{4}$', date_str):
                    return date_str
                
                return date_str
            except:
                return date_str
        
        # 1. @pPatientId (int) - Patient ID patterns
        patient_id_patterns = [
            r'patient\s+id\s+(\d+)',
            r'id\s+(\d+)',
            r'patient\s+(\d{6,})',  # 6+ digits likely an ID
            r'id:\s*(\d+)',
            r'patient\s+number\s+(\d+)',
            r'find\s+patient\s+by\s+id\s+(\d+)',
            r'show\s+patient\s+id\s+(\d+)',
            r'get\s+patient\s+id\s+(\d+)',
            r'patient\s+with\s+id\s+(\d+)',
            r'id\s+is\s+(\d+)',
            r'patient\s+(\d{5,})'  # 5+ digits as fallback
        ]
        
        for pattern in patient_id_patterns:
            match = re.search(pattern, user_lower)
            if match:
                params['PatientId'] = int(match.group(1))
                print(f"🎯 PatientId = {match.group(1)}")
                break
        
        # 2. @pPatientFullName (varchar) - Full name patterns
        name_patterns = [
            r'name\s+(?:is\s+)?["\']?([a-zA-Z\s]+)["\']?',
            r'patient\s+(?:named\s+)?["\']?([a-zA-Z\s]+)["\']?(?:\s+(?:in|from))?',
            r'full\s+name\s+(?:is\s+)?["\']?([a-zA-Z\s]+)["\']?',
            r'whose\s+(?:full\s+)?name\s+(?:is\s+)?["\']?([a-zA-Z\s]+)["\']?',
            r'find\s+(?:patient\s+)?["\']?([a-zA-Z\s]+)["\']?(?:\s+(?:in|from))?',
            r'search\s+(?:for\s+)?(?:patient\s+)?["\']?([a-zA-Z\s]+)["\']?'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, user_lower)
            if match and not any(word in match.group(1).lower() for word in ['male', 'female', 'patient', 'show', 'get', 'find', 'all', 'with', 'by', 'dr', 'doctor']):
                name = match.group(1).strip()
                if len(name) > 1 and name.replace(' ', '').isalpha():
                    params['PatientFullName'] = name
                    print(f"🎯 PatientFullName = {name}")
                    break
        
        # 3. @pPatientNHI (varchar) - NHI patterns
        nhi_patterns = [
            r'nhi\s+(?:number\s+)?(?:is\s+)?["\']?([A-Za-z0-9]+)["\']?',
            r'patient\s+nhi\s+["\']?([A-Za-z0-9]+)["\']?',
            r'nhi\s+["\']?([A-Za-z0-9]+)["\']?',
            r'with\s+nhi\s+["\']?([A-Za-z0-9]+)["\']?',
            r'nhi\s+starting\s+with\s+["\']?([A-Za-z0-9]+)["\']?',
            r'get\s+patient\s+nhi\s+["\']?([A-Za-z0-9]+)["\']?'
        ]
        
        for pattern in nhi_patterns:
            match = re.search(pattern, user_lower)
            if match:
                params['PatientNHI'] = match.group(1).upper()
                print(f"🎯 PatientNHI = {match.group(1).upper()}")
                break
        
        # 4. @pChartNumber (varchar) - Chart number patterns
        chart_patterns = [
            r'chart\s+number\s+(?:like\s+)?["\']?([A-Za-z0-9]+)["\']?',
            r'chart\s+(?:number\s+)?["\']?([A-Za-z0-9]+)["\']?',
            r'with\s+chart\s+number\s+["\']?([A-Za-z0-9]+)["\']?',
            r'chart\s+(?:no|num)\s+["\']?([A-Za-z0-9]+)["\']?',
            r'medical\s+chart\s+["\']?([A-Za-z0-9]+)["\']?'
        ]
        
        for pattern in chart_patterns:
            match = re.search(pattern, user_lower)
            if match:
                params['ChartNumber'] = match.group(1)
                print(f"🎯 ChartNumber = {match.group(1)}")
                break
        
        # 5. @pGenderName (varchar) - Gender patterns
        if any(word in user_lower for word in ['male', 'men', 'man']):
            if not any(word in user_lower for word in ['female', 'women', 'woman']):
                params['GenderName'] = 'male'
                print(f"🎯 GenderName = male")
        elif any(word in user_lower for word in ['female', 'women', 'woman']):
            params['GenderName'] = 'female'
            print(f"🎯 GenderName = female")
        
        # 6. @pPatientDOB (varchar) - Date of Birth patterns
        dob_patterns = [
            r'born\s+on\s+(\d{4}-\d{2}-\d{2})',
            r'dob\s+(\d{4}-\d{2}-\d{2})',
            r'date\s+of\s+birth\s+(\d{4}-\d{2}-\d{2})',
            r'birth\s+date\s+(\d{4}-\d{2}-\d{2})',
            r'born\s+(\d{4}-\d{2}-\d{2})',
            r'dob\s+(\d{2}/\d{2}/\d{4})',
            r'born\s+on\s+(\d{2}/\d{2}/\d{4})',
            r'born\s+in\s+(\d{4})',
            r'dob\s+includes?\s+(\d{4})',
            r'birth.*?(\d{4}-\d{2}-\d{2})'
        ]
        
        for pattern in dob_patterns:
            match = re.search(pattern, user_lower)
            if match:
                params['PatientDOB'] = normalize_date(match.group(1))
                print(f"🎯 PatientDOB = {params['PatientDOB']}")
                break
        
        # 7. @pProviderName (varchar) - Provider patterns
        provider_patterns = [
            r'(?:by\s+)?(?:dr\.?\s+|doctor\s+)([a-zA-Z\s]+)',
            r'provider\s+(?:name\s+)?(?:is\s+)?["\']?([a-zA-Z\s]+)["\']?',
            r'with\s+provider\s+["\']?([a-zA-Z\s]+)["\']?',
            r'assigned\s+to\s+(?:dr\.?\s+)?["\']?([a-zA-Z\s]+)["\']?',
            r'under\s+(?:dr\.?\s+)?["\']?([a-zA-Z\s]+)["\']?'
        ]
        
        for pattern in provider_patterns:
            match = re.search(pattern, user_lower)
            if match:
                provider = match.group(1).strip()
                if len(provider) > 1 and provider.replace(' ', '').isalpha():
                    params['ProviderName'] = provider
                    print(f"🎯 ProviderName = {provider}")
                    break
        
        # 8. @pEmail (varchar) - Email patterns
        email_patterns = [
            r'email\s+(?:like\s+)?["\']?([a-zA-Z0-9@._-]+)["\']?',
            r'with\s+email\s+["\']?([a-zA-Z0-9@._-]+)["\']?',
            r'email\s+(?:address\s+)?["\']?([a-zA-Z0-9@._-]+)["\']?',
            r'email\s+containing\s+["\']?([a-zA-Z0-9@._-]+)["\']?'
        ]
        
        for pattern in email_patterns:
            match = re.search(pattern, user_lower)
            if match:
                params['Email'] = match.group(1)
                print(f"🎯 Email = {match.group(1)}")
                break
        
        # 9. @pPhoneNumber (varchar) - Phone patterns
        phone_patterns = [
            r'phone\s+(?:number\s+)?(?:like\s+|containing\s+)?["\']?([0-9\-\s\(\)]+)["\']?',
            r'with\s+phone\s+(?:number\s+)?["\']?([0-9\-\s\(\)]+)["\']?',
            r'phone\s+["\']?([0-9\-\s\(\)]+)["\']?',
            r'contact\s+(?:number\s+)?["\']?([0-9\-\s\(\)]+)["\']?'
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, user_lower)
            if match:
                phone = match.group(1).strip()
                if any(char.isdigit() for char in phone):
                    params['PhoneNumber'] = phone
                    print(f"🎯 PhoneNumber = {phone}")
                    break
        
        # 10. @pFullAddress (varchar) - Address patterns
        address_patterns = [
            r'(?:from\s+)?address\s+["\']?([a-zA-Z0-9\s,.-]+)["\']?',
            r'(?:at\s+|from\s+)["\']?([a-zA-Z0-9\s,.-]+\s+(?:street|road|avenue|ave|st|rd))["\']?',
            r'lives?\s+(?:at\s+)?["\']?([a-zA-Z0-9\s,.-]+)["\']?',
            r'address\s+(?:like\s+)?["\']?([a-zA-Z0-9\s,.-]+)["\']?'
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, user_lower)
            if match:
                address = match.group(1).strip()
                if len(address) > 2:
                    params['FullAddress'] = address
                    print(f"🎯 FullAddress = {address}")
                    break
        
        # 11. @pEnrollmentDate (varchar) - Enrollment date patterns
        enrollment_patterns = [
            r'enrolled\s+on\s+(\d{4}-\d{2}-\d{2})',
            r'enrollment\s+date\s+(\d{4}-\d{2}-\d{2})',
            r'enrolled\s+(\d{4}-\d{2}-\d{2})',
            r'enrollment\s+(\d{2}/\d{2}/\d{4})',
            r'enrolled\s+in\s+(\d{4})',
            r'enrollment.*?(\d{4}-\d{2}-\d{2})'
        ]
        
        for pattern in enrollment_patterns:
            match = re.search(pattern, user_lower)
            if match:
                params['EnrollmentDate'] = normalize_date(match.group(1))
                print(f"🎯 EnrollmentDate = {params['EnrollmentDate']}")
                break
        
        # 12. @pFundingStatus (varchar) - Funding status patterns
        funding_patterns = [
            r'funding\s+status\s+(?:is\s+)?["\']?([a-zA-Z\s]+)["\']?',
            r'with\s+funding\s+(?:status\s+)?["\']?([a-zA-Z\s]+)["\']?',
            r'funding\s+["\']?([a-zA-Z\s]+)["\']?',
            r'funded\s+by\s+["\']?([a-zA-Z\s]+)["\']?'
        ]
        
        for pattern in funding_patterns:
            match = re.search(pattern, user_lower)
            if match:
                funding = match.group(1).strip()
                if len(funding) > 1 and funding.replace(' ', '').isalpha():
                    params['FundingStatus'] = funding
                    print(f"🎯 FundingStatus = {funding}")
                    break
        
        # 13. @pEnrollmentStatus (varchar) - Enrollment status patterns
        enrollment_status_patterns = [
            r'enrollment\s+status\s+(?:is\s+)?["\']?([a-zA-Z\s]*)["\']?',
            r'with\s+(?:enrollment\s+)?status\s+["\']?([a-zA-Z\s]*)["\']?',
            r'status\s+(?:is\s+)?["\']?([a-zA-Z\s]*)["\']?',
            r'enrollment\s+(?:is\s+)?["\']?([a-zA-Z\s]*)["\']?'
        ]
        
        # Special handling for "empty" status
        if 'enrollment status is empty' in user_lower or 'status is empty' in user_lower:
            params['EnrollmentStatus'] = ''
            print(f"🎯 EnrollmentStatus = (empty)")
        else:
            for pattern in enrollment_status_patterns:
                match = re.search(pattern, user_lower)
                if match:
                    status = match.group(1).strip()
                    if status and len(status) > 0:
                        params['EnrollmentStatus'] = status
                        print(f"🎯 EnrollmentStatus = {status}")
                        break
        
        print(f"🎯 FINAL EXTRACTED PARAMS: {params}")
        return params

    def _extract_parameters_with_llm(self, user_input: str) -> Dict[str, Any]:
        """Use LLM to extract parameters from user query"""
        try:
            extraction_prompt = f"""
Extract patient search parameters from this user query: "{user_input}"

Available parameters (return only the ones mentioned):
- PatientId: integer patient ID
- PatientFullName: full name of patient  
- PatientNHI: NHI number
- ChartNumber: chart/medical record number
- GenderName: "male" or "female"
- PatientDOB: date of birth (YYYY-MM-DD format)
- ProviderName: doctor/provider name
- Email: email address
- PhoneNumber: phone number
- FullAddress: address
- EnrollmentDate: enrollment date (YYYY-MM-DD format)
- FundingStatus: funding status
- EnrollmentStatus: enrollment status (use empty string "" for "empty")

Return ONLY a JSON object with the extracted parameters. Examples:
- "show male patients" → {{"GenderName": "male"}}
- "find patient John Smith" → {{"PatientFullName": "John Smith"}}
- "patient with chart number 786" → {{"ChartNumber": "786"}}
- "show patients by Dr. Johnson" → {{"ProviderName": "Dr. Johnson"}}

JSON:"""

            messages = [
                {"role": "system", "content": "You are a parameter extraction assistant. Extract only the mentioned parameters and return valid JSON."},
                {"role": "user", "content": extraction_prompt}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=500
            )

            result_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if result_text.startswith('```json'):
                result_text = result_text[7:-3]
            elif result_text.startswith('```'):
                result_text = result_text[3:-3]
            
            params = json.loads(result_text)
            print(f"🤖 LLM extracted parameters: {params}")
            return params
            
        except Exception as e:
            print(f"❌ LLM parameter extraction failed: {str(e)}")
            # Fallback to manual extraction
            return self._extract_parameters_manually(user_input)




