from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.TodoListView.as_view(), name='list'),
    path('create/', views.TodoCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TodoUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.TodoDeleteView.as_view(), name='delete'),
    path('<int:pk>/toggle/', views.toggle_completed, name='toggle'),
]
