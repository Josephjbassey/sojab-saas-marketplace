from django.urls import path
from .views import TemplateListView, template_detail

app_name = 'templates_catalog'

urlpatterns = [
    path('', TemplateListView.as_view(), name='template_list'),
    path('<slug:slug>/', template_detail, name='template_detail'),
]
