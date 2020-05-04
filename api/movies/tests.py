from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from faker import Factory
from factories import UserFactory, MovieFactory, UserFeedbackFactory

MOVIES_URL = reverse('movies-list')
FEEDBACK_URL = reverse('feedback-list')
LOGOUT_URL = reverse('logout')
LOGIN_URL = reverse('login')

faker = Factory.create()


class MoviesApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.movies = MovieFactory.create_batch(5, created_by=self.user)
        for movie in self.movies:
            UserFeedbackFactory(created_by=self.user, movie=movie)

    def test_get_movie_list(self):
        response = self.client.get(MOVIES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)

    def test_data_type(self):
        response = self.client.get(MOVIES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()[0]['avg_rating'], float)

    def test_average_rating(self):
        response = self.client.get(MOVIES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for data in response.json():
            self.assertLessEqual(data['avg_rating'], 5)
