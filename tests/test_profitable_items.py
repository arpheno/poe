from django.test import client, Client, TestCase
from django.urls import reverse

from frontend.thinking.trades.views import profitable_items


class ProfitableItemsViewTests(TestCase):
    def test_profitable_items(self):
        response = self.client.get(reverse('index'))
        print(response.json())
