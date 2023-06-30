from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'my_notes'

urlpatterns = [
    #path('', TemplateView.as_view(template_name='base_my_notes.html'), name='my_notes'),
    path('', views.section_list, name='my_notes'),
    path('<int:section_id>/', views.section_list, name='section_detail'),
    #path('cat/note/', TemplateView.as_view(template_name='note.html'), name='my_notes'),
]
