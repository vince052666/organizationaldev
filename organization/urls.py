from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('chart/', views.organizational_chart, name='chart'),
]
