from django.db.models import Avg
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HyetInput
from .serializers import HyetInputSerializer


class HyetInputAverageView(APIView):
    def get(self, request, minutes):
        try:
            minutes = int(minutes)
        except ValueError:
            return Response({"error": "Invalid time interval."}, status=400)

        now = timezone.now()
        time_window = now - timezone.timedelta(minutes=minutes)
        recent_data = HyetInput.objects.filter(created_at__gte=time_window)
        average_value = recent_data.aggregate(Avg('value'))['value__avg']

        return Response({"average_value": average_value or 0})



class HyetInputListView(ListAPIView):
    queryset = HyetInput.objects.all().order_by('-created_at')
    serializer_class = HyetInputSerializer
