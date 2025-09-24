from django.db import models

class Customization(models.Model):
    product_id = models.CharField(max_length=50, default='t-shirt')
    custom_text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"T-Shirt with text: '{self.custom_text}'"
    