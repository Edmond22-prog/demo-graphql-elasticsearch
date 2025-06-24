import uuid

from django.db import models


class Category(models.Model):
    uuid = models.CharField(
        max_length=100, primary_key=True, editable=False, default=uuid.uuid4().hex
    )
    name = models.CharField(max_length=50)
    normalized_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
