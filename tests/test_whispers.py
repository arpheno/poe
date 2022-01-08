import json

from django.test import TestCase
from django.urls import reverse


class WhisperViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.post(
            reverse("whispers"),
            json.dumps(
                [
                    {
                        "name": "Vinia's Token",
                        "value": 1.0142842857142857,
                        "price": 1,
                        "expected_profit": 0.01428428571428575,
                    },
                    {
                        "name": "Terrible Secret of Space",
                        "value": 19.112708333333334,
                        "price": 4.85,
                        "expected_profit": 14.262708333333334,
                    },
                ]
            ),
            content_type="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
