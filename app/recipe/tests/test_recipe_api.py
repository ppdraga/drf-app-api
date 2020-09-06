from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from recipe.serializers import RecipeSerializer
from core.models import Recipe


RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    defaults = {
        'title': 'Sample recipe',
        'price': 5.00,
        'time_minutes': 10
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@mail.com',
            password='password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    
    def test_retrieve_recipes(self):
        sample_recipe(user=self.user, title='Recipe_1')
        sample_recipe(user=self.user, title='Recipe_2')

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_recpies_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            email='user2@mail.com',
            password='user2pass'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)
        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

