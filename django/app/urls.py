from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('api/holiday/', views.HolidayList.as_view(), name='holiday_list'),
	path('', views.Top.as_view(), name='top'),
]
