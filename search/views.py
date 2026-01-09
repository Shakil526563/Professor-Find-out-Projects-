from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import Country, City, University, Department, Professor
from .services import ProfessorSearchService

@csrf_exempt
@require_http_methods(["POST"])
def search_professors_api(request):
    """REST API endpoint for professor search"""
    try:
        data = json.loads(request.body)
        
        # Extract search parameters
        country = data.get('country', '')
        city = data.get('city', '')
        university = data.get('university', '')
        department = data.get('department', '')
        skills = data.get('skills', '')
        
        # Validate required fields
        if not all([country, city, university, skills]):
            return JsonResponse({
                'error': 'Missing required fields: country, city, university, skills'
            }, status=400)
        
        # Perform search
        search_service = ProfessorSearchService()
        professors_data = search_service.search_and_extract_professors(
            country, city, university, department, skills
        )
        
        # Save results to database
        saved_professors = []
        for prof_data in professors_data:
            try:
                # Get or create the location hierarchy
                country_obj, _ = Country.objects.get_or_create(
                    name=country,
                    defaults={'code': country[:3].upper()}
                )
                
                city_obj, _ = City.objects.get_or_create(
                    name=city,
                    country=country_obj
                )
                
                university_obj, _ = University.objects.get_or_create(
                    name=prof_data.get('university', university),
                    city=city_obj
                )
                
                department_obj, _ = Department.objects.get_or_create(
                    name=prof_data.get('department', department),
                    university=university_obj
                )
                
                # Create or get professor
                professor, created = Professor.objects.get_or_create(
                    name=prof_data.get('name', ''),
                    department=department_obj,
                    defaults={
                        'email': prof_data.get('email', ''),
                        'portfolio_link': prof_data.get('portfolio_link', ''),
                        'skills': prof_data.get('skills', ''),
                    }
                )
                
                saved_professors.append({
                    'id': professor.id,
                    'name': professor.name,
                    'email': professor.email,
                    'portfolio_link': professor.portfolio_link,
                    'skills': professor.skills,
                    'department': professor.department.name,
                    'university': professor.department.university.name,
                    'city': professor.department.university.city.name,
                    'country': professor.department.university.city.country.name,
                    'created': created
                })
                
            except Exception as e:
                print(f"Error saving professor {prof_data.get('name', 'Unknown')}: {e}")
        
        return JsonResponse({
            'success': True,
            'results_found': len(saved_professors),
            'professors': saved_professors
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def list_professors_api(request):
    """REST API endpoint to list all professors"""
    try:
        # Optional filtering
        country = request.GET.get('country')
        city = request.GET.get('city')
        university = request.GET.get('university')
        department = request.GET.get('department')
        skills = request.GET.get('skills')
        
        professors = Professor.objects.all()
        
        # Apply filters
        if country:
            professors = professors.filter(
                department__university__city__country__name__icontains=country
            )
        if city:
            professors = professors.filter(
                department__university__city__name__icontains=city
            )
        if university:
            professors = professors.filter(
                department__university__name__icontains=university
            )
        if department:
            professors = professors.filter(
                department__name__icontains=department
            )
        if skills:
            professors = professors.filter(skills__icontains=skills)
        
        # Pagination
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size
        
        total_count = professors.count()
        professors_page = professors[start:end]
        
        professors_data = []
        for professor in professors_page:
            professors_data.append({
                'id': professor.id,
                'name': professor.name,
                'email': professor.email,
                'portfolio_link': professor.portfolio_link,
                'skills': professor.skills,
                'department': professor.department.name,
                'university': professor.department.university.name,
                'city': professor.department.university.city.name,
                'country': professor.department.university.city.country.name,
            })
        
        return JsonResponse({
            'success': True,
            'total_count': total_count,
            'page': page,
            'page_size': page_size,
            'professors': professors_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def list_countries_api(request):
    """REST API endpoint to list all countries"""
    try:
        countries = Country.objects.all().order_by('name')
        countries_data = [{'id': c.id, 'name': c.name, 'code': c.code} for c in countries]
        
        return JsonResponse({
            'success': True,
            'countries': countries_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def list_cities_api(request, country_id):
    """REST API endpoint to list cities by country"""
    try:
        cities = City.objects.filter(country_id=country_id).order_by('name')
        cities_data = [{'id': c.id, 'name': c.name} for c in cities]
        
        return JsonResponse({
            'success': True,
            'cities': cities_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def list_universities_api(request, city_id):
    """REST API endpoint to list universities by city"""
    try:
        universities = University.objects.filter(city_id=city_id).order_by('name')
        universities_data = [{'id': u.id, 'name': u.name} for u in universities]
        
        return JsonResponse({
            'success': True,
            'universities': universities_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def list_departments_api(request, university_id):
    """REST API endpoint to list departments by university"""
    try:
        departments = Department.objects.filter(university_id=university_id).order_by('name')
        departments_data = [{'id': d.id, 'name': d.name} for d in departments]
        
        return JsonResponse({
            'success': True,
            'departments': departments_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
