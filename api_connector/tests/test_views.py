from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from api.models import HyetInput
from django.db.models import Avg


class HyetInputTestCase(TestCase):
    def setUp(self):
        now = timezone.now()

        for i in range(1, 6):
            HyetInput.objects.create(
                value=i * 10,
                created_at=now - timezone.timedelta(minutes=i)
            )
        
        self.client = APIClient()

    def test_hyet_input_average_view_invalid_minutes(self):
        response = self.client.get(reverse('hyetinput-average', kwargs={'minutes': 'invalid'}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid time interval.')

    def test_hyet_input_list_view(self):
        response = self.client.get(reverse('hyetinput-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0, "No data was returned from the view")

        self.assertEqual(response.data['results'][0]['value'], 10.0)
        self.assertEqual(response.data['results'][1]['value'], 20.0)
