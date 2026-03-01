"""
Models for the trades app.
"""

from django.db import models


class Item(models.Model):
    """
    Model representing a tradable item.
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Trade(models.Model):
    """
    Model representing a trade transaction.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='trades')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.item.name} at {self.price}"
    
    @property
    def total_value(self):
        """Calculate the total value of the trade."""
        return self.quantity * self.price 