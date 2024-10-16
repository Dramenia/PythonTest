from django.urls import path
from .views import HyetInputAverageView, HyetInputListView

urlpatterns = [
    path('average/<str:minutes>/', HyetInputAverageView.as_view(), name='hyetinput-average'),
    path('list/', HyetInputListView.as_view(), name='hyetinput-list'),
]