import os
import requests
import json
from typing import List, Dict, Any

class TavilySearchService:
    """Service for searching academic profiles using Tavily API"""
    
    def __init__(self):
        self.api_key = os.getenv('TAVILY_API_KEY')
        self.base_url = "https://api.tavily.com/search"
    
    def search_professors(self, country: str, city: str, university: str, 
                         department: str, skills: str) -> List[Dict[str, Any]]:
        """
        Search for professors using Tavily API
        """
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        
        # Construct search query
        query = f"professors {skills} {department} {university} {city} {country} email portfolio site:.edu OR site:.ac"
        
        print(f"Tavily search query: {query}")
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "include_answer": False,
            "include_images": False,
            "include_raw_content": True,
            "max_results": 10
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            results = response.json().get('results', [])
            print(f"Tavily returned {len(results)} results")
            return results
        except requests.exceptions.RequestException as e:
            print(f"Tavily API error: {e}")
            return []

class GroqLLMService:
    """Service for processing search results using Groq LLM"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def extract_professor_info(self, search_results: List[Dict], skills: str) -> List[Dict[str, str]]:
        """
        Extract structured professor information from search results using Groq LLM
        """
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Combine search results into text
        combined_text = ""
        for result in search_results[:5]:  # Limit to first 5 results to avoid token limits
            combined_text += f"Title: {result.get('title', '')}\n"
            combined_text += f"Content: {result.get('content', '')}\n"
            combined_text += f"URL: {result.get('url', '')}\n\n"
        
        if not combined_text.strip():
            return []
        
        prompt = f"""
Extract information about professors with expertise in "{skills}" from the following academic search results. 
Return ONLY a valid JSON array with objects containing these exact fields:
- name: Professor's full name
- email: Email address (if found)
- portfolio_link: Personal/academic website URL (if found)  
- department: Department name
- university: University name
- skills: Relevant skills/expertise areas as comma-separated string

Only include professors who clearly match the requested skills: "{skills}"
Ensure all field names are lowercase and match exactly as specified.
If a field is not found, use an empty string.

Search Results:
{combined_text}

Return only the JSON array, no other text:
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-8b-8192",  # Free tier model
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a precise data extraction assistant. Return only valid JSON arrays with the exact structure requested."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            # Try to parse JSON response - handle cases where LLM adds extra text
            try:
                # First try direct parsing
                professors = json.loads(content)
                if isinstance(professors, list):
                    return professors
                else:
                    print(f"Expected list, got: {type(professors)}")
                    return []
            except json.JSONDecodeError:
                # If direct parsing fails, try to extract JSON from the content
                try:
                    # Look for JSON array in the response
                    start_idx = content.find('[')
                    end_idx = content.rfind(']')
                    
                    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                        json_str = content[start_idx:end_idx + 1]
                        professors = json.loads(json_str)
                        if isinstance(professors, list):
                            print(f"✓ Successfully extracted {len(professors)} professors from LLM response")
                            return professors
                    
                    print(f"Could not extract JSON array from content")
                    print(f"Raw content: {content}")
                    return []
                    
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                    print(f"Raw content: {content}")
                    return []
                
        except requests.exceptions.RequestException as e:
            print(f"Groq API error: {e}")
            return []

class ProfessorSearchService:
    """Main service combining Tavily search and Groq LLM processing"""
    
    def __init__(self):
        self.tavily = TavilySearchService()
        self.groq = GroqLLMService()
    
    def search_and_extract_professors(self, country: str, city: str, university: str,
                                    department: str, skills: str) -> List[Dict[str, str]]:
        """
        Complete professor search workflow: search with Tavily and extract with Groq
        """
        try:
            # Step 1: Search with Tavily
            search_results = self.tavily.search_professors(country, city, university, department, skills)
            
            if not search_results:
                return []
            
            # Step 2: Extract professor info with Groq
            professors = self.groq.extract_professor_info(search_results, skills)
            
            return professors
            
        except Exception as e:
            print(f"Search service error: {e}")
            return []
