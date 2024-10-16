import uuid
from django.db import models

class HyetInput(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
