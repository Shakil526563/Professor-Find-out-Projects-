from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)  # ISO country code
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Countries"

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    
    def __str__(self):
        return f"{self.name}, {self.country.name}"
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Cities"
        unique_together = ['name', 'country']

class University(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='universities')
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}"
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Universities"

class Department(models.Model):
    name = models.CharField(max_length=150)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='departments')
    
    def __str__(self):
        return f"{self.name} - {self.university.name}"
    
    class Meta:
        ordering = ['name']

class Professor(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='professors')
    skills = models.TextField(help_text="Comma-separated list of skills/expertise areas")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.department}"
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'department']
    
    def get_skills_list(self):
        """Return skills as a list"""
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
