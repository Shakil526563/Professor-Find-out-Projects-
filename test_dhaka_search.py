#!/usr/bin/env python3
"""
Test script for searching Dhaka University professors
"""

import requests
import json

def test_dhaka_search():
    """Test search for University of Dhaka professors"""
    
    # Your specified search data
    form_data = {
        'country': 'Bangladesh',
        'city': 'Dhaka',
        'university': 'University of Dhaka',
        'department': 'Computer Science',
        'skills': 'artificial intelligence machine learning'
    }
    
    print("🔍 Searching for University of Dhaka professors...")
    print(f"Search parameters: {json.dumps(form_data, indent=2)}")
    print("=" * 60)
    
    try:
        # Make API request
        response = requests.post(
            'http://127.0.0.1:8002/api/search/',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(form_data)
        )
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('success')}")
            print(f"📊 Results Found: {data.get('results_found')}")
            print()
            
            professors = data.get('professors', [])
            if professors:
                print("👨‍🏫 Professors Found:")
                print("-" * 50)
                
                for i, prof in enumerate(professors, 1):
                    print(f"{i}. {prof.get('name', 'No name')}")
                    print(f"   📧 Email: {prof.get('email', 'Not available')}")
                    print(f"   🏫 Department: {prof.get('department', 'Not available')}")
                    print(f"   🌐 Portfolio: {prof.get('portfolio_link', 'Not available')}")
                    print(f"   🔬 Skills: {prof.get('skills', 'Not available')}")
                    print(f"   🆔 ID: {prof.get('id')}")
                    print(f"   🆕 Created: {prof.get('created')}")
                    print()
            else:
                print("⚠️ No professors found in the response")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running on port 8002")
        print("Run: python manage.py runserver 8002")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_dhaka_search()
