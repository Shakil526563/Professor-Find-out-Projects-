from django.core.management.base import BaseCommand
from search.models import Country, City, University, Department

class Command(BaseCommand):
    help = 'Load sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Countries
        usa, _ = Country.objects.get_or_create(name='United States', code='USA')
        uk, _ = Country.objects.get_or_create(name='United Kingdom', code='GBR')
        canada, _ = Country.objects.get_or_create(name='Canada', code='CAN')
        germany, _ = Country.objects.get_or_create(name='Germany', code='DEU')
        
        # Cities - USA
        boston, _ = City.objects.get_or_create(name='Boston', country=usa)
        stanford, _ = City.objects.get_or_create(name='Stanford', country=usa)
        cambridge_ma, _ = City.objects.get_or_create(name='Cambridge', country=usa)
        new_york, _ = City.objects.get_or_create(name='New York', country=usa)
        
        # Cities - UK
        cambridge_uk, _ = City.objects.get_or_create(name='Cambridge', country=uk)
        oxford, _ = City.objects.get_or_create(name='Oxford', country=uk)
        london, _ = City.objects.get_or_create(name='London', country=uk)
        
        # Cities - Canada
        toronto, _ = City.objects.get_or_create(name='Toronto', country=canada)
        montreal, _ = City.objects.get_or_create(name='Montreal', country=canada)
        
        # Cities - Germany
        munich, _ = City.objects.get_or_create(name='Munich', country=germany)
        berlin, _ = City.objects.get_or_create(name='Berlin', country=germany)
        
        # Universities
        mit, _ = University.objects.get_or_create(
            name='Massachusetts Institute of Technology',
            city=cambridge_ma,
            defaults={'website': 'https://web.mit.edu/'}
        )
        
        stanford_uni, _ = University.objects.get_or_create(
            name='Stanford University',
            city=stanford,
            defaults={'website': 'https://www.stanford.edu/'}
        )
        
        harvard, _ = University.objects.get_or_create(
            name='Harvard University',
            city=cambridge_ma,
            defaults={'website': 'https://www.harvard.edu/'}
        )
        
        cambridge_uni, _ = University.objects.get_or_create(
            name='University of Cambridge',
            city=cambridge_uk,
            defaults={'website': 'https://www.cam.ac.uk/'}
        )
        
        oxford_uni, _ = University.objects.get_or_create(
            name='University of Oxford',
            city=oxford,
            defaults={'website': 'https://www.ox.ac.uk/'}
        )
        
        toronto_uni, _ = University.objects.get_or_create(
            name='University of Toronto',
            city=toronto,
            defaults={'website': 'https://www.utoronto.ca/'}
        )
        
        # Departments
        # MIT
        Department.objects.get_or_create(name='Computer Science and Artificial Intelligence Laboratory', university=mit)
        Department.objects.get_or_create(name='Department of Electrical Engineering and Computer Science', university=mit)
        Department.objects.get_or_create(name='Department of Mathematics', university=mit)
        
        # Stanford
        Department.objects.get_or_create(name='Department of Computer Science', university=stanford_uni)
        Department.objects.get_or_create(name='Department of Electrical Engineering', university=stanford_uni)
        Department.objects.get_or_create(name='Department of Statistics', university=stanford_uni)
        
        # Harvard
        Department.objects.get_or_create(name='John A. Paulson School of Engineering and Applied Sciences', university=harvard)
        Department.objects.get_or_create(name='Department of Statistics', university=harvard)
        
        # Cambridge
        Department.objects.get_or_create(name='Department of Computer Science and Technology', university=cambridge_uni)
        Department.objects.get_or_create(name='Department of Engineering', university=cambridge_uni)
        
        # Oxford
        Department.objects.get_or_create(name='Department of Computer Science', university=oxford_uni)
        Department.objects.get_or_create(name='Department of Engineering Science', university=oxford_uni)
        
        # Toronto
        Department.objects.get_or_create(name='Department of Computer Science', university=toronto_uni)
        Department.objects.get_or_create(name='Department of Electrical and Computer Engineering', university=toronto_uni)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data'))
