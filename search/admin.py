from django.contrib import admin
from .models import Country, City, University, Department, Professor

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    list_filter = ['country']
    search_fields = ['name', 'country__name']
    ordering = ['country__name', 'name']

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'get_country']
    list_filter = ['city__country', 'city']
    search_fields = ['name', 'city__name', 'city__country__name']
    ordering = ['city__country__name', 'city__name', 'name']
    
    def get_country(self, obj):
        return obj.city.country.name
    get_country.short_description = 'Country'
    get_country.admin_order_field = 'city__country__name'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'get_city', 'get_country']
    list_filter = ['university__city__country', 'university__city', 'university']
    search_fields = ['name', 'university__name', 'university__city__name']
    ordering = ['university__city__country__name', 'university__name', 'name']
    
    def get_city(self, obj):
        return obj.university.city.name
    get_city.short_description = 'City'
    get_city.admin_order_field = 'university__city__name'
    
    def get_country(self, obj):
        return obj.university.city.country.name
    get_country.short_description = 'Country'
    get_country.admin_order_field = 'university__city__country__name'

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'get_university', 'email', 'created_at']
    list_filter = ['department__university__city__country', 'department__university', 'created_at']
    search_fields = ['name', 'email', 'skills', 'department__name', 'department__university__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at', 'name']
    
    def get_university(self, obj):
        return obj.department.university.name
    get_university.short_description = 'University'
    get_university.admin_order_field = 'department__university__name'
