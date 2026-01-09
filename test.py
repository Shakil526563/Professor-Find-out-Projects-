#!/usr/bin/env python
"""
Test script for Professor Finder API connections and search functionality
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'professor_finder.settings')
django.setup()

from search.services import TavilySearchService, GroqLLMService, ProfessorSearchService
from dotenv import load_dotenv

def test_environment():
    """Test if environment variables are loaded correctly"""
    print("=== Environment Test ===")
    load_dotenv()
    
    tavily_key = os.getenv('TAVILY_API_KEY')
    groq_key = os.getenv('GROQ_API_KEY')
    
    print(f"TAVILY_API_KEY: {'✓ Set' if tavily_key else '✗ Missing'}")
    print(f"GROQ_API_KEY: {'✓ Set' if groq_key else '✗ Missing'}")
    
    if tavily_key:
        print(f"Tavily key preview: {tavily_key[:10]}...")
    if groq_key:
        print(f"Groq key preview: {groq_key[:10]}...")
    
    return bool(tavily_key and groq_key)

def test_tavily_connection():
    """Test Tavily API connection"""
    print("\n=== Tavily API Test ===")
    
    try:
        tavily = TavilySearchService()
        
        # Simple test query
        results = tavily.search_professors(
            country="Bangladesh",
            city="Dhaka",
            university="University of Dhaka",
            department="Computer Science",
            skills="artificial intelligence"
        )
        
        print(f"✓ Tavily API connection successful")
        print(f"✓ Returned {len(results)} results")
        
        if results:
            print("Sample result:")
            result = results[0]
            print(f"  Title: {result.get('title', 'N/A')[:100]}...")
            print(f"  URL: {result.get('url', 'N/A')}")
            print(f"  Content preview: {result.get('content', 'N/A')[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Tavily API error: {e}")
        return False

def test_groq_connection():
    """Test Groq API connection"""
    print("\n=== Groq API Test ===")
    
    try:
        groq = GroqLLMService()
        
        # Test with sample data
        sample_results = [
            {
                'title': 'Dr. John Smith - MIT Computer Science',
                'content': 'Professor John Smith specializes in artificial intelligence and machine learning at MIT. Email: jsmith@mit.edu',
                'url': 'https://www.mit.edu/~jsmith'
            }
        ]
        
        professors = groq.extract_professor_info(sample_results, "artificial intelligence")
        
        print(f"✓ Groq API connection successful")
        print(f"✓ Extracted {len(professors)} professors")
        
        if professors:
            print("Sample extracted professor:")
            prof = professors[0]
            for key, value in prof.items():
                print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"✗ Groq API error: {e}")
        return False

def test_full_search():
    """Test the complete search workflow"""
    print("\n=== Full Search Test ===")
    
    try:
        search_service = ProfessorSearchService()
        
        professors = search_service.search_and_extract_professors(
            country="Bangladesh",
            city="Dhaka",
            university="University of Dhaka",
            department="Computer Science",
            skills="artificial intelligence machine learning"
        )
        
        print(f"✓ Full search workflow successful")
        print(f"✓ Found {len(professors)} professors")
        
        for i, prof in enumerate(professors[:3]):  # Show first 3
            print(f"\nProfessor {i+1}:")
            for key, value in prof.items():
                print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"✗ Full search error: {e}")
        return False

def test_form_data():
    """Test form processing with sample data"""
    print("\n=== Form Data Test ===")
    
    from search.forms import ProfessorSearchForm
    
    # Test form with sample data
    form_data = {
    'country': 'Bangladesh',
    'city': 'Dhaka',
    'university': 'University of Dhaka',
    'department': 'Computer Science',
    'skills': 'artificial intelligence machine learning'
}

    
    form = ProfessorSearchForm(data=form_data)
    
    if form.is_valid():
        print("✓ Form validation successful")
        print("Form data:")
        for field, value in form.cleaned_data.items():
            print(f"  {field}: {value}")
        return True
    else:
        print("✗ Form validation failed")
        print("Errors:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
        return False

def main():
    """Run all tests"""
    print("Professor Finder API Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Form Data", test_form_data),
        ("Tavily API", test_tavily_connection),
        ("Groq API", test_groq_connection),
        ("Full Search", test_full_search),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ {test_name} test failed with exception: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:<15}: {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\nOverall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 All tests passed! The system should be working.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
