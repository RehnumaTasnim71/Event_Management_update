from django.urls import path
from . import views

from django.shortcuts import redirect

# Default redirect view
def index_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', index_redirect, name='index_redirect'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),

    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/organizer/', views.organizer_dashboard, name='organizer_dashboard'),
    path('dashboard/participant/', views.participant_dashboard, name='participant_dashboard'),
]
