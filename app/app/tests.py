from django.test import TestCase

from app.calc import add

class CalcTest(TestCase):
    """CalcTest"""
    
    def test_add(self):
        self.assertEquals(add(3, 8), 11)
