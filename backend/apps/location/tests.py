from django.test import TestCase
from apps.location import test_helpers
from apps.location.models import *

class TestLocation(TestCase):
    def setUp(self):
        self.test_objects = test_helpers.TestObjects()
        self.test_objects.create()
    
    def test_continent(self):
        assert self.test_objects.continent.name.lower() == "america"