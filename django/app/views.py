from rest_framework import generics
from django.views import generic
from .models import Holiday
from .serializers import HolidaySerializer


class HolidayList(generics.ListAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer


class Top(generic.TemplateView):
    template_name = 'app/index.html'
