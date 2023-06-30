from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'games'

urlpatterns = [
    path('', TemplateView.as_view(template_name='base_games.html'), name='games'),
]
