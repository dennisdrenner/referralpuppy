from django.test import TestCase

# Create your tests here.

from tracker.models import Profile

class ProfileTests(TestCase):
    
    def test_city(self):
        profile = Profile(city='Baltimore')
        self.assertEquals(profile.city, 'Baltimore')


