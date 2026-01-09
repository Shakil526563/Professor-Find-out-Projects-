#!/usr/bin/env python3
"""
REST API Test Script for Professor Finder
Tests all the new REST API endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8002"

def test_countries_api():
    """Test the countries API endpoint"""
    print("=== Testing Countries API ===")
    try:
        response = requests.get(f"{BASE_URL}/api/countries/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Countries found: {len(data.get('countries', []))}")
            if data.get('countries'):
                print(f"First country: {data['countries'][0]}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_search_api():
    """Test the professor search API endpoint"""
    print("=== Testing Professor Search API ===")
    try:
        search_data = {
            "country": "United States",
            "city": "Cambridge",
            "university": "MIT",
            "department": "Computer Science",
            "skills": "artificial intelligence"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/search/",
            headers={"Content-Type": "application/json"},
            data=json.dumps(search_data)
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Results found: {data.get('results_found')}")
            if data.get('professors'):
                print(f"First professor: {data['professors'][0].get('name')}")
                print(f"Professor details: {json.dumps(data['professors'][0], indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_professors_list_api():
    """Test the professors list API endpoint"""
    print("=== Testing Professors List API ===")
    try:
        response = requests.get(f"{BASE_URL}/api/professors/?page_size=5")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Total count: {data.get('total_count')}")
            print(f"Page: {data.get('page')}")
            print(f"Professors in page: {len(data.get('professors', []))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_location_hierarchy():
    """Test the location hierarchy APIs"""
    print("=== Testing Location Hierarchy APIs ===")
    
    # First get countries
    try:
        countries_response = requests.get(f"{BASE_URL}/api/countries/")
        if countries_response.status_code == 200:
            countries = countries_response.json().get('countries', [])
            if countries:
                country_id = countries[0]['id']
                print(f"Testing with country: {countries[0]['name']} (ID: {country_id})")
                
                # Test cities
                cities_response = requests.get(f"{BASE_URL}/api/cities/{country_id}/")
                print(f"Cities API Status: {cities_response.status_code}")
                if cities_response.status_code == 200:
                    cities = cities_response.json().get('cities', [])
                    print(f"Cities found: {len(cities)}")
                    
                    if cities:
                        city_id = cities[0]['id']
                        print(f"Testing with city: {cities[0]['name']} (ID: {city_id})")
                        
                        # Test universities
                        unis_response = requests.get(f"{BASE_URL}/api/universities/{city_id}/")
                        print(f"Universities API Status: {unis_response.status_code}")
                        if unis_response.status_code == 200:
                            unis = unis_response.json().get('universities', [])
                            print(f"Universities found: {len(unis)}")
                            
                            if unis:
                                uni_id = unis[0]['id']
                                print(f"Testing with university: {unis[0]['name']} (ID: {uni_id})")
                                
                                # Test departments
                                depts_response = requests.get(f"{BASE_URL}/api/departments/{uni_id}/")
                                print(f"Departments API Status: {depts_response.status_code}")
                                if depts_response.status_code == 200:
                                    depts = depts_response.json().get('departments', [])
                                    print(f"Departments found: {len(depts)}")
    except Exception as e:
        print(f"Error testing location hierarchy: {e}")
    print()

def main():
    """Run all REST API tests"""
    print("🧪 Professor Finder REST API Test Suite")
    print("=" * 50)
    
    # Test individual endpoints
    test_countries_api()
    test_search_api()
    test_professors_list_api()
    test_location_hierarchy()
    
    print("✅ REST API testing completed!")

if __name__ == "__main__":
    main()
