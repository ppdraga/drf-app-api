from django.test import TestCase

from app.calc import add, subtract


class CalcTest(TestCase):
    """CalcTest"""

    def test_add(self):
        self.assertEquals(add(3, 8), 11)

    def test_subtract(self):
        self.assertEquals(subtract(5, 11), 6)
