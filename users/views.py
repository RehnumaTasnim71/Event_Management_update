from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignUpForm
from .utils import send_activation_email

# Role decorators
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.groups.filter(name='Admin').exists())(view_func)

def organizer_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.groups.filter(name='Organizer').exists())(view_func)

def participant_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.groups.filter(name='Participant').exists())(view_func)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # default role
            group = Group.objects.get(name='Participant')
            user.groups.add(group)
            send_activation_email(user, request)
            messages.success(request, "Account created! Check email for activation link (console backend).")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Account not activated. Check your email.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Account activated!")
        return redirect('dashboard')
    return render(request, 'users/activation_failed.html')

@login_required
def dashboard_redirect(request):
    u = request.user
    if u.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')
    if u.groups.filter(name='Organizer').exists():
        return redirect('organizer_dashboard')
    return redirect('participant_dashboard')

@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'users/dashboards/admin_dashboard.html')

@login_required
@organizer_required
def organizer_dashboard(request):
    return render(request, 'users/dashboards/organizer_dashboard.html')

@login_required
@participant_required
def participant_dashboard(request):
    return render(request, 'users/dashboards/participant_dashboard.html')
#end of file