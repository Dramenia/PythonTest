from rest_framework import serializers
from .models import HyetInput

class HyetInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = HyetInput
        fields = ['id', 'value', 'created_at']
