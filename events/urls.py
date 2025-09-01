from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('create/', views.event_create, name='event_create'),
    path('update/<int:event_id>/', views.event_update, name='event_update'),
    path('delete/<int:event_id>/', views.event_delete, name='event_delete'),
    path('rsvp/<int:event_id>/', views.rsvp_event, name='rsvp_event'),
]
