from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    # Main REST API endpoints
    path('api/search/', views.search_professors_api, name='search_api'),
    path('api/professors/', views.list_professors_api, name='list_professors_api'),
    
    # Location data endpoints
    path('api/countries/', views.list_countries_api, name='list_countries_api'),
    path('api/cities/<int:country_id>/', views.list_cities_api, name='list_cities_api'),
    path('api/universities/<int:city_id>/', views.list_universities_api, name='list_universities_api'),
    path('api/departments/<int:university_id>/', views.list_departments_api, name='list_departments_api'),
]
