import json

from django.test import TestCase
from django.urls import reverse


class WhisperViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(
            reverse("whispers"),
            {
                "name": "Vinia's Token",
                "value": "1.0142842857142857",
                "price": "1",
                "expected_profit": "0.01428428571428575",
            },
        )
        self.assertEqual(response.status_code, 200)
